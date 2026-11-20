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
    for i, w in enumerate(spec["wins"], 1):
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
        chain = f"[{n_in}:a]"
        if tempo > 1.001:
            chain += f"atempo={tempo},"
        start = t + OFFSET
        starts.append((i, start))
        parts.append(chain + f"adelay={int(start*1000)}|{int(start*1000)},volume=1.0[n{n_lbl}]")
        t += w
    pi = n_in + 1                        # pad
    si = pi + 1                          # swell
    ins += ["-stream_loop", "-1", "-i", PAD, "-stream_loop", "-1", "-i", SWELL]
    parts.append(f"[{pi}:a]atrim=0:{durv},volume={PAD_VOL}[pad]")
    parts.append(f"[{si}:a]atrim=0:{durv},volume={SWELL_VOL}[sw]")
    mix = "".join(f"[n{i}]" for i in range(1, n_lbl + 1)) + "[pad][sw]"
    parts.append(f"{mix}amix=inputs={n_lbl+2}:duration=longest:normalize=0,"
                 f"alimiter=limit=0.95,atrim=0:{durv}[aout]")
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
