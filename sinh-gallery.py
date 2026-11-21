#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sinh gallery/index.html: xem trước cả bộ tập ngay trong trình duyệt.

Dùng: python3 sinh-gallery.py

Mỗi tập là một iframe 1080×1920 thu nhỏ, có thanh tua gọi thẳng
`contentWindow.__seek(t)` — trang HTML đã có sẵn hàm đó nên không cần render lại.
Tệp sinh ra nằm ở `gallery/index.html`, dùng được với GitHub Pages (chọn thư mục
`/gallery` trong Settings → Pages) hoặc mở bằng `python3 -m http.server`.
"""
import importlib.util, json, os

BASE = os.environ.get("VH_BASE") or os.path.dirname(os.path.abspath(__file__))
RELEASE = "https://github.com/vanthuonghi/video-html/releases/download/moi-nhat"


def nap(ten, khoa):
    sp = importlib.util.spec_from_file_location(khoa, f"{BASE}/{ten}")
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


dt = nap("dung-tap-do-hoa.py", "dt")
nd = json.load(open(f"{BASE}/noi-dung.json", encoding="utf-8"))


def the(ep, i, tong):
    slug, ten = ep["slug"], ep["ten"]
    giay = ep["total"]
    return f"""    <article class="the" data-slug="{slug}">
      <button class="khung" data-mo="{slug}">
        <img loading="lazy" src="{RELEASE}/{slug}_poster.png" alt="Ảnh bìa tập {i+1}: {ten}">
        <span class="so">TẬP {i+1}/{tong}</span>
        <span class="choi">▶ Xem trước</span>
      </button>
      <h2>{ten}</h2>
      <p class="meta">{giay:.0f} giây · <a href="{RELEASE}/{slug}_co-tieng.mp4" target="_blank" rel="noopener">tải mp4</a>
        · <a href="{RELEASE}/{slug}.srt" target="_blank" rel="noopener">.srt</a></p>
    </article>"""


def trang():
    tong = len(dt.EPISODES)
    the_html = "\n".join(the(ep, i, tong) for i, ep in enumerate(dt.EPISODES))
    dau_tien = dt.EPISODES[0]["slug"]
    return f"""<!doctype html>
<html lang="vi">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{nd['thuong_hieu']} — {tong} tập</title>
<style>
  :root {{ --nen:#0d1113; --chu:#f2f5f4; --nhan:#a9b4b2; --nhan2:#8fa19d; --nhan3:#3fb8a8; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--nen); color:var(--chu);
         font-family:"Noto Sans",system-ui,-apple-system,"Segoe UI",sans-serif; }}
  header {{ padding:56px 32px 24px; max-width:1240px; margin:0 auto; }}
  header .hieu {{ font-size:13px; letter-spacing:.22em; color:var(--nhan2); text-transform:uppercase; }}
  header h1 {{ font-size:clamp(28px,5vw,46px); margin:12px 0 8px; line-height:1.15; }}
  header p {{ color:var(--nhan); margin:0; font-size:16px; }}
  .luoi {{ display:grid; gap:28px; padding:16px 32px 72px; max-width:1240px; margin:0 auto;
           grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); }}
  .the h2 {{ font-size:17px; margin:12px 0 4px; line-height:1.35; }}
  .the .meta {{ margin:0; color:var(--nhan2); font-size:13px; }}
  .the a {{ color:var(--nhan3); text-decoration:none; }}
  .the a:hover {{ text-decoration:underline; }}
  .khung {{ position:relative; display:block; width:100%; padding:0; border:0; cursor:pointer;
            background:#111; border-radius:14px; overflow:hidden; aspect-ratio:9/16; }}
  .khung img {{ width:100%; height:100%; object-fit:cover; display:block; }}
  .khung .so {{ position:absolute; top:10px; left:10px; font-size:11px; letter-spacing:.12em;
                background:rgba(6,17,15,.78); padding:5px 9px; border-radius:999px; }}
  .khung .choi {{ position:absolute; inset:auto 0 0 0; padding:10px; font-size:13px;
                  background:linear-gradient(transparent,rgba(6,17,15,.9)); opacity:0;
                  transition:opacity .18s; }}
  .khung:hover .choi, .khung:focus-visible .choi {{ opacity:1; }}
  /* trình xem */
  #xem {{ position:fixed; inset:0; background:rgba(4,10,9,.94); display:none;
          align-items:center; justify-content:center; gap:28px; padding:24px; z-index:10; }}
  #xem.mo {{ display:flex; }}
  #xem .khung-xem {{ width:min(46vw,430px); aspect-ratio:9/16; position:relative; }}
  #xem iframe {{ position:absolute; inset:0; width:1080px; height:1920px; border:0;
                 transform-origin:top left; background:#000; border-radius:8px; }}
  #xem .ben {{ max-width:340px; }}
  #xem .ben h3 {{ margin:0 0 6px; font-size:22px; }}
  #xem .ben .so {{ color:var(--nhan2); font-size:13px; letter-spacing:.12em; }}
  #xem input[type=range] {{ width:100%; margin:18px 0 6px; accent-color:var(--nhan3); }}
  #xem .hang {{ display:flex; gap:10px; align-items:center; }}
  #xem button {{ background:#16201f; color:var(--chu); border:1px solid #24312f; border-radius:10px;
                 padding:10px 16px; font-size:14px; cursor:pointer; }}
  #xem button:hover {{ border-color:var(--nhan3); }}
  #xem .dong {{ color:var(--nhan2); font-size:13px; margin-top:10px; }}
  @media (max-width:720px) {{
    #xem {{ flex-direction:column; gap:14px; }}
    #xem .khung-xem {{ width:min(64vw,300px); }}
    header, .luoi {{ padding-left:18px; padding-right:18px; }}
  }}
