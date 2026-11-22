#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dựng trọn một tập ở tỉ lệ khung khác 9:16: HTML → khung hình → mp4 → ghép tiếng.

Cùng kịch bản, cùng phụ đề, chỉ đổi khung. Dùng cho một tập mẫu trước khi nhân ra
cả chuỗi (mục 10 của kế hoạch: đừng làm cả bộ khi chưa chứng minh một tập).

Dùng: python3 dung-ti-le-khac.py <slug> --size 1080x1080 [--fps 24] [--workers 4]
                                    [--khong-tieng] [--port 9450]
Ra:   do-hoa/<slug>_WxH.html
      video-do-hoa/<slug>_WxH_co-tieng.mp4  (hoặc <slug>_WxH.mp4 nếu --khong-tieng)

Cần: máy chủ tĩnh phục vụ repo (python3 -m http.server 8899), ffmpeg, và lời đọc
trong .thu-nghiem/giong nếu muốn có tiếng.
"""
import argparse, importlib.util, json, os, subprocess, sys, urllib.request

BASE = os.environ.get("VH_BASE") or os.path.dirname(os.path.abspath(__file__))
GOC = os.environ.get("VH_URL") or "http://127.0.0.1:8899"


def nap(tep, ten):
    sp = importlib.util.spec_from_file_location(ten, os.path.join(BASE, tep))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def mo_duoc(url):
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            return r.status == 200
    except Exception:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--size", required=True, help="WxH, ví dụ 1080x1080 hay 1920x1080")
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--port", type=int, default=9450)
    ap.add_argument("--khong-tieng", action="store_true", help="chỉ dựng hình, bỏ bước ghép tiếng")
    a = ap.parse_args()

    dt = nap("dung-tap-do-hoa.py", "dt")
    try:
        size = tuple(int(x) for x in a.size.lower().split("x"))
    except Exception:
        raise SystemExit(f"--size phải có dạng WxH (nhận: {a.size})")
    if size == dt.KHUNG_GOC:
        raise SystemExit("Khung 9:16 dùng đường ống thường (chup-nhanh + ghep-tieng-tap).")
    ep = next((e for e in dt.EPISODES if e["slug"] == a.slug), None)
    if not ep:
        raise SystemExit(f"Không có tập: {a.slug}")

    hau = "_%dx%d" % size
    trang = os.path.join(BASE, "do-hoa", a.slug + hau + ".html")
    url = f"{GOC}/do-hoa/{a.slug}{hau}.html"
    khung = os.path.join(BASE, ".thu-nghiem", f"frames-{a.slug}{hau}")
    mp4 = os.path.join(BASE, "video-do-hoa", a.slug + hau + ".mp4")

    # 1. trang HTML đúng khung
    os.makedirs(os.path.dirname(trang), exist_ok=True)
    open(trang, "w", encoding="utf-8").write(dt.build_html(ep, size))
    print(f"1/4 trang: {trang}  ({ep['total']}s)")

    if not mo_duoc(url):
        raise SystemExit(f"  !! chưa mở được {url}\n"
                         f"     mở máy chủ trước: cd {BASE} && python3 -m http.server 8899")

    # 2. chụp khung
    subprocess.run([sys.executable, os.path.join(BASE, "chup-nhanh.py"), url, khung,
                    "--size", a.size, "--fps", str(a.fps), "--workers", str(a.workers),
                    "--port", str(a.port), "--clean"], check=True)
    print(f"2/4 khung: {khung}")

    # 3. mã hoá
    os.makedirs(os.path.dirname(mp4), exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(a.fps),
                    "-i", os.path.join(khung, "%05d.jpg"),
                    "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-r", str(a.fps), mp4],
                   check=True)
    print(f"3/4 hình: {mp4}")

    # 4. tiếng (dùng đúng bộ trộn của bản dọc, chỉ đổi tên tệp qua VH_HAU_TO)
    if a.khong_tieng:
        print("4/4 tiếng: bỏ qua (--khong-tieng)")
    else:
        env = dict(os.environ, VH_HAU_TO=hau)
        subprocess.run([sys.executable, os.path.join(BASE, "ghep-tieng-tap.py"), a.slug],
                       env=env, check=True)
        print(f"4/4 tiếng: video-do-hoa/{a.slug}{hau}_co-tieng.mp4")


if __name__ == "__main__":
    main()
