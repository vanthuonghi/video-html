#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kịch bản 22 tập: mỗi tập một dict (slug, ten, total, scenes, html, anim, narration).

Tách khỏi dung-tap-do-hoa.py để sửa nội dung không phải mở tệp một nghìn dòng.
Khung dựng và mọi công cụ vẫn đọc từ đây, nên vẫn đúng một nguồn sự thật.
Sửa xong chạy: python3 kiem-tra-kich-ban.py

Bộ màu chuẩn từ tập 21 là **đỏ–trắng** theo trang speedreading.vn/sp-online: đặt một chỗ
ở BO_MAU_CHUAN cho mọi tập, tập nào muốn quay lại nền tối thì tự khai "phong_cach": "toi".
Cổng kiem-tra-kich-ban.py sẽ nhắc nếu tập từ 21 trở lên không dùng bộ màu đỏ–trắng.
"""
import math
import re

# Đánh dấu cảnh kết thúc: khi dựng trang sẽ được thay bằng thẻ kết thúc dùng chung.
CTA = "@@END@@"


def scene(html):
    return html.strip()


def scene(html):
    return html.strip()

# ---------------------------------------------------------------- TẬP 1
EP1 = {
 "slug": "02_noi-tham-trong-dau", "total": 42.0, "ten": "Nỗi thầm trong đầu",
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
 "slug": "03_bieu-do-tri-quen", "total": 42.0, "ten": "Biểu đồ trí quên",
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
 "slug": "04_nao-giu-5-10-phut", "total": 42.0, "ten": "Não chỉ giữ được 5–10 phút",
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
 "slug": "05_phuhuynh-con-bo-sach", "total": 43.0, "ten": "Con bỏ sách: phụ huynh làm gì",
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
 "slug": "06_ky-thuat-chi-tay", "total": 42.0, "ten": "Kỹ thuật chỉ tay",
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
     const x = Math.max(96, Math.min(r.left - hr.left + frac*Math.min(r.width, 860) - 22, 960 - 70));
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
       const x = Math.max(96, Math.min(r.left - hr.left + frac*r.width - 22, 960 - 70));
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
 "slug": "07_bai-test-60-giay", "total": 46.0, "ten": "Bài test 60 giây",
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
 "slug": "08_truong-nhin", "total": 42.0, "ten": "Trường nhìn: đọc cả cụm",
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
     // khung ngắm không được vượt vùng an toàn: kẹp theo bề rộng thật của chữ
     const rw = a.width + 24;
     const x = Math.min(Math.max((a.left - hr.left) + ((b.left - a.left) * frac) - 12, 96), 984 - rw);
     ret.style.transform = 'translate(' + x + 'px,' + (a.top - hr.top - 10) + 'px)';
     ret.style.width = rw + 'px';
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
 "slug": "09_quyluat-8020", "total": 42.0, "ten": "Quy luật 80/20 khi đọc sách",
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
 "slug": "20_11_cam-on-thay-co", "total": 42.0, "ten": "Cảm ơn thầy cô",
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
 "slug": "10_diem-dung-cua-mat", "total": 42.0, "ten": "Điểm dừng của mắt",
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
 "slug": "11_doc-ngat-quang", "total": 42.0, "ten": "Đọc ngắt quãng mất mạch hiểu",
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

# ---------------------------------------------------------------- TẬP 12 — có phương pháp là nhanh gấp 2-3 lần
EP12 = {
 "slug": "12_gap-2-3-lan", "total": 45.0, "ten": "Đọc nhanh gấp 2–3 lần",
 "scenes": [(0,5.0),(5.0,15.0),(15.0,26.0),(26.0,36.0),(36.0,45.0)],
 "html": [
   scene("""
    <div class="kicker">Đọc nhanh sau một buổi</div>
    <h1>Không phải mắt bạn chậm —<br>bạn <span class="hl">chưa có phương pháp</span></h1>
    <div class="sub">Người đọc bình thường: khoảng hai trăm từ một phút. Đó không phải giới hạn của con mắt.</div>"""),
   scene("""
    <div class="kicker">Khoảng trống nằm ở đâu</div>
    <div class="race">
      <div class="row"><div class="name"><b>Mắt đủ sức nhận</b><span class="val" id="c1v">0 từ/phút</span></div>
        <div class="track"><i class="fill" id="c1f"></i></div></div>
      <div class="row"><div class="name"><b>Thực tế bạn đang đọc</b><span class="val" id="c2v">0 từ/phút</span></div>
        <div class="track"><i class="fill red" id="c2f"></i></div></div>
    </div>
    <div class="badge"><span class="t">Cùng một con mắt</span><span class="v">chênh 2,5 lần</span></div>"""),
   scene("""
    <div class="kicker">Ba việc tạo ra tốc độ</div>
    <div class="list3">
      <div class="it" id="i1"><b>1</b> Đọc cụm ba đến năm từ, thay vì từng chữ một</div>
      <div class="it" id="i2"><b>2</b> Bỏ phát âm trong đầu — đọc bằng mắt, không bằng lời</div>
      <div class="it" id="i3"><b>3</b> Ngón tay dẫn mắt theo nhịp, không để mắt nhảy ngược</div>
    </div>"""),
   scene("""
    <div class="kicker">Ba chặng trong buổi đầu</div>
    <div class="race">
      <div class="row"><div class="name"><b>Bắt đầu</b><span class="val" id="k1v">0</span></div>
        <div class="track"><i class="fill red" id="k1f"></i></div></div>
      <div class="row"><div class="name"><b>Sau khi đọc cụm</b><span class="val" id="k2v">0</span></div>
        <div class="track"><i class="fill" id="k2f"></i></div></div>
      <div class="row"><div class="name"><b>Sau khi bỏ phát âm</b><span class="val" id="k3v">0</span></div>
        <div class="track"><i class="fill" id="k3f"></i></div></div>
    </div>
    <div class="note">Số trên hình là minh hoạ nhịp tăng; mức thật tuỳ điểm xuất phát của mỗi người.</div>"""),
   scene(CTA),
 ],
 "anim": [
   "",
   """function(t, el){
     const a = ease(span(t, 6.8, 9.2)), b = ease(span(t, 9.4, 11.6));
     el.querySelector('#c1f').style.width = (a*100)+'%';
     el.querySelector('#c1v').textContent = 'khoảng ' + Math.round(a*500) + ' từ/phút';
     el.querySelector('#c2f').style.width = (b*40)+'%';
     el.querySelector('#c2v').textContent = 'khoảng ' + Math.round(b*200) + ' từ/phút';
   }""",
   """function(t, el){ [1,2,3].forEach(function(k){ el.querySelector('#i'+k).style.opacity = ease(span(t,16.8+(k-1)*0.8, 17.7+(k-1)*0.8)); }); }""",
   """function(t, el){
     const a1 = ease(span(t,27.6,29.4)), a2 = ease(span(t,29.4,31.2)), a3 = ease(span(t,31.2,33.0));
     el.querySelector('#k1f').style.width = (a1*250/600*100)+'%';
     el.querySelector('#k1v').textContent = Math.round(a1*250);
     el.querySelector('#k2f').style.width = (a2*400/600*100)+'%';
     el.querySelector('#k2v').textContent = Math.round(a2*400);
     el.querySelector('#k3f').style.width = (a3*550/600*100)+'%';
     el.querySelector('#k3v').textContent = Math.round(a3*550);
   }""",
   "",
 ],
 "narration": [
   (0, "Mắt không chậm. Bạn chưa có phương pháp."),
   (1, "Mắt đủ sức nhận khoảng năm trăm từ một phút. Nhưng bạn đang đọc khoảng hai trăm. Khoảng trống đó là do cách đọc."),
   (2, "Ba việc tạo ra tốc độ: đọc theo cụm ba đến năm từ, bỏ phát âm trong đầu, và để ngón tay dẫn mắt."),
   (3, "Ba chặng trong buổi đầu: đọc cụm, bỏ phát âm, rồi tăng nhịp. Số trên hình là minh hoạ."),
   (4, "Mục tiêu của buổi đầu là gấp đôi. Lớp bảy buổi, học phí chín trăm tám mươi nghìn."),
 ],
}

# ---------------------------------------------------------------- TẬP 13 — B4: đọc tiêu đề trước
EP13 = {
 "slug": "13_tieude-chinh-phu", "total": 45.0, "ten": "Đọc tiêu đề chính phụ trước",
 "scenes": [(0,5.0),(5.0,15.0),(15.0,26.0),(26.0,36.0),(36.0,45.0)],
 "html": [
   scene("""
    <div class="kicker">Nắm một quyển sách trong năm phút</div>
    <h1>Đọc <span class="hl">tiêu đề</span> trước,<br>nội dung sau</h1>
    <div class="sub">Tiêu đề chương là bản tóm tắt mà tác giả đã viết sẵn cho bạn.</div>"""),
   scene("""
    <div class="kicker">Một trang sách, nhìn từ xa</div>
    <div class="page" id="pg1">
      <div class="pg t" id="t1"></div>
      <div class="pg" id="b1"></div><div class="pg" id="b2"></div>
      <div class="pg t" id="t2"></div>
      <div class="pg" id="b3"></div><div class="pg" id="b4"></div><div class="pg" id="b5"></div>
    </div>
    <div class="pgmark"><span id="tt1">tiêu đề chương</span><span id="tt2">chữ nhỏ bên dưới</span></div>"""),
   scene("""
    <div class="kicker">Thứ tự lật sách cho đúng</div>
    <div class="list3">
      <div class="it" id="i1"><b>1</b> Bìa, tựa sách và lời giới thiệu</div>
      <div class="it" id="i2"><b>2</b> Mục lục — cả quyển sách trên một trang</div>
      <div class="it" id="i3"><b>3</b> Tiêu đề từng chương, đọc liền một mạch</div>
    </div>
    <div class="note">Ba bước này mất khoảng năm phút, và bạn biết ngay sách nói về cái gì.</div>"""),
   scene("""
    <div class="kicker">Vì sao lại hiệu quả</div>
    <h1 style="font-size:76px">Phần thân sách chỉ để<br><span class="hl">chứng minh</span> điều tiêu đề đã nói</h1>
    <div class="sub">Nên khi đã nắm tiêu đề, bạn đọc phần thân nhanh hơn hẳn — vì biết mình đang đọc để làm gì.</div>"""),
   scene(CTA),
 ],
 "anim": [
   "",
   """function(t, el){
     const a = ease(span(t, 6.6, 7.8)), b = ease(span(t, 8.4, 9.6));
     el.querySelector('#t1').style.opacity = a; el.querySelector('#t2').style.opacity = a*0.9;
     ['b1','b2','b3','b4','b5'].forEach(function(k, i){
       el.querySelector('#'+k).style.opacity = b*(0.35 + (i%2)*0.1);
     });
     el.querySelector('#tt1').style.opacity = a; el.querySelector('#tt2').style.opacity = b;
   }""",
   """function(t, el){ [1,2,3].forEach(function(k){ el.querySelector('#i'+k).style.opacity = ease(span(t,16.6+(k-1)*0.9, 17.5+(k-1)*0.9)); }); }""",
   "",
   "",
 ],
 "narration": [
   (0, "Tiêu đề chương là bản tóm tắt tác giả viết sẵn."),
   (1, "Nhìn một trang sách từ xa: những dòng tiêu đề đậm, phần chữ nhỏ bên dưới là chứng minh."),
   (2, "Thứ tự đúng: bìa và lời giới thiệu, rồi mục lục, rồi tiêu đề từng chương đọc liền một mạch."),
   (3, "Ba bước này mất khoảng năm phút, và bạn biết ngay quyển sách nói về cái gì."),
   (4, "Đó là bước chọn sách trong khoá Đọc hiệu quả Speed Reading."),
 ],
}

# ---------------------------------------------------------------- TẬP 14 — B5: bản đồ 4 lớp
EP14 = {
 "slug": "14_ban-do-4-lop", "total": 45.0, "ten": "Bản đồ 4 lớp của một chương",
 "scenes": [(0,5.0),(5.0,15.0),(15.0,26.0),(26.0,36.0),(36.0,45.0)],
 "html": [
   scene("""
    <div class="kicker">Một quyển sách có bốn lớp</div>
    <h1>Đa số người đọc<br>chỉ chạm <span class="bad">lớp cuối</span></h1>
    <div class="sub">Đọc mãi không nắm được sách nói gì, thường là vì bắt đầu từ lớp khó nhất.</div>"""),
   scene("""
    <div class="kicker">Bốn lớp, từ ngoài vào trong</div>
    <div class="cards">
      <div class="crd" id="c1"><div class="idx">1</div><div class="txt"><b>Bìa, tựa và lời giới thiệu</b><span>tác giả nói trước quyển này để làm gì</span></div></div>
      <div class="crd" id="c2"><div class="idx">2</div><div class="txt"><b>Mục lục</b><span>cả quyển sách trên một trang</span></div></div>
      <div class="crd" id="c3"><div class="idx">3</div><div class="txt"><b>Tiêu đề từng chương</b><span>câu trả lời đã nằm ở đây</span></div></div>
      <div class="crd" id="c4"><div class="idx">4</div><div class="txt"><b>Chi tiết trong chương</b><span>chỉ đọc ở chỗ bạn thật sự cần</span></div></div>
    </div>"""),
   scene("""
    <div class="kicker">Cách dùng bốn lớp này</div>
    <div class="list3">
      <div class="it" id="i1"><b>1</b> Ba lớp đầu để quyết định: sách này có ích với mình không</div>
      <div class="it" id="i2"><b>2</b> Lớp bốn chỉ đọc ở phần bạn cần dùng ngay</div>
      <div class="it" id="i3"><b>3</b> Phần đã hiểu rồi thì bỏ qua, không đọc lại</div>
    </div>"""),
   scene("""
    <div class="kicker">Kết quả</div>
    <h1 style="font-size:78px">Mười phút là biết<br><span class="hl">sách có ích hay không</span></h1>
    <div class="sub">Thay vì đọc hai trăm trang rồi mới tiếc thời gian.</div>"""),
   scene(CTA),
 ],
 "anim": [
   "",
   """function(t, el){ [1,2,3,4].forEach(function(k){ el.querySelector('#c'+k).style.opacity = ease(span(t, 6.4+(k-1)*1.5, 7.4+(k-1)*1.5)); }); }""",
   """function(t, el){ [1,2,3].forEach(function(k){ el.querySelector('#i'+k).style.opacity = ease(span(t,16.8+(k-1)*0.9, 17.7+(k-1)*0.9)); }); }""",
   "",
   "",
 ],
 "narration": [
   (0, "Sách có bốn lớp. Đa số chỉ chạm lớp cuối."),
   (1, "Bốn lớp từ ngoài vào: bìa và lời giới thiệu, mục lục, tiêu đề từng chương, rồi mới tới chi tiết."),
   (2, "Ba lớp đầu để quyết định. Lớp bốn chỉ đọc ở phần bạn cần dùng ngay."),
   (3, "Mười phút là biết sách có ích hay không, thay vì đọc hai trăm trang rồi mới tiếc."),
   (4, "Đây là cách chọn sách tôi dạy trong buổi thứ hai của khoá."),
 ],
}

# ---------------------------------------------------------------- TẬP 15 — A7: đọc nhanh khác đọc lướt
EP15 = {
 "slug": "15_doc-nhanh-vs-doc-luot", "total": 45.0, "ten": "Đọc nhanh khác đọc lướt",
 "scenes": [(0,5.0),(5.0,15.0),(15.0,26.0),(26.0,36.0),(36.0,45.0)],
 "html": [
   scene("""
    <div class="kicker">Hai cách đọc rất dễ lẫn</div>
    <h1>Đọc nhanh <span class="hl">không phải</span><br>là đọc lướt</h1>
    <div class="sub">Cùng nhanh như nhau, nhưng một cách giữ được ý, một cách làm mất ý.</div>"""),
   scene("""
    <div class="kicker">Khác nhau ở chỗ giữ ý</div>
    <div class="versus">
      <div class="vs"><div class="nm">Đọc lướt</div><div class="meter"><i class="m2" id="v1"></i></div>
        <div class="note" id="n1">Bỏ sót ý chính, đọc xong không kể lại được</div></div>
      <div class="vs"><div class="nm">Đọc nhanh có phương pháp</div><div class="meter"><i id="v2"></i></div>
        <div class="note" id="n2">Giữ nguyên ý, chỉ tăng tốc độ</div></div>
    </div>"""),
   scene("""
    <div class="kicker">Phép thử ba mươi giây</div>
    <div class="list3">
      <div class="it" id="i1"><b>1</b> Đọc xong, gấp sách lại và kể ba ý chính</div>
      <div class="it" id="i2"><b>2</b> Không kể được là bạn chỉ đang lướt</div>
      <div class="it" id="i3"><b>3</b> Kể được mà nhanh hơn — đó mới là đọc nhanh</div>
    </div>"""),
   scene("""
    <div class="kicker">Quy tắc để tự kiểm</div>
    <h1 style="font-size:78px">Nhanh hơn mà<br><span class="hl">hiểu như cũ</span></h1>
    <div class="sub">Hễ hiểu giảm là bạn đã đọc lướt. Nhanh hơn mà mất ý thì không phải đọc nhanh, chỉ là đọc ẩu.</div>"""),
   scene(CTA),
 ],
 "anim": [
   "",
   """function(t, el){
     const a = ease(span(t, 6.6, 8.6)), b = ease(span(t, 7.4, 9.4));
     el.querySelector('#v1').style.width = (a*30)+'%';
     el.querySelector('#v2').style.width = (b*100)+'%';
     el.querySelector('#n1').style.opacity = 0.5 + a*0.5;
     el.querySelector('#n2').style.opacity = 0.5 + b*0.5;
   }""",
   """function(t, el){ [1,2,3].forEach(function(k){ el.querySelector('#i'+k).style.opacity = ease(span(t,16.8+(k-1)*0.9, 17.7+(k-1)*0.9)); }); }""",
   "",
   "",
 ],
 "narration": [
   (0, "Đọc nhanh không phải đọc lướt."),
   (1, "Đọc lướt thì bỏ sót ý chính. Đọc nhanh có phương pháp thì giữ nguyên ý, chỉ tăng tốc độ."),
   (2, "Phép thử: đọc xong, gấp sách lại và kể ba ý chính. Không kể được là bạn đang lướt."),
   (3, "Quy tắc tự kiểm rất đơn giản: nhanh hơn mà hiểu như cũ. Hễ hiểu giảm là đã lướt."),
   (4, "Phân biệt được hai cách này là điều kiện đầu tiên để luyện đọc nhanh."),
 ],
}

# ---------------------------------------------------------------- TẬP 16 — B7: năm câu hỏi trước khi mở sách
EP16 = {
 "slug": "16_nam-cau-hoi", "total": 45.0, "ten": "Năm câu hỏi trước khi mở sách",
 "scenes": [(0,5.0),(5.0,15.0),(15.0,26.0),(26.0,36.0),(36.0,45.0)],
 "html": [
   scene("""
    <div class="kicker">Trước khi mở sách</div>
    <h1>Năm câu hỏi<br><span class="hl">quyết định cách đọc</span></h1>
    <div class="sub">Đọc mà không có câu hỏi thì não không biết phải giữ lại cái gì.</div>"""),
   scene("""
    <div class="kicker">Hỏi năm câu này trước</div>
    <div class="list20">
      <div class="it" id="i1"><b>1</b> Tôi cần gì ở quyển sách này?</div>
      <div class="it" id="i2"><b>2</b> Tác giả là ai, viết cho ai đọc?</div>
      <div class="it" id="i3"><b>3</b> Quyển này trả lời câu hỏi nào?</div>
      <div class="it" id="i4"><b>4</b> Chỗ nào tôi phải đọc kỹ?</div>
      <div class="it" id="i5"><b>5</b> Chỗ nào tôi bỏ qua được?</div>
    </div>"""),
   scene("""
    <div class="kicker">Làm thế nào cho nhanh</div>
    <h1 style="font-size:74px">Ghi năm câu ra giấy,<br>rồi đọc để <span class="hl">tìm câu trả lời</span></h1>
    <div class="sub">Không cần viết dài. Mỗi câu một dòng, mất chưa tới hai phút.</div>"""),
   scene("""
    <div class="kicker">Vì sao lại hiệu quả</div>
    <h1 style="font-size:78px">Não giữ lại thứ<br>nó đang <span class="hl">đi tìm</span></h1>
    <div class="sub">Đọc có câu hỏi thì đọc xong bạn còn nhớ. Đọc không mục đích thì đọc xong là hết.</div>"""),
   scene(CTA),
 ],
 "anim": [
   "",
   """function(t, el){ [1,2,3,4,5].forEach(function(k){ el.querySelector('#i'+k).style.opacity = ease(span(t, 6.3+(k-1)*0.75, 7.1+(k-1)*0.75)); }); }""",
   "",
   "",
   "",
 ],
 "narration": [
   (0, "Đọc mà không có câu hỏi thì não không biết phải giữ lại cái gì."),
   (1, "Năm câu hỏi trước khi mở sách: tôi cần gì, tác giả là ai, sách trả lời câu hỏi nào, chỗ nào đọc kỹ, chỗ nào bỏ qua."),
   (2, "Ghi năm câu đó ra giấy rồi đọc để tìm câu trả lời. Mỗi câu một dòng, mất chưa tới hai phút."),
   (3, "Não giữ lại thứ nó đang đi tìm. Đọc có câu hỏi thì đọc xong bạn còn nhớ."),
   (4, "Cách đặt câu hỏi này tôi dạy ngay buổi đầu của khoá."),
 ],
}

# ---------------------------------------------------------------- TẬP 17 — B8: ghi chép đúng
EP17 = {
 "slug": "17_ghi-chep-dung", "total": 45.0, "ten": "Ghi chép đúng cách",
 "scenes": [(0,5.0),(5.0,15.0),(15.0,26.0),(26.0,36.0),(36.0,45.0)],
 "html": [
   scene("""
    <div class="kicker">Ghi chép</div>
    <h1>Ghi cả trang —<br>mà <span class="bad">không nhớ gì</span></h1>
    <div class="sub">Vì não không nhớ chữ. Não nhớ cấu trúc của bài.</div>"""),
   scene("""
    <div class="kicker">Hai kiểu trang vở</div>
    <div class="versus">
      <div class="vs"><div class="nm">Ghi chi tiết</div><div class="meter"><i class="m2" id="v1"></i></div>
        <div class="note">Mười lăm dòng chữ nhỏ. Đọc lại cũng không nhớ.</div></div>
      <div class="vs"><div class="nm">Ghi tiêu đề</div><div class="meter"><i id="v2"></i></div>
        <div class="note">Ba dòng lớn. Liếc một lần là nhớ cả bài.</div></div>
    </div>"""),
   scene("""
    <div class="kicker">Ba nguyên tắc ghi chép</div>
    <div class="list3">
      <div class="it" id="i1"><b>1</b> Chỉ ghi tiêu đề và ý chính, không ghi lời giảng</div>
      <div class="it" id="i2"><b>2</b> Mỗi ý một dòng, chừa khoảng trống bên dưới</div>
      <div class="it" id="i3"><b>3</b> Chỗ chưa hiểu thì đánh dấu, đừng chép lại</div>
    </div>"""),
   scene("""
    <div class="kicker">Vì sao lại nhớ hơn</div>
    <h1 style="font-size:78px">Não nhớ <span class="hl">cấu trúc</span>,<br>không nhớ chữ</h1>
    <div class="sub">Một trang ba dòng lớn dễ nhớ hơn một trang đầy chữ — vì bạn nhìn thấy hình dạng của cả bài.</div>"""),
   scene(CTA),
 ],
 "anim": [
   "",
   """function(t, el){
     const a = ease(span(t, 6.6, 8.6)), b = ease(span(t, 7.4, 9.4));
     el.querySelector('#v1').style.width = (a*100)+'%';
     el.querySelector('#v2').style.width = (b*25)+'%';
   }""",
   """function(t, el){ [1,2,3].forEach(function(k){ el.querySelector('#i'+k).style.opacity = ease(span(t,16.7+(k-1)*0.9, 17.6+(k-1)*0.9)); }); }""",
   "",
   "",
 ],
 "narration": [
   (0, "Ghi cả trang mà không nhớ gì — vì não không nhớ chữ."),
   (1, "Trang ghi chi tiết có mười lăm dòng chữ nhỏ. Trang ghi tiêu đề chỉ ba dòng lớn, mà liếc một lần là nhớ."),
   (2, "Ba nguyên tắc: chỉ ghi tiêu đề và ý chính, mỗi ý một dòng, và đánh dấu chỗ chưa hiểu thay vì chép lại."),
   (3, "Não nhớ cấu trúc, không nhớ chữ. Một trang ba dòng lớn dễ nhớ hơn một trang đầy chữ."),
   (4, "Đây là cách ghi chép trong buổi thứ tư của khoá."),
 ],
}

# ---------------------------------------------------------------- TẬP 18 — B9: sơ đồ một trang
EP18 = {
 "slug": "18_so-do-1-trang", "total": 45.0, "ten": "Sơ đồ một trang cho một quyển sách",
 "scenes": [(0,5.0),(5.0,15.0),(15.0,26.0),(26.0,36.0),(36.0,45.0)],
 "html": [
   scene("""
    <div class="kicker">Một trang cho cả quyển sách</div>
    <h1>Đọc xong,<br>đọng lại <span class="hl">một trang</span></h1>
    <div class="sub">Không phải tóm tắt dài. Là một trang bạn tự vẽ, nhìn phát là nhớ cả quyển.</div>"""),
   scene("""
    <div class="kicker">Một trang gồm những gì</div>
    <div class="badge"><span class="t">Chủ đề chính</span><span class="v">một câu</span></div>
    <div class="cards">
      <div class="crd" id="c1"><div class="idx">1</div><div class="txt"><b>Bốn ý lớn nhất</b><span>mỗi ý một dòng</span></div></div>
      <div class="crd" id="c2"><div class="idx">2</div><div class="txt"><b>Ví dụ đáng nhớ</b><span>thứ bạn kể lại được cho người khác</span></div></div>
      <div class="crd" id="c3"><div class="idx">3</div><div class="txt"><b>Việc áp dụng được</b><span>làm ngay trong tuần này</span></div></div>
      <div class="crd" id="c4"><div class="idx">4</div><div class="txt"><b>Chỗ còn chưa hiểu</b><span>để lần sau đọc lại đúng đó</span></div></div>
    </div>"""),
   scene("""
    <div class="kicker">Cách làm, mỗi chương một nhánh</div>
    <div class="list3">
      <div class="it" id="i1"><b>1</b> Đọc xong chương nào, thêm nhánh cho chương đó</div>
      <div class="it" id="i2"><b>2</b> Nhánh nào quên thì mở lại đúng chỗ đó, không đọc lại cả sách</div>
      <div class="it" id="i3"><b>3</b> Hết sách, bạn có một trang nhìn là nhớ cả quyển</div>
    </div>"""),
   scene("""
    <div class="kicker">Lợi ích thật</div>
    <h1 style="font-size:74px">Nhìn lại một trang<br>nhanh hơn <span class="hl">đọc lại hai trăm trang</span></h1>
    <div class="sub">Và lần ôn nào cũng bắt đầu từ đúng chỗ bạn còn yếu.</div>"""),
   scene(CTA),
 ],
 "anim": [
   "",
   """function(t, el){ [1,2,3,4].forEach(function(k){ el.querySelector('#c'+k).style.opacity = ease(span(t, 6.3+(k-1)*1.4, 7.3+(k-1)*1.4)); }); }""",
   """function(t, el){ [1,2,3].forEach(function(k){ el.querySelector('#i'+k).style.opacity = ease(span(t,16.8+(k-1)*0.9, 17.7+(k-1)*0.9)); }); }""",
   "",
   "",
 ],
 "narration": [
   (0, "Đọc xong cả quyển, thứ đọng lại chỉ cần một trang giấy."),
   (1, "Một trang gồm: chủ đề chính trong một câu, bốn ý lớn nhất, ví dụ đáng nhớ, việc áp dụng được, và chỗ còn chưa hiểu."),
   (2, "Đọc xong chương nào thì thêm nhánh cho chương đó. Nhánh nào quên thì mở lại đúng chỗ đó."),
   (3, "Nhìn lại một trang nhanh hơn đọc lại hai trăm trang, và lần ôn nào cũng vào đúng chỗ bạn còn yếu."),
   (4, "Đây là bước cuối của mỗi buổi học trong khoá."),
 ],
}

# ---------------------------------------------------------------- TẬP 19 — B10: lịch ôn 1-3-6
EP19 = {
 "slug": "19_lich-on-1-3-6", "total": 45.0, "ten": "Lịch ôn ngày 1-3-6",
 "scenes": [(0,5.0),(5.0,15.0),(15.0,26.0),(26.0,36.0),(36.0,45.0)],
 "html": [
   scene("""
    <div class="kicker">Ôn đúng lúc</div>
    <h1>Không ôn thì một ngày<br>mất <span class="bad">một nửa</span></h1>
    <div class="sub">Và phần còn lại rơi tiếp mỗi ngày. Đây là quy luật của trí nhớ, không phải bạn kém.</div>"""),
   scene("""
    <div class="kicker">Nếu không ôn lại lần nào</div>
    <div class="chart" id="c1">
      <div class="col"><div class="num" id="a0">0%</div><div class="bar" id="b0"></div><div class="lab">vừa học</div></div>
      <div class="col"><div class="num" id="a1">0%</div><div class="bar red" id="b1"></div><div class="lab">1 ngày</div></div>
      <div class="col"><div class="num" id="a3">0%</div><div class="bar red" id="b3"></div><div class="lab">3 ngày</div></div>
      <div class="col"><div class="num" id="a6">0%</div><div class="bar red" id="b6"></div><div class="lab">6 ngày</div></div>
    </div>"""),
   scene("""
    <div class="kicker">Nếu ôn vào ngày 1, ngày 3 và ngày 6</div>
    <div class="chart" id="c2">
      <div class="col"><div class="num">100%</div><div class="bar" style="height:100%"></div><div class="lab">vừa học</div></div>
      <div class="col"><div class="num" id="d1">0%</div><div class="bar" id="e1"></div><div class="lab">ngày 1</div></div>
      <div class="col"><div class="num" id="d3">0%</div><div class="bar" id="e3"></div><div class="lab">ngày 3</div></div>
      <div class="col"><div class="num" id="d6">0%</div><div class="bar" id="e6"></div><div class="lab">ngày 6</div></div>
    </div>
    <div class="note">Mỗi lần ôn chỉ năm phút, không phải học lại từ đầu.</div>"""),
   scene("""
    <div class="kicker">Ba mốc cần nhớ</div>
    <h1 style="font-size:80px">Ngày <span class="hl">1</span> · ngày <span class="hl">3</span> · ngày <span class="hl">6</span></h1>
    <div class="sub">Đúng ba lần đó là đủ chặn đường rơi của trí nhớ. Sau đó bạn nhớ dài hạn.</div>"""),
   scene(CTA),
 ],
 "anim": [
   "",
   """function(t, el){
     const s = [[7.0,100,'a0','b0'], [8.2,50,'a1','b1'], [9.4,37,'a3','b3'], [10.6,18,'a6','b6']];
     s.forEach(function(x){
       const p = ease(span(t, x[0], x[0]+1.6));
       el.querySelector('#'+x[3]).style.height = (p*x[1])+'%';
       el.querySelector('#'+x[2]).textContent = Math.round(p*x[1])+'%';
     });
   }""",
   """function(t, el){
     const s = [[17.0,95,'d1','e1'], [18.6,92,'d3','e3'], [20.2,90,'d6','e6']];
     s.forEach(function(x){
       const p = ease(span(t, x[0], x[0]+1.6));
       el.querySelector('#'+x[3]).style.height = (p*x[1])+'%';
       el.querySelector('#'+x[2]).textContent = Math.round(p*x[1])+'%';
     });
   }""",
   "",
   "",
 ],
 "narration": [
   (0, "Không ôn thì sau một ngày bạn mất một nửa."),
   (1, "Vừa học một trăm phần trăm. Một ngày còn năm mươi. Ba ngày ba mươi bảy. Sáu ngày mười tám."),
   (2, "Nếu ôn vào ngày một, ngày ba và ngày sáu, mức nhớ giữ ở chín mươi phần trăm trở lên."),
   (3, "Ba mốc đó là đủ để chặn đường rơi của trí nhớ. Mỗi lần chỉ năm phút."),
   (4, "Lịch ôn này tôi dạy kèm theo từng buổi học."),
 ],
}

# ---------------------------------------------------------------- TẬP 20 — C1: tựa sách đánh lừa
EP20 = {
 "slug": "20_tua-sach-danh-lua", "total": 45.0, "ten": "Tựa sách chưa chắc đúng nội dung",
 "scenes": [(0,5.0),(5.0,15.0),(15.0,26.0),(26.0,36.0),(36.0,45.0)],
 "html": [
   scene("""
    <div class="kicker">Chọn sách</div>
    <h1>Tựa sách hấp dẫn<br>chưa chắc <span class="bad">đúng nội dung</span></h1>
    <div class="sub">Tựa được viết để bán sách. Mục lục mới là thứ nói quyển sách có gì.</div>"""),
   scene("""
    <div class="kicker">Hai quyển trên cùng một kệ</div>
    <div class="versus">
      <div class="vs"><div class="nm">Quyển tựa hay</div><div class="meter"><i class="m2" id="v1"></i></div>
        <div class="note">Mục lục chung chung. Đọc xong không dùng được gì.</div></div>
      <div class="vs"><div class="nm">Quyển tựa thường</div><div class="meter"><i id="v2"></i></div>
        <div class="note">Ba chương nói đúng việc bạn đang cần làm.</div></div>
    </div>"""),
   scene("""
    <div class="kicker">Ba bước trước khi trả tiền</div>
    <div class="list3">
      <div class="it" id="i1"><b>1</b> Đọc mục lục trước khi tin tựa sách</div>
      <div class="it" id="i2"><b>2</b> Đếm số chương nói về việc bạn đang cần</div>
      <div class="it" id="i3"><b>3</b> Chỉ mua khi có ít nhất hai chương đúng nhu cầu</div>
    </div>"""),
   scene("""
    <div class="kicker">Đổi cách chọn là đổi cả tủ sách</div>
    <h1 style="font-size:74px">Hai chương đúng việc<br><span class="hl">đáng hơn</span> mười chương nghe hay</h1>
    <div class="sub">Một quyển dùng được hai chương vẫn hơn mười quyển đọc xong để đó.</div>"""),
   scene(CTA),
 ],
 "anim": [
   "",
   """function(t, el){
     const a = ease(span(t, 6.6, 8.6)), b = ease(span(t, 7.4, 9.4));
     el.querySelector('#v1').style.width = (a*30)+'%';
     el.querySelector('#v2').style.width = (b*100)+'%';
   }""",
   """function(t, el){ [1,2,3].forEach(function(k){ el.querySelector('#i'+k).style.opacity = ease(span(t,16.8+(k-1)*0.9, 17.7+(k-1)*0.9)); }); }""",
   "",
   "",
 ],
 "narration": [
   (0, "Tựa sách được viết để bán sách, không phải để nói đúng nội dung."),
   (1, "Hai quyển cùng một kệ: một quyển tựa rất hay nhưng mục lục chung chung, một quyển tựa thường mà có ba chương đúng việc bạn cần."),
   (2, "Ba bước trước khi trả tiền: đọc mục lục, đếm số chương đúng nhu cầu, và chỉ mua khi có ít nhất hai chương."),
   (3, "Một quyển dùng được hai chương vẫn hơn mười quyển đọc xong để đó."),
   (4, "Đây là cách chọn sách trong buổi thứ hai của khoá."),
 ],
}

# ---------------------------------------------------------------- TẬP 21 — B6: lướt có cấu trúc
EP21 = {
 "slug": "21_skim-co-cau-truc", "total": 45.0, "ten": "Lướt có cấu trúc: 300 trang trong 15 phút",
 "phong_cach": "do-trang",
 "scenes": [(0,8.0),(8.0,22.0),(22.0,31.0),(31.0,38.5),(38.5,45.0)],
 "html": [
   scene("""
    <div class="kicker">Đọc lướt có cấu trúc</div>
    <h1>Ba trăm trang<br>trong <span class="hl">mười lăm phút</span></h1>
    <div class="sub">Không phải đọc hết. Là biết <b>chỗ nào đáng đọc trước</b>.</div>"""),
   scene("""
    <div class="kicker">Bốn lớp để lướt</div>
    <div class="list20">
      <div class="it"><b>1</b>Bìa và mục lục — sách nói về việc gì</div>
      <div class="it"><b>2</b>Tiêu đề chương — bản đồ cuốn sách</div>
      <div class="it"><b>3</b>Câu đầu, câu cuối mỗi đoạn — ý chính</div>
      <div class="it"><b>4</b>Bảng biểu và chữ in đậm — chỗ tác giả nhấn</div>
    </div>"""),
   scene("""
    <div class="kicker">Lượt một: lướt hết để đánh dấu</div>
    <div class="race">
      <div class="row"><div class="name"><b>Trang đã lướt qua</b><span class="val" id="e1v">0 trang</span></div>
        <div class="track"><i class="fill" id="e1f"></i></div></div>
      <div class="row"><div class="name"><b>Trang cần đọc kỹ</b><span class="val" id="e2v">0 trang</span></div>
        <div class="track"><i class="fill red" id="e2f"></i></div></div>
    </div>
    <div class="badge"><span class="t">Chỉ khoảng một phần năm</span><span class="v">20%</span></div>"""),
   scene("""
    <div class="kicker">Ba lượt, ba mục đích</div>
    <div class="chart" id="c1">
      <div class="col"><div class="num" id="n1">0 phút</div><div class="bar" id="b1"></div><div class="lab">mục lục<br>và tiêu đề</div></div>
      <div class="col"><div class="num" id="n2">0 phút</div><div class="bar" id="b2"></div><div class="lab">câu đầu<br>câu cuối</div></div>
      <div class="col"><div class="num" id="n3">0 phút</div><div class="bar" id="b3"></div><div class="lab">phần<br>đọc kỹ</div></div>
    </div>
    <div class="note">Mười lăm phút cho ba trăm trang — nhờ chọn chỗ đọc, không phải đọc nhanh hơn.</div>"""),
   scene(CTA),
 ],
 "anim": [
   "",
   """function(t, el){
     const t0 = [9.0, 10.5, 12.0, 13.5];
     el.querySelectorAll('.list20 .it').forEach(function(x, k){
       x.style.opacity = ease(span(t, t0[k], t0[k] + 0.6)).toFixed(3);
     });
   }""",
   """function(t, el){
     const p1 = ease(span(t, 23.3, 26.3)), p2 = ease(span(t, 27.2, 29.6));
     el.querySelector('#e1f').style.width = (p1 * 100) + '%';
     el.querySelector('#e2f').style.width = (p2 * 20) + '%';
     el.querySelector('#e1v').textContent = Math.round(p1 * 300) + ' trang';
     el.querySelector('#e2v').textContent = Math.round(p2 * 60) + ' trang';
   }""",
   """function(t, el){
     const s = [[32.4, 25, 2, 'n1', 'b1'], [33.5, 62, 5, 'n2', 'b2'], [34.6, 100, 8, 'n3', 'b3']];
     s.forEach(function(x){
       const p = ease(span(t, x[0], x[0] + 1.3));
       el.querySelector('#' + x[4]).style.height = (p * x[1]) + '%';
       el.querySelector('#' + x[3]).textContent = Math.round(p * x[2]) + ' phút';
     });
   }""",
   "",
 ],
 "narration": [
   (0, "Ba trăm trang trong mười lăm phút. Không phải đọc hết, mà là biết chỗ nào đáng đọc trước."),
   (1, "Bốn lớp để lướt. Bìa và mục lục cho biết sách nói về gì. Tiêu đề chương là bản đồ cuốn sách. Câu đầu và câu cuối mỗi đoạn chứa ý chính. Chữ in đậm là chỗ tác giả nhấn."),
   (2, "Lượt một bạn lướt hết ba trăm trang để đánh dấu. Chỉ khoảng hai mươi phần trăm là chỗ đọc kỹ."),
   (3, "Ba lượt: hai phút cho mục lục và tiêu đề, năm phút cho câu đầu câu cuối, tám phút cho phần đáng đọc."),
   (4, "Cách lướt này tôi dạy kèm trong từng buổi học."),
 ],
}

# ------------------------------------------------- ĐỊNH DẠNG CHUẨN TỪ TẬP 23 TRỞ ĐI
# Sáu phần bắt buộc, theo đúng thứ tự (cổng kiem-tra-kich-ban.py chặn nếu thiếu):
#   1. hook     — câu mở gợi tò mò, nói trúng việc người xem đang gặp
#   2. gia_tri  — biết nội dung này thì được gì (lợi ích cụ thể, đo được)
#   3. hieu_biet— cơ chế mới: vì sao lại như vậy (phần "hiểu biết mới")
#   4. lam_gi   — việc cần làm, thành bước, làm được ngay
#   5. thong_diep — một câu chốt để nhớ
#   6. ket_khoa — giới thiệu khoá 7 buổi Zoom + thẻ kết thúc trỏ speedreading.vn/sp-online
# Mỗi tập mới phải khai "cau_truc": CAU_TRUC_CHUAN (kiểm tự động), dài ≥ 110 giây,
# tối thiểu 9 cảnh, cảnh cuối là CTA. Tập 01–22 giữ nguyên định dạng cũ đã đăng.
CAU_TRUC_CHUAN = ["hook", "gia_tri", "hieu_biet", "lam_gi", "thong_diep", "ket_khoa"]

# ---------------------------------------------------------------- TẬP 23 — E4: 7 bước đọc giáo trình
EP23 = {
 "slug": "23_hoc-sinh-7-buoc-doc-giao-trinh",
 "total": 152.0,
 "ten": "Học sinh: 7 bước đọc giáo trình để thuộc bài",
 "cau_truc": CAU_TRUC_CHUAN,
 "phong_cach": "do-trang",
 "scenes": [(0,9.0),(9.0,19.0),(19.0,30.0),(30.0,47.0),(47.0,63.0),
            (63.0,77.0),(77.0,94.0),(94.0,111.0),(111.0,126.0),(126.0,144.0),(144.0,152.0)],
 "html": [
   # 1. hook
   scene("""
    <div class="kicker">Học sinh · mùa thi</div>
    <h1>Đọc lại ba lần<br>vẫn <span class="hl">quên sạch</span></h1>
    <div class="sub">Không phải bạn kém trí nhớ — <b>cách đọc chưa đúng</b>.</div>"""),
   # 1. hook (nỗi đau cụ thể)
   scene("""
    <div class="kicker">Điều ai cũng gặp</div>
    <div class="list3">
      <div class="it"><b>Đọc lại ba lần</b> — gấp sách là quên</div>
      <div class="it"><b>Hai tiếng liền một chỗ</b> — nhớ ít hơn bốn lượt ngắn</div>
      <div class="it"><b>Vào phòng thi</b> — không kể lại được gì</div>
    </div>"""),
   # 2. giá trị
   scene("""
    <div class="kicker">Bảy bước này cho bạn gì</div>
    <div class="list20">
      <div class="it"><b>1</b>Một chương giáo trình: nắm trong khoảng 15 phút</div>
      <div class="it"><b>2</b>Nhớ tới ngày thi — không phải đọc lại lần hai</div>
      <div class="it"><b>3</b>Biết ngay chỗ mình chưa nhớ, trong lúc đang đọc</div>
    </div>
    <div class="note">Bảy bước · một lượt đọc · không thức trắng.</div>"""),
   # 3. hiểu biết mới — nhận ra khác nhớ lại
   scene("""
    <div class="kicker">Đọc lại và làm bài là hai việc khác nhau</div>
    <div class="versus">
      <div class="vs"><b style="font-size:52px">NHẬN RA</b>
        <div class="note">Thấy mặt chữ là thấy quen. Đọc lại luyện việc này.</div></div>
      <div class="vs"><b style="font-size:52px">NHỚ LẠI</b>
        <div class="note">Không có chữ mà vẫn kể được. Đề thi hỏi việc này.</div></div>
    </div>
    <div class="sub">Đọc lại luyện một đằng, đề thi hỏi một nẻo.</div>"""),
   # 3. hiểu biết mới — vì sao phải gọi lại theo mốc
   scene("""
    <div class="kicker">Vì sao phải gọi lại theo mốc</div>
    <div class="race">
      <div class="row"><div class="name"><b>Không gọi lại</b><span class="val" id="q1v">tụt nhanh theo ngày</span></div>
        <div class="track"><i class="fill" id="q1f"></i></div></div>
      <div class="row"><div class="name"><b>Gọi lại ở mốc 1–3–6 ngày</b><span class="val" id="q2v">giữ được mức cao</span></div>
        <div class="track"><i class="fill red" id="q2f"></i></div></div>
    </div>
    <div class="note">Hình minh hoạ. Mỗi mốc năm phút, bằng cách tự kể lại — không phải đọc lại.</div>"""),
   # 3. hiểu biết mới — hai cái bẫy
   scene("""
    <div class="kicker">Hai cái bẫy nữa</div>
    <div class="list3">
      <div class="it"><b>Đọc liền hai tiếng</b> — não chỉ giữ liền mạch 5–10 phút</div>
      <div class="it"><b>Chép nguyên câu vào vở</b> — đang chép, không đang nhớ</div>
    </div>"""),
   # 4. việc cần làm — bước 1–4
   scene("""
    <div class="kicker">Bước 1–4 · đọc để hiểu</div>
    <div class="list20">
      <div class="it"><b>1</b>Lướt chương ba phút: tiêu đề, câu đầu, câu cuối</div>
      <div class="it"><b>2</b>Đọc câu hỏi cuối chương trước khi vào thân bài</div>
      <div class="it"><b>3</b>Đọc chậm một lượt, mỗi đoạn gạch một từ khoá</div>
      <div class="it"><b>4</b>Gấp sách, tự trả lời từng câu hỏi cuối chương</div>
    </div>"""),
   # 4. việc cần làm — bước 5–7
   scene("""
    <div class="kicker">Bước 5–7 · đọc để nhớ</div>
    <div class="list20">
      <div class="it"><b>5</b>Chỗ nào không kể được → mở đúng chỗ đó, đọc lại một lần</div>
      <div class="it"><b>6</b>Sơ đồ một trang cho chương — chỉ ghi từ khoá</div>
      <div class="it"><b>7</b>Ôn ở mốc 1–3–6 ngày, mỗi lần năm phút</div>
    </div>"""),
   # 5. thông điệp
   scene("""
    <div class="kicker">Thông điệp</div>
    <h1>Đọc để nhớ là<br>một <span class="hl">quy trình</span></h1>
    <div class="sub">Một lượt đọc đúng quy trình thay cho ba lượt đọc lại.</div>"""),
   # 6. giới thiệu khoá 7 buổi
   scene("""
    <div class="kicker">Khoá đọc hiệu quả · 7 buổi Zoom</div>
    <div class="list20">
      <div class="it"><b>1</b>Buổi đầu: luyện mắt theo kỹ thuật 3-2-1</div>
      <div class="it"><b>2</b>Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm</div>
      <div class="it"><b>3</b>Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc</div>
    </div>
    <div class="note">Sửa lỗi ngay trong buổi · hỗ trợ Zalo 1:1 · 980.000đ · hoàn phí sau buổi 1 nếu không hợp.</div>"""),
   scene(CTA),
 ],
 "anim": [
   "",
   """function(t, el){
     const t0 = [10.0, 11.6, 13.2];
     el.querySelectorAll('.list3 .it').forEach(function(x, k){
       x.style.opacity = ease(span(t, t0[k], t0[k] + 0.7)).toFixed(3);
     });
   }""",
   """function(t, el){
     const t0 = [20.4, 22.4, 24.4];
     el.querySelectorAll('.list20 .it').forEach(function(x, k){
       x.style.opacity = ease(span(t, t0[k], t0[k] + 0.7)).toFixed(3);
     });
     el.querySelector('.note').style.opacity = ease(span(t, 26.6, 27.6)).toFixed(3);
   }""",
   """function(t, el){
     const p = ease(span(t, 32.0, 34.0));
     el.querySelectorAll('.vs').forEach(function(x, k){
       x.style.opacity = (p * (k ? 1 : 1)).toFixed(3);
       x.style.transform = 'translateY(' + ((1 - p) * 24) + 'px)';
     });
     el.querySelector('.sub').style.opacity = ease(span(t, 42.0, 43.4)).toFixed(3);
   }""",
   """function(t, el){
     const p1 = ease(span(t, 48.6, 54.0));   // không gọi lại: thanh tụt xuống
     const p2 = ease(span(t, 55.0, 60.0));   // gọi lại theo mốc: thanh giữ mức cao
     // Không in con số phần trăm: đây là hình minh hoạ, không phải số đo.
     el.querySelector('#q1f').style.width = (100 - p1 * 84) + '%';
     el.querySelector('#q2f').style.width = (p2 * 94) + '%';
   }""",
   """function(t, el){
     const t0 = [64.0, 66.0];
     el.querySelectorAll('.list3 .it').forEach(function(x, k){
       x.style.opacity = ease(span(t, t0[k], t0[k] + 0.7)).toFixed(3);
     });
   }""",
   """function(t, el){
     const t0 = [78.2, 80.0, 81.8, 83.6];
     el.querySelectorAll('.list20 .it').forEach(function(x, k){
       x.style.opacity = ease(span(t, t0[k], t0[k] + 0.7)).toFixed(3);
     });
   }""",
   """function(t, el){
     const t0 = [95.2, 97.4, 99.6];
     el.querySelectorAll('.list20 .it').forEach(function(x, k){
       x.style.opacity = ease(span(t, t0[k], t0[k] + 0.7)).toFixed(3);
     });
   }""",
   "",
   """function(t, el){
     const t0 = [127.0, 129.6, 132.2];
     el.querySelectorAll('.list20 .it').forEach(function(x, k){
       x.style.opacity = ease(span(t, t0[k], t0[k] + 0.7)).toFixed(3);
     });
     el.querySelector('.note').style.opacity = ease(span(t, 135.0, 136.4)).toFixed(3);
   }""",
   "",
 ],
 "narration": [
   (0, "Bạn đọc lại một chương ba lần, gấp sách, và vẫn quên sạch. Không phải bạn kém trí nhớ."),
   (1, "Ba lần đọc lại vẫn không nhớ. Ngồi hai tiếng liền cho ra ít hơn bốn lượt ngắn. Tới phòng thi, không kể lại được gì."),
   (2, "Bảy bước dưới đây gom thành một quy trình: nắm một chương trong khoảng mười lăm phút, nhớ tới ngày thi, và biết ngay chỗ mình còn chưa nhớ."),
   (3, "Đây là chỗ quan trọng nhất. Đọc lại là việc nhận ra: thấy mặt chữ, thấy quen, não báo mình biết rồi. Làm bài là việc nhớ lại: không có chữ, bạn phải tự kể. Đọc lại luyện việc thứ nhất, đề thi hỏi việc thứ hai."),
   (4, "Trí nhớ rơi theo ngày nếu bạn không gọi lại: sau một tuần, nhiều chương gần như phải đọc từ đầu. Nhưng gọi lại ở ba mốc — một ngày, ba ngày, sáu ngày — thì chương đó ở lại. Mỗi mốc chỉ năm phút."),
   (5, "Hai cái bẫy nữa. Não chỉ giữ liền mạch năm đến mười phút, nên đọc liền hai tiếng thì phần sau không vào. Chép nguyên câu vào vở là đang chép, không phải đang nhớ."),
   (6, "Bước một: lướt chương ba phút — tiêu đề, câu đầu, câu cuối. Bước hai: đọc câu hỏi cuối chương trước khi vào thân bài. Bước ba: đọc chậm một lượt, mỗi đoạn gạch một từ khoá. Bước bốn: gấp sách, tự trả lời từng câu hỏi."),
   (7, "Bước năm: chỗ nào không kể được, mở đúng chỗ đó, đọc lại một lần. Bước sáu: vẽ một sơ đồ một trang cho chương, chỉ ghi từ khoá. Bước bảy: ôn lại ở mốc một, ba, sáu ngày — mỗi lần năm phút, bằng cách tự kể lại."),
   (8, "Thông điệp ở đây: đọc để nhớ là một quy trình, không phải một lần đọc. Một lượt đọc đúng quy trình thay được ba lượt đọc lại — vì não nhớ bằng cách gọi lại, không phải bằng cách nhìn lại."),
   (9, "Bảy bước này là bản rút gọn của quy trình trong khoá. Khoá có bảy buổi Zoom: buổi đầu luyện mắt theo kỹ thuật ba hai một, buổi hai chuyển sang đọc cụm ba đến năm từ, các buổi sau vào quy trình đọc, ghi chép và ôn theo mốc."),
   (10, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ],
}

# ---------------------------------------------------------------- TẬP 22 — bài test tốc độ đọc, bản đầy đủ
# Các tập đứng trước theo đúng thứ tự đăng — văn bản cho bài test lấy từ chính lời đọc của chúng.
_DS_TAP = [EP1, EP2, EP3, EP4, EP5, EP7, EP8, EP9, EP20_11, EP10, EP11, EP12,
           EP13, EP14, EP15, EP16, EP17, EP18, EP19, EP20, EP21]

# Mốc tốc độ của bài test: (từ/phút, số từ hiện mỗi lần, gợi ý dưới thanh chạy)
#
# Ở 24 hình/giây, một từ tại mốc 1.000 từ/phút chỉ có 1,4 khung hình — không ai đọc kịp
# và video chỉ còn là nhấp nháy. Nên mốc càng cao thì mỗi lần hiện càng nhiều từ (đúng
# cách đọc cụm mà khoá dạy), còn số từ mỗi phút vẫn giữ đúng con số ghi trên màn hình.
MOC_TEST = [
    (200,  1, "Chậm hơn tốc độ nói. Ai cũng theo được mốc này."),
    (250,  1, "Đúng tốc độ giọng đọc trong đầu — cái hãm quen thuộc."),
    (300,  2, "Nhanh hơn giọng nói một chút. Nhiều người bắt đầu hụt ở đây."),
    (350,  2, "Nhịp đã gấp rưỡi tốc độ nói, nhưng vẫn đều."),
    (400,  2, "Mắt phải đọc theo cụm, không nhẩm từng chữ nữa."),
    (450,  2, "Mức học viên đạt sau khoá: bỏ hẳn giọng đọc trong đầu."),
    (500,  3, "Mỗi lần hai đến ba từ. Ngưỡng của người đã luyện."),
    (600,  3, "Nhịp này cần mắt nhận cả cụm, tai không nhẩm nữa."),
    (700,  4, "Chỉ còn mắt làm việc. Theo được là bạn đã bỏ đọc thầm."),
    (800,  4, "Mức đọc của người luyện lâu năm."),
    (900,  5, "Rất ít người giữ được mốc này mà vẫn hiểu nội dung."),
    (1000, 5, "Mốc cao nhất. Đây là giới hạn để bạn biết mình còn bao xa."),
]

CO_CHU_MOI_LAN = {1: 118, 2: 96, 3: 78, 4: 64, 5: 54}
CHAY, GIAI_THICH, KET = 10.0, 9.0, 8.0     # mỗi mốc chạy 10 giây, hiện từ trong 9 giây đầu


def so_tu_moc(wpm, c):
    """Số từ cần hiện cho một mốc: đủ cho 9 giây ở tốc độ đó, làm tròn theo cả cụm."""
    return math.ceil(wpm * GIAI_THICH / 60 / c) * c


def _van_ban_test(so_tu):
    """Văn bản cho bài test: ghép câu trong lời đọc của các tập trước (nội dung thật của
    kênh, người xem đọc lại đúng thứ mình đã học), hết thì nối tiếp PASSAGE cho đủ từ."""
    cau = []
    for ep in _DS_TAP:
        for _i, t in ep.get("narration", []):
            for c in re.split(r"(?<=[.!?:])\s+", t.strip()):
                if c and c not in cau:
                    cau.append(c)
    tu = [w.replace('"', "").replace("<", "").replace(">", "") for w in " ".join(cau).split()]
    while len(tu) < so_tu:
        tu += PASSAGE
    return tu[:so_tu]


ANIM_MOC = """function(t, el){
     const box = el.querySelector('.flash');
     const W = box.dataset.words.split('|'), c = +box.dataset.chunk;
     const wpm = +box.dataset.wpm, t0 = +box.dataset.t0;
     const j = Math.max(0, Math.floor((t - t0) / (c * 60 / wpm)));
     const so = Math.min((j + 1) * c, W.length);
     box.querySelector('.w').textContent = j * c < W.length ? W.slice(j * c, so).join(' ') : '—';
     el.querySelector('.cnt').textContent = so + '/' + W.length + ' từ';
     el.querySelector('.pg').style.width = (lock(j / Math.ceil(W.length / c), 0, 1) * 100) + '%';
   }"""


def _bai_test_dai():
    """Bài test đầy đủ: cảnh mở đầu + 12 mốc tốc độ + cảnh kết, chạy 2 phút 20 giây."""
    van_ban = _van_ban_test(sum(so_tu_moc(w, c) for w, c, _g in MOC_TEST))
    scenes = [(0.0, GIAI_THICH)]
    html = [scene("""
    <div class="kicker">Bài test tốc độ đọc — bản đầy đủ</div>
    <h1>Từ hai trăm<br>đến <span class="hl">một nghìn</span><br>từ một phút</h1>
    <div class="sub">Mười hai mốc, đi từ chậm đến nhanh. Mốc nào bạn bắt đầu hụt, đó là tốc độ đọc hiện tại.</div>""")]
    anim = [""]

    vt = 0
    for k, (wpm, c, goi_y) in enumerate(MOC_TEST):
        a, n = GIAI_THICH + k * CHAY, so_tu_moc(wpm, c)
        doan, vt = van_ban[vt:vt + n], vt + n
        scenes.append((a, a + CHAY))
        html.append(scene(f"""
    <div class="kicker" style="margin-bottom:14px">Mốc {k + 1}/{len(MOC_TEST)} — {wpm} từ một phút</div>
    <div class="flash" data-words="{'|'.join(doan)}" data-wpm="{wpm}" data-chunk="{c}"
         data-t0="{a + 0.45:.2f}" style="height:430px">
      <span class="w" style="font-size:{CO_CHU_MOI_LAN[c]}px;line-height:1.16;max-width:888px;text-align:center">—</span></div>
    <div class="testbar"><span class="cnt" id="m{k}c">0/{n} từ</span>
      <div class="track"><i class="pg" id="m{k}p"></i></div><span class="rate">{wpm} từ/phút</span></div>
    <div class="sub" style="font-size:34px;margin-top:30px">{goi_y}</div>"""))
        anim.append(ANIM_MOC)

    a = GIAI_THICH + len(MOC_TEST) * CHAY
    scenes.append((a, a + KET))
    html.append(scene("""
    <div class="kicker">Mốc bạn hụt chính là tốc độ hiện tại</div>
    <h1 style="font-size:76px">Ghi mốc đó<br><span class="hl">vào bình luận</span></h1>
    <div class="sub">Người đọc thường dừng ở 200–300. Sau khoá, phần lớn học viên giữ được 450–600 mà vẫn hiểu nội dung.</div>
    <div class="cta"><div class="a">Khoá học</div><div class="b">Đọc hiệu quả Speed Reading</div><div class="c">Học phí 980.000đ · có buổi 1 hoàn tiền</div></div>"""))
    anim.append("")

    tong = a + KET + 3.0          # khung dựng tự nối thêm 3 giây thẻ kết thúc
    return {"slug": "22_bai-test-toc-do-day-du", "total": round(tong, 2),
            "ten": "Bài test tốc độ đọc: 200 đến 1.000 từ một phút",
            "phong_cach": "do-trang",
            "scenes": scenes, "html": html, "anim": anim,
            "narration": [
                (0, "Mười hai mốc, từ hai trăm đến một nghìn từ một phút. Mốc nào bạn bắt đầu hụt, đó là tốc độ đọc hiện tại."),
                (len(MOC_TEST) + 1, "Ghi mốc bạn dừng lại vào bình luận nhé. Cách luyện để đi tiếp có trong buổi đầu của khoá."),
            ]}


EP22 = _bai_test_dai()

# Bộ màu chuẩn của cả chuỗi từ 22/11: đỏ–trắng theo trang speedreading.vn/sp-online.
# Đặt một chỗ cho mọi tập cũ, tập nào muốn quay lại nền tối thì tự khai "phong_cach": "toi".
BO_MAU_CHUAN = "do-trang"
for _ep in _DS_TAP:
    _ep.setdefault("phong_cach", BO_MAU_CHUAN)



# ---------------------------------------------------------------- TẬP AI AGENT — sâu hơn, màu công nghệ
EP_AI_AGENT = {
 "slug": "23_ai-agent-tu-nuoi-kenh", "total": 96.0,
 "ten": "AI Agent tự nuôi kênh: từ ý tưởng đến bài đăng mỗi ngày",
 "brand": "VĂN HỈ OFFICIAL · AI AGENT",
 "dang_ky": "https://vanhi.id.vn",
 "dang_ky_nhan": "Xem thêm tại vanhi.id.vn",
 "phong_cach": "toi",
 "css_extra": """
  #bg{background:
      radial-gradient(1200px 900px at 16% 8%, rgba(0,180,255,.20), transparent 60%),
      radial-gradient(1000px 820px at 84% 90%, rgba(120,80,255,.16), transparent 62%),
      linear-gradient(165deg,#050b18 0%,#0a1630 52%,#050b18 100%)!important}
  .grain{opacity:.06}
  .kicker{color:#38d9ff!important}
  h1{color:#f0f7ff}
  h1 .hl{color:#38d9ff!important}
  .sub{color:#a8bed4}
  .sub b{color:#eaf6ff}
  .techcard{display:flex;flex-direction:column;gap:20px;margin-top:18px}
  .techcard .tc{background:rgba(10,28,56,.78);border:2px solid rgba(56,217,255,.38);border-radius:24px;padding:28px 34px;opacity:0}
  .techcard .tc .tl{font-size:30px;color:#38d9ff;font-weight:800;letter-spacing:.04em;margin-bottom:10px}
  .techcard .tc .tt{font-size:42px;line-height:1.32;color:#eaf6ff}
  .techcard .tc .ts{font-size:28px;color:#9fb8d0;margin-top:10px}
  .bigq{font-size:62px;line-height:1.25;font-weight:800;color:#f0f7ff;text-align:center;margin:26px 0}
  .bigq em{font-style:normal;color:#38d9ff}
  .flow{display:flex;flex-direction:column;gap:16px;margin-top:16px}
  .flow .fw{display:flex;align-items:center;gap:22px;background:rgba(10,28,56,.7);border:1px solid rgba(56,217,255,.3);border-radius:20px;padding:22px 28px;opacity:0}
  .flow .fw .fn{width:64px;height:64px;border-radius:18px;background:#38d9ff;color:#051224;font-size:32px;font-weight:900;display:grid;place-items:center;flex:0 0 auto}
  .flow .fw .ft{font-size:36px;color:#eaf6ff;font-weight:700}
  .flow .fw .fd{font-size:26px;color:#9fb8d0;margin-top:4px}
  .msg{display:flex;flex-direction:column;gap:18px;margin-top:18px}
  .msg .mb{max-width:86%;padding:24px 30px;border-radius:22px;font-size:36px;line-height:1.35;opacity:0}
  .msg .mb.u{align-self:flex-end;background:#38d9ff;color:#051224;font-weight:700}
  .msg .mb.a{align-self:flex-start;background:rgba(10,28,56,.8);border:1px solid rgba(56,217,255,.3);color:#eaf6ff}
  .stat{display:flex;gap:22px;margin-top:20px;justify-content:center}
  .stat .st{flex:1;background:rgba(10,28,56,.7);border:1px solid rgba(56,217,255,.3);border-radius:20px;padding:22px 12px;text-align:center;opacity:0}
  .stat .st b{display:block;font-size:48px;color:#38d9ff;font-weight:900}
  .stat .st span{font-size:24px;color:#9fb8d0}
  #brand{color:#38d9ff!important}
  .nx,.endinfo,.ticket{color:#c9dcf0!important}
  .nx .nxt{color:#eaf6ff!important}
 """,
 "scenes": [
   (0,8.0),(8.0,20.0),(20.0,34.0),(34.0,48.0),(48.0,62.0),
   (62.0,76.0),(76.0,88.0),(88.0,96.0)
 ],
 "html": [
   scene("""<div class="kicker">Một câu hỏi</div>
    <div class="bigq">Bạn có kênh.<br>Bạn có ý tưởng.<br><em>Vậy mà ngày nào cũng bí đăng?</em></div>
    <div class="sub">Không phải bạn lười. Là mỗi ngày bạn phải bắt đầu lại từ con số không.</div>"""),
   scene("""<div class="kicker">01 · Giá trị khi biết</div>
    <h1 style="font-size:74px">Thứ tốn bạn<br><span class="hl">không phải ý tưởng.</span></h1>
    <div class="techcard" id="c1">
      <div class="tc"><div class="tl">Tốn thật</div><div class="tt">Viết lại caption, làm lại ảnh, nhớ lại giờ đăng.</div><div class="ts">Một tiếng mỗi ngày, nhân 30 là 30 tiếng.</div></div>
      <div class="tc"><div class="tl">Hiểu ra</div><div class="tt">Việc lặp lại nên giao cho máy, không phải cho bạn.</div></div>
    </div>"""),
   scene("""<div class="kicker">02 · Hiểu biết mới</div>
    <h1 style="font-size:72px">Chatbot chờ bạn hỏi.<br><span class="hl">Agent tự làm tiếp.</span></h1>
    <div class="techcard" id="c2">
      <div class="tc"><div class="tl">Chatbot</div><div class="tt">Bạn gõ một câu, nó trả một câu, rồi thôi.</div></div>
      <div class="tc"><div class="tl">AI Agent</div><div class="tt">Nhận mục tiêu, tự chia việc, tự chạy đến khi xong.</div><div class="ts">Có công cụ, có bộ nhớ, có lịch chạy.</div></div>
    </div>"""),
   scene("""<div class="kicker">03 · Cấu tạo</div>
    <h1 style="font-size:70px">Agent = <span class="hl">Mục tiêu</span><br>+ Công cụ + Bộ nhớ</h1>
    <div class="flow" id="f3">
      <div class="fw"><div class="fn">1</div><div><div class="ft">Mục tiêu</div><div class="fd">"Kênh có bài mỗi ngày"</div></div></div>
      <div class="fw"><div class="fn">2</div><div><div class="ft">Công cụ</div><div class="fd">Sheet · Drive · Buffer</div></div></div>
      <div class="fw"><div class="fn">3</div><div><div class="ft">Bộ nhớ</div><div class="fd">Nhớ chủ đề đã làm, giữ không đăng trùng</div></div></div>
    </div>"""),
   scene("""<div class="kicker">04 · Ta cần làm gì</div>
    <h1 style="font-size:70px">Bạn chỉ việc<br><span class="hl">duyệt một dòng.</span></h1>
    <div class="msg" id="m4">
      <div class="mb u">"Chủ đề hôm nay: AI Agent cho Spa. Đăng 14h."</div>
      <div class="mb a">Đã viết caption. Đã tạo ảnh. Đã hẹn 14h trên 3 kênh.</div>
      <div class="mb u">"Ổn. Ngày mai làm tiếp chủ đề 15."</div>
      <div class="mb a">Đã ghi nhớ. Hẹn gặp bạn 8h30 sáng mai.</div>
    </div>"""),
   scene("""<div class="kicker">05 · Thông điệp</div>
    <h1 style="font-size:68px">Máy làm phần <span class="hl">mệt.</span><br>Bạn giữ phần <span class="hl">quyết định.</span></h1>
    <div class="techcard" id="c5">
      <div class="tc"><div class="tl">Không phải</div><div class="tt">Agent thay bạn sáng tạo. Nó thay bạn lặp lại.</div></div>
      <div class="tc"><div class="tl">Kết quả</div><div class="tt">15 phút mỗi sáng. Còn lại kênh tự chạy.</div></div>
    </div>"""),
   scene("""<div class="kicker">06 · Kết quả thật</div>
    <h1 style="font-size:72px">Hệ thống đang<br><span class="hl">chạy mỗi ngày.</span></h1>
    <div class="stat" id="s6">
      <div class="st"><b>8h30</b><span>tạo nội dung</span></div>
      <div class="st"><b>12h</b><span>bài đầu lên sóng</span></div>
      <div class="st"><b>15h</b><span>bài thứ hai</span></div>
    </div>
    <div class="sub">Có cron tự đổi model khi hết free. Có job tự giữ kết nối Google.</div>"""),
   scene("""<div class="kicker">Bắt đầu</div>
    <h1 style="font-size:76px">Muốn kênh bạn<br><span class="hl">tự chạy?</span></h1>
    <div class="sub">Xem thêm quy trình và dịch vụ tại <b>vanhi.id.vn</b>.<br>Từ một chủ đề đến ba kênh, không cần biết code.</div>"""),
 ],
 "anim": [
   "",
   """function(t, el){
     [1,2].forEach(function(k){
       var c = el.querySelector('#c1 .tc:nth-child('+k+')');
       if(!c) return;
       var o = ease(span(t, 9.5+k*3.2, 10.6+k*3.2));
       c.style.opacity = o; c.style.transform='translateY('+((1-o)*22)+'px)';
     });
   }""",
   """function(t, el){
     [1,2].forEach(function(k){
       var c = el.querySelector('#c2 .tc:nth-child('+k+')');
       if(!c) return;
       c.style.opacity = ease(span(t, 21.5+k*3.4, 22.8+k*3.4));
     });
   }""",
   """function(t, el){
     var ws = el.querySelectorAll('#f3 .fw');
     ws.forEach(function(w,i){ w.style.opacity = ease(span(t, 35.5+i*2.6, 36.8+i*2.6)); });
   }""",
   """function(t, el){
     var ms = el.querySelectorAll('#m4 .mb');
     ms.forEach(function(m,i){ m.style.opacity = ease(span(t, 49.5+i*2.8, 50.8+i*2.8)); });
   }""",
   """function(t, el){
     [1,2].forEach(function(k){
       var c = el.querySelector('#c5 .tc:nth-child('+k+')');
       if(!c) return;
       c.style.opacity = ease(span(t, 63.5+k*3.4, 64.8+k*3.4));
     });
   }""",
   """function(t, el){
     var ss = el.querySelectorAll('#s6 .st');
     ss.forEach(function(s,i){ s.style.opacity = ease(span(t, 77.5+i*2.2, 78.8+i*2.2)); });
   }""",
   "",
 ],
 "narration": [
   (0, "Bạn có kênh, bạn có ý tưởng. Vậy mà ngày nào cũng bí đăng. Không phải bạn lười. Là mỗi ngày bạn phải bắt đầu lại từ con số không."),
   (1, "Thứ tốn bạn không phải là ý tưởng. Là viết lại caption, làm lại ảnh, nhớ lại giờ đăng. Một tiếng mỗi ngày, nhân ba mươi là ba mươi tiếng."),
   (2, "Hiểu ra một điều: việc lặp lại nên giao cho máy, không phải cho bạn. Chatbot chờ bạn hỏi, trả một câu rồi thôi. AI Agent nhận mục tiêu, tự chia việc, tự chạy đến khi xong."),
   (3, "Agent gồm ba thứ. Mục tiêu: kênh có bài mỗi ngày. Công cụ: Sheet, Drive, Buffer. Và bộ nhớ: nhớ chủ đề đã làm để không đăng trùng."),
   (4, "Bạn chỉ việc duyệt một dòng. Ghi chủ đề và giờ đăng. Agent viết caption, tạo ảnh, hẹn giờ trên ba kênh, rồi tự ghi nhớ cho ngày mai."),
   (5, "Thông điệp ở đây: máy làm phần mệt, bạn giữ phần quyết định. Agent không thay bạn sáng tạo. Nó thay bạn lặp lại. Mười lăm phút mỗi sáng, còn lại kênh tự chạy."),
   (6, "Hệ thống này đang chạy thật. Tám giờ ba mươi tạo nội dung. Mười hai giờ bài đầu lên sóng. Ba giờ chiều bài thứ hai. Có cron tự đổi model khi hết free, có job tự giữ kết nối Google."),
   (7, "Muốn kênh bạn tự chạy? Xem thêm quy trình và dịch vụ tại van hi dot i d v n. Từ một chủ đề đến ba kênh, không cần biết code."),
 ],
}


EPISODES = _DS_TAP + [EP22, EP23, EP_AI_AGENT]
