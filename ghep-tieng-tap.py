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
# Hậu tố tên tệp cho khung khác 9:16, ví dụ VH_HAU_TO=_1080x1080 → <slug>_1080x1080.mp4
# đọc vào và ghi ra <slug>_1080x1080_co-tieng.mp4. Để trống thì giữ nguyên tên cũ.
HAU_TO = os.environ.get("VH_HAU_TO", "")


def load_taps():
    import importlib.util
    base = os.path.dirname(os.path.abspath(__file__))
    sp = importlib.util.spec_from_file_location("dt", f"{base}/dung-tap-do-hoa.py")
    dt = importlib.util.module_from_spec(sp); sp.loader.exec_module(dt)
    return {e["slug"]: {"total": e["total"],
                        "wins": [round(b - a, 3) for a, b in e["scenes"]]} for e in dt.EPISODES}

OFFSET = 0.35          # lời đọc vào sau khi cảnh đã hiện
GAP = 0.5              # chừa chỗ cuối cảnh
# Nhạc nền là giai điệu chuông (sinh-nhac.py), rõ hơn tiếng ù cũ ở cùng mức to,
# nên hạ xuống để vẫn nằm dưới giọng đọc. Tiếng chuyển cảnh là chuông, không phải
# nhiễu gió, nên cũng nhẹ hơn.
PAD_VOL = 0.14
SWELL_VOL = 0.28
# Nhạc nền tự hạ khi có giọng đọc (sidechain), thay vì để nhạc lấn suốt video.
DUCK_THRESHOLD = 0.02  # ~ -34 dB: trên mức này coi là có giọng (0,03 chỉ hạ được ~4 dB)
DUCK_RATIO = 6
DUCK_ATTACK = 20       # ms
DUCK_RELEASE = 350     # ms
# Chuẩn hoá độ to, để mọi tập nghe đều nhau. −16 LUFS là mức giọng đọc đạt được
# mà không phải ép đỉnh (ép mạnh làm chính bộ chặn đỉnh kéo độ to ngược lại).
LOUD_I, LOUD_TP, LOUD_LRA = -16, -1.5, 11


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip())


def do_to(f):
    """Độ to tích hợp (LUFS) của một tệp, đọc từ ebur128."""
    st = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", f, "-af",
                         "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    for line in reversed(st.splitlines()):
        s = line.strip()
        if s.startswith("I:") and "LUFS" in s:
            try:
                return float(s.split(":")[1].replace("LUFS", "").strip())
            except ValueError:
                pass
    return LOUD_I


def ghep(slug):
    spec = TAPS[slug]
    video = f"{OUT}/{slug}{HAU_TO}.mp4"
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
        # siết nhẹ đỉnh giọng đọc: hạ được chênh động để cả tập đạt đúng mức to mà
        # không phải ép đỉnh ở khâu cuối (tập nhiều chỗ lặng trước đây bị hụt mức)
        parts.append(chain + "acompressor=threshold=-18dB:ratio=3:attack=8:release=180,"
                             f"adelay={int(start*1000)}|{int(start*1000)},volume=1.0,"
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
                 f"atrim=0:{durv},aresample=48000[aout]")
    out = f"{OUT}/{slug}{HAU_TO}_co-tieng.mp4"
    mix = f"{OUT}/{slug}{HAU_TO}_hon-hop.wav"

    # lượt 1: dựng bản hoà trộn thô (chưa chuẩn hoá) để đo
    cmd = (["ffmpeg", "-v", "error", "-y", "-i", video] + ins +
           ["-filter_complex", ";".join(parts), "-map", "[aout]",
            "-c:a", "pcm_s16le", "-ar", "48000", mix])
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  {slug}: LỖI {r.stderr.strip()[:300]}")
        return

    # lượt 2: đo độ to thật của bản hoà trộn rồi mới chuẩn hoá (một lượt đoán mò
    # cho ra độ to lệch tới 3 LU giữa các tập, nghe rõ khi phát liền nhau)
    gain = max(-30.0, min(30.0, LOUD_I - do_to(mix)))
    lim = 10 ** (LOUD_TP / 20.0)
    # tăng/giảm đúng bằng chênh lệch đo được rồi chặn đỉnh ở mức TP; đo lại sau khi
    # mã hoá và chỉnh nốt phần còn lệch, để các tập lệch nhau không quá 0,3 LU
    for lan in range(6):
        ln = f"volume={gain:.2f}dB,alimiter=limit={lim:.4f}:attack=5:release=50:level=false"
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", mix,
                            "-map", "0:v", "-map", "1:a", "-af", ln + ",aresample=48000",
                            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                            "-movflags", "+faststart", out], capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  {slug}: LỖI {r.stderr.strip()[:300]}")
            os.remove(mix)
            return
        do_ra = do_to(out)
        lech = LOUD_I - do_ra
        if os.environ.get("VH_DEBUG"):
            print(f"    [debug] lượt {lan+1}: mix {do_to(mix):.2f} · gain {gain:.2f} · ra {do_ra:.2f} · lệch {lech:.2f}")
        if abs(lech) <= 0.3:
            break
        gain += lech

    if abs(LOUD_I - do_to(out)) > 0.5:
        print(f"    CẢNH BÁO còn lệch {LOUD_I - do_to(out):+.1f} LU so với mức đích")
    os.remove(mix)
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
          f"mức trung bình {mean} · đỉnh {peak} · {do_to(out):.1f} LUFS")
    print(f"    lời đọc vào ở: " + ", ".join(f"cảnh {i}@{s:.2f}s" for i, s in starts))


if __name__ == "__main__":
    TAPS = load_taps()
    for s in (sys.argv[1:] or list(TAPS)):
        ghep(s)
