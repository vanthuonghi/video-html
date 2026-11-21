#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ghép lời đọc vào từng tập video đồ hoạ (lời đọc sinh sẵn trong .thu-nghiem/giong).
Dùng: python3 ghep-tieng-tap.py [slug ...]
"""
import os, subprocess, sys

BASE = os.environ.get("VH_BASE") or os.path.dirname(os.path.abspath(__file__))
GIONG = f"{BASE}/.thu-nghiem/giong"
OUT = f"{BASE}/video-do-hoa"
AUD = f"{BASE}/.thu-nghiem/audio"
PAD = f"{AUD}/pad.wav"
SWELL = f"{AUD}/swell.wav"

TAPS = None  # dựng từ chính kịch bản trong dung-tap-do-hoa.py, không chép tay


def load_taps():
    import importlib.util
    base = os.path.dirname(os.path.abspath(__file__))
    sp = importlib.util.spec_from_file_location("dt", f"{base}/dung-tap-do-hoa.py")
    dt = importlib.util.module_from_spec(sp); sp.loader.exec_module(dt)
    return {e["slug"]: {"total": e["total"],
                        "wins": [round(b - a, 3) for a, b in e["scenes"]]} for e in dt.EPISODES}

OFFSET = 0.35          # lời đọc vào sau khi cảnh đã hiện
GAP = 0.5              # chừa chỗ cuối cảnh
PAD_VOL = 0.30
SWELL_VOL = 0.45
# Nhạc nền tự hạ khi có giọng đọc (sidechain), thay vì để nhạc lấn suốt video.
DUCK_THRESHOLD = 0.03  # ~ -30 dB: trên mức này coi là có giọng
DUCK_RATIO = 6
DUCK_ATTACK = 20       # ms
DUCK_RELEASE = 350     # ms
# Chuẩn hoá độ to về mức nền tảng dùng, để mọi tập nghe đều nhau.
LOUD_I, LOUD_TP, LOUD_LRA = -14, -1.5, 11


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip())


def ghep(slug):
    spec = TAPS[slug]
    video = f"{OUT}/{slug}.mp4"
    if not os.path.exists(video):
        print(f"  {slug}: CHƯA CÓ VIDEO {video}")
        return
    durv = dur(video)
    if abs(durv - spec["total"]) > 0.05:
        print(f"  {slug}: CẢNH BÁO video dài {durv:.1f}s nhưng kịch bản {spec['total']}s "
              f"-> phần lời sau mốc {durv:.1f}s sẽ bị mất")
    ins, parts, starts = [], [], []
    t = 0.0
    n_in, n_lbl = 0, 0
    moc = []                     # mốc bắt đầu từng cảnh, để đặt tiếng vút chuyển cảnh
    for i, w in enumerate(spec["wins"], 1):
        moc.append(round(t, 3))
        f = f"{GIONG}/{slug}-sc{i}.mp3"
        if not os.path.exists(f) or os.path.getsize(f) < 4000:
            print(f"    cảnh {i}: không có lời đọc (chỉ nhạc nền)")
            t += w
            continue
        d = dur(f)
        room = w - OFFSET - GAP
        tempo = 1.0 if d <= room else round(d / room, 3)
        ins += ["-i", f]
        n_in += 1          # thứ tự đầu vào thật, không phải số cảnh
        n_lbl += 1
        chain = f"[{n_in}:a]aresample=48000,"
        if tempo > 1.001:
            chain += f"atempo={tempo},"
        start = t + OFFSET
        starts.append((i, start))
        parts.append(chain + f"adelay={int(start*1000)}|{int(start*1000)},volume=1.0,"
                             f"aformat=channel_layouts=mono[n{n_lbl}]")
        t += w

    # nền trầm: một bản lặp, cắt đúng độ dài video
    pi = n_in + 1
    ins += ["-stream_loop", "-1", "-i", PAD]
    parts.append(f"[{pi}:a]atrim=0:{durv},volume={PAD_VOL},"
                 f"aformat=channel_layouts=mono[pad]")

    if n_lbl:
        # gộp lời đọc thành một tín hiệu: vừa để mix, vừa làm khoá ducking cho nhạc nền
        parts.append("".join(f"[n{i}]" for i in range(1, n_lbl + 1)) +
                     f"amix=inputs={n_lbl}:duration=longest:normalize=0,"
                     f"aformat=channel_layouts=mono,asplit=2[narr][khoa]")
        parts.append(f"[pad][khoa]sidechaincompress=threshold={DUCK_THRESHOLD}:"
                     f"ratio={DUCK_RATIO}:attack={DUCK_ATTACK}:release={DUCK_RELEASE}[padduck]")
        mix_lbl = ["[narr]", "[padduck]"]
    else:
        mix_lbl = ["[pad]"]

    # tiếng vút: chỉ một bản ngắn ở mỗi mốc chuyển cảnh, không lặp suốt video
    bounds = moc[1:]
    if bounds:
        ins += ["-i", SWELL]
        sw = pi + 1
        if len(bounds) > 1:
            parts.append(f"[{sw}:a]asplit={len(bounds)}" + "".join(f"[s{k}]" for k in range(len(bounds))))
            srcs = [f"[s{k}]" for k in range(len(bounds))]
        else:
            srcs = [f"[{sw}:a]"]
        for k, (at, src) in enumerate(zip(bounds, srcs)):
            parts.append(f"{src}adelay={int(at*1000)}|{int(at*1000)},volume={SWELL_VOL},"
                         f"aformat=channel_layouts=mono[sw{k}]")
            mix_lbl.append(f"[sw{k}]")

    parts.append("".join(mix_lbl) +
                 f"amix=inputs={len(mix_lbl)}:duration=longest:normalize=0,"
                 f"atrim=0:{durv},loudnorm=I={LOUD_I}:TP={LOUD_TP}:LRA={LOUD_LRA},"
                 f"aresample=48000[aout]")
    out = f"{OUT}/{slug}_co-tieng.mp4"
    cmd = (["ffmpeg", "-v", "error", "-y", "-i", video] + ins +
           ["-filter_complex", ";".join(parts), "-map", "0:v", "-map", "[aout]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out])
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  {slug}: LỖI {r.stderr.strip()[:300]}")
        return
    # đo mức âm lượng (phải để ffmpeg ở mức thông tin mặc định, -v error sẽ nuốt mất số liệu)
    st = subprocess.run(["ffmpeg", "-hide_banner", "-i", out, "-af", "volumedetect",
                         "-f", "null", "-"], capture_output=True, text=True).stderr
    mean = peak = "không đọc được"
    for line in st.splitlines():
        if "mean_volume:" in line:
            mean = line.split("mean_volume:")[-1].strip()
        if "max_volume:" in line:
            peak = line.split("max_volume:")[-1].strip()
    if mean == "không đọc được":
        print(f"  {slug}: CẢNH BÁO không đo được mức âm lượng")
    print(f"  {slug}: xong · {dur(out):.1f}s · {os.path.getsize(out)/1048576:.1f} MB · "
          f"mức trung bình {mean} · đỉnh {peak}")
    print(f"    lời đọc vào ở: " + ", ".join(f"cảnh {i}@{s:.2f}s" for i, s in starts))


if __name__ == "__main__":
    TAPS = load_taps()
    for s in (sys.argv[1:] or list(TAPS)):
        ghep(s)
