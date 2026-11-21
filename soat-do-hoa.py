#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Soát bố cục từng tập: quét theo thời gian, tìm phần tử tràn khỏi vùng an toàn,
và in các giá trị số đang hiển thị để đối chiếu với thanh/biểu đồ.

Vùng an toàn 9:16 (khớp CSS trong dung-tap-do-hoa.py):
  x ∈ [96, 984], y ∈ [220, 1580] — chừa đỉnh cho thanh trạng thái, chừa đáy cho
  caption và nút của TikTok/Reels/Shorts. #brand nằm riêng ở dải trên cùng.

Dùng:
  python3 soat-do-hoa.py                        # soát mọi tập trong do-hoa/
  python3 soat-do-hoa.py 08_truong-nhin --step 2.5 --fail
Mã thoát 1 khi có tràn và bật --fail (dùng làm cổng trong CI).
Cần một máy chủ tĩnh phục vụ thư mục repo, mặc định http://127.0.0.1:8899.
"""
import argparse, importlib.util, json, os, subprocess, sys, time, urllib.request

BASE = os.environ.get("VH_BASE") or os.path.dirname(os.path.abspath(__file__))
GOC = os.environ.get("VH_URL") or "http://127.0.0.1:8899"
SAFE = {"trai": 96, "phai": 984, "tren": 220, "duoi": 1580}
BRAND = {"trai": 96, "phai": 984, "tren": 100, "duoi": 200}


def nap(tep, ten):
    sp = importlib.util.spec_from_file_location(ten, os.path.join(BASE, tep))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


cn = nap("chup-nhanh.py", "cn")
dt = nap("dung-tap-do-hoa.py", "dt")

AUDIT = r"""
(() => {
  const SAFE = __SAFE__, BRAND = __BRAND__;
  const out = {scene: -1, overflow: [], values: {}};
  const ngoai = (r, b) => r.left < b.trai - 1 || r.right > b.phai + 1 ||
                          r.top < b.tren - 1 || r.bottom > b.duoi + 1;
  const scenes = document.querySelectorAll('.scene');
  let best = -1, bestO = 0.05;
  scenes.forEach((s,i)=>{ const o = parseFloat(getComputedStyle(s).opacity); if (o > bestO) { bestO = o; best = i; } });
  out.scene = best;
  const ten = el => el.tagName + (el.id ? '#'+el.id : '') +
      (el.className && typeof el.className === 'string' ? '.'+el.className.split(' ')[0] : '');
  const ghi = (loai, el, r) => out.overflow.push({
      tag: loai + ten(el), x: Math.round(r.left), r: Math.round(r.right),
      y: Math.round(r.top), b: Math.round(r.bottom),
      txt: (el.textContent||'').trim().slice(0,28) });
  const kiem = (el, root, box, loai) => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    let o = parseFloat(cs.opacity); let p = el.parentElement;
    while (p && p !== root) { o *= parseFloat(getComputedStyle(p).opacity) || 0; p = p.parentElement; }
    if (o < 0.06) return;
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) return;
    if (ngoai(r, box)) ghi(loai, el, r);
  };
  if (best >= 0) {
    const root = scenes[best];
    root.querySelectorAll('*').forEach(el => kiem(el, root, SAFE, ''));
  }
  // dòng thương hiệu nằm ngoài khung cảnh, có dải an toàn riêng ở trên cùng
  document.querySelectorAll('#brand').forEach(el => kiem(el, document.body, BRAND, ''));
  // đo mực chữ thật bằng Range: khung khối không phình ra khi chữ tràn, nên cách đo khung bị sót
  scenes.forEach((s) => {
    if (parseFloat(getComputedStyle(s).opacity) < 0.3) return;
    s.querySelectorAll('h1,h2,.sub,.lines,.cluster,.list20,.list3,.crd,.badge,.cta,.testbar,.legend,.ages,.race,.chart,.grid,.stack,.waves,.eyewrap,.flash,.note').forEach(el => {
      const rg = document.createRange(); rg.selectNodeContents(el);
      const r = rg.getBoundingClientRect();
      if (r.width < 2 || r.height < 2) return;
      if (ngoai(r, SAFE)) ghi('MỰC CHỮ ', el, r);
    });
  });
  ['e1v','e1f2','e1f','e1v2','e3v','e3f','n21','n22','n31','n32','g1n','v1','v2','a1','a2','a3'].forEach(id=>{
    const el = document.getElementById(id);
    if (!el) return;
    out.values[id] = el.style.width ? el.style.width : (el.textContent||'').trim().slice(0,14);
  });
  return JSON.stringify(out);
})()
""".replace("__SAFE__", json.dumps(SAFE)).replace("__BRAND__", json.dumps(BRAND))


def audit(slug, total, step):
    """Trả về số chỗ tràn tìm thấy cho một tập."""
    port = 9600 + abs(hash(slug)) % 300
    prof = f"/tmp/chrome-prof-{port}"
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
            print(f"  {slug}: LỖI không mở được trình duyệt (CHROME_PATH?)")
            return 1
        c = cn.CDP(ws)
        c.send("Page.enable")
        c.send("Runtime.enable")
        c.send("Emulation.setDeviceMetricsOverride", width=1080, height=1920,
               deviceScaleFactor=1, mobile=False)
        for _ in range(60):
            if c.eval("(typeof window.__total==='number')?window.__total:null"):
                break
            time.sleep(0.25)
        seen = {}
        values = {}
        t = 0.0
        while t <= total:
            c.eval(f"window.__seek({t:.3f})")
            r = json.loads(c.eval(AUDIT))
            for o in r["overflow"]:
                khoa = (o["tag"], o["txt"])
                seen.setdefault(khoa, {"o": o, "ts": [], "scene": r["scene"]})["ts"].append(round(t, 1))
            for k, v in r.get("values", {}).items():
                if v:
                    values.setdefault(r["scene"], {})[k] = v
            t += step
        print(f"\n=== {slug} ===")
        if not seen:
            print("  bố cục: KHÔNG có phần tử tràn vùng an toàn")
        for (tag, txt), v in seen.items():
            o = v["o"]
            moc = ", ".join(str(x) for x in v["ts"][:5])
            print(f"  cảnh {v['scene']}: TRÀN {tag} '{txt}' "
                  f"x={o['x']} phải={o['r']} y={o['y']} đáy={o['b']} lúc t={moc}")
        for sc, kv in sorted(values.items()):
            if kv:
                print(f"  cảnh {sc} giá trị cuối: " + json.dumps(kv, ensure_ascii=False))
        return len(seen)
    finally:
        p.terminate()
        try:
            p.wait(timeout=10)
        except Exception:
            p.kill()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tap", nargs="*", help="mã tập; bỏ trống = mọi tập trong do-hoa/")
    ap.add_argument("--step", type=float, default=0.5, help="bước lấy mẫu, giây (CI dùng 2.5)")
    ap.add_argument("--fail", action="store_true", help="mã thoát 1 khi có tràn")
    a = ap.parse_args()

    tong = {e["slug"]: e["total"] for e in dt.EPISODES}
    thu_muc = os.path.join(BASE, "do-hoa")
    co = sorted(f[:-5] for f in os.listdir(thu_muc) if f.endswith(".html")) if os.path.isdir(thu_muc) else []
    chon = [t.replace(".html", "") for t in a.tap] or co
    thieu = [t for t in chon if t not in tong]
    if thieu:
        raise SystemExit("Không có tập: " + ", ".join(thieu))
    if not chon:
        raise SystemExit("Chưa có trang nào trong do-hoa/. Chạy: python3 dung-tap-do-hoa.py")

    tran = 0
    for s in chon:
        tran += audit(s, tong[s], a.step)
    print(f"\nKẾT LUẬN: {'KHÔNG tràn vùng an toàn' if tran == 0 else str(tran) + ' chỗ tràn'}")
    return 1 if (tran and a.fail) else 0


if __name__ == "__main__":
    sys.exit(main())