</style>

<header>
  <div class="hieu">{nd['thuong_hieu']}</div>
  <h1>{tong} tập đọc nhanh — xem trước ngay tại đây</h1>
  <p>{nd['mo_ta_cuoi']} · <a href="{nd['dang_ky']}" target="_blank" rel="noopener"
     style="color:var(--nhan3)">{nd['dang_ky_nhan'].lower()}</a></p>
</header>

<main class="luoi">
{the_html}
</main>

<div id="xem" role="dialog" aria-modal="true" aria-label="Xem trước tập">
  <div class="khung-xem"><iframe id="khung" src="about:blank" title="Xem trước tập"></iframe></div>
  <div class="ben">
    <div class="so" id="so"></div>
    <h3 id="ten"></h3>
    <input id="tua" type="range" min="0" max="100" step="0.02" value="0" aria-label="Tua thời gian">
    <div class="hang">
      <button id="chay">▶ Phát</button>
      <button id="dong">Đóng</button>
    </div>
    <div class="dong" id="gio">0,0s / 0,0s</div>
  </div>
</div>

<script>
const TONG = {tong};
const ds = {json.dumps([{"slug": e["slug"], "ten": e["ten"], "total": e["total"]} for e in dt.EPISODES], ensure_ascii=False)};
const xem = document.getElementById('xem');
const khung = document.getElementById('khung');
const tua = document.getElementById('tua');
const gio = document.getElementById('gio');
const nut = document.getElementById('chay');
let dang = null, dangChay = false, moc = 0;

function datCo(vua) {{
  // iframe là 1080×1920 thật, chỉ thu nhỏ bằng transform cho khớp khung xem
  const r = khung.parentElement.getBoundingClientRect();
  khung.style.transform = `scale(${{r.width / 1080}})`;
  khung.style.width = '1080px';
  khung.style.height = '1920px';
}}
addEventListener('resize', () => {{ if (xem.classList.contains('mo')) datCo(false); }});

function mo(slug) {{
  dang = ds.find(x => x.slug === slug);
  document.getElementById('so').textContent = `TẬP ${{ds.indexOf(dang) + 1}}/${{TONG}}`;
  document.getElementById('ten').textContent = dang.ten;
  tua.max = dang.total;
  tua.value = 0; moc = 0; setChay(false);
  khung.src = `../do-hoa/${{slug}}.html`;
  xem.classList.add('mo');
  requestAnimationFrame(() => datCo(true));
  khung.onload = () => seek(0);
}}

function seek(t) {{
  moc = Math.max(0, Math.min(dang ? dang.total : 0, t));
  tua.value = moc;
  gio.textContent = `${{moc.toFixed(1).replace('.', ',')}}s / ${{dang ? dang.total.toFixed(1).replace('.', ',') : 0}}s`;
  try {{ khung.contentWindow.__seek(moc); }} catch (e) {{}}
}}

function setChay(v) {{
  dangChay = v;
  nut.textContent = v ? '❚❚ Dừng' : '▶ Phát';
}}

let truoc = 0;
function vong(now) {{
  if (dangChay) {{
    const dt = (now - truoc) / 1000;
    truoc = now;
    let t = moc + dt;
    if (t >= dang.total) {{ t = dang.total; setChay(false); }}
    seek(t);
  }} else {{ truoc = now; }}
  requestAnimationFrame(vong);
}}
requestAnimationFrame(vong);

document.querySelectorAll('[data-mo]').forEach(b => b.addEventListener('click', () => mo(b.dataset.mo)));
tua.addEventListener('input', () => {{ setChay(false); seek(parseFloat(tua.value)); }});
nut.addEventListener('click', () => {{
  if (moc >= dang.total - 0.05) seek(0);
  truoc = performance.now(); setChay(!dangChay);
}});
function dong() {{ setChay(false); xem.classList.remove('mo'); khung.src = 'about:blank'; }}
document.getElementById('dong').addEventListener('click', dong);
addEventListener('keydown', e => {{
  if (e.key === 'Escape') dong();
  if (!dang || !xem.classList.contains('mo')) return;
  if (e.key === 'ArrowRight') {{ setChay(false); seek(moc + 2); }}
  if (e.key === 'ArrowLeft') {{ setChay(false); seek(moc - 2); }}
  if (e.key === ' ') {{ e.preventDefault(); nut.click(); }}
}});
</script>
</html>
"""


def main():
    ra = f"{BASE}/gallery"
    os.makedirs(ra, exist_ok=True)
    p = f"{ra}/index.html"
    open(p, "w", encoding="utf-8").write(trang())
    print(f"  {len(dt.EPISODES)} tập · {os.path.getsize(p)//1024} KB · {p}")
    print("  bật Pages: Settings → Pages → thư mục /gallery")
    if "dang-ky" in nd.get("dang_ky", ""):
        print("  CẢNH BÁO: `dang_ky` trong noi-dung.json vẫn là link mẫu")


if __name__ == "__main__":
    main()
