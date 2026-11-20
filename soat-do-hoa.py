#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Soát bố cục từng tập: quét theo thời gian, tìm phần tử tràn khỏi vùng an toàn
và kiểm các con số hiển thị có khớp với thanh/biểu đồ hay không."""
import json, os, subprocess, sys, time, urllib.request
import importlib.util
spec = importlib.util.spec_from_file_location("cn", "/home/vider/speedreading-90days/chup-nhanh.py")
cn = importlib.util.module_from_spec(spec); spec.loader.exec_module(cn)

TAP = ["02_noi-tham-trong-dau", "03_bieu-do-tri-quen", "04_nao-giu-5-10-phut",
       "05_phuhuynh-con-bo-sach", "06_ky-thuat-chi-tay"]

AUDIT = r"""
(() => {
  const out = {scene: -1, overflow: [], values: {}};
  const scenes = document.querySelectorAll('.scene');
  let best = -1, bestO = 0.05;
  scenes.forEach((s,i)=>{ const o = parseFloat(getComputedStyle(s).opacity); if (o > bestO) { bestO = o; best = i; } });
  out.scene = best;
  if (best >= 0) {
    const root = scenes[best];
    root.querySelectorAll('*').forEach(el => {
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') return;
      let o = parseFloat(cs.opacity); let p = el.parentElement;
      while (p && p !== root) { o *= parseFloat(getComputedStyle(p).opacity) || 0; p = p.parentElement; }
      if (o < 0.06) return;
      const r = el.getBoundingClientRect();
      if (r.width < 2 || r.height < 2) return;
      if (r.left < 30 || r.right > 1050 || r.top < 60 || r.bottom > 1860) {
        out.overflow.push({tag: el.tagName + (el.id ? '#'+el.id : '') + (el.className && typeof el.className === 'string' ? '.'+el.className.split(' ')[0] : ''),
                           x: Math.round(r.left), r: Math.round(r.right), y: Math.round(r.top), b: Math.round(r.bottom),
                           txt: (el.textContent||'').trim().slice(0,28)});
      }
    });
  }
  ['e1v','e1f2','e1f','e1v2','e3v','e3f','n21','n22','n31','n32','g1n','v1','v2','a1','a2','a3'].forEach(id=>{
    const el = document.getElementById(id);
    if (!el) return;
    const cs = getComputedStyle(el);
    out.values[id] = el.style.width ? el.style.width : (el.textContent||'').trim().slice(0,14);
  });
  return JSON.stringify(out);
})()
"""

def audit(slug, total):
    port = 9600 + abs(hash(slug)) % 300
    prof = f"/tmp/chrome-prof-{port}"; os.makedirs(prof, exist_ok=True)
    url = f"http://127.0.0.1:8899/do-hoa/{slug}.html"
    p = subprocess.Popen([cn.CHROME, "--headless=new", f"--remote-debugging-port={port}",
        f"--user-data-dir={prof}", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
        "--window-size=1080,1920", "--disable-dev-shm-usage", "--mute-audio", url],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        ws = None
        for _ in range(60):
            try:
                d = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=3))
                pg = [t for t in d if t.get("type") == "page" and t.get("webSocketDebuggerUrl")]
                if pg: ws = pg[0]["webSocketDebuggerUrl"]; break
            except Exception: pass
            time.sleep(0.4)
        c = cn.CDP(ws)
        c.send("Page.enable"); c.send("Runtime.enable")
        c.send("Emulation.setDeviceMetricsOverride", width=1080, height=1920, deviceScaleFactor=1, mobile=False)
        for _ in range(60):
            if c.eval("(typeof window.__total==='number')?window.__total:null"): break
            time.sleep(0.25)
        seen, over, vals = {}, {}, {}
        t = 0.0
        while t <= total:
            c.eval(f"window.__seek({t:.3f})")
            r = json.loads(c.eval(AUDIT))
            if r["scene"] >= 0:
                for o in r["overflow"]:
                    over.setdefault(r["scene"], []).append((round(t,1), o))
            for k, v in r.get("values", {}).items():
                if v: (seen.setdefault(r["scene"], {}) or {})[k] = v
            t += 0.5
        print(f"\n=== {slug} ===")
        if not over:
            print("  bố cục: KHÔNG có phần tử tràn vùng an toàn")
        for sc, items in sorted(over.items()):
            uniq = {}
            for tt, o in items: uniq.setdefault((o["tag"], o["txt"]), []).append(tt)
            for (tag, txt), ts in uniq.items():
                print(f"  cảnh {sc}: TRÀN {tag} '{txt}' x={[i[1]['x'] for i in items if (i[1]['tag'],i[1]['txt'])==(tag,txt)][0]} "
                      f"phải={[i[1]['r'] for i in items if (i[1]['tag'],i[1]['txt'])==(tag,txt)][0]} "
                      f"y={[i[1]['y'] for i in items if (i[1]['tag'],i[1]['txt'])==(tag,txt)][0]} lúc t={ts[:4]}")
        for sc, kv in sorted(seen.items()):
            if kv: print(f"  cảnh {sc} giá trị cuối: " + json.dumps(kv, ensure_ascii=False))
    finally:
        p.terminate()


if __name__ == "__main__":
    # đọc tổng thời lượng từ chính file dựng tập, không chép tay
    import importlib.util
    sp = importlib.util.spec_from_file_location("dt", "/home/vider/speedreading-90days/dung-tap-do-hoa.py")
    dt = importlib.util.module_from_spec(sp); sp.loader.exec_module(dt)
    totals = {e["slug"]: e["total"] for e in dt.EPISODES}
    for s in (sys.argv[1:] or TAP):
        s = s.replace(".html", "")
        audit(s, totals[s])
