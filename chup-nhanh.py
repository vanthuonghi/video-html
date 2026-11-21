#!/usr/bin/env python3
"""Chụp khung hình HTML thành ảnh, hỗ trợ chia việc song song và đo tốc độ.

Dùng:
  python3 chup-nhanh.py URL OUTDIR [--from N] [--to M] [--port P] [--fps F]
  python3 chup-nhanh.py URL OUTDIR --workers 4 --total 40
"""
import argparse, base64, json, os, re, shutil, subprocess, sys, time, urllib.request
import websocket


def find_chrome():
    """Tìm trình duyệt: biến môi trường trước, rồi tới PATH, cuối cùng là bản cài sẵn trên máy này."""
    env = os.environ.get("CHROME_PATH")
    if env and os.path.exists(env):
        return env
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        p = shutil.which(name)
        if p:
            return p
    for p in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium",
              os.path.expanduser("~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")):
        if os.path.exists(p):
            return p
    raise SystemExit("Không tìm thấy trình duyệt. Đặt biến CHROME_PATH trỏ tới file chrome.")


CHROME = find_chrome()
W, H = 1080, 1920


class CDP:
    def __init__(self, ws_url):
        self.ws = websocket.create_connection(ws_url, timeout=60, suppress_origin=True)
        self.n = 0

    def send(self, method, **params):
        self.n += 1
        mid = self.n
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})

    def eval(self, expr):
        r = self.send("Runtime.evaluate", expression=expr, returnByValue=True)
        return r.get("result", {}).get("value")


def capture(url, outdir, port, frm, to, fps, quality, gpu, total, label="", probe_only=False):
    os.makedirs(outdir, exist_ok=True)
    profile = f"/tmp/chrome-prof-{port}"
    os.makedirs(profile, exist_ok=True)
    flags = [CHROME, "--headless=new", f"--remote-debugging-port={port}",
             f"--user-data-dir={profile}", "--no-sandbox", "--hide-scrollbars",
             "--force-device-scale-factor=1", f"--window-size={W},{H}",
             "--disable-dev-shm-usage", "--mute-audio"]
    if not gpu:
        flags.append("--disable-gpu")
    flags.append(url)
    chrome = subprocess.Popen(flags, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        ws_url = None
        for _ in range(80):
            try:
                data = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=3))
                pages = [t for t in data if t.get("type") == "page" and t.get("webSocketDebuggerUrl")]
                if pages:
                    ws_url = pages[0]["webSocketDebuggerUrl"]
                    break
            except Exception:
                pass
            time.sleep(0.4)
        if not ws_url:
            print(f"  [{label or port}] không kết nối được trình duyệt")
            return 0.0
        c = CDP(ws_url)
        c.send("Page.enable"); c.send("Runtime.enable")
        c.send("Emulation.setDeviceMetricsOverride", width=W, height=H,
               deviceScaleFactor=1, mobile=False)
        if not total:
            for _ in range(80):
                total = c.eval("(typeof window.__total === 'number') ? window.__total : null")
                if total:
                    break
                time.sleep(0.25)
        if not total:
            print(f"  [{label or port}] trang chưa sẵn sàng")
            return 0.0
        if probe_only:
            print(f"TOTAL={total}")
            return 0.0
        n_total = int(round(total * fps))
        hi = min(to if to is not None else n_total - 1, n_total - 1)
        t0 = time.time(); n = 0
        for i in range(frm, hi + 1):
            c.eval(f"window.__seek({i / fps:.4f})")
            shot = c.send("Page.captureScreenshot", format="jpeg", quality=quality,
                          fromSurface=True, optimizeForSpeed=True)
            with open(f"{outdir}/{i:05d}.jpg", "wb") as fh:
                fh.write(base64.b64decode(shot["data"]))
            n += 1
        el = time.time() - t0
        if n:
            print(f"  [{label or port}] {frm}–{hi}: {n} khung · {el:.1f}s · {n/el:.1f} khung/giây")
        return n / el if n else 0.0
    finally:
        try:
            chrome.terminate(); chrome.wait(timeout=10)
        except Exception:
            chrome.kill()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url"); ap.add_argument("outdir")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--quality", type=int, default=90)
    ap.add_argument("--from", dest="frm", type=int, default=0)
    ap.add_argument("--to", type=int, default=None)
    ap.add_argument("--port", type=int, default=9222)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--gpu", action="store_true")
    ap.add_argument("--total", type=float, default=None)
    ap.add_argument("--clean", action="store_true", help="xoá ảnh cũ trong thư mục đích")
    ap.add_argument("--probe", action="store_true", help="chỉ đọc tổng thời lượng của trang rồi thoát")
    a = ap.parse_args()

    if a.probe:
        capture(a.url, a.outdir, a.port, 0, 0, a.fps, a.quality, a.gpu, None, probe_only=True)
        return

    if a.clean:
        for f in os.listdir(a.outdir) if os.path.isdir(a.outdir) else []:
            if f.endswith(".jpg"):
                os.remove(os.path.join(a.outdir, f))

    if a.workers <= 1:
        t0 = time.time()
        capture(a.url, a.outdir, a.port, a.frm, a.to, a.fps, a.quality, a.gpu, a.total)
        print(f"  tổng thời gian: {time.time()-t0:.1f}s")
        return

    # hỏi thẳng trang xem nó dài bao nhiêu giây, không đoán
    total = a.total
    if not total:
        r = subprocess.run([sys.executable, __file__, a.url, "/tmp/probe-frames",
                            "--probe", "--port", str(a.port + 90)],
                           capture_output=True, text=True)
        m = re.search(r"TOTAL=([0-9.]+)", r.stdout)
        if not m:
            print("!! không đọc được tổng thời lượng của trang:")
            print((r.stdout or "")[-300:], (r.stderr or "")[-300:])
            return
        total = float(m.group(1))
        print(f"  trang dài {total}s")
    n_total = int(round(total * a.fps))
    hi = n_total - 1 if a.to is None else a.to
    lo = a.frm
    per = max(1, (hi - lo + 1) // a.workers)
    procs, t0 = [], time.time()
    for k in range(a.workers):
        s = lo + k * per
        e = hi if k == a.workers - 1 else s + per - 1
        if s > hi:
            break
        procs.append(subprocess.Popen([
            sys.executable, __file__, a.url, a.outdir, "--from", str(s), "--to", str(e),
            "--port", str(a.port + k), "--fps", str(a.fps), "--quality", str(a.quality),
            "--total", str(total)] + (["--gpu"] if a.gpu else [])))
    for p in procs:
        p.wait()
    el = time.time() - t0
    got = len([f for f in os.listdir(a.outdir) if f.endswith(".jpg")])
    want = hi - lo + 1
    canh_bao = "" if got == want else "   <<< THIẾU KHUNG, kiểm lại"
    print(f"TỔNG: {a.workers} tiến trình · cần {want} khung · có {got} khung · {el:.1f}s · {got/el:.1f} khung/giây{canh_bao}")


if __name__ == "__main__":
    main()
