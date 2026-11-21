#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chụp ảnh bìa (poster PNG) cho từng tập ở đúng mốc cover_at.

Ảnh bìa là khung hình đã vẽ xong nội dung, để dùng làm thumbnail khi đăng.
Ra: video-do-hoa/<slug>_poster.png (1080×1920)

Dùng: python3 sinh-poster.py [slug ...]
Cần máy chủ tĩnh đang phục vụ repo (mặc định http://127.0.0.1:8899).
"""
import base64, importlib.util, json, os, subprocess, sys, time, urllib.request

BASE = os.environ.get("VH_BASE") or os.path.dirname(os.path.abspath(__file__))
GOC = os.environ.get("VH_URL") or "http://127.0.0.1:8899"
OUT = f"{BASE}/video-do-hoa"


def nap(ten_tep, ten):
    sp = importlib.util.spec_from_file_location(ten, os.path.join(BASE, ten_tep))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


cn = nap("chup-nhanh.py", "cn")
dt = nap("dung-tap-do-hoa.py", "dt")


def chup(slug, giay):
    port = 9900 + abs(hash(slug)) % 90
    prof = f"/tmp/chrome-poster-{port}"
    os.makedirs(prof, exist_ok=True)
    url = f"{GOC}/do-hoa/{slug}.html"
    p = subprocess.Popen([cn.CHROME, "--headless=new", f"--remote-debugging-port={port}",
                          f"--user-data-dir={prof}", "--no-sandbox", "--disable-gpu",
                          "--hide-scrollbars", "--window-size=1080,1920",
                          "--disable-dev-shm-usage", "--mute-audio", url],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        ws = None
        for _ in range(60):
            try:
                d = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=3))
                pg = [t for t in d if t.get("type") == "page" and t.get("webSocketDebuggerUrl")]
                if pg:
                    ws = pg[0]["webSocketDebuggerUrl"]
                    break
            except Exception:
                pass
            time.sleep(0.4)
        if not ws:
            print(f"  {slug}: không mở được trình duyệt (CHROME_PATH?)")
            return False
        c = cn.CDP(ws)
        c.send("Page.enable")
        c.send("Runtime.enable")
        c.send("Emulation.setDeviceMetricsOverride", width=1080, height=1920,
               deviceScaleFactor=1, mobile=False)
        san_sang = False
        for _ in range(60):
            if c.eval("(typeof window.__total==='number')?window.__total:null"):
                san_sang = True
                break
            time.sleep(0.25)
        if not san_sang:
            print(f"  {slug}: trang chưa tải được ({url})")
            return False
        c.eval(f"window.__seek({giay:.3f})")
        time.sleep(0.35)               # để khung vẽ xong trước khi chụp
        shot = c.send("Page.captureScreenshot", format="png", fromSurface=True)
        ra = f"{OUT}/{slug}_poster.png"
        with open(ra, "wb") as fh:
            fh.write(base64.b64decode(shot["data"]))
        # bản 4:5 cho feed/YouTube: cắt giữa khung, giữ nguyên phần tiêu đề
        thumb = f"{OUT}/{slug}_thumb.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", ra, "-vf",
                        "crop=1080:1350:0:200", thumb], check=False)
        print(f"  {slug}: poster ở {giay:.1f}s · {os.path.getsize(ra)//1024} KB · "
              f"thumb {os.path.getsize(thumb)//1024} KB · {ra}")
        return True
    finally:
        try:
            p.terminate()
            p.wait(timeout=10)
        except Exception:
            p.kill()


def main():
    os.makedirs(OUT, exist_ok=True)
    chon = sys.argv[1:] or [e["slug"] for e in dt.EPISODES]
    loi = 0
    for ep in dt.EPISODES:
        if ep["slug"] in chon and not chup(ep["slug"], dt.cover_at(ep)):
            loi += 1
    return 1 if loi else 0


if __name__ == "__main__":
    sys.exit(main())
