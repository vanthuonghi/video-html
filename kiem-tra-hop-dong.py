#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kiểm hợp đồng render: cùng một mốc t phải cho ra cùng một khung hình.

Chụp ba mốc (đầu, giữa, cuối tập) ở **hai phiên trình duyệt khác nhau** rồi so.
Khung khác nhau nghĩa là hình còn phụ thuộc thời điểm chụp hay phụ thuộc máy —
khi đó mọi phép so sánh ảnh và mọi lần dựng lại đều không đáng tin.

So bằng PSNR chứ không bằng băm từng byte: ở khung thu phóng (1:1, 16:9), Chrome
rasterize chữ ở tỉ lệ khác nhau giữa hai phiên, nên mép chữ lệch dưới một mức điểm
ảnh — mắt không thấy, nhưng băm thì khác. Ngưỡng 45 dB là "không phân biệt được".

Dùng: python3 kiem-tra-hop-dong.py [slug ...]
Mã thoát 1 nếu có mốc lệch quá ngưỡng. Cần máy chủ tĩnh ở http://127.0.0.1:8899.
"""
import argparse, base64, importlib.util, json, os, re, subprocess, sys, tempfile, time, urllib.request

BASE = os.environ.get("VH_BASE") or os.path.dirname(os.path.abspath(__file__))
GOC = os.environ.get("VH_URL") or "http://127.0.0.1:8899"
NGUONG_PSNR = 45.0          # dB; dưới mức này là khác biệt nhìn thấy được


def nap(tep, ten):
    sp = importlib.util.spec_from_file_location(ten, os.path.join(BASE, tep))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


cn = nap("chup-nhanh.py", "cn")
dt = nap("dung-tap-do-hoa.py", "dt")


def ten_tep(slug, size):
    return f"{slug}.html" if tuple(size) == dt.KHUNG_GOC else f"{slug}_{size[0]}x{size[1]}.html"


def psnr(a, b):
    """PSNR giữa hai ảnh PNG (dB). Dùng ffmpeg vì nó đã là phụ thuộc của repo."""
    with tempfile.TemporaryDirectory() as d:
        pa, pb = os.path.join(d, "a.png"), os.path.join(d, "b.png")
        open(pa, "wb").write(a)
        open(pb, "wb").write(b)
        r = subprocess.run(["ffmpeg", "-hide_banner", "-i", pa, "-i", pb, "-lavfi", "psnr",
                            "-f", "null", "-"], capture_output=True, text=True)
        m = re.search(r"average:([0-9.]+|inf)", r.stderr or "")
        return float("inf") if (m and m.group(1) == "inf") else (float(m.group(1)) if m else 0.0)


def mot_phien(slug, mocs, size, port):
    """Mở trình duyệt, chụp từng mốc, trả về {mốc: ảnh PNG}. Mỗi lần gọi là phiên mới."""
    prof = f"/tmp/chrome-prof-{port}"
    os.makedirs(prof, exist_ok=True)
    rong, cao = size
    p = subprocess.Popen([cn.CHROME, "--headless=new", f"--remote-debugging-port={port}",
                          f"--user-data-dir={prof}", "--no-sandbox", "--disable-gpu",
                          "--hide-scrollbars", f"--window-size={rong},{cao}",
                          "--disable-dev-shm-usage", "--mute-audio",
                          f"{GOC}/do-hoa/{ten_tep(slug, size)}"],
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
            raise SystemExit(f"  {slug}: không mở được trình duyệt (CHROME_PATH?)")
        c = cn.CDP(ws)
        c.send("Page.enable")
        c.send("Runtime.enable")
        c.send("Network.enable"); c.send("Network.setCacheDisabled", cacheDisabled=True)
        c.send("Emulation.setDeviceMetricsOverride", width=rong, height=cao,
               deviceScaleFactor=1, mobile=False)
        # chờ đủ font và đủ ảnh (mã QR ở thẻ kết thúc) rồi mới chụp: ảnh chưa giải mã
        # xong ở một phiên là ra khung khác, dù bố cục không đổi
        san_sang = False
        for _ in range(80):
            if c.eval("(typeof window.__total==='number') && document.fonts.status==='loaded'"
                      " && Array.from(document.images).every(i=>i.complete && i.naturalWidth>0)"):
                san_sang = True
                break
            time.sleep(0.25)
        if not san_sang:
            print(f"  {slug}: cảnh báo — font/ảnh chưa nạp xong, kết quả có thể nhiễu")
        # khung đầu cần thời gian vẽ; chờ một lần rồi mới chụp, nếu không sẽ so ảnh trắng
        c.eval(f"window.__seek({mocs[0]:.3f})")
        time.sleep(0.3)
        ra = {}
        for t in mocs:
            c.eval(f"window.__seek({t:.3f})")
            c.ve_xong()
            shot = c.send("Page.captureScreenshot", format="png", fromSurface=True)
            ra[t] = base64.b64decode(shot["data"])
        return ra
    finally:
        p.terminate()
        try:
            p.wait(timeout=10)
        except Exception:
            p.kill()


def kiem(slug, total, size, port):
    mocs = [round(total * 0.05, 2), round(total * 0.5, 2), round(total - 0.05, 2)]
    a = mot_phien(slug, mocs, size, port)
    b = mot_phien(slug, mocs, size, port + 1)
    lech, do = [], {}
    for t in mocs:
        if a[t] == b[t]:
            do[t] = float("inf")
        else:
            do[t] = psnr(a[t], b[t])
        if do[t] < NGUONG_PSNR:
            lech.append(t)
    print(f"\n=== {slug} ({size[0]}×{size[1]}) ===")
    for t in mocs:
        muc = "giống hệt" if do[t] == float("inf") else f"PSNR {do[t]:.1f} dB"
        print(f"  t={t:>5}s  {muc}  {'khớp' if do[t] >= NGUONG_PSNR else 'LỆCH'}")
    if lech:
        print(f"  !! {len(lech)} mốc khác nhau nhìn thấy được: {', '.join(str(t) for t in lech)}")
    else:
        print("  cùng mốc t → cùng khung hình ở hai phiên khác nhau")
    return len(lech)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tap", nargs="*", help="mã tập; bỏ trống = hai tập đầu")
    ap.add_argument("--size", default="1080x1920")
    a = ap.parse_args()
    try:
        size = tuple(int(x) for x in a.size.lower().split("x"))
    except Exception:
        raise SystemExit(f"--size phải có dạng WxH (nhận: {a.size})")

    tong = {e["slug"]: e["total"] for e in dt.EPISODES}
    chon = a.tap or [e["slug"] for e in dt.EPISODES[:2]]
    thieu = [t for t in chon if t not in tong]
    if thieu:
        raise SystemExit("Không có tập: " + ", ".join(thieu))
    for s in chon:
        if not os.path.exists(os.path.join(BASE, "do-hoa", ten_tep(s, size))):
            raise SystemExit(f"Chưa có do-hoa/{ten_tep(s, size)}. Chạy: python3 dung-tap-do-hoa.py")

    port = 9800 + abs(hash(str(size))) % 100
    lech = 0
    for i, s in enumerate(chon):
        lech += kiem(s, tong[s], size, port + i * 2)
    print(f"\nKẾT LUẬN: {'TẤT ĐỊNH — cùng mốc t ra cùng khung' if lech == 0 else str(lech) + ' mốc lệch'}")
    return 1 if lech else 0


if __name__ == "__main__":
    sys.exit(main())
