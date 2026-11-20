#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kiểm tra một tập đã dựng: đúng thời lượng, có hình, có tiếng, và tiếng không bị câm.
Dùng: python3 kiem-tra.py <slug> [<slug> ...]      (mã thoát 1 nếu có tập lỗi)
"""
import importlib.util, json, os, subprocess, sys

BASE = os.environ.get("VH_BASE") or os.path.dirname(os.path.abspath(__file__))
OUT = f"{BASE}/video-do-hoa"


def load_episodes():
    sp = importlib.util.spec_from_file_location("dt", f"{BASE}/dung-tap-do-hoa.py")
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    return {e["slug"]: e for e in m.EPISODES}


def probe(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration,size:stream=codec_type,codec_name,width,height",
                        "-of", "json", f], capture_output=True, text=True)
    return json.loads(r.stdout)


def do_muc(f):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    mean = peak = None
    for line in r.splitlines():
        if "mean_volume:" in line:
            mean = float(line.split("mean_volume:")[-1].strip().split()[0])
        if "max_volume:" in line:
            peak = float(line.split("max_volume:")[-1].strip().split()[0])
    return mean, peak


def main():
    eps = load_episodes()
    args = sys.argv[1:] or list(eps)
    loi = 0
    for slug in args:
        ep = eps[slug]
        f = f"{OUT}/{slug}_co-tieng.mp4"
        print(f"\n=== {slug}")
        if not os.path.exists(f):
            print("  LỖI: chưa có tệp video"); loi += 1; continue
        d = probe(f)
        dur = float(d["format"]["duration"]); size = int(d["format"]["size"])
        vs = [s for s in d["streams"] if s["codec_type"] == "video"]
        aud = [s for s in d["streams"] if s["codec_type"] == "audio"]
        ok = True
        if abs(dur - ep["total"]) > 0.15:
            print(f"  LỖI: thời lượng {dur:.2f}s lệch so với kịch bản {ep['total']}s"); ok = False
        else:
            print(f"  thời lượng {dur:.2f}s khớp kịch bản")
        if not vs:
            print("  LỖI: không có luồng hình"); ok = False
        elif vs[0]["width"] != 1080 or vs[0]["height"] != 1920:
            print(f"  LỖI: khung {vs[0]['width']}x{vs[0]['height']}, phải là 1080x1920"); ok = False
        else:
            print(f"  khung {vs[0]['width']}x{vs[0]['height']} đúng")
        if not aud:
            print("  LỖI: không có luồng tiếng"); ok = False
        else:
            mean, peak = do_muc(f)
            if mean is None or mean < -40:
                print(f"  LỖI: tiếng gần như câm (trung bình {mean} dB)"); ok = False
            else:
                print(f"  tiếng: trung bình {mean} dB · đỉnh {peak} dB")
        print(f"  dung lượng {size/1048576:.1f} MB · số cảnh {len(ep['scenes'])}")
        loi += (not ok)
    print(f"\nKẾT LUẬN: {'TẤT CẢ ĐẠT' if loi == 0 else str(loi) + ' tập LỖI'}")
    return 1 if loi else 0


if __name__ == "__main__":
    sys.exit(main())
