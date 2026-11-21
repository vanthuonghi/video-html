#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dựng 5 tập video đồ hoạ giải thích từ một khuôn chung.
Mỗi tập: các cảnh có mốc thời gian, phần HTML của cảnh, hàm vẽ theo thời gian, và lời đọc.
Chạy: python3 dung-tap-do-hoa.py            -> ghi file html vào do-hoa/
      python3 dung-tap-do-hoa.py --loi-doc  -> in danh sách lời đọc cần sinh
"""
import json, os, sys

BASE = os.environ.get("VH_BASE") or os.path.dirname(os.path.abspath(__file__))
OUT = f"{BASE}/do-hoa"

CSS = """
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{width:1080px;height:1920px;overflow:hidden;background:#0d1113}
  body{font-family:"Noto Sans","DejaVu Sans",system-ui,sans-serif;color:#f2f5f4;-webkit-font-smoothing:antialiased}
  #stage{position:absolute;inset:0;overflow:hidden}
  #bg{position:absolute;inset:-10%;background:
      radial-gradient(1200px 900px at 20% 12%, rgba(63,184,168,.16), transparent 60%),
      radial-gradient(900px 800px at 85% 88%, rgba(63,184,168,.10), transparent 62%),
      linear-gradient(160deg,#0d1113 0%,#121a19 55%,#0d1113 100%);will-change:transform}
  .grain{position:absolute;inset:0;opacity:.05;background-image:radial-gradient(#fff 1px, transparent 1px);background-size:6px 6px}
  .scene{position:absolute;inset:0;padding:150px 90px;display:flex;flex-direction:column;justify-content:center;opacity:0;will-change:transform,opacity}
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
  .cw{font-size:58px;font-weight:800;color:#5e6f6b}
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
  .fixline{position:relative;display:flex;gap:14px;flex-wrap:nowrap;margin-top:14px}
  .fxw{font-size:52px;font-weight:800;color:#8fa19d;padding:10px 12px;border-radius:14px;white-space:nowrap}
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
  #brand{position:absolute;left:90px;bottom:110px;font-size:32px;color:#6f807c;font-weight:700;letter-spacing:.08em}
"""

JS_FRAME = """
const SCENES = __SCENES__;
const ANIM = __ANIM__;
const TOTAL = __TOTAL__;
const ease = x => x<0?0:x>1?1:(x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2);
const span = (t,a,b) => (t-a)/(b-a);
const lock = (x,a,b) => Math.max(a, Math.min(b, x));
const $ = id => document.getElementById(id);
function seek(t){
  $('bg').style.transform = 'scale(1.06) translate(' + (Math.sin(t*.16)*10) + 'px,' + (Math.cos(t*.13)*10) + 'px)';
  SCENES.forEach(function(s,i){
    const el = document.querySelector('[data-scene="'+i+'"]');
    const inA = ease(span(t, s.start, s.start+0.6));
    const out = 1-ease(span(t, s.end-0.6, s.end));
    el.style.opacity = inA*out;
    el.style.transform = 'translateY(' + ((1-inA)*30) + 'px)';
    if (ANIM[i]) ANIM[i](t, el);
  });
  $('brand').style.opacity = t>1 ? (t>TOTAL-1.2?.9:.5) : 0;
}
window.__seek = seek; window.__total = TOTAL; seek(0);
"""

CTA = """
    <div class="kicker">Khoá học</div>
    <h1 style="font-size:82px">Đọc hiệu quả<br><span class="hl">Speed Reading</span></h1>
    <div class="sub">7 buổi · đọc cụm · chống đọc thầm · ghi nhớ khoa học</div>
    <div class="cta"><div class="a">Bắt đầu</div><div class="b">Đăng ký lớp gần nhất</div><div class="c">Học phí 980.000đ · có buổi 1 hoàn tiền</div></div>
"""

def scene(html):
    return html.strip()

# ---------------------------------------------------------------- TẬP 1
EP1 = {
 "slug": "02_noi-tham-trong-dau", "total": 42.0,
 "scenes": [(0,5.0),(5.0,16.0),(16.0,26.0),(26.0,35.0),(35.0,42.0)],
 "html": [
   scene("""
    <div class="kicker">Cơ chế đọc nhanh</div>
    <h1>Mắt bạn chạy<br>nhanh hơn<br><span class="hl">miệng bạn nói</span></h1>
    <div class="sub">Và đó là lý do bạn bị kẹt ở hai trăm từ một phút.</div>"""),
   scene("""
    <div class="kicker">Hai tốc độ trong cùng một việc đọc</div>
    <div class="race">
      <div class="row"><div class="name"><b>Mắt đọc</b><span class="val" id="e1v">0 từ/phút</span></div>
        <div class="track"><i class="fill" id="e1f"></i><i class="cap" id="e1c"></i></div>
        <div class="caplbl" id="e1cl">Giọng đọc trong đầu cản lại ở đây</div></div>
      <div class="row"><div class="name"><b>Giọng đọc trong đầu</b><span class="val" id="e1v2">0 từ/phút</span></div>
        <div class="track"><i class="fill red" id="e1f2"></i></div></div>
    </div>
    <div class="badge"><span class="t">Mắt nhanh hơn giọng đọc</span><span class="v">2×</span></div>"""),
   scene("""
    <div class="kicker">Vì sao lại như vậy</div>
    <h1 style="font-size:78px">Não đọc bằng cách<br><span class="hl">nghe lại từng chữ</span></h1>
    <div class="waves">
      <div class="ch">Đ</div><div class="ch">ọ</div><div class="ch">c</div>
      <div class="wv"><i class="wave"></i></div><div class="wv"><i class="wave"></i></div>
      <div class="wv"><i class="wave"></i></div><div class="wv"><i class="wave"></i></div>
      <div class="wv"><i class="wave"></i></div>
    </div>
    <div class="sub">Chữ nào chưa được phát âm trong đầu thì não chưa nhận là đã đọc.<br><b>Nên miệng quyết định tốc độ, không phải mắt.</b></div>"""),
   scene("""
    <div class="kicker">Cách gỡ</div>
    <h1 style="font-size:78px">Đọc bằng mắt,<br><span class="hl">không đọc bằng lời</span></h1>
    <div class="race">
      <div class="row"><div class="name"><b>Mắt đọc sau khi bỏ phát âm</b><span class="val" id="e3v">0</span></div>
        <div class="track"><i class="fill" id="e3f"></i></div></div>
    </div>
    <div class="sub">Bỏ giọng đọc trong đầu là bước đầu tiên, và là bước khó nhất.</div>"""),
   scene(CTA),
 ],
 "anim": [
   "",
   """function(t, el){
     const eRaw  = ease(span(t,6.0,7.6));     // mắt tự nó lên tới 500
     const q     = ease(span(t,7.3,9.4));     // giọng đọc trong đầu lên tới 250
     const clamp = ease(span(t,10.0,11.8));   // giọng đọc kéo mắt về trần
     const eye = eRaw - (eRaw - 0.5)*clamp;
     $('e1f').style.width = (eye*100)+'%';
     $('e1f2').style.width = (q*50)+'%';
     $('e1v').textContent = Math.round(eye*500)+' từ/phút';
     $('e1v2').textContent = Math.round(q*250)+' từ/phút';
     $('e1c').style.opacity = clamp;
     $('e1c').style.left = 'calc(50% - 2px)';
     $('e1cl').style.opacity = clamp;
   }""",
   """function(t, el){
     const w = el.querySelectorAll('.wave');
     const hs = [40, 76, 110, 76, 40];
     const p = ease(span(t,17.6,19.4));
     w.forEach(function(x,i){
       const on = lock(p*4 - i*0.6, 0, 1);
       x.style.opacity = on;
       x.style.height = (on*hs[i]) + 'px';
     });
   }""",
   """function(t, el){
     const p = ease(span(t,27.5,30.5));
     $('e3f').style.width = (p*100)+'%';
     $('e3v').textContent = Math.round(p*500)+' từ/phút';
   }""",
   "",
 ],
 "narration": [
   (0, "Mắt bạn chạy nhanh hơn miệng bạn rất nhiều."),
   (1, "Đây là hai tốc độ. Mắt có thể nhận hai trăm từ một phút, nhưng giọng đọc trong đầu thì chậm hơn."),
   (2, "Vì não đọc bằng cách nghe lại từng chữ. Chữ nào chưa được phát âm thì não chưa nhận."),
   (3, "Muốn nhanh hơn, phải đọc bằng mắt. Bỏ giọng đọc trong đầu, tốc độ tăng gấp đôi."),
   (4, "Đó là nguyên lý thứ hai trong khoá đọc hiệu quả Speed Reading."),
 ],
}

# ---------------------------------------------------------------- TẬP 2
EP2 = {
 "slug": "03_bieu-do-tri-quen", "total": 42.0,
 "scenes": [(0,5.0),(5.0,15.0),(15.0,25.0),(25.0,34.5),(34.5,42.0)],
 "html": [
   scene("""
    <div class="kicker">Trí nhớ</div>
    <h1>Học xong một ngày,<br>bạn đã mất<br><span class="bad">một nửa</span></h1>
    <div class="sub">Đây là biểu đồ trí quên, được vẽ từ năm 1885 và vẫn đúng tới hôm nay.</div>"""),
   scene("""
    <div class="kicker">Còn nhớ được bao nhiêu</div>
    <div class="chart" id="c2">
      <div class="col"><div class="num" id="n20">100%</div><div class="bar" id="b20"></div><div class="lab">vừa học</div></div>
      <div class="col"><div class="num" id="n21">—</div><div class="bar red" id="b21"></div><div class="lab">1 ngày</div></div>
      <div class="col"><div class="num" id="n22">—</div><div class="bar red" id="b22"></div><div class="lab">2 ngày</div></div>
    </div>
    <div class="sub" id="s2t" style="opacity:0">Sau một ngày bạn chỉ còn nhớ khoảng <b>một nửa</b>.</div>"""),
   scene("""
    <div class="kicker">Và tiếp tục rơi</div>
    <div class="chart" id="c3">
      <div class="col"><div class="num">37%</div><div class="bar red" style="height:37%"></div><div class="lab">2 ngày</div></div>
      <div class="col"><div class="num" id="n31">—</div><div class="bar red" id="b31"></div><div class="lab">4 ngày</div></div>
      <div class="col"><div class="num" id="n32">—</div><div class="bar red" id="b32"></div><div class="lab">7 ngày</div></div>
    </div>
    <div class="sub" id="s3t" style="opacity:0">Tới ngày thứ bảy, còn lại <b>dưới 10%</b>. Đây là lý do học dồn trước kỳ thi gần như không còn gì.</div>"""),
   scene("""
    <div class="kicker">Cách chặn</div>
    <h1 style="font-size:78px">Xem lại <span class="hl">5 phút</span><br>vào ngày thứ 1, 3 và 6</h1>
    <div class="chart" style="height:420px">
      <div class="col"><div class="num">95%</div><div class="bar" style="height:95%"></div><div class="lab">ngày 1</div></div>
      <div class="col"><div class="num">93%</div><div class="bar" style="height:93%"></div><div class="lab">ngày 3</div></div>
      <div class="col"><div class="num">90%</div><div class="bar" style="height:90%"></div><div class="lab">ngày 6</div></div>
    </div>
    <div class="sub">Mỗi lần chỉ cần năm phút, không phải đọc lại từ đầu.</div>"""),
   scene(CTA),
 ],
 "anim": [
   "",
   """function(t, el){
     const p = ease(span(t,6.0,7.4));
     $('b20').style.height = '100%';
     const q = ease(span(t,7.8,9.8));
     $('b21').style.height = (q*50)+'%';
     $('n21').textContent = q>0.05 ? Math.round(q*50)+'%' : '—';
     const r = ease(span(t,10.4,12.4));
     $('b22').style.height = (r*37)+'%';
     $('n22').textContent = r>0.05 ? Math.round(r*37)+'%' : '—';
     $('s2t').style.opacity = ease(span(t,12.8,13.6));
   }""",
   """function(t, el){
     const q = ease(span(t,16.5,18.5));
     $('b31').style.height = (q*18)+'%';
     $('n31').textContent = q>0.05 ? Math.round(q*18)+'%' : '—';
     const r = ease(span(t,19.2,21.4));
     $('b32').style.height = (r*9)+'%';
     $('n32').textContent = r>0.05 ? Math.round(r*9)+'%' : '—';
     $('s3t').style.opacity = ease(span(t,21.8,22.6));
   }""",
   """function(t, el){
     const bars = el.querySelectorAll('.bar');
     bars.forEach(function(b,i){ b.style.height = (ease(span(t,26.6+i*0.5,28.4+i*0.5))*[95,93,90][i])+'%'; });
   }""",
   "",
 ],
 "narration": [
   (0, "Học xong một ngày, bạn đã mất một nửa."),
   (1, "Biểu đồ trí quên được vẽ từ năm một tám tám năm. Sau một ngày, bạn chỉ còn nhớ khoảng năm mươi phần trăm."),
   (2, "Ngày thứ hai còn ba mươi bảy phần trăm. Ngày thứ tư còn mười tám. Tới ngày thứ bảy thì dưới mười phần trăm."),
   (3, "Cách chặn rất đơn giản: xem lại năm phút vào ngày hôm sau, rồi ngày thứ ba, ngày thứ sáu. Trí nhớ giữ gần như nguyên vẹn."),
   (4, "Học một lần rồi quên dần, hay học ba lần để nhớ mãi. Chọn cách thứ hai."),
 ],
}

# ---------------------------------------------------------------- TẬP 3
EP3 = {
 "slug": "04_nao-giu-5-10-phut", "total": 42.0,
 "scenes": [(0,5.0),(5.0,15.0),(15.0,25.5),(25.5,34.5),(34.5,42.0)],
 "html": [
   scene("""
    <div class="kicker">Trí nhớ tạm thời</div>
    <h1>Đọc liền hai tiếng,<br>bạn nhớ được<br><span class="bad">bao nhiêu?</span></h1>
    <div class="sub">Câu trả lời làm nhiều người bỏ thói quen đọc một mạch.</div>"""),
   scene("""
    <div class="kicker">Trí nhớ tạm thời như một bảng trắng</div>
    <div class="grid" id="g1"><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span></div>
    <div class="gridline"><span>phút thứ 10</span><span id="g1n">đang ghi…</span><span>phút thứ 60</span></div>"""),
   scene("""
    <div class="kicker">Và nó bắt đầu tràn</div>
    <div class="grid" id="g2"><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span></div>
    <div class="badge"><span class="t">Trí nhớ tạm thời giữ được</span><span class="v">5–10 phút</span></div>
    <div class="sub">Phần ghi trước đó bị đẩy ra để lấy chỗ cho phần mới.</div>"""),
   scene("""
    <div class="kicker">Cách làm đúng</div>
    <h1 style="font-size:76px">Đọc theo khối<br><span class="hl">10 phút</span>, rồi ghi 1 dòng</h1>
    <div class="grid" style="grid-template-columns:repeat(6,1fr)">
      <span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span><span class="blk"></span>
    </div>
    <div class="sub">Hết mỗi khối, viết lại một dòng. Cuối buổi bạn còn nguyên bản đồ nội dung, thay vì chỉ nhớ đoạn cuối.</div>"""),
   scene(CTA),
 ],
 "anim": [
   "",
   """function(t, el){
     const blocks = el.querySelectorAll('.blk');
     const n = ease(span(t,6.2,13.6))*blocks.length;
     blocks.forEach(function(b,i){
       const on = i < n;
       b.style.opacity = on ? 1 : 0;
       b.style.background = on ? '#3fb8a8' : 'transparent';
       if (on) { const age = n - i; b.style.opacity = age < 3 ? 0.35 : 1; }
     });
     $('g1n').textContent = 'đang ghi ' + Math.max(0, Math.round(n*2.5)) + ' phút';
   }""",
   """function(t, el){
     const blocks = el.querySelectorAll('.blk');
     blocks.forEach(function(b,i){ b.style.opacity = 1; b.style.background = '#3fb8a8'; });
     const drop = ease(span(t,16.4,20.4));       // các ô cũ mờ dần
     blocks.forEach(function(b,i){
       const keep = i >= blocks.length*0.72;      // chỉ giữ lại phần mới nhất
       b.style.opacity = keep ? 1 : (1 - drop*0.9);
       b.style.background = keep ? '#3fb8a8' : '#7d463c';
     });
   }""",
   """function(t, el){
     const blocks = el.querySelectorAll('.blk');
     const step = Math.floor(lock(span(t,26.6,32.0),0,5.99));
     blocks.forEach(function(b,i){ b.style.opacity = i<=step ? 1 : 0.12; });
   }""",
   "",
 ],
 "narration": [
   (0, "Đọc liền hai tiếng, bạn nhớ được bao nhiêu?"),
   (1, "Trí nhớ tạm thời của não chỉ giữ được năm tới mười phút. Phần ghi trước đó bị đẩy ra để lấy chỗ cho phần mới."),
   (2, "Đó là lý do ngồi hai tiếng đọc một mạch thường chỉ còn nhớ đoạn cuối."),
   (3, "Đọc theo từng khối mười phút, hết mỗi khối ghi lại một dòng. Cuối buổi bạn còn nguyên bản đồ nội dung."),
   (4, "Đọc ít hơn mà nhớ nhiều hơn. Đó là cách học trong khoá Speed Reading."),
 ],
}

# ---------------------------------------------------------------- TẬP 4
EP4 = {
 "slug": "05_phuhuynh-con-bo-sach", "total": 43.0,
 "scenes": [(0,5.5),(5.5,15.0),(15.0,25.0),(25.0,34.0),(34.0,43.0)],
 "html": [
   scene("""
    <div class="kicker">Dành cho phụ huynh</div>
    <h1 style="font-size:80px">Con đọc hai trang<br>rồi đặt sách xuống.<br><span class="hl">Không phải con lười.</span></h1>"""),
   scene("""
    <div class="kicker">Ba yếu tố khoa học</div>
    <div class="cards">
      <div class="crd" id="k1"><div class="idx">1</div><div class="txt"><b>Gánh nặng nhận thức</b><span>Đọc là việc nặng: dịch từng chữ, nối câu, dựng hình ảnh</span></div></div>
      <div class="crd" id="k2"><div class="idx">2</div><div class="txt"><b>Thiếu phần thưởng tức thì</b><span>Sách không trả kết quả ngay như điện thoại</span></div></div>
      <div class="crd" id="k3"><div class="idx">3</div><div class="txt"><b>Ảnh hưởng của môi trường</b><span>Tiếng tivi, người nói chuyện, màn hình sáng</span></div></div>
    </div>"""),
   scene("""
    <div class="kicker">Vì sao điện thoại luôn thắng</div>
    <div class="versus">
      <div class="vs"><div class="nm">Điện thoại</div><div class="meter"><i class="m2" id="v1"></i></div><div class="note">Phần thưởng tới ngay lập tức</div></div>
      <div class="vs"><div class="nm">Sách</div><div class="meter"><i id="v2"></i></div><div class="note">Phải đọc vài chục trang mới thấy giá trị</div></div>
    </div>
    <div class="sub">Não trẻ luôn chọn cái cho kết quả nhanh. Đây là sinh lý, không phải tính cách.</div>"""),
   scene("""
    <div class="kicker">Đòi con đọc bao lâu là vừa</div>
    <div class="ages">
      <div class="ageline"><div class="age">6 – 8 tuổi</div><div class="ab"><i id="a1"></i></div><div class="mins">10–15 phút</div></div>
      <div class="ageline"><div class="age">9 – 11 tuổi</div><div class="ab"><i id="a2"></i></div><div class="mins">20–30 phút</div></div>
      <div class="ageline"><div class="age">từ 12 tuổi</div><div class="ab"><i id="a3"></i></div><div class="mins">luyện dần</div></div>
    </div>
    <div class="sub">Đòi con ngồi lâu hơn khả năng của não chỉ làm con sợ việc đọc.</div>"""),
   scene("""
    <div class="kicker">Ba việc làm được ngay tối nay</div>
    <h1 style="font-size:70px">Kể chuyện trước,<br><span class="hl">đọc sau</span></h1>
    <div class="sub">Mỗi lần chỉ 5–10 phút. Có tranh ảnh. Cả nhà cùng ngồi đọc, và khen sau mỗi chương — đó là phần thưởng tức thì thay cho điện thoại.</div>"""),
 ],
 "anim": [
   "",
   """function(t, el){
     $('k1').style.opacity = ease(span(t,6.4,7.2));
     $('k2').style.opacity = ease(span(t,9.0,9.8));
     $('k3').style.opacity = ease(span(t,11.6,12.4));
   }""",
   """function(t, el){
     $('v1').style.width = (ease(span(t,16.2,18.0))*100)+'%';
     $('v2').style.width = (ease(span(t,17.4,20.4))*22)+'%';
   }""",
   """function(t, el){
     $('a1').style.width = (ease(span(t,26.2,28.0))*30)+'%';
     $('a2').style.width = (ease(span(t,28.4,30.2))*65)+'%';
     $('a3').style.width = (ease(span(t,30.6,32.4))*100)+'%';
   }""",
   "",
 ],
 "narration": [
   (0, "Con đọc hai trang rồi đặt sách xuống. Không phải vì con lười."),
   (1, "Có ba yếu tố khoa học: gánh nặng nhận thức, thiếu phần thưởng tức thì, và ảnh hưởng của môi trường."),
   (2, "Điện thoại cho phần thưởng ngay lập tức, còn sách thì không. Não trẻ luôn chọn cái cho kết quả nhanh."),
   (3, "Bé sáu tới tám tuổi tập trung được mười tới mười lăm phút. Chín tới mười một tuổi thì hai mươi tới ba mươi phút."),
   (4, "Kể câu chuyện trước khi cho đọc. Mỗi lần năm tới mười phút. Và cả nhà cùng ngồi đọc."),
 ],
}

# ---------------------------------------------------------------- TẬP 5
EP5 = {
 "slug": "06_ky-thuat-chi-tay", "total": 42.0,
 "scenes": [(0,5.0),(5.0,15.0),(15.0,25.0),(25.0,34.0),(34.0,42.0)],
 "html": [
   scene("""
    <div class="kicker">Kỹ thuật đầu tiên</div>
    <h1>Mắt bạn không tự<br>biết đi nhanh.<br><span class="hl">Nó cần vật dẫn đường.</span></h1>"""),
   scene("""
    <div class="kicker">Bước 1 — đặt ngón tay và trượt theo nhịp hiện tại</div>
    <div class="lines" id="l1">
      <div class="ln"><span class="wd">Đọc</span> <span class="wd">nhanh</span> <span class="wd">không</span> <span class="wd">phải</span> <span class="wd">là</span> <span class="wd">đọc</span> <span class="wd">lướt</span></div>
      <div class="ln"><span class="wd">Mắt</span> <span class="wd">bám</span> <span class="wd">theo</span> <span class="wd">một</span> <span class="wd">vật</span> <span class="wd">chuyển</span> <span class="wd">động</span></div>
      <div class="ln"><span class="wd">và</span> <span class="wd">đi</span> <span class="wd">nhanh</span> <span class="wd">hơn</span> <span class="wd">bình</span> <span class="wd">thường</span></div>
    </div>
    <div class="finger" style="opacity:0"></div>"""),
   scene("""
    <div class="kicker">Bước 2 — tăng dần theo nhịp đếm</div>
    <div class="lines" id="l2">
      <div class="ln"><span class="wd">Ba</span></div>
      <div class="ln"><span class="wd">Hai</span></div>
      <div class="ln"><span class="wd">Một</span> <span class="wd">—</span> <span class="wd">trượt</span> <span class="wd">nhanh</span> <span class="wd">hơn</span> <span class="wd">một</span> <span class="wd">chút</span></div>
    </div>
    <div class="tempo"><div class="beat" id="b1">3</div><div class="beat" id="b2">2</div><div class="beat" id="b3">1</div><span style="font-size:34px;color:#8fa19d">rồi tăng tốc</span></div>
    <div class="finger" style="opacity:0"></div>"""),
   scene("""
    <div class="kicker">Vì sao hiệu quả</div>
    <div class="cards">
      <div class="crd" id="w1"><div class="idx">1</div><div class="txt"><b>Mắt bám theo vật chuyển động</b><span>Đây là phản xạ tự nhiên, không cần cố</span></div></div>
      <div class="crd" id="w2"><div class="idx">2</div><div class="txt"><b>Ngăn mắt nhảy ngược dòng</b><span>Phần lớn thời gian đọc bị mất ở chỗ nhảy lại</span></div></div>
    </div>"""),
   scene(CTA),
 ],
 "anim": [
   "",
   """function(t, el){
     const lns = el.querySelectorAll('.ln');
     const total = 3;
     const prog = lock(span(t,6.0,13.8),0,1) * total;
     lns.forEach(function(ln,i){
       const words = ln.querySelectorAll('.wd');
       words.forEach(function(w,j){
         const w0 = i + j/words.length;
         w.classList.toggle('lit', w0 < prog);
       });
     });
     const f = document.querySelectorAll('[data-scene="1"] .finger')[0];
     const cur = lock(prog,0.001,3-0.001);
     const li = Math.min(2, Math.floor(cur));
     const ln = lns[li];
     const r = ln.getBoundingClientRect(), hr = el.getBoundingClientRect();
     const frac = cur - li;
     const x = Math.min(r.left - hr.left + frac*Math.min(r.width, 860) - 22, 1000 - 70);
     f.style.transform = 'translate(' + x + 'px,' + (r.top - hr.top - 26) + 'px)';
     f.style.opacity = 1;
   }""",
   """function(t, el){
     const beats = [ $('b1'), $('b2'), $('b3') ];
     const k = Math.floor(lock(span(t,16.4,24.4),0,2.999));
     beats.forEach(function(b,i){ b.classList.toggle('on', i<=k); });
     const lns = el.querySelectorAll('.ln');
     lns.forEach(function(ln,i){ ln.style.opacity = i<=k ? 1 : 0.18; });
     const f = document.querySelectorAll('[data-scene="2"] .finger')[0];
     if (f){
       const ln = lns[Math.min(2,k)];
       const r = ln.getBoundingClientRect(), hr = el.getBoundingClientRect();
       const frac = lock(span(t,16.4 + k*2.7, 16.4 + k*2.7 + 2.4),0,1);
       const x = Math.min(r.left - hr.left + frac*r.width - 22, 1000 - 70);
       f.style.transform = 'translate(' + x + 'px,' + (r.top - hr.top - 26) + 'px)';
       f.style.opacity = 1;
     }
   }""",
   """function(t, el){
     $('w1').style.opacity = ease(span(t,26.2,27.0));
     $('w2').style.opacity = ease(span(t,28.6,29.4));
   }""",
   "",
 ],
 "narration": [
   (0, "Mắt bạn không tự biết đi nhanh. Nó cần một vật dẫn đường."),
   (1, "Đặt ngón tay dưới dòng chữ và trượt theo nhịp đọc hiện tại. Mắt sẽ bám theo ngón tay."),
   (2, "Sau đó tăng dần. Đếm ba, hai, một, rồi trượt nhanh hơn một chút. Nhịp tay kéo mắt đi."),
   (3, "Cách này hiệu quả vì mắt vốn bám theo vật chuyển động, và ngón tay ngăn mắt nhảy ngược lên dòng trên."),
   (4, "Chỉ cần một ngón tay. Kỹ thuật này có trong buổi đầu tiên của khoá."),
 ],
}

# ---------------------------------------------------------------- TẬP 7 — bài kiểm tra 60 giây
PASSAGE = ("Đọc nhanh không phải là đọc lướt. Đọc lướt là bỏ qua nội dung. Đọc nhanh là mở rộng vùng nhìn "
           "để mắt nhận nhiều chữ hơn trong một lần dừng. Người đọc chậm dừng ở từng chữ. Người đọc nhanh "
           "gom ba đến năm chữ một lần dừng. Mắt vẫn nhìn rõ, não vẫn hiểu, chỉ khác là số lần dừng ít hơn. "
           "Muốn làm được điều đó, trước hết phải bỏ giọng đọc trong đầu. Giọng đọc trong đầu chạy theo tốc "
           "độ nói, khoảng hai trăm năm mươi từ một phút. Trong khi mắt có thể nhận gấp đôi con số đó nếu "
           "không bị giữ lại. Bước thứ hai là mở rộng vùng nhìn rõ. Bước thứ ba là đọc theo cụm có nghĩa "
           "thay vì đọc từng từ rời rạc. Bước thứ tư là luyện mỗi ngày mười lăm phút với ngón tay dẫn đường. "
           "Sau hai tuần, phần lớn học viên tăng tốc độ đọc gấp đôi mà vẫn trả lời được câu hỏi về nội dung. "
           "Điều quan trọng nhất không phải là con số từ một phút, mà là bạn hiểu được bao nhiêu sau khi đọc xong.").split()


def _flash(scene_from, scene_to, wpm, t0, css_id):
    seg = PASSAGE[scene_from:scene_to]
    return (f'<div class="flash" data-words="{"|".join(seg)}" data-wpm="{wpm}" data-t0="{t0}">'
            f'<span class="w" id="{css_id}w">—</span></div>')


EP7 = {
 "slug": "07_bai-test-60-giay", "total": 46.0,
 "scenes": [(0,5.5),(5.5,16.0),(16.0,29.0),(29.0,39.0),(39.0,46.0)],
 "html": [
   scene("""
    <div class="kicker">Bài kiểm tra 60 giây</div>
    <h1>Bạn đọc được<br>bao nhiêu từ<br><span class="hl">một phút?</span></h1>
    <div class="sub">Xem hết video rồi tự tính. Không cần giấy bút, không cần bấm giờ.</div>"""),
   scene("""
    <div class="kicker">Mốc 1 — 200 từ một phút</div>
    <div class="flash" data-words="__A__" data-wpm="200" data-t0="6.0"><span class="w" id="f1w">—</span></div>
    <div class="testbar"><span class="cnt" id="f1c">0 từ</span><div class="track"><i class="pg" id="f1p"></i></div><span class="rate">200 từ/phút</span></div>
    <div class="sub">Đọc thầm theo từng từ hiện ra. Giữ đúng tốc độ này.</div>"""),
   scene("""
    <div class="kicker">Mốc 2 — 300 từ một phút</div>
    <div class="flash" data-words="__B__" data-wpm="300" data-t0="16.5"><span class="w" id="f2w">—</span></div>
    <div class="testbar"><span class="cnt" id="f2c">0 từ</span><div class="track"><i class="pg" id="f2p"></i></div><span class="rate">300 từ/phút</span></div>
    <div class="sub">Nhanh hơn một chút. Nếu bắt đầu hụt, ghi nhớ mốc này.</div>"""),
   scene("""
    <div class="kicker">Mốc 3 — 450 từ một phút</div>
    <div class="flash" data-words="__C__" data-wpm="450" data-t0="29.5"><span class="w" id="f3w">—</span></div>
    <div class="testbar"><span class="cnt" id="f3c">0 từ</span><div class="track"><i class="pg" id="f3p"></i></div><span class="rate">450 từ/phút</span></div>
    <div class="sub">Đây là tốc độ của người đã luyện. Còn theo kịp không?</div>"""),
   scene("""
    <div class="kicker">Bạn hụt ở mốc nào?</div>
    <h1 style="font-size:76px">Ghi mốc đó<br><span class="hl">vào bình luận</span></h1>
    <div class="sub">Mốc 200 là người đọc thường. Mốc 300 là người đã luyện vài tuần. Mốc 450 là mức học viên đạt sau khoá.</div>
    <div class="cta"><div class="a">Khoá học</div><div class="b">Đọc hiệu quả Speed Reading</div><div class="c">Học phí 980.000đ · có buổi 1 hoàn tiền</div></div>"""),
 ],
 "anim": [
   "",
   """function(t, el){
     const box = el.querySelector('.flash');
     const w = box.dataset.words.split('|'), rate = +box.dataset.wpm, t0 = +box.dataset.t0;
     const i = Math.max(0, Math.floor((t - t0) / (60/rate)));
     box.querySelector('.w').textContent = i < w.length ? w[i] : '—';
     el.querySelector('.cnt').textContent = Math.min(i+1, w.length) + '/' + w.length + ' từ';
     el.querySelector('.pg').style.width = (lock(i/w.length,0,1)*100) + '%';
   }""",
   """function(t, el){
     const box = el.querySelector('.flash');
     const w = box.dataset.words.split('|'), rate = +box.dataset.wpm, t0 = +box.dataset.t0;
     const i = Math.max(0, Math.floor((t - t0) / (60/rate)));
     box.querySelector('.w').textContent = i < w.length ? w[i] : '—';
     el.querySelector('.cnt').textContent = Math.min(i+1, w.length) + '/' + w.length + ' từ';
     el.querySelector('.pg').style.width = (lock(i/w.length,0,1)*100) + '%';
   }""",
   """function(t, el){
     const box = el.querySelector('.flash');
     const w = box.dataset.words.split('|'), rate = +box.dataset.wpm, t0 = +box.dataset.t0;
     const i = Math.max(0, Math.floor((t - t0) / (60/rate)));
     box.querySelector('.w').textContent = i < w.length ? w[i] : '—';
     el.querySelector('.cnt').textContent = Math.min(i+1, w.length) + '/' + w.length + ' từ';
     el.querySelector('.pg').style.width = (lock(i/w.length,0,1)*100) + '%';
   }""",
   "",
 ],
 "narration": [
   (0, "Bạn đọc được bao nhiêu từ một phút? Thử ngay bây giờ."),
   (4, "Bạn hụt ở mốc nào thì ghi vào bình luận nhé."),
 ],
}

# ---------------------------------------------------------------- TẬP 8 — trường nhìn
EP8 = {
 "slug": "08_truong-nhin", "total": 42.0,
 "scenes": [(0,5.0),(5.0,16.0),(16.0,26.0),(26.0,35.0),(35.0,42.0)],
 "html": [
   scene("""
    <div class="kicker">Trường nhìn</div>
    <h1>Mắt bạn chỉ nhìn rõ<br>một chữ. Nhưng não<br><span class="hl">đọc được cả cụm.</span></h1>"""),
   scene("""
    <div class="kicker">Điểm nhìn rõ chỉ bằng hạt đậu</div>
    <div class="cluster" id="cl1">
      <span class="cw dim">Người</span><span class="cw dim">đọc</span><span class="cw sharp">nhanh</span><span class="cw dim">không</span><span class="cw dim">dừng</span>
    </div>
    <div class="reticle" id="ret1"></div>
    <div class="sub">Phần nhìn rõ rất nhỏ. Mọi thứ quanh nó mờ đi — nhưng não vẫn nhận ra chữ.</div>"""),
   scene("""
    <div class="kicker">Hai vùng trường nhìn</div>
    <div class="eyewrap">
      <div class="ring outer" id="r1"></div>
      <div class="ring inner" id="r2"></div>
      <div class="eyedot"></div>
    </div>
    <div class="legend"><span class="l1">Vùng nhìn rõ</span><span class="l2">Vùng nhận dạng chữ</span></div>
    <div class="sub">Đọc từng chữ là chỉ dùng vùng nhỏ. Đọc cụm là dùng cả vùng rộng hơn.</div>"""),
   scene("""
    <div class="kicker">Luyện mở rộng vùng nhận dạng</div>
    <div class="cluster big" id="cl2">
      <span class="cw wide" id="w1">Người</span><span class="cw wide" id="w2">đọc</span><span class="cw wide" id="w3">nhanh</span>
    </div>
    <div class="cluster big" id="cl3">
      <span class="cw wide" id="w4">không</span><span class="cw wide" id="w5">dừng</span><span class="cw wide" id="w6">lại</span>
    </div>
    <div class="sub">Ba tới năm chữ một lần dừng. Đây là nền tảng của đọc cụm.</div>"""),
   scene(CTA),
 ],
 "anim": [
   "",
   """function(t, el){
     const ws = el.querySelectorAll('.cw'), ret = el.querySelector('.reticle');
     const prog = lock(span(t,6.0,13.6),0,1) * (ws.length-1);
     ws.forEach(function(w,i){ w.classList.toggle('sharp', Math.abs(i - prog) < 0.5); });
     const cur = lock(prog, 0.001, ws.length-1.001);
     const li = Math.floor(cur);
     const a = ws[li].getBoundingClientRect(), b = ws[Math.min(li+1,ws.length-1)].getBoundingClientRect();
     const hr = el.getBoundingClientRect();
     const frac = cur - li;
     const x = (a.left - hr.left) + ((b.left - a.left) * frac) - 12;
     ret.style.transform = 'translate(' + x + 'px,' + (a.top - hr.top - 10) + 'px)';
     ret.style.width = (a.width + 24) + 'px';
     ret.style.height = (a.height + 20) + 'px';
     ret.style.opacity = 1;
   }""",
   """function(t, el){
     const o = ease(span(t,17.0,19.4)), i = ease(span(t,18.4,20.0));
     const r1 = el.querySelector('#r1'), r2 = el.querySelector('#r2');
     r1.style.opacity = o; r1.style.width = r1.style.height = (260 + o*440) + 'px';
     r2.style.opacity = i; r2.style.width = r2.style.height = (120 + i*110) + 'px';
   }""",
   """function(t, el){
     [1,2,3].forEach(function(k){ el.querySelector('#w'+k).style.opacity = ease(span(t,27.0+k*0.45, 28.0+k*0.45)); });
     [4,5,6].forEach(function(k){ el.querySelector('#w'+k).style.opacity = ease(span(t,28.8+k*0.45, 29.8+k*0.45)); });
   }""",
   "",
 ],
 "narration": [
   (0, "Mắt bạn chỉ nhìn rõ được một chữ tại một thời điểm."),
   (1, "Vùng nhìn rõ rất nhỏ, chỉ bằng hạt đậu. Nhưng quanh nó, não vẫn nhận ra chữ."),
   (2, "Nếu bạn chỉ dùng vùng nhỏ, mỗi chữ là một lần dừng. Nếu dùng cả vùng rộng hơn, một lần dừng được ba tới năm chữ."),
   (3, "Luyện tập là mở rộng dần vùng nhận dạng chữ. Đó là nền tảng của đọc cụm."),
   (4, "Đây là bài tập đầu tiên trong buổi hai của khoá Speed Reading."),
 ],
}

# ---------------------------------------------------------------- TẬP 9 — quy luật 80/20
EP9 = {
 "slug": "09_quyluat-8020", "total": 42.0,
 "scenes": [(0,5.0),(5.0,15.0),(15.0,25.0),(25.0,34.0),(34.0,42.0)],
 "html": [
   scene("""
    <div class="kicker">Quy luật trong sách</div>
    <h1>80% giá trị của một quyển sách<br>nằm ở <span class="hl">20% số trang</span></h1>"""),
   scene("""
    <div class="kicker">Vậy 20% đó nằm ở đâu</div>
    <div class="stack" id="st1"></div>
    <div class="badge"><span class="t">Số trang cần đọc kỹ</span><span class="v">2 trên 10</span></div>"""),
   scene("""
    <div class="kicker">Bốn chỗ luôn có giá trị nhất</div>
    <div class="list20">
      <div class="it" id="i1"><b>1</b> Bìa, lời giới thiệu, đoạn mở đầu</div>
      <div class="it" id="i2"><b>2</b> Mục lục — xem cả quyển sách trong một trang</div>
      <div class="it" id="i3"><b>3</b> Tiêu đề chính và tiêu đề phụ của từng chương</div>
      <div class="it" id="i4"><b>4</b> Đoạn đầu và đoạn cuối mỗi chương</div>
    </div>"""),
   scene("""
    <div class="kicker">Cách đọc theo quy luật này</div>
    <h1 style="font-size:74px">Đọc 20% trước,<br>rồi mới quyết định<br><span class="hl">đọc tiếp hay bỏ</span></h1>
    <div class="sub">Nếu 20% đầu đã đủ giá trị, bạn tiết kiệm 80% thời gian. Nếu chưa, bạn mới đọc sâu phần còn lại.</div>"""),
   scene(CTA),
 ],
 "anim": [
   "",
   """function(t, el){
     const st = el.querySelector('#st1');
     if (!st.dataset.built){
       for (let k=0;k<10;k++){
         const d = document.createElement('div');
         d.className = 'pgbar'; d.dataset.k = k;
         d.innerHTML = '<span class="pi">' + (k+1) + '</span>';
         st.appendChild(d);
       }
       st.dataset.built = '1';
     }
     const on = [2,7];
     st.querySelectorAll('.pgbar').forEach(function(b){
       const k = +b.dataset.k;
       b.classList.toggle('on', on.indexOf(k) >= 0 && t > 8.0 + (on.indexOf(k))*0.6);
     });
   }""",
   """function(t, el){ [1,2,3,4].forEach(function(k){ el.querySelector('#i'+k).style.opacity = ease(span(t,16.2+(k-1)*0.9, 17.0+(k-1)*0.9)); }); }""",
   "",
   "",
 ],
 "narration": [
   (0, "Tám mươi phần trăm giá trị của một quyển sách nằm ở hai mươi phần trăm số trang."),
   (1, "Nghĩa là hai trang trên mười. Đọc hết mười trang là bỏ phí tám trang."),
   (2, "Bốn chỗ luôn có giá trị nhất: phần mở đầu, mục lục, các tiêu đề, và đoạn đầu cuối mỗi chương."),
   (3, "Đọc hai mươi phần trăm trước, rồi mới quyết định có đọc tiếp hay không."),
   (4, "Đây là cách học viên đọc xong một quyển sách trong hai buổi tối."),
 ],
}

EP20_11 = {
 "slug": "20_11_cam-on-thay-co", "total": 42.0,
 "brand": "VĂN HỈ OFFICIAL · 20/11",
 "css_extra": """
  #bg{background:
      radial-gradient(1100px 900px at 18% 10%, rgba(255,179,71,.20), transparent 60%),
      radial-gradient(900px 800px at 82% 88%, rgba(224,131,116,.14), transparent 62%),
      linear-gradient(160deg,#1a0f08 0%,#2a1a0e 55%,#120a06 100%)!important}
  .kicker{color:#ffb347!important}
  h1 .hl{color:#ffb347!important}
  .sub b{color:#ffd9a8!important}
  .warmcard{display:flex;flex-direction:column;gap:26px;margin-top:14px}
  .warmcard .wc{background:#2a1c12;border:2px solid #4a3120;border-radius:22px;padding:34px 40px;opacity:0}
  .warmcard .wc .wl{font-size:34px;color:#ffb347;font-weight:700;margin-bottom:12px}
  .warmcard .wc .wt{font-size:46px;line-height:1.35}
  .warmcard .wc .ws{font-size:30px;color:#c9ae91;margin-top:12px}
  .heart{font-size:150px;text-align:center;opacity:0;line-height:1}
  .ripple{font-size:40px;color:#ffb347;text-align:center;opacity:0;margin-top:26px}
 """,
 "scenes": [(0,5.0),(5.0,15.0),(15.0,25.0),(25.0,35.0),(35.0,42.0)],
 "html": [
   scene("""<div class="kicker">20 tháng 11</div>
    <h1>Hôm nay con<br><span class="hl">nhớ thầy cô.</span></h1>
    <div class="sub">Không chỉ là một ngày lịch. Là một cái tên hiện lên trong đầu.</div>"""),
   scene("""<div class="kicker">Điều thầy dạy</div>
    <div class="warmcard" id="wc1">
      <div class="wc"><div class="wl">Công thức</div><div class="wt">Có thể quên.</div></div>
      <div class="wc"><div class="wl">Cách đặt câu hỏi</div><div class="wt">Ở lại suốt đời.</div></div>
    </div>"""),
   scene("""<div class="kicker">Điều cô dạy</div>
    <div class="heart" id="ht1">♥</div>
    <div class="ripple" id="rp1">Đọc chậm lại, để hiểu chữ đang nói gì.</div>
    <div class="sub">Cô không dạy con đọc nhanh hơn. Cô dạy con dừng lại lâu hơn.</div>"""),
   scene("""<div class="kicker">Một tiết học</div>
    <div class="warmcard" id="wc2">
      <div class="wc"><div class="wl">Lúc đó</div><div class="wt">Giọng con còn run.</div></div>
      <div class="wc"><div class="wl">Hôm nay</div><div class="wt">Con vẫn đang đặt câu hỏi.</div></div>
    </div>"""),
   scene("""<div class="kicker">Lời cảm ơn</div>
    <h1 style="font-size:80px">Cảm ơn<br><span class="hl">thầy cô.</span></h1>
    <div class="sub">Có một người thầy hay người cô bạn nhớ mãi?<br>Comment tên họ bên dưới nhé.</div>"""),
 ],
 "anim": [
   "",
   """function(t, el){
     [1,2].forEach(function(k){
       var c = el.querySelector('.wc:nth-child('+k+')');
       c.style.opacity = ease(span(t, 6.4+k*1.8, 7.4+k*1.8));
       c.style.transform = 'translateY('+((1-ease(span(t,6.4+k*1.8,7.4+k*1.8)))*24)+'px)';
     });
   }""",
   """function(t, el){
     var h = el.querySelector('#ht1'), r = el.querySelector('#rp1');
     var o = ease(span(t,16.0,17.6)); h.style.opacity=o; h.style.transform='scale('+(0.7+o*0.3)+')';
     r.style.opacity = ease(span(t,18.2,19.6));
   }""",
   """function(t, el){
     [1,2].forEach(function(k){
       var c = el.querySelector('.wc:nth-child('+k+')');
       c.style.opacity = ease(span(t, 26.4+k*1.8, 27.4+k*1.8));
     });
   }""",
   "",
 ],
 "narration": [
   (0, "Hôm nay là hai mươi tháng mười một. Hỉ ngồi nhớ lại những người đã dạy mình."),
   (1, "Không phải họ dạy công thức. Mà dạy cách đặt câu hỏi. Công thức có thể quên. Cách hỏi thì ở lại suốt đời."),
   (2, "Cô dạy Hỉ đọc chậm lại, để hiểu chữ đang nói gì. Cô không dạy đọc nhanh hơn. Cô dạy dừng lại lâu hơn."),
   (3, "Thầy bắt Hỉ đứng dậy trình bày, dù giọng lúc đó còn run. Hôm nay Hỉ vẫn đang đặt câu hỏi."),
   (4, "Cảm ơn thầy cô. Nếu bạn cũng có một người bạn nhớ mãi, comment tên họ bên dưới nhé."),
 ],
}

# ---------------------------------------------------------------- TẬP 10 — A1: điểm dừng của mắt
EP10 = {
 "slug": "10_diem-dung-cua-mat", "total": 42.0,
 "scenes": [(0,5.0),(5.0,15.0),(15.0,25.0),(25.0,34.0),(34.0,42.0)],
 "html": [
   scene("""
    <div class="kicker">Vì sao bạn đọc chậm</div>
    <h1>Mắt không đọc cả dòng —<br>mắt <span class="hl">nhảy từng chữ</span></h1>
    <div class="sub">Mỗi lần dừng, mắt chỉ nhận được một chữ. Một dòng mười chữ là mười lần dừng.</div>"""),
   scene("""
    <div class="kicker">Theo dõi mắt trên một dòng chữ</div>
    <div class="fixline" id="fl1">
      <span class="fixdot" id="dt1"></span>
      <span class="fxw">Học</span><span class="fxw">đọc</span><span class="fxw">nhanh</span><span class="fxw">cần</span><span class="fxw">luyện</span><span class="fxw">mắt</span>
    </div>
    <div class="fixcount" id="c1"><span class="n" id="n1">0</span><span class="u">điểm dừng cho sáu chữ</span></div>"""),
   scene("""
    <div class="kicker">Cùng dòng chữ đó, đọc theo cụm</div>
    <div class="fixline" id="fl2">
      <div class="clwrap"><span class="fxw">Học</span><span class="fxw">đọc</span><span class="fxw">nhanh</span></div>
      <div class="clwrap"><span class="fxw">cần</span><span class="fxw">luyện</span><span class="fxw">mắt</span></div>
    </div>
    <div class="fixcount" id="c2"><span class="n ok" id="n2">—</span><span class="u">điểm dừng, thay vì sáu</span></div>"""),
   scene("""
    <div class="kicker">Cùng một dòng, hai tốc độ</div>
    <div class="race">
      <div class="row"><div class="name"><b>Đọc từng chữ</b><span class="val" id="e1v">0 từ/phút</span></div>
        <div class="track"><i class="fill red" id="e1f"></i></div></div>
      <div class="row"><div class="name"><b>Đọc theo cụm ba từ</b><span class="val" id="e2v">0 từ/phút</span></div>
        <div class="track"><i class="fill" id="e2f"></i></div></div>
    </div>
    <div class="badge"><span class="t">Ít điểm dừng hơn</span><span class="v">nhanh hơn</span></div>"""),
   scene(CTA),
 ],
 "anim": [
   "",
   """function(t, el){
     const ws = el.querySelectorAll('.fxw'), dot = el.querySelector('#dt1');
     const n = ws.length;
     const p = lock((t - 7.6) / 5.2, 0, 0.999);
     const k = Math.floor(p * n);
     ws.forEach(function(w, i){ w.classList.toggle('lit', i === k && t > 7.4); });
     const bt = ws[k].getBoundingClientRect(), bp = el.querySelector('.fixline').getBoundingClientRect();
     dot.style.opacity = t > 7.2 ? 1 : 0;
     dot.style.transform = 'translateX(' + (bt.left - bp.left + bt.width/2 - 13) + 'px)';
     el.querySelector('#n1').textContent = (t > 7.2 ? k + 1 : 0);
   }""",
   """function(t, el){
     const bx = el.querySelectorAll('.clwrap');
     bx.forEach(function(b, i){ b.style.opacity = ease(span(t, 17.0 + i*0.8, 18.1 + i*0.8)); });
     el.querySelector('#n2').textContent = (t > 18.4 ? '2' : '—');
     el.querySelectorAll('#fl2 .fxw').forEach(function(w, i){
       w.style.color = (t > 18.6 + i*0.12) ? '#f2f5f4' : '#8fa19d';
     });
   }""",
   """function(t, el){
     const a = ease(span(t, 28.0, 31.0)), b = ease(span(t, 28.6, 31.6));
     el.querySelector('#e1f').style.width = (a*50)+'%';
     el.querySelector('#e1v').textContent = Math.round(a*250)+' từ/phút';
     el.querySelector('#e2f').style.width = (b*100)+'%';
     el.querySelector('#e2v').textContent = Math.round(b*450)+' từ/phút';
   }""",
   "",
 ],
 "narration": [
   (0, "Mắt không đọc cả dòng — mắt nhảy từng chữ một."),
   (1, "Sáu chữ này, mắt phải dừng sáu lần. Mỗi lần chỉ nhận được một chữ."),
   (2, "Đọc theo cụm ba từ, mắt chỉ còn dừng hai lần. Đó là lý do tốc độ tăng."),
   (3, "Hai con số hai trăm năm mươi và bốn trăm năm mươi từ một phút là minh hoạ."),
   (4, "Đọc cụm là kỹ thuật đầu tiên trong khoá Đọc hiệu quả Speed Reading."),
 ],
}

# ---------------------------------------------------------------- TẬP 11 — A6: đọc ngắt quãng mất mạch hiểu
EP11 = {
 "slug": "11_doc-ngat-quang", "total": 42.0,
 "scenes": [(0,5.0),(5.0,15.0),(15.0,25.0),(25.0,34.0),(34.0,42.0)],
 "html": [
   scene("""
    <div class="kicker">Vì sao đọc mãi không vào</div>
    <h1>Đọc mười phút, nghỉ mười phút —<br><span class="bad">mạch hiểu đứt</span></h1>
    <div class="sub">Không phải bạn kém tập trung. Là cách chia thời gian đang sai.</div>"""),
   scene("""
    <div class="kicker">Hai cách chia ba mươi phút đọc</div>
    <div class="tl">
      <div class="tlrow"><div class="nm">Đọc liền</div>
        <div class="bars"><i class="seg" id="s1" style="flex:3"></i></div></div>
      <div class="tlrow"><div class="nm">Đọc ngắt quãng</div>
        <div class="bars"><i class="seg" id="s2" style="flex:1"></i><i class="gap" id="g1" style="flex:1"></i><i class="seg" id="s3" style="flex:1"></i><i class="gap" id="g2" style="flex:1"></i><i class="seg" id="s4" style="flex:1"></i></div></div>
    </div>
    <div class="note">Cùng ba mươi phút, khác nhau ở chỗ mạch hiểu có bị cắt hay không.</div>"""),
   scene("""
    <div class="kicker">Mạch hiểu bị cắt ở mỗi chỗ nghỉ</div>
    <div class="chain" id="ch"></div>
    <div class="hieubar"><span class="lb">Đọc liền</span><span class="tr"><i id="h1b"></i></span><span class="pc" id="h1p">0%</span></div>
    <div class="hieubar"><span class="lb">Đọc ngắt quãng</span><span class="tr"><i class="bad" id="h2b"></i></span><span class="pc" id="h2p">0%</span></div>
    <div class="note">Hai cột này là minh hoạ cho độ chênh, không phải số đo của anh.</div>"""),
   scene("""
    <div class="kicker">Cách sửa, làm được ngay tối nay</div>
    <div class="list3">
      <div class="it" id="i1"><b>1</b> Đọc liền hai mươi đến hai mươi lăm phút, rồi nghỉ ba đến năm phút</div>
      <div class="it" id="i2"><b>2</b> Trước khi nghỉ, ghi lại đúng một câu chốt vừa đọc được</div>
      <div class="it" id="i3"><b>3</b> Lần sau mở sách, đọc lại câu đó rồi mới đọc tiếp</div>
    </div>"""),
   scene(CTA),
 ],
 "anim": [
   "",
   """function(t, el){
     const a = ease(span(t, 6.6, 8.2)), b = ease(span(t, 9.0, 10.4)), c = ease(span(t, 10.6, 12.0));
     el.querySelector('#s1').style.width = (a*100)+'%';
     el.querySelector('#s2').style.width = (b*100)+'%';
     el.querySelector('#s3').style.width = (b*100)+'%';
     el.querySelector('#s4').style.width = (c*100)+'%';
   }""",
   """function(t, el){
     const ch = el.querySelector('#ch');
     if (!ch.dataset.built){
       const gaps = [3, 7];                       // hai chỗ nghỉ cắt mạch
       for (let i=0;i<11;i++){
         const L = document.createElement('i'); L.className = 'link';
         L.style.left = (3 + i*7.6) + '%'; L.style.width = '7.6%';
         if (gaps.indexOf(i) >= 0) L.dataset.gap = '1';
         ch.appendChild(L);
         const N = document.createElement('span'); N.className = 'nd';
         N.style.left = 'calc(' + (3 + i*7.6) + '% - 10px)';
         ch.appendChild(N);
       }
       ch.dataset.built = '1';
     }
     ch.querySelectorAll('.link').forEach(function(L, i){
       const on = ease(span(t, 17.0 + i*0.35, 17.9 + i*0.35));
       L.style.opacity = L.dataset.gap ? 0 : on;              // chỗ nghỉ: mạch không nối
       L.style.background = L.dataset.gap ? '#e08374' : '#3fb8a8';
       L.style.width = (on*7.6)+'%';
     });
     ch.querySelectorAll('.nd').forEach(function(N, i){
       N.style.opacity = ease(span(t, 16.8 + i*0.35, 17.6 + i*0.35));
     });
     const p1 = ease(span(t, 20.0, 22.0)), p2 = ease(span(t, 20.4, 22.4));
     el.querySelector('#h1b').style.width = (p1*100)+'%';
     el.querySelector('#h1p').textContent = Math.round(p1*100)+'%';
     el.querySelector('#h2b').style.width = (p2*60)+'%';
     el.querySelector('#h2p').textContent = Math.round(p2*60)+'%';
   }""",
   """function(t, el){ [1,2,3].forEach(function(k){ el.querySelector('#i'+k).style.opacity = ease(span(t, 26.4+(k-1)*0.8, 27.3+(k-1)*0.8)); }); }""",
   "",
 ],
 "narration": [
   (0, "Đọc mười phút, nghỉ mười phút — mạch hiểu đứt."),
   (1, "Cùng ba mươi phút: đọc liền một mạch, hoặc chia ba lần, giữa có khoảng nghỉ."),
   (2, "Mỗi khoảng nghỉ cắt đứt mạch hiểu. Hai cột này là minh hoạ, không phải số đo của anh."),
   (3, "Cách sửa: đọc liền hai mươi lăm phút, nghỉ năm phút, ghi một câu chốt trước khi nghỉ."),
   (4, "Giữ mạch hiểu liền mạch là nguyên tắc thứ ba trong khoá học."),
 ],
}

EPISODES = [EP1, EP2, EP3, EP4, EP5, EP7, EP8, EP9, EP20_11, EP10, EP11]


def build_html(ep):
    sc = [{"start": a, "end": b} for a, b in ep["scenes"]]
    anims = [("null" if not a.strip() else "(" + a.strip() + ")") for a in ep["anim"]]
    js = (JS_FRAME
          .replace("__SCENES__", json.dumps(sc))
          .replace("__ANIM__", "[" + ",".join(anims) + "]")
          .replace("__TOTAL__", str(ep["total"])))
    scenes_html = "\n".join(
        f'<div class="scene" data-scene="{i}">{h}</div>' for i, h in enumerate(ep["html"]))
    # đoạn chữ cho bài kiểm tra tốc độ: A 200 từ/phút, B 300, C 450
    for ph, seg in (("__A__", PASSAGE[0:34]), ("__B__", PASSAGE[34:99]), ("__C__", PASSAGE[99:140])):
        scenes_html = scenes_html.replace(ph, "|".join(seg))
    extra_css = ep.get("css_extra", "")
    brand_text = ep.get("brand", "SPEED READING VIỆT NAM")
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<title>{ep['slug']}</title>
<style>{CSS}
{extra_css}</style>
</head>
<body>
<div id="stage">
  <div id="bg"></div>
  <div class="grain"></div>
  {scenes_html}
  <div id="brand">{brand_text}</div>
</div>
<script>
{js}
</script>
</body>
</html>
"""


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
    for ep in EPISODES:
        p = f"{OUT}/{ep['slug']}.html"
        open(p, "w", encoding="utf-8").write(build_html(ep))
        print(f"đã ghi {p}  ({len(ep['html'])} cảnh, tổng {ep['total']}s)")


if __name__ == "__main__":
    main()
