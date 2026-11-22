#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dựng trang HTML cho từng tập video đồ hoạ từ một khuôn chung.

Kịch bản (slug, cảnh, HTML từng cảnh, hàm vẽ theo thời gian, lời đọc) nằm ở
kich-ban.py; tệp này giữ khung: CSS, JS __seek, phụ đề, thẻ kết thúc, tỉ lệ khung.

Chạy: python3 dung-tap-do-hoa.py                     -> ghi do-hoa/<slug>.html
      python3 dung-tap-do-hoa.py --loi-doc           -> in danh sách lời đọc cần sinh
      python3 dung-tap-do-hoa.py --size 1080x1080 --tap <slug>
"""
import importlib.util, json, os, re, subprocess, sys

BASE = os.environ.get("VH_BASE") or os.path.dirname(os.path.abspath(__file__))
OUT = f"{BASE}/do-hoa"
GIONG = f"{BASE}/.thu-nghiem/giong"
OFFSET, GAP = 0.35, 0.5      # khớp ghep-tieng-tap.py: lời đọc vào sau khi cảnh hiện
SO_TU_CUE = 4                # số từ mỗi dòng phụ đề

# Kịch bản nằm ở kich-ban.py (tên tệp có dấu gạch nên nạp theo đường dẫn).
_sp = importlib.util.spec_from_file_location("kich_ban", os.path.join(BASE, "kich-ban.py"))
_kb = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(_kb)
CTA, EPISODES, PASSAGE = _kb.CTA, _kb.EPISODES, _kb.PASSAGE

# Khung thiết kế gốc là 9:16 (1080×1920). Tỉ lệ khác dùng chính các cảnh đó:
# thu phóng vừa khung và nới bề ngang cột nội dung, không dựng lại bố cục.
KHUNG_GOC = (1080, 1920)
COT_RONG_NHAT = 1320.0       # bề ngang cột nội dung tối đa, tính theo px thiết kế

CSS = """
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{width:1080px;height:1920px;overflow:hidden;background:#0d1113}
  /* font tải sẵn trong do-hoa/fonts: mọi máy dựng ra cùng một bố cục chữ */
  body{font-family:"VH Noto Sans","Noto Sans","DejaVu Sans",sans-serif;color:#f2f5f4;-webkit-font-smoothing:antialiased}
  #stage{position:absolute;inset:0;overflow:hidden}
  #bg{position:absolute;inset:-10%;background:
      radial-gradient(1200px 900px at 20% 12%, rgba(63,184,168,.16), transparent 60%),
      radial-gradient(900px 800px at 85% 88%, rgba(63,184,168,.10), transparent 62%),
      linear-gradient(160deg,#0d1113 0%,#121a19 55%,#0d1113 100%);will-change:transform}
  .grain{position:absolute;inset:0;opacity:.05;background-image:radial-gradient(#fff 1px, transparent 1px);background-size:6px 6px}
  /* vùng an toàn 9:16: đỉnh chừa thanh trạng thái, đáy chừa caption + nút của nền tảng */
  .scene{position:absolute;inset:0;padding:220px 96px 350px;display:flex;flex-direction:column;justify-content:center;opacity:0;will-change:transform,opacity}
  .kicker{font-size:34px;letter-spacing:.14em;text-transform:uppercase;color:#3fb8a8;font-weight:700;margin-bottom:38px}
  h1{font-size:92px;line-height:1.12;font-weight:800;letter-spacing:-.02em}
  h1 .hl{color:#3fb8a8}
  h1 .bad{color:#e08374}
  .sub{font-size:40px;line-height:1.42;color:#a9b4b2;margin-top:40px}
  .sub b{color:#f2f5f4}
  /* thanh tốc độ */
  .race{margin-top:30px}
  .race .row{margin-bottom:52px}
  .race .name{font-size:36px;color:#a9b4b2;margin-bottom:14px;display:flex;justify-content:space-between}
  .race .name b{color:#f2f5f4}
  .track{height:56px;border-radius:14px;background:#1a2523;overflow:hidden;position:relative}
  .fill{height:100%;border-radius:14px;background:linear-gradient(90deg,#2f8f84,#3fb8a8);width:0}
  .fill.red{background:linear-gradient(90deg,#b96254,#e08374)}
  .cap{position:absolute;left:0;top:-14px;bottom:-14px;width:5px;background:#e08374;opacity:0}
  .caplbl{font-size:30px;color:#e08374;margin-top:8px;opacity:0}
  .val{font-variant-numeric:tabular-nums}
  /* biểu đồ cột */
  .chart{display:flex;align-items:flex-end;gap:26px;height:700px;margin-top:20px}
  .col{flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;height:100%}
  .col .bar{width:100%;border-radius:14px 14px 0 0;background:linear-gradient(180deg,#3fb8a8,#1f6f67);height:0}
  .col .bar.red{background:linear-gradient(180deg,#e08374,#8f463a)}
  .col .num{font-size:44px;font-weight:800;font-variant-numeric:tabular-nums;margin-bottom:12px}
  .col .lab{font-size:30px;color:#8fa19d;margin-top:16px;text-align:center}
  /* lưới ô nhớ */
  .grid{display:grid;grid-template-columns:repeat(8,1fr);gap:16px;margin-top:20px}
  .blk{height:86px;border-radius:12px;background:#3fb8a8;opacity:0}
  .gridline{font-size:32px;color:#8fa19d;margin-top:26px;display:flex;justify-content:space-between}
  /* thẻ nguyên nhân */
  .cards{display:flex;flex-direction:column;gap:34px;margin-top:10px}
  .crd{display:flex;gap:30px;align-items:center;background:#16211f;border:2px solid #24322f;border-radius:22px;padding:36px 40px;opacity:0}
  .crd .idx{width:86px;height:86px;border-radius:22px;background:#3fb8a8;color:#06211e;font-size:52px;font-weight:800;display:grid;place-items:center;flex:0 0 auto}
  .crd .txt b{display:block;font-size:44px}
  .crd .txt span{font-size:32px;color:#9fb0ac}
  /* so sánh điện thoại / sách */
  .versus{display:flex;gap:34px;margin-top:20px}
  .vs{flex:1;background:#16211f;border:2px solid #24322f;border-radius:22px;padding:34px;text-align:center}
  .vs .nm{font-size:38px;font-weight:700;margin-bottom:18px}
  .vs .meter{height:44px;border-radius:12px;background:#1a2523;overflow:hidden}
  .vs .meter i{display:block;height:100%;width:0;background:#3fb8a8;border-radius:12px}
  .vs .m2{background:#e08374}
  .vs .note{font-size:30px;color:#8fa19d;margin-top:16px}
  /* bảng tuổi */
  .ages{margin-top:20px}
  .ageline{display:flex;align-items:center;gap:26px;margin-bottom:30px}
  .ageline .age{width:270px;font-size:38px;font-weight:700}
  .ageline .ab{flex:1;height:44px;border-radius:12px;background:#1a2523;overflow:hidden}
  .ageline .ab i{display:block;height:100%;width:0;background:#3fb8a8;border-radius:12px}
  .ageline .mins{font-size:38px;font-weight:700;color:#cfe9e4;width:330px;text-align:right}
  /* câu chữ cho tập chỉ tay */
  .lines{font-size:42px;line-height:1.5;font-weight:700;position:relative;margin-top:10px}
  .lines .ln{margin-bottom:22px;white-space:nowrap}
  .lines .wd{display:inline-block;padding:2px 5px;border-radius:10px;color:#8fa19d}
  .lines .wd.lit{color:#f2f5f4;background:#22423d}
  .finger{position:absolute;top:0;left:0;width:70px;height:104px;border-radius:20px;background:rgba(63,184,168,.9);will-change:transform}
  .finger::after{content:"";position:absolute;left:24px;top:12px;width:22px;height:56px;border-radius:11px;background:#0d1113;opacity:.35}
  .tempo{display:flex;gap:26px;margin-top:40px;align-items:center}
  .beat{width:104px;height:104px;border-radius:50%;border:5px solid #24322f;display:grid;place-items:center;font-size:54px;font-weight:800;color:#5e6f6b}
  .beat.on{background:#3fb8a8;border-color:#3fb8a8;color:#06211e}
  .badge{display:inline-flex;align-items:center;gap:18px;margin-top:44px;background:#16211f;border:2px solid #24322f;border-radius:999px;padding:20px 40px}
  .badge .t{font-size:34px;color:#8fa19d}
  .badge .v{font-size:60px;font-weight:800;font-variant-numeric:tabular-nums}
  /* sóng âm trong đầu */
  .waves{display:flex;align-items:center;gap:20px;margin:36px 0 8px}
  .waves .ch{font-size:66px;font-weight:800;color:#f2f5f4}
  .waves .wv{width:56px;height:130px;display:flex;align-items:center;justify-content:center}
  .waves .wave{display:block;width:18px;border-radius:10px;background:#3fb8a8;opacity:0}
  /* bài kiểm tra tốc độ đọc */
  .flash{height:300px;display:flex;align-items:center;justify-content:center;margin:20px 0 8px}
  .flash .w{font-size:118px;font-weight:800;letter-spacing:-.02em;color:#f2f5f4}
  .testbar{display:flex;align-items:center;gap:24px;margin-top:8px}
  .testbar .cnt,.testbar .rate{font-size:30px;color:#8fa19d;font-variant-numeric:tabular-nums;white-space:nowrap}
  .testbar .track{flex:1;height:18px;border-radius:9px;background:#1a2523;overflow:hidden}
  .testbar .pg{display:block;height:100%;width:0;background:#3fb8a8}
  /* trường nhìn */
  .cluster{display:flex;gap:24px;justify-content:center;margin-top:18px}
  .cluster.big{margin-top:10px}
  .cw{font-size:54px;font-weight:800;color:#5e6f6b}
  .cw.sharp{color:#f2f5f4}
  .cw.dim{color:#485754}
  .cw.wide{font-size:64px;color:#cfe9e4;opacity:0}
  .reticle{position:absolute;left:0;top:0;border:5px solid #3fb8a8;border-radius:18px;opacity:0;will-change:transform}
  .eyewrap{position:relative;height:720px;display:grid;place-items:center;margin-top:8px}
  .ring{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);border-radius:50%;border:5px dashed #3fb8a8;opacity:0}
  .ring.inner{border-style:solid;border-color:#e08374}
  .eyedot{width:34px;height:34px;border-radius:50%;background:#f2f5f4}
  .legend{display:flex;gap:44px;justify-content:center;font-size:30px;margin-top:16px}
  .legend .l1{color:#e08374}
  .legend .l2{color:#3fb8a8}
  /* quy luật 80/20 */
  .stack{display:flex;flex-direction:column;gap:12px;margin-top:14px}
  .pgbar{height:44px;border-radius:12px;background:#1a2523;display:flex;align-items:center;padding-left:18px}
  .pgbar.on{background:#3fb8a8}
  .pgbar .pi{font-size:26px;color:#f2f5f4;opacity:.45;font-weight:700}
  .list20{display:flex;flex-direction:column;gap:26px;margin-top:14px}
  .list20 .it{font-size:38px;color:#cfe9e4;opacity:0}
  .list20 .it b{display:inline-grid;place-items:center;width:54px;height:54px;border-radius:16px;background:#3fb8a8;color:#06211e;font-size:30px;margin-right:18px}
  .cta{margin-top:56px;background:#3fb8a8;color:#06211e;border-radius:26px;padding:38px 44px}
  .cta .a{font-size:32px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;opacity:.75}
  .cta .b{font-size:56px;font-weight:800;margin-top:10px;line-height:1.2}
  .cta .c{font-size:32px;margin-top:12px;opacity:.85}
  /* A1 — điểm dừng của mắt */
  .fixline{position:relative;display:flex;gap:10px;flex-wrap:nowrap;margin-top:14px}
  .fxw{font-size:44px;font-weight:800;color:#8fa19d;padding:10px 10px;border-radius:14px;white-space:nowrap}
  .fxw.lit{color:#f2f5f4;background:#22423d}
  .fxw.cl{background:#16211f;border:3px solid #2f8f84}
  .fixdot{position:absolute;left:0;top:-26px;width:26px;height:26px;border-radius:50%;background:#e08374;will-change:transform}
  .fixcount{display:flex;align-items:baseline;gap:24px;margin-top:52px}
  .fixcount .n{font-size:120px;font-weight:800;color:#e08374;font-variant-numeric:tabular-nums}
  .fixcount .u{font-size:40px;color:#8fa19d}
  .fixcount .n.ok{color:#3fb8a8}
  /* A6 — mạch hiểu đứt khi đọc ngắt quãng */
  .tl{display:flex;flex-direction:column;gap:14px;margin-top:10px}
  .tlrow{display:flex;align-items:center;gap:20px}
  .tlrow .nm{width:300px;font-size:34px;color:#cfe9e4;font-weight:700}
  .tlrow .bars{flex:1;display:flex;gap:8px;align-items:center}
  .seg{height:54px;border-radius:12px;background:linear-gradient(90deg,#2f8f84,#3fb8a8);width:0}
  .gap{width:0;height:6px;border-radius:3px;background:#3a4a47;align-self:center}
  .chain{position:relative;height:150px;margin-top:6px}
  .chain .link{position:absolute;height:6px;background:#3fb8a8;border-radius:3px;top:72px;width:0;transform-origin:left center}
  .chain .nd{position:absolute;top:62px;width:26px;height:26px;border-radius:50%;background:#cfe9e4;opacity:0}
  .hieubar{display:flex;align-items:center;gap:20px;margin-top:26px}
  .hieubar .lb{width:300px;font-size:32px;color:#8fa19d}
  .hieubar .tr{flex:1;height:44px;border-radius:12px;background:#1a2523;overflow:hidden}
  .hieubar .tr i{display:block;height:100%;width:0;background:#3fb8a8;border-radius:12px}
  .hieubar .tr i.bad{background:#e08374}
  .hieubar .pc{width:170px;text-align:right;font-size:36px;font-weight:800;font-variant-numeric:tabular-nums}
  .list3{display:flex;flex-direction:column;gap:30px;margin-top:14px}
  .list3 .it{font-size:40px;color:#cfe9e4;opacity:0}
  .list3 .it b{display:inline-grid;place-items:center;width:58px;height:58px;border-radius:16px;background:#3fb8a8;color:#06211e;font-size:32px;margin-right:20px}
  .note{font-size:30px;color:#8fa19d;margin-top:26px}
  .clwrap{display:flex;gap:10px;padding:8px 12px;border:3px solid #2f8f84;border-radius:18px;opacity:0}
  /* B4 — một trang sách nhìn từ xa */
  .page{background:#16211f;border:3px solid #24322f;border-radius:24px;padding:34px 38px;margin-top:16px}
  .pg{height:26px;border-radius:9px;background:#2a3835;margin-bottom:15px;opacity:0}
  .pg.t{height:38px;background:#3fb8a8}
  .pg.tshort{width:62%}
  .pgmark{display:flex;justify-content:space-between;font-size:30px;color:#8fa19d;margin-top:20px}
  /* thẻ kết thúc — dùng chung cho mọi tập */
  .nx{margin-top:26px;background:#16211f;border:2px solid #24322f;border-left:8px solid #3fb8a8;border-radius:18px;padding:24px 30px}
  .nx .nxl{font-size:26px;letter-spacing:.12em;text-transform:uppercase;color:#3fb8a8;font-weight:700}
  .nx .nxt{font-size:40px;font-weight:700;margin-top:8px;line-height:1.3}
  .ticket{display:flex;gap:26px;align-items:center;margin-top:30px;background:#16211f;border:2px solid #24322f;border-radius:22px;padding:24px}
  .ticket .qr{width:200px;height:200px;background:#f2f5f4;padding:8px;border-radius:12px;flex:0 0 auto}
  .ticket .tl{font-size:30px;color:#a9b4b2;line-height:1.45}
  .ticket .tu{font-size:28px;color:#3fb8a8;font-weight:700;margin-top:10px;word-break:break-all}
  .endinfo{font-size:32px;color:#8fa19d;margin-top:26px}
  .endinfo b{color:#cfe9e4}
  .dots{display:flex;gap:12px;margin-top:28px}
  .dots i{width:20px;height:20px;border-radius:50%;background:#2c3b38}
  .dots i.on{background:#3fb8a8}
  /* phụ đề cháy vào khung: nằm trên dải UI của nền tảng */
  #cap{position:absolute;left:96px;right:96px;bottom:380px;text-align:center;font-size:44px;
       font-weight:700;line-height:1.25;opacity:0}
  #cap span{background:rgba(6,17,15,.78);padding:8px 20px;border-radius:16px;
            -webkit-box-decoration-break:clone;box-decoration-break:clone}
  #thanh{position:absolute;left:0;bottom:340px;height:4px;background:#3fb8a8;opacity:.55;width:0}
  #brand{position:absolute;left:96px;top:132px;font-size:32px;color:#6f807c;font-weight:700;letter-spacing:.08em}
"""

# Phong cách thương hiệu thứ hai, theo trang speedreading.vn/sp-online: nền trắng, đỏ thương
# hiệu (đỏ Tailwind red-600/700/800), chữ Inter. Bật cho một tập bằng khoá
# "phong_cach": "do-trang". Viết thành lớp phủ chồng lên CSS gốc nên mọi tập cũ không đổi.
CSS_DO_TRANG = """
  html,body{background:#fff}
  body{font-family:"VH Inter","Noto Sans",sans-serif;color:#0f172a}
  #bg{background:
      radial-gradient(1100px 820px at 18% 10%, rgba(220,38,38,.10), transparent 62%),
      radial-gradient(900px 760px at 86% 90%, rgba(220,38,38,.07), transparent 64%),
      linear-gradient(168deg,#ffffff 0%,#fff7f7 52%,#ffffff 100%)}
  .grain{opacity:.07;background-image:radial-gradient(#dc2626 1px, transparent 1px)}
  .kicker{color:#dc2626}
  h1{color:#0f172a}
  h1 .hl{color:#dc2626}
  h1 .bad{color:#991b1b}
  .sub{color:#475569}
  .sub b{color:#0f172a}
  .race .name{color:#64748b}
  .race .name b{color:#0f172a}
  .track{background:#fecaca}
  .fill{background:linear-gradient(90deg,#ef4444,#dc2626)}
  .fill.red{background:linear-gradient(90deg,#b91c1c,#7f1d1d)}
  .cap{background:#b91c1c}
  .caplbl{color:#b91c1c}
  .col .bar{background:linear-gradient(180deg,#ef4444,#dc2626)}
  .col .bar.red{background:linear-gradient(180deg,#b91c1c,#7f1d1d)}
  .col .lab{color:#64748b}
  .blk{background:#dc2626}
  .gridline{color:#64748b}
  .crd{background:#fff;border-color:#fecaca}
  .crd .idx{background:#dc2626;color:#fff}
  .crd .txt b{color:#0f172a}
  .crd .txt span{color:#64748b}
  .vs{background:#fff;border-color:#fecaca}
  .vs .nm{color:#0f172a}
  .vs .meter{background:#fee2e2}
  .vs .meter i{background:#dc2626}
  .vs .note{color:#64748b}
  .ageline .age{color:#0f172a}
  .ageline .ab{background:#fee2e2}
  .ageline .ab i{background:#dc2626}
  .ageline .mins{color:#0f172a}
  .lines{color:#0f172a}
  .lines .wd{color:#94a3b8}
  .lines .wd.lit{color:#0f172a;background:#fee2e2}
  .finger{background:rgba(220,38,38,.92)}
  .finger::after{background:#fff}
  .beat{border-color:#fecaca;color:#94a3b8}
  .beat.on{background:#dc2626;border-color:#dc2626;color:#fff}
  .badge{background:#fff;border-color:#fecaca}
  .badge .t{color:#64748b}
  .badge .v{color:#0f172a}
  .waves .ch{color:#0f172a}
  .waves .wave{background:#dc2626}
  .flash .w{color:#0f172a}
  .testbar .cnt,.testbar .rate{color:#64748b}
  .testbar .track{background:#fee2e2}
  .testbar .pg{background:#dc2626}
  .cluster .cw{color:#94a3b8}
  .cluster .cw.sharp{color:#0f172a}
  .cluster .cw.dim{color:#cbd5e1}
  .cluster .cw.wide{color:#334155}
  .reticle{border-color:#dc2626}
  .ring{border-color:#dc2626}
  .ring.inner{border-color:#991b1b}
  .eyedot{background:#0f172a}
  .legend .l1{color:#991b1b}
  .legend .l2{color:#dc2626}
  .stack .pgbar{background:#fee2e2}
  .stack .pgbar.on{background:#dc2626}
  .stack .pgbar .pi{color:#fff}
  .list20 .it{color:#0f172a}
  .list20 .it b{background:#dc2626;color:#fff}
  .cta{background:#dc2626;color:#fff}
  .cta .a,.cta .c{color:#fff}
  .fixline .fxw{color:#94a3b8}
  .fixline .fxw.lit{color:#0f172a;background:#fee2e2}
  .fixline .fxw.cl{background:#fff;border-color:#dc2626}
  .fixdot{background:#dc2626}
  .fixcount .n{color:#b91c1c}
  .fixcount .n.ok{color:#dc2626}
  .fixcount .u{color:#64748b}
  .tl .seg{background:linear-gradient(90deg,#ef4444,#dc2626)}
  .tl .gap{background:#fecaca}
  .chain .link{background:#dc2626}
  .chain .nd{background:#0f172a}
  .hieubar .lb{color:#64748b}
  .hieubar .tr{background:#fee2e2}
  .hieubar .tr i{background:#dc2626}
  .hieubar .tr i.bad{background:#991b1b}
  .hieubar .pc{color:#0f172a}
  .list3 .it{color:#0f172a}
  .list3 .it b{background:#dc2626;color:#fff}
  .note{color:#64748b}
  .clwrap{border-color:#dc2626}
  .page{background:#fff;border-color:#fecaca}
  .page .pg{background:#fee2e2}
  .page .pg.t{background:#dc2626}
  .pgmark{color:#64748b}
  .nx{background:#fff1f2;border-color:#fecaca;border-left-color:#dc2626}
  .nx .nxl{color:#dc2626}
  .nx .nxt{color:#0f172a}
  .ticket{background:#fff;border-color:#fecaca}
  .ticket .qr{background:#fff}
  .ticket .tl{color:#475569}
  .ticket .tu{color:#b91c1c}
  .endinfo{color:#64748b}
  .endinfo b{color:#0f172a}
  .dots i{background:#fecaca}
  .dots i.on{background:#dc2626}
  #cap span{background:rgba(153,27,27,.92);color:#fff}
  #thanh{background:#dc2626}
  #brand{color:#b91c1c}
  .cta{border-radius:26px}
  .ticket .qr{padding:8px;border-radius:12px}
"""

JS_FRAME = """
const SCENES = __SCENES__;
const ANIM = __ANIM__;
const TOTAL = __TOTAL__;
const CUES = __CUES__;
const ease = x => x<0?0:x>1?1:(x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2);
const span = (t,a,b) => (t-a)/(b-a);
const lock = (x,a,b) => Math.max(a, Math.min(b, x));
const $ = id => document.getElementById(id);
function seek(t){
  window.__da_seek = true;
  $('bg').style.transform = 'scale(1.06) translate(' + (Math.sin(t*.16)*10) + 'px,' + (Math.cos(t*.13)*10) + 'px)';
  SCENES.forEach(function(s,i){
    const el = document.querySelector('[data-scene="'+i+'"]');
    // Cảnh vào sớm 0,6 giây — đúng lúc cảnh trước đang mờ đi — để hai cảnh giao nhau
    // thành một lần chuyển mượt. Nếu để cảnh vào đúng mốc bắt đầu của nó thì tại mốc đó
    // cả hai cảnh đều mờ hết, và trên nền trắng (bộ màu đỏ–trắng) khung hình nháy trắng
    // một nhịp — trên nền tối thì không thấy.
    const inA = i ? ease(span(t, s.start-0.6, s.start)) : ease(span(t, s.start, s.start+0.6));
    const out = 1-ease(span(t, s.end-0.6, s.end));
    el.style.opacity = inA*out;
    el.style.transform = 'translateY(' + ((1-inA)*30) + 'px)';
    if (ANIM[i]) ANIM[i](t, el);
  });
  $('brand').style.opacity = t>1 ? (t>TOTAL-1.2?.9:.5) : 0;
  $('thanh').style.width = (100*Math.max(0, Math.min(1, t/TOTAL))) + '%';
  let cue = null;
  for (let k = 0; k < CUES.length; k++) {
    if (t >= CUES[k][0] && t < CUES[k][1]) { cue = CUES[k]; break; }
  }
  const cap = $('cap');
  // mờ dần tính bằng t, không dùng CSS transition: khung hình phải là hàm của t,
  // không được phụ thuộc máy chụp nhanh hay chậm
  if (cue) {
    cap.innerHTML = '<span>' + cue[2] + '</span>';
    cap.style.opacity = Math.max(0, Math.min(1, (t - cue[0]) / 0.08, (cue[1] - t) / 0.08)).toFixed(3);
  } else { cap.style.opacity = 0; }
}
window.__seek = seek;
// Chỉ tự về t=0 khi chưa ai gọi __seek. Nếu không, promise của fonts.ready có thể
// chạy sau lệnh seek của máy chụp và kéo khung về 0 — khung hình sai mà không báo lỗi.
document.fonts.ready.then(function(){ if (!window.__da_seek) seek(0); window.__total = TOTAL; });
"""

# ---------------------------------------------------------------- cấu hình chung
MAC_DINH = {
  "thuong_hieu": "SPEED READING VIỆT NAM",
  "dang_ky": "https://speedreading.vn/dang-ky",
  "dang_ky_nhan": "Quét mã để nhận lịch lớp gần nhất",
}


def doc_cau_hinh():
    try:
        with open(f"{BASE}/noi-dung.json", encoding="utf-8") as f:
            return {**MAC_DINH, **json.load(f)}
    except Exception:
        return dict(MAC_DINH)


CAU_HINH = doc_cau_hinh()

# Đánh dấu cảnh kết thúc: khi dựng trang sẽ được thay bằng thẻ kết thúc dùng chung.


def endcard(i, ep):
    """Thẻ kết thúc thống nhất: số tập, teaser tập sau, mã QR đăng ký."""
    so, tong = i + 1, len(EPISODES)
    sau = EPISODES[i + 1] if i + 1 < len(EPISODES) else None
    if sau:
        nx = ('<div class="nx"><div class="nxl">Tập sau</div>'
              f'<div class="nxt">{sau.get("ten", sau["slug"])}</div></div>')
    else:
        nx = ('<div class="nx"><div class="nxl">Hết chuỗi</div>'
              '<div class="nxt">Xem lại từ đầu để nhớ đủ các bước</div></div>')
    cham = "".join('<i class="%s"></i>' % ("on" if k <= i else "")
                   for k in range(tong))
    link_ep = ep.get("dang_ky") or CAU_HINH["dang_ky"]
    ten_ngan = link_ep.replace("https://", "").replace("http://", "").rstrip("/")
    # Phong cách đỏ–trắng: cuối video trỏ về trang lớp Zoom online (speedreading.vn/sp-online)
    if ep.get("phong_cach") == "do-trang":
        link = ep.get("dang_ky") or CAU_HINH.get("dang_ky_online", CAU_HINH["dang_ky"])
        nhan = ep.get("dang_ky_nhan") or CAU_HINH.get("dang_ky_nhan_online", CAU_HINH["dang_ky_nhan"])
        qr = "assets/qr-sp-online.svg"
        ten_ngan = link.replace("https://", "").replace("http://", "").rstrip("/")
        cuoi = "Lớp <b>7 buổi Zoom</b> · <b>980.000đ</b> · hoàn phí nếu không hài lòng sau buổi 1"
    else:
        nhan, qr = ep.get("dang_ky_nhan") or CAU_HINH["dang_ky_nhan"], "assets/qr.svg"
        cuoi = "Lớp <b>7 buổi</b> · <b>980.000đ</b> · buổi 1 không hợp thì hoàn tiền"
    return f"""
    <div class="kicker">Tập {so}/{tong}</div>
    <h1 style="font-size:62px">Đọc hiệu quả<br><span class="hl">Speed Reading</span></h1>
    {nx}
    <div class="ticket">
      <img class="qr" src="{qr}" alt="Mã QR đăng ký lớp">
      <div><div class="tl">{nhan}</div>
        <div class="tu">{ten_ngan}</div></div>
    </div>
    <div class="dots">{cham}</div>
    <div class="endinfo">{cuoi}</div>"""


def _dur(f):
    try:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", f], capture_output=True, text=True)
        return float(r.stdout.strip())
    except Exception:
        return 0.0


def captions(ep):
    """Dòng phụ đề theo mốc từng từ của edge-tts (nếu đã sinh giọng kèm mốc).

    Mốc đo trong từng tệp mp3, nên phải cộng mốc cảnh và chia theo tốc độ tua mà
    ghep-tieng-tap.py dùng khi lời đọc dài hơn chỗ trống của cảnh.
    """
    ra, t = [], 0.0
    for i, (a, b) in enumerate(ep["scenes"]):
        w = b - a
        mp3 = f"{GIONG}/{ep['slug']}-sc{i+1}.mp3"
        moc = mp3.replace(".mp3", ".words.json")
        if not (os.path.exists(mp3) and os.path.exists(moc)):
            t += w
            continue
        try:
            words = json.load(open(moc, encoding="utf-8"))["words"]
        except Exception:
            t += w
            continue
        d = _dur(mp3)
        room = w - OFFSET - GAP
        tempo = 1.0 if (d <= 0 or d <= room) else round(d / room, 3)
        # edge-tts trả từ không kèm dấu câu, nên phải đối chiếu với lời đọc gốc để biết
        # chỗ nào hết câu: câu "chữ. Chữ nào…" không được gộp thành một dòng.
        goc = re.findall(r"\S+", dict(ep["narration"]).get(i, ""))
        nhu_cau = [x.rstrip().endswith((".", "!", "?", ":")) for x in goc]
        nhom, cur = [], []
        for k, (st, en, tu) in enumerate(words):
            cur.append((st, en, tu))
            het_cau = k < len(nhu_cau) and nhu_cau[k]
            if len(cur) >= SO_TU_CUE or het_cau:
                nhom.append(cur)
                cur = []
        if cur:
            nhom.append(cur)
        for g in nhom:
            s = t + OFFSET + g[0][0] / tempo
            e = min(t + OFFSET + g[-1][1] / tempo + 0.12, b - 0.15)
            if e - s >= 0.25:
                ra.append([round(s, 2), round(e, 2), " ".join(x[2] for x in g)])
        t += w
    # cue sau bắt đầu thì cue trước phải hết: tránh hai dòng cùng hiện chồng nhau
    for k in range(len(ra) - 1):
        ra[k][1] = round(min(ra[k][1], ra[k + 1][0]), 2)
    return ra


def cover_at(ep):
    """Mốc chụp ảnh bìa: cảnh mở đầu, sau khi tiêu đề đã hiện xong."""
    if "cover_at" in ep:
        return ep["cover_at"]
    a, b = ep["scenes"][0]
    return round(a + (b - a) * 0.80, 2)


# Thẻ kết thúc dùng chung: tập nào kết thúc bằng cảnh riêng thì nối thêm 3 giây
# thẻ kết thúc, và mọi thứ (phụ đề, cửa sổ lời đọc, kiểm tra thời lượng) theo đó.
THEM_CUOI = 3.0
for _ep in EPISODES:
    if _ep["html"][-1].strip() != CTA:
        _a = _ep["scenes"][-1][1]
        _ep["total"] = round(_a + THEM_CUOI, 2)
        _ep["scenes"] = list(_ep["scenes"]) + [(_a, _ep["total"])]
        _ep["html"] = list(_ep["html"]) + [CTA]
        _ep["anim"] = list(_ep["anim"]) + [""]


def _so_tap(ep):
    return next(i for i, e in enumerate(EPISODES) if e["slug"] == ep["slug"])


def hop_khung(size=KHUNG_GOC):
    """Số đo khung đích: hệ số thu phóng, kích thước sân khấu và bề ngang cột nội dung."""
    rong, cao = size
    k = min(cao / KHUNG_GOC[1], rong / KHUNG_GOC[0])
    return {"rong": rong, "cao": cao, "k": k,
            "rong_goc": rong / k, "cao_goc": cao / k,
            "cot": min(rong / k, COT_RONG_NHAT)}


def css_khung(size):
    """CSS thêm cho khung khác 9:16.

    Sân khấu được vẽ ở toạ độ thiết kế rồi thu phóng vừa khung, nên mọi cảnh giữ
    nguyên tỉ lệ đã soát. Cột nội dung rộng ra (tối đa COT_RONG_NHAT) để khung
    vuông/ngang không bị một dải hẹp ở giữa, còn nền #bg phủ kín cả khung.
    """
    if tuple(size) == KHUNG_GOC:
        return ""
    h = hop_khung(size)
    k, rg, cot = h["k"], h["rong_goc"], h["cot"]
    return f"""
  /* khung {h['rong']}×{h['cao']}: thu phóng {k:.4f} từ khung thiết kế 1080×1920 */
  html,body{{width:{h['rong']}px;height:{h['cao']}px}}
  #stage{{width:{rg:.2f}px;height:{h['cao_goc']:.2f}px;transform:scale({k:.6f});transform-origin:0 0}}
  .scene{{left:50%;right:auto;bottom:auto;width:{cot:.2f}px;height:{h['cao_goc']:.2f}px;
         margin-left:{-cot / 2:.2f}px}}
  #cap{{left:50%;right:auto;width:{cot - 192:.2f}px;margin-left:{-(cot - 192) / 2:.2f}px}}
  #brand{{left:calc(50% - {cot / 2 - 96:.2f}px)}}
"""


def build_html(ep, size=KHUNG_GOC):
    sc = [{"start": a, "end": b} for a, b in ep["scenes"]]
    anims = [("null" if not a.strip() else "(" + a.strip() + ")") for a in ep["anim"]]
    js = (JS_FRAME
          .replace("__SCENES__", json.dumps(sc))
          .replace("__ANIM__", "[" + ",".join(anims) + "]")
          .replace("__TOTAL__", str(ep["total"]))
          .replace("__CUES__", json.dumps(captions(ep), ensure_ascii=False)))
    htmls = [endcard(_so_tap(ep), ep) if h == CTA else h for h in ep["html"]]
    scenes_html = "\n".join(
        f'<div class="scene" data-scene="{i}">{h}</div>' for i, h in enumerate(htmls))
    # đoạn chữ cho bài kiểm tra tốc độ: A 200 từ/phút, B 300, C 450
    for ph, seg in (("__A__", PASSAGE[0:34]), ("__B__", PASSAGE[34:99]), ("__C__", PASSAGE[99:140])):
        scenes_html = scenes_html.replace(ph, "|".join(seg))
    extra_css = ep.get("css_extra", "")
    brand_text = ep.get("brand", "SPEED READING VIỆT NAM")
    do_trang = ep.get("phong_cach") == "do-trang"
    font_link = ('<link rel="stylesheet" href="fonts/noto-sans.css">\n'
                 '<link rel="stylesheet" href="fonts/inter.css">' if do_trang
                 else '<link rel="stylesheet" href="fonts/noto-sans.css">')
    theme_css = (CSS_DO_TRANG if do_trang else "") + ep.get("css_extra", "")
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<title>{ep['slug']}</title>
{font_link}
<style>{CSS}
{theme_css}
{extra_css}{css_khung(size)}</style>
</head>
<body>
<div id="stage">
  <div id="bg"></div>
  <div class="grain"></div>
  {scenes_html}
  <div id="thanh"></div>
  <div id="cap"></div>
  <div id="brand">{brand_text}</div>
</div>
<script>
{js}
</script>
</body>
</html>
"""


def doc_size(argv):
    """Đọc --size WxH. Sai định dạng thì dừng ngay, không đoán."""
    for i, a in enumerate(argv):
        gt = a.split("=", 1)[1] if a.startswith("--size=") else (
            argv[i + 1] if a == "--size" and i + 1 < len(argv) else None)
        if gt is None:
            continue
        try:
            rong, cao = (int(x) for x in gt.lower().split("x"))
        except Exception:
            raise SystemExit(f"--size phải có dạng WxH, ví dụ 1080x1080 (nhận: {gt})")
        if min(rong, cao) < 320 or max(rong, cao) > 4096:
            raise SystemExit(f"--size ngoài khoảng hợp lý 320–4096: {gt}")
        if rong % 2 or cao % 2:
            raise SystemExit(f"--size phải chẵn (H.264 yêu cầu): {gt}")
        return (rong, cao)
    return KHUNG_GOC


def doc_tap(argv):
    """Đọc --tap slug... để chỉ dựng một vài tập."""
    for i, a in enumerate(argv):
        if a == "--tap":
            return [x for x in argv[i + 1:] if not x.startswith("--")]
    return []


def main():
    if "--loi-doc" in sys.argv:
        tasks = []
        for ep in EPISODES:
            for idx, text in ep["narration"]:
                tasks.append({"file": f"{BASE}/.thu-nghiem/giong/{ep['slug']}-sc{idx+1}.mp3",
                              "text": text, "tap": ep["slug"], "canh": idx + 1})
        print(json.dumps(tasks, ensure_ascii=False, indent=1))
        return
    os.makedirs(OUT, exist_ok=True)
    size = doc_size(sys.argv)
    chon = doc_tap(sys.argv)
    hau = "" if size == KHUNG_GOC else "_%dx%d" % size
    co_phu_de = []
    for ep in EPISODES:
        if chon and ep["slug"] not in chon:
            continue
        p = f"{OUT}/{ep['slug']}{hau}.html"
        open(p, "w", encoding="utf-8").write(build_html(ep, size))
        print(f"đã ghi {p}  ({len(ep['html'])} cảnh, tổng {ep['total']}s)")
        if captions(ep):
            co_phu_de.append(ep["slug"])
    # Bản commit lại phải là bản KHÔNG có mốc từ: máy chủ dựng lại trang lúc chụp, còn CI
    # kiểm "do-hoa/*.html khớp generator" trong một máy không có tệp lời đọc, nên trang
    # nhúng mốc từ sẽ bị coi là lệch. Nhắc ngay để không mất một vòng CI.
    if co_phu_de:
        print(f"  LƯU Ý: {len(co_phu_de)} trang có phụ đề theo mốc từ "
              f"({', '.join(co_phu_de[:4])}{'…' if len(co_phu_de) > 4 else ''}) — "
              f"trang đem commit phải dựng khi CHƯA có tệp lời đọc, nếu không CI báo lệch generator.")


if __name__ == "__main__":
    main()
