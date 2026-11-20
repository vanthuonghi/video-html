#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sinh nhạc nền bằng ffmpeg — repo không cần kèm tệp âm thanh nào.
Ra: .thu-nghiem/audio/pad.wav (nền trầm) và swell.wav (tiếng vút chuyển cảnh).
Dùng: python3 sinh-nhac.py
"""
import os, subprocess, sys

BASE = os.environ.get("VH_BASE") or os.path.dirname(os.path.abspath(__file__))
AUD = f"{BASE}/.thu-nghiem/audio"


def chay(args, ten):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"LỖI khi tạo {ten}:\n{(r.stderr or '')[-500:]}")
        sys.exit(1)


def main():
    os.makedirs(AUD, exist_ok=True)
    pad, swell = f"{AUD}/pad.wav", f"{AUD}/swell.wav"

    # nền trầm: hai âm thấp chồng nhau, rung nhẹ, cắt đuôi cao
    chay(["ffmpeg", "-v", "error", "-y",
          "-f", "lavfi", "-i", "sine=frequency=110:sample_rate=48000:duration=90",
          "-f", "lavfi", "-i", "sine=frequency=163:sample_rate=48000:duration=90",
          "-filter_complex",
          "[0:a][1:a]amix=inputs=2:normalize=0,tremolo=f=0.12:d=0.35,"
          "lowpass=f=420,volume=0.5,aformat=channel_layouts=mono[a]",
          "-map", "[a]", "-c:a", "pcm_s16le", pad], "pad.wav")

    # tiếng vút: một dải nhiễu hẹp, vào ra êm — nghe như tiếng gió lướt khi chuyển cảnh
    chay(["ffmpeg", "-v", "error", "-y",
          "-f", "lavfi", "-i", "anoisesrc=color=pink:sample_rate=48000:duration=1.1",
          "-filter_complex",
          "highpass=f=300,lowpass=f=2600,tremolo=f=9:d=0.6,"
          "afade=t=in:st=0:d=0.3,afade=t=out:st=0.6:d=0.5,"
          "volume=0.35,aformat=channel_layouts=mono[a]",
          "-map", "[a]", "-c:a", "pcm_s16le", swell], "swell.wav")

    for f in (pad, swell):
        d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip()
        print(f"  {os.path.basename(f):10s} {d}s  {os.path.getsize(f)//1024} KB")


if __name__ == "__main__":
    main()
