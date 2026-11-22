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

# ---------------------------------------------------------------- TẬP 2

# ---------------------------------------------------------------- TẬP 3

# ---------------------------------------------------------------- TẬP 4

# ---------------------------------------------------------------- TẬP 5

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

# ---------------------------------------------------------------- TẬP 9 — quy luật 80/20

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

# ---------------------------------------------------------------- TẬP 11 — A6: đọc ngắt quãng mất mạch hiểu

# ---------------------------------------------------------------- TẬP 12 — có phương pháp là nhanh gấp 2-3 lần

# ---------------------------------------------------------------- TẬP 13 — B4: đọc tiêu đề trước

# ---------------------------------------------------------------- TẬP 14 — B5: bản đồ 4 lớp

# ---------------------------------------------------------------- TẬP 15 — A7: đọc nhanh khác đọc lướt

# ---------------------------------------------------------------- TẬP 16 — B7: năm câu hỏi trước khi mở sách

# ---------------------------------------------------------------- TẬP 17 — B8: ghi chép đúng

# ---------------------------------------------------------------- TẬP 18 — B9: sơ đồ một trang

# ---------------------------------------------------------------- TẬP 19 — B10: lịch ôn 1-3-6

# ---------------------------------------------------------------- TẬP 20 — C1: tựa sách đánh lừa

# ---------------------------------------------------------------- TẬP 21 — B6: lướt có cấu trúc

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

# ---------------------------------------------------------------- BỘ DỰNG TẬP THEO SÁU PHẦN
# Viết một tập mới = khai một bảng sáu phần, không phải viết lại HTML và hàm vẽ.
# Mỗi dòng: (kiểu cảnh, số giây, dữ liệu, lời đọc)
#   "h1"    : (kicker, tiêu đề, phụ đề)
#   "list"  : (kicker, [từng mục], ghi chú)        — 4 mục trở lên tự dùng .list20
#   "thanh" : (kicker, [(nhãn, giá trị hiện sẵn)], ghi chú)
# Cổng kiem-tra-kich-ban.py vẫn là nơi chặn: đủ 6 phần, ≥ 110 giây, ≥ 9 cảnh, CTA cuối.


def canh_h1(kicker, tieu_de, phu=""):
    them = f'<div class="sub">{phu}</div>' if phu else ""
    return scene(f'<div class="kicker">{kicker}</div>\n    <h1>{tieu_de}</h1>\n    {them}')


def canh_list(kicker, muc, kieu="list20", ghi_chu=None):
    dong = "\n".join(f'      <div class="it">{x}</div>' for x in muc)
    them = f'\n    <div class="note">{ghi_chu}</div>' if ghi_chu else ""
    return scene(f'<div class="kicker">{kicker}</div>\n    <div class="{kieu}">\n{dong}\n    </div>{them}')


def canh_thanh(kicker, hang, ghi_chu=None):
    """Hai thanh để so sánh định tính — cố ý không in con số, tránh thành số liệu giả."""
    rows = "\n".join(
        f'      <div class="row"><div class="name"><b>{n}</b><span class="val">{v}</span></div>'
        f'\n        <div class="track"><i class="fill{" red" if k else ""}"></i></div></div>'
        for k, (n, v) in enumerate(hang))
    them = f'\n    <div class="note">{ghi_chu}</div>' if ghi_chu else ""
    return scene(f'<div class="kicker">{kicker}</div>\n    <div class="race">\n{rows}\n    </div>{them}')


def anim_hien(kieu, t_bat_dau, so_muc, buoc=1.8, dai=0.7):
    """JS làm hiện dần từng mục của cảnh, tính từ mốc bắt đầu của cảnh."""
    t0 = ", ".join(f"{(t_bat_dau + i * buoc):.1f}" for i in range(so_muc))
    return ("function(t, el){\n"
            f"     const t0 = [{t0}];\n"
            f"     el.querySelectorAll('.{kieu} .it, .race .row, .note').forEach(function(x, k){{\n"
            "       const m = t0[Math.min(k, t0.length - 1)];\n"
            "       x.style.opacity = ease(span(t, m, m + " + str(dai) + ")).toFixed(3);\n"
            "     });\n"
            "   }")


def dua_tap(slug, ten, be, phong_cach="do-trang"):
    """Dựng dict một tập từ bảng sáu phần (xem chú thích ngay trên)."""
    scenes, html, anim, narration = [], [], [], []
    t = 0.0
    for i, (kieu, giay, du_lieu, loi) in enumerate(be):
        scenes.append((round(t, 1), round(t + giay, 1)))
        if kieu == "cta":
            html.append(scene(CTA))
            anim.append("")
        elif kieu == "h1":
            html.append(canh_h1(*du_lieu))
            anim.append("")
        elif kieu == "list":
            kicker, muc, ghi_chu = (list(du_lieu) + [None])[:3]
            kieu_list = "list20" if len(muc) > 3 else "list3"
            html.append(canh_list(kicker, muc, kieu_list, ghi_chu))
            anim.append(anim_hien(kieu_list, t + 1.0, len(muc) + (1 if ghi_chu else 0)))
        elif kieu == "thanh":
            kicker, hang, ghi_chu = (list(du_lieu) + [None])[:3]
            html.append(canh_thanh(kicker, hang, ghi_chu))
            anim.append(anim_hien("race", t + 1.0, len(hang) + (1 if ghi_chu else 0)))
        else:
            raise ValueError(f"{slug}: kiểu cảnh lạ {kieu!r}")
        narration.append((i, loi))
        t += giay
    return {"slug": slug, "total": round(t, 1), "ten": ten, "cau_truc": CAU_TRUC_CHUAN,
            "phong_cach": phong_cach, "scenes": scenes, "html": html, "anim": anim,
            "narration": narration}


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

# ------------------------------------------- TẬP 24 — C2: chọn sách trong năm phút ở nhà sách
EP24 = dua_tap(
 "24_chon-sach-nam-phut", "Chọn sách: năm phút ở nhà sách", [
  ("h1", 9.0, ("Nhà sách · vài phút quyết định",
    "Mua một cuốn sách<br>mất <span class=\"hl\">2 đến 5 phút</span>",
    "Nhưng nó ở với bạn hàng tuần — hoặc nằm im trên kệ."),
   "Ở nhà sách bạn thường chỉ có hai đến năm phút trước khi quyết định. Và cuốn sách đó ở với bạn hàng tuần, hoặc nằm im trên kệ."),
  ("list", 12.0, ("Ba sai lầm hay mắc", [
    "<b>Mua theo tựa</b> — tựa được viết để bán",
    "<b>Đọc thử trang đầu</b> — trang đầu quyển nào cũng dễ",
    "<b>Không mở mục lục</b> — nên không biết sách có gì"], None),
   "Ba sai lầm: mua theo tựa, vì tựa sách được viết để bán. Đọc thử trang đầu, mà trang đầu thì quyển nào cũng dễ. Và không mở mục lục, nên không biết sách có gì."),
  ("list", 12.0, ("Năm phút này cho bạn gì", [
    "Biết chắc cuốn sách có ích hay không",
    "Không mua sách chỉ hay ở bìa",
    "Mỗi lần vào nhà sách mua đúng một quyển"],
    "Năm phút → hoặc mua, hoặc đi tiếp."),
   "Quy trình năm phút này giúp bạn biết chắc cuốn sách có ích hay không, thay vì mua theo cảm giác ở bìa."),
  ("h1", 13.0, ("Vì sao đọc trang đầu là sai",
    "Trang đầu<br><span class=\"hl\">không phải</span> cuốn sách",
    "Nhà xuất bản chăm chút trang đầu. Giá trị thật nằm ở cấu trúc."),
   "Đọc trang đầu không cho bạn biết gì về giá trị của cuốn sách, vì nhà xuất bản nào cũng chăm chút trang đầu."),
  ("thanh", 13.0, ("Hai cách thử khác nhau", [
    ("Đọc trang đầu", "thử vận may"),
    ("Xem mục lục và một chương giữa", "đúng nhu cầu")],
    "Cùng năm phút, khác chỗ nhìn là khác kết quả."),
   "Cách nhanh nhất là nhìn cấu trúc: mục lục, rồi mở đúng chương liên quan tới việc bạn đang cần. Đó mới là thứ quyết định cuốn sách có ích hay không."),
  ("list", 14.0, ("Phút 1–2 · tựa phụ và mục lục", [
    "Đọc tựa phụ — nói sách giải quyết việc gì",
    "Xem mục lục, đếm chương đúng nhu cầu của bạn",
    "Lướt phần giới thiệu tác giả"], None),
   "Phút thứ nhất và thứ hai: đọc tựa phụ, xem mục lục và đếm số chương đúng nhu cầu của bạn, rồi lướt phần giới thiệu tác giả."),
  ("list", 14.0, ("Phút 3–5 · mở đúng một chương", [
    "Mở chương liên quan nhất, đọc hai trang ở giữa chương",
    "Gấp lại, tự hỏi vừa đọc được ý gì",
    "Ít nhất hai chương như vậy thì hãy mua"], None),
   "Phút thứ ba đến thứ năm: mở chương liên quan nhất, đọc hai trang ở giữa chương đó, rồi gấp sách tự hỏi bạn vừa đọc được ý gì. Ít nhất hai chương như vậy thì hãy mua."),
  ("h1", 13.0, ("Thông điệp",
    "Mua sách là<br>một <span class=\"hl\">quyết định</span>",
    "Năm phút chọn đúng rẻ hơn nhiều giờ đọc nhầm."),
   "Thông điệp ở đây: mua sách là một quyết định, không phải một cảm hứng. Năm phút chọn đúng rẻ hơn nhiều giờ đọc nhầm."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom", [
    "Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
    "Buổi hai: chọn sách, đọc cụm, bỏ đọc thầm",
    "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Quy trình chọn sách này nằm trong buổi thứ hai của khoá. Khoá bảy buổi Zoom, học phí chín trăm tám mươi nghìn, hoàn phí nếu sau buổi một bạn thấy không hợp."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

# ------------------------------------------- TẬP 25 — D1: khoảng cách mắt và góc cổ khi đọc
EP25 = dua_tap(
 "25_khoang-cach-mat-va-co", "Khoảng cách mắt và góc cổ khi đọc", [
  ("h1", 9.0, ("Đọc lâu · cổ và mắt",
    "Mỏi cổ làm bạn<br><span class=\"hl\">đọc chậm lại</span>",
    "Không phải ý chí — mà là tư thế đang chặn dòng chữ."),
   "Đọc được ba mươi phút là cổ mỏi, mắt nặng, và bạn tự nhủ mình hết tập trung. Thật ra chỉ là tư thế đang chặn bạn."),
  ("list", 12.0, ("Ba dấu hiệu tư thế sai", [
    "Cúi đầu, sách cách mắt dưới 30 cm",
    "Cổ nghiêng hẳn sang một bên",
    "Mắt phải nhảy quãng xa để bám dòng chữ"], None),
   "Ba dấu hiệu: sách quá gần mắt, cổ nghiêng hẳn sang một bên, và mắt phải nhảy quãng xa để bám theo dòng chữ."),
  ("list", 12.0, ("Sửa tư thế được gì", [
    "Đọc lâu hơn mà không mỏi",
    "Dòng chữ đứng yên, mắt đỡ phải điều tiết",
    "Bỏ được kiểu ngồi bó cổ mỗi tối"],
    "Ba điều chỉnh nhỏ, kiểm được ngay trong một buổi."),
   "Ba điều chỉnh nhỏ dưới đây giúp bạn đọc lâu hơn mà không mỏi, và giữ được dòng đọc thẳng."),
  ("h1", 14.0, ("Vì sao khoảng cách lại quyết định",
    "Gần quá thì<br>mắt phải <span class=\"hl\">níu lại</span>",
    "Càng gần, cơ mắt càng phải kéo — nhanh mỏi, dễ sai dòng."),
   "Khi sách quá gần, cơ mắt phải kéo nhiều hơn cho mỗi chữ, nên mỏi nhanh và bạn dễ nhảy sai dòng. Khoảng cách vừa phải là khoảng ba mươi đến bốn mươi lăm xăng-ti-mét."),
  ("list", 13.0, ("Ba con số để tự soát", [
    "Sách: 35–45 cm · màn hình máy tính: từ 50 cm",
    "Điện thoại: khoảng 30 cm, hơi ngẩng mắt xuống",
    "Cứ 20 phút: nhìn ra xa 20 giây"],
    "Đây là hướng dẫn phổ biến của ngành nhãn khoa về làm việc gần."),
   "Ba con số: sách cách mắt khoảng ba mươi lăm đến bốn mươi lăm xăng-ti-mét, màn hình từ nửa mét trở lên, và cứ hai mươi phút thì nhìn ra xa hai mươi giây."),
  ("list", 13.0, ("Việc cần làm · trong 5 phút", [
    "Đặt sách xuống bàn, chống khuỷu tay",
    "Đo bằng gang tay: khoảng hai gang từ mắt tới trang",
    "Gá sách cao lên cho cổ khỏi cúi"], None),
   "Việc cần làm ngay: đặt sách xuống bàn, chống khuỷu tay, đo khoảng cách bằng hai gang tay, và gá sách lên cao để cổ thẳng."),
  ("list", 13.0, ("Với màn hình thì khác một chút", [
    "Màn hình ngang tầm mắt, đừng thấp hơn",
    "Tai — vai — hông thành một đường thẳng",
    "Đổi tư thế sau mỗi 20 phút"], None),
   "Với màn hình, để ngang tầm mắt chứ đừng thấp hơn. Ngồi sao cho tai, vai và hông thẳng một đường, và đổi tư thế sau mỗi hai mươi phút."),
  ("h1", 13.0, ("Thông điệp",
    "Đọc lâu không phải<br>là <span class=\"hl\">chịu đau</span>",
    "Đọc lâu là khi mắt và cổ được đặt đúng chỗ."),
   "Thông điệp: đọc lâu không phải là chịu đau. Đọc lâu là khi mắt và cổ được đặt đúng chỗ ngay từ đầu."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom", [
    "Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
    "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
    "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Tư thế và khoảng cách được chỉnh ngay trong buổi đầu của khoá, vì sửa được chỗ này thì tốc độ lên nhanh hơn. Khoá bảy buổi Zoom, học phí chín trăm tám mươi nghìn đồng."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

# ------------------------------------------- TẬP 26 — D2: ánh sáng và nhịp đổi tiêu cự
EP26 = dua_tap(
 "26_anh-sang-va-tu-the", "Ánh sáng đọc sách và nhịp đổi tiêu cự", [
  ("h1", 9.0, ("Ánh sáng khi đọc",
    "Đèn sáng chưa chắc<br><span class=\"hl\">đủ để đọc</span>",
    "Sáng chói mà sai hướng thì mắt vẫn phải gắng."),
   "Đèn phòng sáng chói nhưng đặt sai hướng thì mắt bạn vẫn phải gắng, và độ mỏi vẫn tăng đều."),
  ("list", 12.0, ("Ba kiểu chiếu sáng hay gặp", [
    "Đèn trần hắt xuống → bóng tay và bóng sách",
    "Đèn sau lưng → giấy chói vào mắt",
    "Đèn bàn đặt lệch → một nửa trang tối"], None),
   "Ba kiểu hay gặp: đèn trần hắt xuống tạo bóng tay, đèn phía sau lưng làm giấy chói, và đèn bàn đặt lệch làm nửa trang tối."),
  ("list", 12.0, ("Sửa hai thứ được gì", [
    "Mắt đỡ mỏi khi đọc buổi tối",
    "Tốc độ đọc giữ đều tới phút cuối",
    "Hết cảm giác chữ bị nhòe cuối buổi"],
    "Hai điều chỉnh: hướng đèn, và nhịp đổi tiêu cự."),
   "Hai điều chỉnh dưới đây giữ cho tốc độ đọc không tuột ở hai mươi phút cuối buổi tối."),
  ("h1", 14.0, ("Vì sao đổi tiêu cự mới là chính",
    "Nhìn gần mãi<br>thì <span class=\"hl\">cơ mắt bị giữ</span>",
    "Đổi khoảng cách chính là để cơ mắt được thả ra."),
   "Mắt không được thiết kế để nhìn gần liên tục hàng giờ. Khi bạn giữ tiêu cự gần mãi, cơ mắt bị giữ ở một trạng thái, nên hết buổi là nhòe và mỏi."),
  ("list", 13.0, ("Nhịp đổi tiêu cự", [
    "Nhìn gần: cơ mắt co lại và giữ liên tục",
    "Nhìn xa khoảng 20 giây: cơ mắt giãn ra",
    "Khoảng 30 phút đổi một lần là đủ để hồi"],
    "Không cần nghỉ dài — chỉ cần đổi khoảng cách."),
   "Đổi tiêu cự là cách thả cơ mắt ra. Không cần nghỉ dài: cứ khoảng ba mươi phút, ngước lên nhìn một vật ở xa trong hai mươi giây là đủ."),
  ("list", 13.0, ("Việc cần làm · đèn", [
    "Đèn bàn đặt chếch bên tay không viết, hắt vào trang",
    "Chùm sáng không chiếu thẳng vào mắt",
    "Trang giấy sáng đều, không có vùng tối"], None),
   "Với đèn: đặt chếch bên tay không viết, hắt vào trang giấy, và để chùm sáng không chiếu thẳng vào mắt."),
  ("list", 13.0, ("Việc cần làm · nhịp đọc", [
    "Đặt nhắc mỗi 30 phút",
    "Mỗi lần nhắc: nhìn xa 20 giây, chớp mắt vài lần",
    "Đọc trên màn hình: hạ độ sáng vừa phải"], None),
   "Với nhịp đọc: đặt nhắc ba mươi phút một lần. Mỗi lần nhắc thì nhìn ra xa khoảng hai mươi giây, chớp mắt vài lần rồi đọc tiếp."),
  ("h1", 13.0, ("Thông điệp",
    "Mắt cần được<br><span class=\"hl\">đổi cự ly</span>",
    "Không phải nghỉ nhiều, mà là đổi khoảng cách đều."),
   "Thông điệp: mắt không cần nghỉ nhiều, mắt cần được đổi cự ly đều. Ba mươi phút một lần, hai mươi giây."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom", [
    "Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
    "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
    "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Đèn và nhịp đổi tiêu cự là phần đầu của buổi một, vì mắt còn mỏi thì không luyện nhanh được. Khoá có bảy buổi Zoom và hoàn phí nếu sau buổi một bạn thấy không hợp."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

# ------------------------------------------- TẬP 27 — D3: vừa đọc vừa nghe nhạc
EP27 = dua_tap(
 "27_vua-doc-vua-nghe-nhac", "Vừa đọc vừa nghe nhạc: não chia kênh thế nào", [
  ("h1", 9.0, ("Vừa đọc vừa nghe nhạc",
    "Nhạc không làm bạn<br><span class=\"hl\">đọc chậm</span> — có khi ngược lại",
    "Nhưng nó lấy đi một thứ khác: chỗ trống trong bộ nhớ."),
   "Vừa đọc vừa nghe nhạc không nhất thiết làm bạn đọc chậm hơn. Nhưng nó lấy đi một thứ khác."),
  ("list", 12.0, ("Ba kiểu nhạc khác nhau hoàn toàn", [
    "Nhạc có lời tiếng Việt → tranh chỗ với chữ đang đọc",
    "Nhạc có lời ngoại ngữ → ít tranh hơn, vẫn có giai điệu",
    "Nhạc không lời, nhịp đều → cản ít nhất"], None),
   "Ba kiểu nhạc khác nhau hoàn toàn: nhạc có lời tiếng Việt tranh chỗ với chữ trên trang, nhạc ngoại ngữ ít tranh hơn, và nhạc không lời cản ít nhất."),
  ("list", 12.0, ("Biết điều này để làm gì", [
    "Chọn loại nhạc theo việc đang đọc",
    "Biết lúc nào nên tắt hẳn",
    "Không đổ lỗi chung chung cho mất tập trung"],
    "Một tiêu chí duy nhất: lần đọc này có cần nhớ lại không?"),
   "Biết điều này để chọn nhạc theo việc đang đọc, và để biết lúc nào nên tắt hẳn."),
  ("h1", 15.0, ("Đọc và nghe dùng chung một kênh",
    "Cùng một kênh<br><span class=\"hl\">xử lý chữ</span>",
    "Chữ trên trang và lời trong bài hát đi vào cùng một cửa."),
   "Chữ trên trang và lời trong bài hát đi vào cùng một cửa xử lý ngôn ngữ. Đó là lý do nhạc có lời tiếng Việt kéo tốc độ đọc xuống rõ hơn nhạc không lời."),
  ("list", 15.0, ("Nghiên cứu không đồng nhất", [
    "Có người đọc nhanh hơn khi nghe nhạc quen",
    "Có người chậm hẳn khi nhạc có lời",
    "Kết quả phụ thuộc: đọc để nhớ hay đọc để lướt"],
    "Điểm chung: đọc để nhớ thì nhạc có lời gây hại rõ nhất."),
   "Các nghiên cứu không đồng nhất: có người đọc nhanh hơn khi nghe nhạc quen, có người chậm hẳn. Điểm chung là khi bạn cần nhớ lại nội dung, nhạc có lời gây hại rõ nhất."),
  ("list", 14.0, ("Việc cần làm · theo loại việc đọc", [
    "Đọc để nhớ (giáo trình, sách kỹ năng) → tắt lời",
    "Đọc lướt, đọc cho vui → nhạc nào cũng được",
    "Đọc để ghi chép → không mở nhạc"], None),
   "Việc cần làm: đọc để nhớ thì tắt nhạc có lời; đọc lướt hay đọc cho vui thì nhạc nào cũng được; còn khi ghi chép thì đừng mở nhạc."),
  ("list", 14.0, ("Tự kiểm trong 15 phút", [
    "Đọc 5 phút có nhạc có lời → gấp sách, kể lại ba ý",
    "Đọc 5 phút im lặng → gấp sách, kể lại ba ý",
    "Bên nào kể được nhiều hơn là bên hợp với bạn"],
    "Kết quả của người khác không thay được kết quả của bạn."),
   "Muốn biết chắc thì tự kiểm: đọc năm phút có nhạc, gấp sách kể lại ba ý; rồi đọc năm phút im lặng và làm lại. Bên nào kể được nhiều hơn là bên hợp với bạn."),
  ("h1", 13.0, ("Thông điệp",
    "Nhạc không xấu —<br>nó <span class=\"hl\">chiếm chỗ</span>",
    "Đọc để nhớ thì đừng để lời bài hát ngồi cùng chỗ với chữ."),
   "Thông điệp: nhạc không xấu, nó chỉ chiếm chỗ. Khi việc đọc cần nhớ lại thì đừng để lời bài hát ngồi cùng chỗ với chữ."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom", [
    "Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
    "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
    "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Trong khoá, phần ghi chép và ôn theo mốc là phần nhạy với tiếng ồn nhất, nên tôi nhắc học viên tắt nhạc có lời đúng những lúc đó. Khoá bảy buổi Zoom, học phí chín trăm tám mươi nghìn đồng."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

# ------------------------------------------- TẬP 28 — E3: người đi làm, 30 phút mỗi ngày nên đọc gì
EP28 = dua_tap(
 "28_di-lam-30-phut-moi-ngay", "Người đi làm: 30 phút mỗi ngày nên đọc gì", [
  ("h1", 9.0, ("Người đi làm · ba mươi phút",
    "Ba mươi phút mỗi ngày<br>đọc <span class=\"hl\">cái gì</span>?",
    "Đọc sai thứ thì ba mươi phút cũng trôi mất."),
   "Bạn có ba mươi phút mỗi ngày, và câu hỏi thật không phải đọc thế nào, mà là đọc cái gì."),
  ("list", 12.0, ("Ba cách dùng sai ba mươi phút", [
    "Đọc tin trên mạng rồi hết giờ",
    "Mỗi cuốn đọc vài trang rồi bỏ",
    "Chờ có thời gian dài mới đọc — mà không bao giờ có"], None),
   "Ba cách làm mất ba mươi phút: đọc tin trên mạng rồi hết giờ, đọc mỗi cuốn vài trang rồi bỏ, và chờ một khoảng thời gian dài mới đọc."),
  ("list", 13.0, ("Chọn đúng thì được gì", [
    "Ba mươi phút thành 20–30 cuốn một năm",
    "Kiến thức dùng được ngay vào việc đang làm",
    "Đọc đều, không phải quyết định lại mỗi ngày"],
    "Cùng số phút, khác thứ đọc là khác kết quả."),
   "Chọn đúng thì ba mươi phút mỗi ngày thành hai mươi đến ba mươi cuốn một năm, và phần lớn là sách dùng được ngay cho công việc."),
  ("h1", 14.0, ("Vì sao thứ đọc quyết định",
    "Sách để làm việc<br>khác <span class=\"hl\">sách để đọc cho nhẹ</span>",
    "Một loại cần ghi chép và làm theo. Một loại chỉ cần đọc cho nhẹ đầu."),
   "Sách để làm việc và sách để đọc cho nhẹ là hai loại khác nhau. Loại thứ nhất cần ghi chép và làm theo, và không nên đọc lúc bạn đã mệt."),
  ("list", 14.0, ("Ba túi thời gian khác nhau", [
    "Lúc chờ, lúc đi đường (5–10 phút): bài ngắn, tin, tổng hợp",
    "Buổi tối 30 phút liền: sách kỹ năng, đọc kèm ghi chép",
    "Cuối tuần: sách dài, chủ đề lớn"], None),
   "Ba túi thời gian cần ba loại đọc khác nhau: lúc chờ thì đọc bài ngắn; buổi tối có ba mươi phút liền thì đọc sách kỹ năng kèm ghi chép; cuối tuần thì dành cho sách dài."),
  ("list", 13.0, ("Việc cần làm · chọn một chủ đề", [
    "Chọn đúng một chủ đề gắn với việc đang làm",
    "Xếp hàng ba cuốn, đọc lần lượt",
    "Đọc xong một cuốn mới sang cuốn tiếp"], None),
   "Việc cần làm: chọn đúng một chủ đề gắn với việc bạn đang làm, xếp hàng ba cuốn và đọc lần lượt, xong một cuốn rồi mới sang cuốn khác."),
  ("list", 13.0, ("Việc cần làm · đặt giờ cố định", [
    "Ba mươi phút cùng một khung giờ mỗi ngày",
    "Đọc trên máy: tắt thông báo, chỉ một cửa sổ",
    "Sau mỗi lần đọc, ghi lại một câu đáng dùng"], None),
   "Và đặt một khung giờ cố định, ba mươi phút, cùng một chỗ mỗi ngày. Đọc trên máy thì tắt thông báo và chỉ mở một cửa sổ."),
  ("h1", 13.0, ("Thông điệp",
    "Ba mươi phút là<br><span class=\"hl\">một cuốn sách mỗi tháng</span>",
    "Nhưng chỉ khi bạn chọn đúng thứ để đọc."),
   "Thông điệp: ba mươi phút mỗi ngày là một cuốn sách mỗi tháng, với điều kiện bạn chọn đúng thứ để đọc."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom", [
    "Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
    "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
    "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Người đi làm thường vào khoá vì không có nhiều thời gian: ba mươi phút mỗi ngày, đọc đúng thứ, và có quy trình để nhớ. Học phí chín trăm tám mươi nghìn đồng, hoàn phí sau buổi một."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

# ------------------------------------------- TẬP 29 — C3: ba lớp kiểm tra một quyển sách
EP29 = dua_tap(
 "29_ba-lop-kiem-tra-sach", "Ba lớp kiểm tra một quyển sách", [
  ("h1", 9.0, ("Ba lớp kiểm tra một quyển sách",
    "Cuốn sách này có đáng<br><span class=\"hl\">tiền và thời gian</span>?",
    "Ba câu hỏi, mỗi câu một phút, trả lời trước khi trả tiền."),
   "Một cuốn sách đáng tiền hay không thì kiểm được trong ba phút, bằng ba câu hỏi. Mỗi câu trả lời một lớp."),
  ("list", 12.0, ("Ba lớp kiểm tra", [
    "<b>Lớp 1</b> — nội dung dựa trên gì",
    "<b>Lớp 2</b> — mục lục có trả đúng lời hứa ở tựa",
    "<b>Lớp 3</b> — có bước làm được, hay chỉ nói ý tưởng"], None),
   "Ba lớp: lớp thứ nhất xem nội dung dựa trên gì, lớp thứ hai xem mục lục có trả đúng lời hứa ở tựa, lớp thứ ba xem sách có bước làm được hay chỉ nói ý tưởng."),
  ("list", 12.0, ("Kiểm xong thì được gì", [
    "Biết sách hợp với mình ở đâu, không hợp ở đâu",
    "Không mua vì bìa, cũng không bỏ vì tựa dở",
    "Dùng được cho cả sách giấy và sách mua online"],
    "Ba phút kiểm, thay cho ba tuần đọc dở."),
   "Kiểm xong thì bạn biết cuốn sách hợp với mình ở chỗ nào và không hợp ở chỗ nào, và dùng được cả khi mua sách online."),
  ("h1", 14.0, ("Vì sao phải kiểm theo lớp",
    "Một cuốn sách có thể<br>đúng nửa này, <span class=\"hl\">sai nửa kia</span>",
    "Tựa đúng không có nghĩa nội dung đúng. Cấu trúc đẹp không có nghĩa làm được."),
   "Không có cuốn sách nào đúng hoặc sai toàn bộ. Một cuốn có thể có nội dung tốt nhưng cấu trúc lộn xộn, hoặc ngược lại. Vì vậy phải kiểm theo từng lớp."),
  ("list", 13.0, ("Lớp 1 · nội dung dựa trên gì", [
    "Tác giả có làm nghề này không, làm bao lâu",
    "Số liệu có ghi nguồn hay chỉ nói chung chung",
    "Cuối sách có phần ghi chú, tài liệu tham khảo không"], None),
   "Lớp thứ nhất: tác giả có làm nghề này không và làm bao lâu, số liệu có ghi nguồn hay chỉ nói chung chung, và cuối sách có phần ghi chú hay tài liệu tham khảo không."),
  ("list", 13.0, ("Lớp 2 và 3 · cấu trúc và việc làm được", [
    "Mục lục: mỗi chương trả lời một câu hỏi cụ thể",
    "Trong chương: có bước, có ví dụ, có chỗ để làm theo",
    "Đọc một chương bất kỳ rồi gấp lại: kể được điều gì?"], None),
   "Lớp thứ hai và thứ ba: mỗi chương trong mục lục phải trả lời một câu hỏi cụ thể; trong chương phải có bước và ví dụ; và sau khi đọc một chương, gấp sách lại bạn phải kể được một điều cụ thể."),
  ("list", 14.0, ("Việc cần làm · ba câu hỏi", [
    "Câu 1: tác giả này dựa vào đâu để nói?",
    "Câu 2: mục lục có việc gì cho từng chương?",
    "Câu 3: sau chương đầu, tôi làm được gì?"], None),
   "Việc cần làm: hỏi ba câu. Tác giả dựa vào đâu để nói. Mục lục có việc gì cho từng chương. Và sau chương đầu tiên, tôi làm được gì."),
  ("list", 13.0, ("Trượt hai lớp thì để lại", [
    "Trượt lớp nguồn: sách để đọc cho vui — mượn, đừng mua",
    "Trượt lớp việc làm được: chỉ nên đọc thư viện",
    "Đủ cả ba lớp: mua, và đọc theo quy trình"], None),
   "Nếu trượt hai trong ba lớp thì để cuốn sách lại: sách chỉ để đọc cho vui thì mượn, không cần mua. Đủ cả ba lớp thì mua và đọc theo quy trình."),
  ("h1", 13.0, ("Thông điệp",
    "Đáng tiền là cuốn<br><span class=\"hl\">trả lời được ba câu</span>",
    "Nguồn · cấu trúc · việc làm được."),
   "Thông điệp: một cuốn sách đáng tiền là cuốn trả lời được cả ba câu hỏi — nguồn, cấu trúc, và việc làm được."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom", [
    "Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
    "Buổi hai: chọn sách, đọc cụm, bỏ đọc thầm",
    "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Ba lớp kiểm tra này là phần chọn sách trong buổi thứ hai của khoá. Khoá bảy buổi Zoom, học phí chín trăm tám mươi nghìn đồng, hoàn phí nếu sau buổi một bạn thấy không hợp."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

# ------------------------------------------- TẬP 30 — F1: người Việt đọc bao nhiêu, CEO đọc bao nhiêu
# Số liệu lấy từ nguồn công khai, ghi rõ nguồn trên màn hình: Cục Xuất bản, In và Phát hành
# (báo cáo 2024), Vụ Thư viện — Bộ VH-TT&DL (khảo sát 2013), Bill Gates trả lời New York Times
# 2016. Số liệu đổi theo năm, nên tập nào dùng lại phải tra lại trước khi đăng.
EP30 = dua_tap(
 "30_thoi-quen-doc-nguoi-viet", "Người Việt đọc bao nhiêu — và vì sao CEO đọc gấp mấy chục lần", [
  ("h1", 9.0, ("Số liệu 2024 · Cục Xuất bản",
    "Người Việt: <span class=\"hl\">5,9 bản sách</span><br>mỗi năm",
    "Nghe không tệ. Nhưng 77% trong đó là sách giáo khoa."),
   "Số liệu năm hai nghìn hai mươi tư: bình quân mỗi người Việt được hưởng năm phẩy chín bản sách một năm. Nghe không tệ."),
  ("list", 13.0, ("Nhưng nhìn kỹ thì khác", [
    "461 triệu bản là sách giáo khoa — 77% tổng số",
    "Sách đọc tự nguyện chỉ còn 135 triệu bản",
    "Chia cho 101 triệu dân: khoảng 1,3 bản một người"],
    "Nguồn: Cục Xuất bản, In và Phát hành — báo cáo 2024."),
   "Nhưng trong đó, bốn trăm sáu mươi mốt triệu bản là sách giáo khoa, chiếm bảy mươi bảy phần trăm. Sách đọc tự nguyện chỉ còn khoảng một phẩy ba bản một người một năm."),
  ("list", 13.0, ("Hiểu đúng con số để làm gì", [
    "Không tự nhận mình đọc nhiều dựa vào con số chung",
    "Biết mốc thật của người Việt: khoảng 1–1,3 cuốn một năm",
    "Đặt mục tiêu theo tuần thay vì theo năm"], None),
   "Hiểu đúng con số giúp bạn không tự huyễn hoặc: mốc thật của người Việt là khoảng một đến một phẩy ba cuốn một năm."),
  ("h1", 14.0, ("Vì sao có hai con số khác nhau",
    "Cùng một dữ liệu,<br>khác <span class=\"hl\">cách đếm</span>",
    "Bản in ra, bản bán được, bản thực sự được đọc — ba con số khác nhau."),
   "Có lúc bạn nghe người Việt đọc không tới một cuốn một năm, có lúc nghe gần sáu bản. Cả hai đều có nguồn, chỉ khác cách đếm: bản in ra, bản bán được, hay bản thực sự được đọc."),
  ("list", 13.0, ("Còn thói quen đọc thì sao", [
    "26% người Việt hoàn toàn không đọc sách",
    "44% thỉnh thoảng mới cầm sách",
    "30% đọc thường xuyên"],
    "Nguồn: Vụ Thư viện, Bộ Văn hóa, Thể thao và Du lịch."),
   "Theo Vụ Thư viện, hai mươi sáu phần trăm người Việt hoàn toàn không đọc sách, bốn mươi bốn phần trăm thỉnh thoảng mới cầm sách, và ba mươi phần trăm đọc thường xuyên."),
  ("list", 14.0, ("Đầu kia của khoảng cách", [
    "<b>Bill Gates</b>: khoảng 50 cuốn một năm — gần 1 cuốn mỗi tuần",
    "<b>Warren Buffett</b>: đọc 5–6 giờ mỗi ngày",
    "Điểm chung không phải đọc nhanh hơn, mà là đọc đều hơn"],
    "Nguồn: Bill Gates trả lời New York Times (2016); báo chí trong nước tổng hợp."),
   "Ở đầu kia: Bill Gates nói ông đọc khoảng năm mươi cuốn một năm, tức gần một cuốn mỗi tuần. Warren Buffett đọc năm đến sáu giờ mỗi ngày. Điểm chung không phải họ đọc nhanh hơn, mà là đọc đều hơn."),
  ("h1", 13.0, ("Năm mươi cuốn là bao nhiêu mỗi ngày",
    "50 cuốn một năm<br>≈ <span class=\"hl\">50 phút mỗi ngày</span>",
    "Ở 250 từ/phút, một cuốn 300 trang là khoảng 6 giờ đọc."),
   "Năm mươi cuốn một năm là khoảng ba trăm giờ đọc. Chia cho ba trăm sáu mươi lăm ngày, mỗi ngày khoảng năm mươi phút ở tốc độ hai trăm năm mươi từ một phút. Đọc nhanh gấp đôi thì chỉ còn hai mươi lăm phút."),
  ("list", 14.0, ("Việc cần làm · tuần này", [
    "Chọn một cuốn mỏng, đặt mốc 1 cuốn mỗi tuần",
    "Cố định 30 phút cùng một giờ mỗi ngày",
    "Ghi lại số trang đọc được để thấy mình tiến bộ"],
    "1 cuốn mỗi tuần là 52 cuốn một năm — mức của Bill Gates."),
   "Việc cần làm: chọn một cuốn mỏng và đặt mốc một cuốn mỗi tuần, cố định ba mươi phút cùng một giờ mỗi ngày, và ghi lại số trang đọc được để thấy mình tiến bộ."),
  ("h1", 13.0, ("Thông điệp",
    "Khoảng cách không nằm ở<br><span class=\"hl\">tốc độ đọc</span>",
    "Nằm ở số ngày bạn thật sự cầm sách — tốc độ chỉ làm việc đó dễ hơn."),
   "Thông điệp: khoảng cách giữa một cuốn và năm mươi cuốn một năm không nằm ở tốc độ đọc, mà ở số ngày bạn thật sự cầm sách. Tốc độ chỉ làm việc đó dễ hơn."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom", [
    "Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
    "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
    "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Nếu mục tiêu của bạn là năm mươi cuốn một năm thì ba mươi phút mỗi ngày là chưa đủ, trừ khi bạn đọc nhanh hơn. Khoá bảy buổi Zoom dạy đúng phần tốc độ đó: học phí chín trăm tám mươi nghìn đồng, hoàn phí sau buổi một nếu bạn thấy không hợp."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

# ------------------------------------------- TẬP 31 — F2: số liệu đo tốc độ đọc sinh viên đại học
# Số liệu có nguồn: nghiên cứu 15 tuần trên 206 sinh viên đại học tại Việt Nam (Tran và cộng sự,
# 2024) — đo tốc độ đọc bài tiếng Anh. Mốc tham chiếu 200–300 từ/phút là mốc phổ biến trong
# tài liệu về tốc độ đọc. Không dùng số liệu lớp riêng vì chưa có sự đồng ý của trường.
EP31 = dua_tap(
 "31_sinh-vien-doc-bao-nhieu-tu-mot-phut", "Sinh viên Việt đọc bao nhiêu từ một phút — số liệu đo được", [
  ("h1", 9.0, ("Số liệu nghiên cứu · 2024",
    "Sinh viên Việt đọc<br><span class=\"hl\">124 từ một phút</span>",
    "Đo trên 206 sinh viên đại học, đọc bài tiếng Anh, trước khi luyện."),
   "Nghiên cứu 2024 đo tốc độ đọc bài tiếng Anh của hai trăm lẻ sáu sinh viên đại học Việt Nam: một trăm hai mươi bốn từ một phút."),
  ("list", 13.0, ("Con số này nói với bạn điều gì", [
    "Bạn không đọc chậm vì kém — đó là mức trung bình",
    "Tốc độ đọc đo được, nên so sánh được",
    "Biết mốc của mình để đặt mục tiêu cụ thể"], None),
   "Con số này cho thấy bạn không đọc chậm vì kém cỏi — đó là mức trung bình. Và vì đo được nên nó so sánh được, và bạn đặt mục tiêu được."),
  ("list", 13.0, ("Luyện 15 tuần thì sao", [
    "Nhóm luyện: 124 → 136 từ/phút (tăng 12 từ)",
    "Nhóm không luyện: 120 → 123 từ/phút (tăng 3 từ)",
    "Điểm hiểu bài cũng tăng, không bị giảm"],
    "Nguồn: Tran và cộng sự, 2024 — 206 sinh viên đại học, luyện 15 tuần."),
   "Sau mười lăm tuần luyện, nhóm luyện tăng lên một trăm ba mươi sáu từ một phút, còn nhóm không luyện gần như đứng yên. Điểm hiểu bài cũng tăng theo, không giảm."),
  ("h1", 14.0, ("Vì sao phải nhấn mạnh chữ “luyện”",
    "Đọc nhanh là<br><span class=\"hl\">kỹ năng, không phải năng khiếu</span>",
    "Hai nhóm học cùng thời gian — khác nhau ở cách luyện."),
   "Hai nhóm có cùng thời gian học. Khác nhau ở chỗ một nhóm luyện có phương pháp, một nhóm đọc theo cách cũ. Nên tốc độ đọc là kỹ năng, không phải năng khiếu."),
  ("list", 13.0, ("Đặt con số vào thang chung", [
    "Người lớn đọc thường: 200–250 từ/phút",
    "Sinh viên đại học: khoảng 300 từ/phút",
    "Tài liệu kỹ thuật khó: 100–200 từ/phút"],
    "Mốc tham chiếu phổ biến trong tài liệu về tốc độ đọc. Đọc tiếng Việt thường nhanh hơn đọc ngoại ngữ."),
   "Để so sánh: người lớn đọc thường khoảng hai trăm đến hai trăm năm mươi từ một phút, sinh viên đại học khoảng ba trăm. Đọc tiếng Việt thường nhanh hơn đọc ngoại ngữ, nhưng phần cải thiện thì vẫn đo được như nhau."),
  ("list", 13.0, ("Việc cần làm · tự đo trước", [
    "Làm bài test 60 giây, ghi lại mốc bạn dừng",
    "Luyện 15 phút mỗi ngày theo kỹ thuật",
    "Đo lại sau 14 ngày và ghi lại con số mới"], None),
   "Việc cần làm: tự đo trước bằng một bài test sáu mươi giây và ghi lại mốc bạn dừng. Luyện mười lăm phút mỗi ngày, rồi đo lại sau mười bốn ngày."),
  ("list", 14.0, ("Luyện đúng ba thứ", [
    "Bỏ đọc thầm từng chữ — đọc theo cụm",
    "Dùng tay hoặc bút dẫn mắt theo dòng",
    "Đọc lặp lại một bài quen để đo tốc độ"], None),
   "Ba thứ cần luyện: bỏ đọc thầm từng chữ và đọc theo cụm, dùng tay hoặc bút dẫn mắt, và đọc lặp lại một bài quen để đo tốc độ."),
  ("h1", 13.0, ("Thông điệp",
    "Tốc độ đọc<br>luyện <span class=\"hl\">được</span>",
    "Sinh viên trong nghiên cứu tăng 12 từ một phút sau 15 tuần — con số đo được."),
   "Thông điệp: tốc độ đọc luyện được. Sinh viên trong nghiên cứu tăng mười hai từ một phút sau mười lăm tuần, và đó là con số đo được, không phải lời hứa."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom", [
    "Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
    "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
    "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Ba thứ cần luyện ở trên là nội dung hai buổi đầu của khoá. Khoá bảy buổi Zoom, học phí chín trăm tám mươi nghìn đồng, hoàn phí nếu sau buổi một bạn thấy không hợp."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

# ------------------------------------------------- TẬP DỰNG LẠI THEO ĐỊNH DẠNG SÁU PHẦN
# 19 tập dưới đây thay cho bản 45 giây cũ (không còn trong tệp này).
T02 = dua_tap(
 "02_noi-tham-trong-dau", "Nỗi thầm trong đầu", [
  ("h1", 9.0, ("Đọc thầm trong đầu",
    'Mắt bạn chạy nhanh<br>hơn <span class="hl">miệng bạn</span>',
    "Có một giọng đọc đang chạy trong đầu bạn — và nó chậm hơn bạn tưởng."),
   "Bạn đọc chậm không phải vì mắt, mà vì một giọng đọc đang chạy trong đầu."),
  ("list", 12.0, ("Biết điều này bạn được gì", [
    "Đọc nhanh gấp đôi mà không phải cố thêm",
    "Hiểu vì sao mãi không vượt tốc độ cũ",
    "Biết đúng chỗ cần sửa: bỏ tiếng nói trong đầu"],
    "Một thay đổi nhỏ, tốc độ đổi khác."),
   "Biết cơ chế này, bạn đọc nhanh gấp đôi mà không phải cố gắng thêm, và biết đúng chỗ cần sửa."),
  ("h1", 14.0, ("Vì sao lại như vậy",
    'Não đọc bằng cách<br><span class="hl">nghe lại từng chữ</span>',
    "Chữ chưa được phát âm thì não chưa nhận."),
   "Não đọc bằng cách nghe lại từng chữ. Chữ nào chưa được phát âm trong đầu thì não chưa nhận là đã đọc."),
  ("list", 13.0, ("Hai tốc độ trong cùng một người", [
    "Mắt nhận được khoảng hai trăm từ một phút",
    "Giọng đọc trong đầu chạy chậm hơn thế",
    "Chênh lệch đó là phần tốc độ bị mất"],
    "Mắt nhanh, miệng chậm — đọc bị khoá ở tốc độ của miệng."),
   "Mắt bạn nhận được khoảng hai trăm từ một phút. Nhưng giọng đọc trong đầu thì chậm hơn nhiều, và nó khoá tốc độ đọc của bạn lại."),
  ("list", 13.0, ("Vì sao giọng trong đầu chặn bạn", [
    "Bạn không thể đọc nhanh hơn nhịp phát âm",
    "Nhịp phát âm chậm hơn tốc độ của mắt",
    "Nên giọng trong đầu là nút chặn tốc độ"], None),
   "Bạn không thể đọc nhanh hơn nhịp phát âm trong đầu. Vì nhịp đó chậm hơn tốc độ của mắt, nên chính nó là nút chặn tốc độ đọc."),
  ("list", 13.0, ("Bước 1 · đọc nhanh hơn nhịp nói", [
    "Tăng tốc đọc vượt tốc độ đọc thành tiếng",
    "Để giọng trong đầu không theo kịp, rồi tự tắt",
    "Còn nghe từng chữ là chưa tắt được"], None),
   "Bước một: tăng tốc đọc vượt tốc độ đọc thành tiếng. Khi nhanh hơn nhịp nói, giọng trong đầu không theo kịp và tự tắt."),
  ("list", 13.0, ("Bước 2 · tự kiểm trong lúc đọc", [
    "Tự hỏi: có đang nghe từng chữ không?",
    "Còn nghe rõ từng tiếng là chưa bỏ được",
    "Chậm lại một chút rồi tăng tốc lần nữa"], None),
   "Bước hai: tự kiểm trong lúc đọc. Còn nghe rõ từng tiếng trong đầu nghĩa là bạn chưa bỏ được, hãy tăng tốc thêm một chút."),
  ("list", 13.0, ("Bước 3 · luyện mỗi ngày năm phút", [
    "Mỗi ngày luyện năm phút trên một bài quen",
    "Đọc bằng mắt, không đọc bằng miệng",
    "Sau vài ngày, tốc độ mới thành thói quen"], None),
   "Bước ba: mỗi ngày luyện năm phút trên một bài quen, đọc bằng mắt chứ không đọc bằng miệng. Vài ngày là thành thói quen."),
  ("h1", 13.0, ("Thông điệp",
    'Bỏ tiếng nói,<br>tốc độ <span class="hl">tăng gấp đôi</span>',
    "Mắt đã đủ nhanh — việc còn lại là để mắt tự đọc."),
   "Thông điệp: mắt bạn đã đủ nhanh. Bỏ giọng đọc trong đầu thì tốc độ tăng gấp đôi, và việc còn lại chỉ là để mắt tự đọc."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom", [
    "Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
    "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
    "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Nguyên lý bỏ đọc thầm này là nội dung buổi thứ hai của khoá. Khoá bảy buổi Zoom, học phí chín trăm tám mươi nghìn đồng, hoàn phí nếu sau buổi một bạn thấy không hợp."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

T03 = dua_tap(
 "03_bieu-do-tri-quen", "Biểu đồ trí quên", [
  ("h1", 9.0, ("Biểu đồ trí quên",
    'Học xong một ngày<br>đã mất <span class="hl">một nửa</span>',
    "Không phải trí nhớ kém — đó là cách trí nhớ vốn hoạt động."),
   "Học xong một ngày, bạn đã mất một nửa. Đó không phải lỗi của trí nhớ kém."),
  ("list", 12.0, ("Biết đường rơi để chặn lại", [
    "Biết trí nhớ rơi lúc nào, rơi bao nhiêu",
    "Có ba mốc ôn để giữ gần nguyên vẹn",
    "Không phải học lại từ đầu mỗi lần quên"],
    "Chặn được đường rơi thì học một lần là đủ."),
   "Biết trí nhớ rơi vào lúc nào và rơi bao nhiêu, bạn dùng ba mốc ôn để giữ lại gần như nguyên vẹn."),
  ("h1", 14.0, ("Đường quên có hình dạng",
    'Trí nhớ rơi<br><span class="hl">nhanh nhất ngày đầu</span>',
    "Đường quên được vẽ từ năm một tám tám năm."),
   "Đường quên được vẽ từ năm một tám tám năm. Nó rơi nhanh nhất ngay ngày đầu, rồi chậm dần về sau."),
  ("list", 13.0, ("Số còn lại theo từng ngày", [
    "Ngày một: còn khoảng năm mươi phần trăm",
    "Ngày hai: ba mươi bảy phần trăm",
    "Ngày bốn: mười tám phần trăm",
    "Ngày bảy: dưới mười phần trăm"],
    "Số liệu từ biểu đồ trí quên, năm một tám tám năm."),
   "Sau một ngày còn khoảng năm mươi phần trăm. Ngày hai còn ba mươi bảy. Ngày bốn còn mười tám. Tới ngày bảy thì dưới mười phần trăm."),
  ("list", 13.0, ("Vì sao phải ôn ngay hôm sau", [
    "Rơi mạnh nhất là trong ngày đầu",
    "Lần ôn sớm nhất đáng giá nhất",
    "Để vài ngày mới xem lại là đã muộn"], None),
   "Rơi mạnh nhất là trong ngày đầu. Nên lần ôn đáng giá nhất là ngay hôm sau, chứ không phải để vài ngày sau mới xem lại."),
  ("list", 13.0, ("Mốc 1 · ngày hôm sau", [
    "Xem lại năm phút vào ngày hôm sau",
    "Đọc lại phần ghi, không đọc lại cả bài",
    "Tự kể lại ý chính bằng miệng"], None),
   "Mốc thứ nhất: xem lại năm phút vào ngày hôm sau. Đọc lại phần ghi của bạn, rồi tự kể lại ý chính bằng miệng."),
  ("list", 13.0, ("Mốc 2 · ngày thứ ba", [
    "Xem lại lần hai vào ngày thứ ba",
    "Mỗi lần chỉ khoảng năm phút",
    "Chỗ nào quên thì mở đúng chỗ đó"], None),
   "Mốc thứ hai: xem lại vào ngày thứ ba, cũng khoảng năm phút. Chỗ nào quên thì mở đúng chỗ đó, đừng đọc lại cả bài."),
  ("list", 13.0, ("Mốc 3 · ngày thứ sáu", [
    "Xem lại lần ba vào ngày thứ sáu",
    "Đến đây trí nhớ giữ gần như nguyên vẹn",
    "Ba mốc là đủ để chặn đường rơi"], None),
   "Mốc thứ ba: xem lại vào ngày thứ sáu. Ba mốc một, ba, sáu là đủ để chặn đường rơi và giữ trí nhớ gần như nguyên vẹn."),
  ("h1", 13.0, ("Thông điệp",
    'Học một lần rồi quên<br>hay ôn ba lần <span class="hl">để nhớ</span>',
    "Chọn cách thứ hai: ôn ba lần để nhớ mãi."),
   "Học một lần rồi quên dần, hay ôn ba lần để nhớ mãi. Đường rơi không đổi, nhưng bạn chọn được cách đứng lại trên nó."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom", [
    "Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
    "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
    "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Lịch ôn ba mốc này được kèm theo từng buổi trong khoá. Khoá có bảy buổi Zoom, học phí chín trăm tám mươi nghìn đồng, hoàn phí nếu sau buổi một bạn thấy không hợp."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

T04 = dua_tap(
 "04_nao-giu-5-10-phut", "Não chỉ giữ được 5–10 phút", [
  ("h1", 9.0, ("Não chỉ giữ 5–10 phút",
    'Đọc liền hai tiếng<br>nhớ được <span class="hl">bao nhiêu</span>?',
    "Thường chỉ còn đoạn cuối — không phải bạn lười."),
   "Bạn ngồi đọc liền hai tiếng. Hỏi lại thì phần lớn đã biến mất, chỉ còn nhớ đoạn cuối."),
  ("list", 12.0, ("Biết giới hạn này để làm gì", [
    "Chia buổi đọc cho khớp trí nhớ tạm thời",
    "Cuối buổi còn nguyên bản đồ nội dung",
    "Đọc ít hơn mà nhớ nhiều hơn"],
    "Đọc theo khối mười phút thay vì đọc một mạch."),
   "Biết giới hạn năm tới mười phút, bạn chia buổi đọc thành từng khối, và cuối buổi còn nguyên bản đồ nội dung."),
  ("h1", 14.0, ("Trí nhớ tạm thời rất ngắn",
    'Não chỉ giữ<br><span class="hl">năm tới mười phút</span>',
    "Phần cũ bị đẩy ra để lấy chỗ cho phần mới."),
   "Trí nhớ tạm thời của não chỉ giữ được khoảng năm tới mười phút. Phần ghi trước đó bị đẩy ra để lấy chỗ cho phần mới đang vào."),
  ("list", 13.0, ("Vì sao đọc một mạch lại phí", [
    "Đọc càng lâu, phần đầu càng bị đẩy ra",
    "Ngồi hai tiếng thường chỉ nhớ đoạn cuối",
    "Không phải bạn lười — trí nhớ tạm thời có hạn"], None),
   "Đọc càng lâu thì phần đầu càng bị đẩy ra. Vì vậy ngồi hai tiếng đọc một mạch thường chỉ còn nhớ đoạn cuối."),
  ("list", 13.0, ("Vì sao phải ghi ngay", [
    "Ghi lại là lúc đưa nội dung ra khỏi trí nhớ tạm",
    "Khối sau không xoá mất khối trước",
    "Một dòng là đủ, không cần chép cả câu"], None),
   "Ghi lại một dòng ngay sau mỗi khối là lúc bạn đưa nội dung ra khỏi trí nhớ tạm thời, để khối sau không xoá mất khối trước."),
  ("list", 13.0, ("Bước 1 · chia khối mười phút", [
    "Chia buổi đọc thành từng khối mười phút",
    "Mỗi khối một chủ đề hoặc một mục",
    "Đặt báo hết khối trước khi bắt đầu"], None),
   "Bước một: chia buổi đọc thành từng khối mười phút, mỗi khối một chủ đề, và đặt báo để biết khi nào hết khối."),
  ("list", 13.0, ("Bước 2 · ghi một dòng mỗi khối", [
    "Hết mỗi khối, ghi lại một dòng",
    "Một dòng là ý chính, không chép cả câu",
    "Ghi xong mới sang khối tiếp theo"], None),
   "Bước hai: hết mỗi khối, ghi lại một dòng ý chính, không chép cả câu. Ghi xong rồi mới sang khối tiếp theo."),
  ("list", 13.0, ("Bước 3 · lắp thành bản đồ", [
    "Cuối buổi, xếp các dòng thành một bản đồ",
    "Nhìn một lượt là thấy cả buổi đọc",
    "Chỗ nào trống là chỗ bạn cần xem lại"], None),
   "Bước ba: cuối buổi, xếp các dòng lại thành một bản đồ. Nhìn một lượt là thấy cả buổi đọc, chỗ nào trống là chỗ cần xem lại."),
  ("h1", 13.0, ("Thông điệp",
    'Đọc ít hơn<br>mà <span class="hl">nhớ nhiều hơn</span>',
    "Đọc theo khối, ghi theo khối — thay vì đọc một mạch."),
   "Thông điệp: đọc ít hơn mà nhớ nhiều hơn. Chia khối và ghi lại để trí nhớ tạm thời không phải giữ quá sức."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom", [
    "Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
    "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
    "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Cách đọc theo khối mười phút này là nội dung trong khoá. Khoá có bảy buổi Zoom, học phí chín trăm tám mươi nghìn đồng, và hoàn phí nếu sau buổi một bạn thấy không hợp."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

T08 = dua_tap(
 "08_truong-nhin", "Trường nhìn: đọc cả cụm", [
  ("h1", 9.0, ("Trường nhìn khi đọc",
    'Mắt chỉ nhìn rõ<br><span class="hl">một chữ</span> một lúc',
    "Nhưng quanh chữ đó, não vẫn nhận ra chữ khác."),
   "Mắt bạn chỉ nhìn rõ được một chữ tại một thời điểm. Nhưng quanh nó, não vẫn nhận ra chữ."),
  ("list", 12.0, ("Mở rộng trường nhìn được gì", [
    "Một lần dừng mắt nhận ba tới năm chữ",
    "Ít lần dừng hơn nên đọc nhanh hơn",
    "Đây là nền tảng của đọc cụm"],
    "Đọc cụm bắt đầu từ việc mở rộng vùng nhìn rõ."),
   "Mở rộng trường nhìn thì một lần dừng mắt nhận được ba tới năm chữ thay vì một chữ, nên số lần dừng giảm."),
  ("h1", 14.0, ("Vùng nhìn rõ rất nhỏ",
    'Vùng nhìn rõ<br>chỉ bằng <span class="hl">hạt đậu</span>',
    "Quanh nó là vùng mờ — nhưng não vẫn nhận ra chữ."),
   "Vùng nhìn rõ của mắt rất nhỏ, chỉ bằng hạt đậu. Quanh nó là vùng mờ, nhưng não vẫn nhận ra chữ trong vùng đó."),
  ("list", 13.0, ("Mỗi lần dừng được mấy chữ", [
    "Chỉ dùng vùng nhỏ: mỗi chữ một lần dừng",
    "Dùng cả vùng rộng: một lần dừng ba tới năm chữ",
    "Cùng đôi mắt, khác số lần dừng"], None),
   "Nếu bạn chỉ dùng vùng nhỏ thì mỗi chữ là một lần dừng mắt. Dùng cả vùng rộng hơn thì một lần dừng được ba tới năm chữ."),
  ("list", 13.0, ("Vùng nhận chữ mở rộng được", [
    "Vùng nhận dạng chữ luyện rộng được",
    "Rộng dần từng chút, không cần gắng",
    "Đây là nền tảng của đọc cụm"], None),
   "Vùng nhận dạng chữ mở rộng được bằng luyện tập, mỗi lần rộng thêm một chút. Đó là nền tảng của đọc cụm."),
  ("list", 13.0, ("Bước 1 · nhìn cả cụm ba chữ", [
    "Đặt mắt vào giữa cụm ba chữ",
    "Cố nhận cả cụm trong một lần dừng",
    "Không đọc từng chữ trong cụm"], None),
   "Bước một: đặt mắt vào giữa một cụm ba chữ, và cố nhận cả cụm trong một lần dừng, chứ đừng đọc từng chữ."),
  ("list", 13.0, ("Bước 2 · rộng dần lên năm chữ", [
    "Quen cụm ba chữ thì tăng lên năm chữ",
    "Giữ mắt ở giữa cụm, đừng kéo sang hai đầu",
    "Mỗi ngày luyện vài phút"], None),
   "Bước hai: khi đã quen cụm ba chữ thì tăng lên năm chữ, vẫn giữ mắt ở giữa cụm và mỗi ngày luyện vài phút."),
  ("list", 13.0, ("Bước 3 · kiểm trên bài quen", [
    "Lấy một bài đã đọc, đọc lại theo cụm",
    "Đếm số lần dừng mắt trên một dòng",
    "Số lần dừng giảm là trường nhìn rộng ra"], None),
   "Bước ba: lấy một bài đã đọc và đọc lại theo cụm, đếm số lần dừng mắt trên một dòng. Số lần dừng giảm là trường nhìn đang rộng ra."),
  ("h1", 13.0, ("Thông điệp",
    'Đọc cả cụm<br>thay vì <span class="hl">từng chữ</span>',
    "Một lần dừng mắt, ba tới năm chữ."),
   "Thông điệp: đọc cả cụm thay vì từng chữ. Một lần dừng mắt nhận ba tới năm chữ thì tốc độ tăng mà mắt không phải làm việc nhiều hơn."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom", [
    "Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
    "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
    "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Mở rộng trường nhìn là bài tập đầu tiên trong buổi hai của khoá. Khoá có bảy buổi Zoom, học phí chín trăm tám mươi nghìn đồng, hoàn phí nếu sau buổi một bạn thấy không hợp."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

T09 = dua_tap(
 "09_quyluat-8020", "Quy luật 80/20 khi đọc sách", [
  ("h1", 9.0, ("Quy luật 80/20 khi đọc",
    'Giá trị nằm ở<br><span class="hl">hai mươi phần trăm</span> số trang',
    "Tức là hai trang trên mười."),
   "Tám mươi phần trăm giá trị của một quyển sách nằm ở hai mươi phần trăm số trang."),
  ("list", 12.0, ("Biết quy luật này được gì", [
    "Đọc hai mươi phần trăm trước, rồi quyết định",
    "Không mất một buổi cho phần ít giá trị",
    "Đọc xong một quyển trong hai buổi tối"],
    "Đọc đúng chỗ trước, rồi mới đọc tiếp nếu cần."),
   "Biết quy luật này, bạn đọc hai mươi phần trăm trước rồi mới quyết định có đọc tiếp hay không, thay vì đọc hết."),
  ("h1", 14.0, ("Hai trang trên mười",
    'Hai mươi phần trăm<br>là <span class="hl">hai trang trên mười</span>',
    "Đọc hết mười trang là bỏ phí tám trang."),
   "Hai mươi phần trăm nghĩa là hai trang trên mười. Đọc hết cả mười trang thì tám trang trong đó là phần ít giá trị nhất."),
  ("list", 13.0, ("Bốn chỗ giá trị nhất", [
    "Phần mở đầu của sách",
    "Mục lục",
    "Các tiêu đề",
    "Đoạn đầu và cuối mỗi chương"],
    "Bốn chỗ này là phần đáng đọc trước."),
   "Bốn chỗ luôn có giá trị nhất: phần mở đầu, mục lục, các tiêu đề, và đoạn đầu cùng đoạn cuối của mỗi chương."),
  ("list", 13.0, ("Vì sao bốn chỗ đó đắt giá", [
    "Tiêu đề và mục lục cho biết sách nói về gì",
    "Đoạn đầu và cuối mỗi chương giữ ý chính",
    "Phần giữa thường chỉ để chứng minh, ví dụ"], None),
   "Tiêu đề và mục lục cho biết cả quyển sách nói về gì. Đoạn đầu và đoạn cuối mỗi chương thường là chỗ chứa ý chính."),
  ("list", 13.0, ("Bước 1 · mở đầu và mục lục", [
    "Đọc phần mở đầu để biết sách giải quyết việc gì",
    "Xem mục lục, đánh dấu chương liên quan",
    "Chưa đọc thân bài"], None),
   "Bước một: đọc phần mở đầu và mục lục. Bạn biết sách giải quyết việc gì, và đánh dấu những chương liên quan tới nhu cầu của mình."),
  ("list", 13.0, ("Bước 2 · tiêu đề và đoạn đầu cuối", [
    "Đọc liền một mạch các tiêu đề của chương",
    "Với mỗi chương, đọc đoạn đầu và đoạn cuối",
    "Đánh dấu chỗ cần đọc kỹ hơn"], None),
   "Bước hai: đọc liền các tiêu đề của từng chương, rồi với mỗi chương đọc đoạn đầu và đoạn cuối. Đánh dấu chỗ bạn cần đọc kỹ."),
  ("list", 13.0, ("Bước 3 · rồi mới quyết định", [
    "Đọc xong hai mươi phần trăm, dừng lại",
    "Hỏi: phần còn lại có đáng đọc kỹ không",
    "Chỉ đọc tiếp chương bạn thật sự cần"], None),
   "Bước ba: đọc xong hai mươi phần trăm, dừng lại và hỏi phần còn lại có đáng đọc kỹ hay không. Chỉ đọc tiếp chương bạn thật sự cần."),
  ("h1", 13.0, ("Thông điệp",
    'Đọc đúng chỗ<br>trước khi <span class="hl">đọc hết</span>',
    "Hai mươi phần trăm trước, rồi mới quyết định."),
   "Thông điệp: đọc đúng chỗ trước khi đọc hết. Đọc hai mươi phần trăm đầu tiên, rồi mới quyết định có bỏ thời gian cho phần còn lại hay không."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom", [
    "Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
    "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
    "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Đọc hai mươi phần trăm trước là bước chọn sách trong khoá. Khoá có bảy buổi Zoom, học phí chín trăm tám mươi nghìn đồng, hoàn phí nếu sau buổi một bạn thấy không hợp."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

# -*- coding: utf-8 -*-
# Nhóm B — 5 tập viết theo bộ dựng sáu phần (dua_tap). KHÔNG sửa tệp nào trong repo.
# T06, T05, T10, T11, T12

# ------------------------------------------------- TẬP 06 — Kỹ thuật chỉ tay
T06 = dua_tap(
 "06_ky-thuat-chi-tay", "Kỹ thuật chỉ tay", [
  ("h1", 9.0, ("Kỹ thuật chỉ tay",
    "Mắt không tự đi nhanh<br>Nó cần <span class=\"hl\">vật dẫn đường</span>",
    "Không phải ý chí — mắt cần một mốc để bám."),
   "Mắt bạn không tự biết đi nhanh. Nó cần một vật dẫn đường."),
  ("list", 13.0, ("Vì sao mắt hay chậm lại", [
    "Mắt nhảy ngược lên dòng trên",
    "Dòng dài, không có mốc để bám",
    "Nhịp đọc lúc nhanh lúc chậm"], None),
   "Đọc một mình, mắt bạn hay nhảy ngược lên dòng trên. Dòng dài mà không có mốc, nên nhịp đọc lúc nhanh lúc chậm."),
  ("list", 13.0, ("Có vật dẫn thì được gì", [
    "Nhịp đọc đều, không nhảy dòng",
    "Tăng tốc mà vẫn bám đúng dòng",
    "Kiểm soát được lúc nào nhanh, lúc nào chậm"],
    "Một ngón tay, ba thay đổi đo được trong buổi đầu."),
   "Có một ngón tay dẫn đường, nhịp đọc của bạn đều hơn, mắt không nhảy dòng, và bạn kiểm soát được tốc độ."),
  ("h1", 14.0, ("Vì sao tay kéo được mắt",
    "Mắt vốn bám theo<br><span class=\"hl\">vật chuyển động</span>",
    "Không phải mẹo vặt — đây là cách mắt hoạt động."),
   "Cách này hiệu quả vì mắt vốn bám theo vật chuyển động. Ngón tay di chuyển thì mắt tự đi theo."),
  ("list", 13.0, ("Ngón tay còn làm một việc nữa", [
    "Mắt có xu hướng nhảy lại dòng trên",
    "Ngón tay chặn đúng chỗ đó",
    "Nên mắt đi một chiều, không lùi"], None),
   "Ngón tay còn ngăn mắt nhảy ngược lên dòng trên. Mắt đi một chiều theo tay, không lùi lại, nên đọc liền mạch hơn."),
  ("list", 14.0, ("Việc cần làm · bước một và hai", [
    "Đặt ngón tay dưới dòng đang đọc",
    "Trượt theo đúng nhịp đọc hiện tại",
    "Để mắt bám theo ngón tay"], None),
   "Đặt ngón tay dưới dòng chữ và trượt theo đúng nhịp đọc hiện tại của bạn. Mắt sẽ tự bám theo ngón tay."),
  ("list", 14.0, ("Việc cần làm · bước ba", [
    "Đếm ba, hai, một trong đầu",
    "Trượt nhanh hơn một chút mỗi lần",
    "Nhịp tay kéo mắt đi theo"], None),
   "Sau đó tăng dần. Đếm ba, hai, một, rồi trượt nhanh hơn một chút. Nhịp tay sẽ kéo mắt bạn đi theo."),
  ("h1", 13.0, ("Thông điệp",
    "Chỉ cần<br><span class=\"hl\">một ngón tay</span>",
    "Không cần công cụ gì thêm."),
   "Thông điệp: chỉ cần một ngón tay. Kỹ thuật này có trong buổi đầu tiên của khoá đọc hiệu quả."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom", [
    "Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
    "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
    "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Kỹ thuật chỉ tay này nằm trong buổi đầu của khoá. Khoá bảy buổi Zoom, học phí chín trăm tám mươi nghìn đồng, hoàn phí sau buổi một nếu bạn thấy không hợp."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

# ------------------------------------------------- TẬP 05 — Con bỏ sách: phụ huynh làm gì
T05 = dua_tap(
 "05_phuhuynh-con-bo-sach", "Con bỏ sách: phụ huynh làm gì", [
  ("h1", 9.0, ("Phụ huynh · con bỏ sách",
    "Con đọc hai trang<br>rồi <span class=\"hl\">đặt sách xuống</span>",
    "Không phải vì con lười."),
   "Con đọc hai trang rồi đặt sách xuống. Không phải vì con lười."),
  ("list", 13.0, ("Ba yếu tố khiến con buông sách", [
    "Gánh nặng nhận thức",
    "Thiếu phần thưởng tức thì",
    "Ảnh hưởng của môi trường"], None),
   "Có ba yếu tố: gánh nặng nhận thức, thiếu phần thưởng tức thì, và ảnh hưởng của môi trường xung quanh."),
  ("list", 13.0, ("Hiểu đúng thì được gì", [
    "Bỏ cách trách con lười",
    "Sửa đúng chỗ thay vì ép đọc",
    "Đặt thời lượng đọc hợp độ tuổi"],
    "Ba yếu tố, ba chỗ để sửa — không phải ép con ngồi lâu."),
   "Hiểu đúng ba yếu tố này, bạn bỏ cách trách con lười và sửa đúng chỗ thay vì ép con ngồi lâu."),
  ("h1", 14.0, ("Vì sao não trẻ chọn điện thoại",
    "Não luôn chọn<br><span class=\"hl\">kết quả nhanh</span>",
    "Điện thoại thưởng ngay, sách thì thưởng chậm."),
   "Điện thoại cho phần thưởng ngay lập tức, còn sách thì không. Não trẻ luôn chọn cái cho kết quả nhanh."),
  ("list", 14.0, ("Con tập trung được bao lâu", [
    "Sáu tới tám tuổi: mười tới mười lăm phút",
    "Chín tới mười một tuổi: hai mươi tới ba mươi phút",
    "Quá ngưỡng đó thì con buông sách"], None),
   "Bé sáu tới tám tuổi chỉ tập trung được mười tới mười lăm phút. Chín tới mười một tuổi thì hai mươi tới ba mươi phút."),
  ("list", 14.0, ("Việc cần làm · trước khi đọc", [
    "Kể câu chuyện trước khi cho con đọc",
    "Mỗi lần năm tới mười phút",
    "Chia nhỏ thay vì ngồi liền"], None),
   "Kể câu chuyện trước khi cho con đọc, mỗi lần năm tới mười phút. Chia thành nhiều lần thay vì bắt con ngồi liền một mạch."),
  ("list", 14.0, ("Việc cần làm · cả nhà cùng đọc", [
    "Cả nhà cùng ngồi đọc, không màn hình",
    "Người lớn đọc trước để con bắt chước",
    "Để sách ở chỗ con hay ngồi"], None),
   "Và cả nhà cùng ngồi đọc. Người lớn đọc trước để con bắt chước, và để sách ở chỗ con hay ngồi."),
  ("h1", 13.0, ("Thông điệp",
    "Con không lười —<br>con đang <span class=\"hl\">bị kéo</span>",
    "Đổi phần thưởng và thời lượng thì con đọc tiếp."),
   "Thông điệp: con không lười, con đang bị kéo bởi việc cho kết quả nhanh hơn. Đổi phần thưởng và thời lượng thì con đọc tiếp."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom", [
    "Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
    "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
    "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Phần thưởng, thời lượng và môi trường là những gì tôi hướng dẫn phụ huynh trong khoá. Khoá bảy buổi Zoom, học phí chín trăm tám mươi nghìn đồng, hoàn phí sau buổi một."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

# ------------------------------------------------- TẬP 10 — Điểm dừng của mắt
T10 = dua_tap(
 "10_diem-dung-cua-mat", "Điểm dừng của mắt", [
  ("h1", 9.0, ("Điểm dừng của mắt",
    "Mắt không đọc cả dòng<br>— mắt <span class=\"hl\">nhảy từng chữ</span>",
    "Đọc không phải một đường thẳng liền mạch."),
   "Mắt bạn không đọc cả dòng. Mắt nhảy từng chữ một."),
  ("list", 13.0, ("Mỗi chữ là một lần dừng", [
    "Sáu chữ, mắt dừng sáu lần",
    "Mỗi lần chỉ nhận được một chữ",
    "Dừng càng nhiều, đọc càng chậm"], None),
   "Sáu chữ, mắt phải dừng sáu lần. Mỗi lần chỉ nhận được một chữ. Dừng càng nhiều thì đọc càng chậm."),
  ("list", 13.0, ("Đọc theo cụm thì được gì", [
    "Sáu chữ chỉ còn hai lần dừng",
    "Mắt nhận ba từ mỗi lần dừng",
    "Tốc độ tăng mà không đọc thêm"],
    "Cùng số chữ, khác số lần dừng là khác tốc độ."),
   "Đọc theo cụm ba từ, sáu chữ chỉ còn hai lần dừng. Mỗi lần mắt nhận được ba từ, nên tốc độ tăng."),
  ("h1", 14.0, ("Vì sao dừng ít lại nhanh hơn",
    "Ít điểm dừng<br>— <span class=\"hl\">ít thời gian chết</span>",
    "Giữa hai lần dừng, mắt gần như không nhận gì."),
   "Tốc độ đọc phụ thuộc số lần dừng, không phải số chữ. Giữa hai lần dừng, mắt gần như không nhận thêm gì."),
  ("thanh", 14.0, ("Hai cách đọc cùng một dòng", [
    ("Dừng từng chữ", "nhiều lần dừng"),
    ("Đọc cụm ba từ", "ít lần dừng")],
    "Hai con số hai trăm năm mươi và bốn trăm năm mươi từ một phút là minh hoạ."),
   "Hai con số hai trăm năm mươi và bốn trăm năm mươi từ một phút là minh hoạ cho khoảng cách này."),
  ("list", 14.0, ("Việc cần làm · tập nhìn cụm", [
    "Trượt mắt theo cụm ba từ",
    "Đừng đọc từng chữ một",
    "Gom cụm theo nghĩa, không theo số"], None),
   "Việc cần làm: tập cho mắt trượt theo cụm ba từ thay vì từng chữ, và gom cụm theo nghĩa chứ đừng đếm chữ."),
  ("list", 14.0, ("Việc cần làm · đo lại", [
    "Đọc một đoạn quen, đếm số lần dừng",
    "Tăng dần cụm: ba, rồi bốn, rồi năm",
    "Đo lại tốc độ sau mỗi tuần"], None),
   "Đọc một đoạn quen rồi đếm số lần mắt dừng. Tăng dần cụm lên ba, bốn, năm từ, và đo lại tốc độ mỗi tuần."),
  ("h1", 13.0, ("Thông điệp",
    "Đọc nhanh hơn bắt đầu<br>từ <span class=\"hl\">điểm dừng</span>",
    "Bớt điểm dừng thì tốc độ lên — không cần đọc thêm chữ."),
   "Thông điệp: muốn nhanh hơn thì giảm số điểm dừng, chứ không phải đọc thêm chữ."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom", [
    "Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
    "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
    "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Đọc cụm là kỹ thuật đầu tiên trong khoá. Khoá bảy buổi Zoom, học phí chín trăm tám mươi nghìn đồng, hoàn phí sau buổi một nếu bạn thấy không hợp."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

# ------------------------------------------------- TẬP 11 — Đọc ngắt quãng mất mạch hiểu
T11 = dua_tap(
 "11_doc-ngat-quang", "Đọc ngắt quãng mất mạch hiểu", [
  ("h1", 9.0, ("Đọc ngắt quãng · mạch hiểu",
    "Đọc mười phút, nghỉ mười phút<br>— mạch hiểu <span class=\"hl\">đứt</span>",
    "Nghe hợp lý, nhưng tốn hơn bạn nghĩ."),
   "Đọc mười phút rồi nghỉ mười phút. Nghe hợp lý, nhưng mạch hiểu bị đứt."),
  ("list", 13.0, ("Giữ mạch hiểu thì được gì", [
    "Hiểu sâu hơn, không phải đọc lại",
    "Nhớ nội dung chính tới cuối buổi",
    "Đọc xong kể lại được mạch chính"], None),
   "Giữ được mạch hiểu, bạn hiểu sâu hơn và nhớ nội dung chính tới cuối buổi, thay vì đọc lại từ đầu."),
  ("thanh", 13.0, ("Cùng ba mươi phút, hai cách", [
    ("Đọc liền một mạch", "một mạch hiểu"),
    ("Chia ba lần, có nghỉ", "ba lần đứt")],
    "Hai cột này là minh hoạ, không phải số đo của bạn."),
   "Cùng ba mươi phút: đọc liền một mạch, hoặc chia ba lần mà giữa mỗi lần có khoảng nghỉ."),
  ("h1", 14.0, ("Vì sao nghỉ lại cắt mạch",
    "Mỗi khoảng nghỉ<br>là một lần <span class=\"hl\">đứt mạch</span>",
    "Não phải dựng lại mạch hiểu từ đầu sau mỗi lần nghỉ."),
   "Nghỉ giữa chừng cắt đứt mạch hiểu. Quay lại, não phải dựng lại mạch từ đầu, mất thêm thời gian."),
  ("list", 14.0, ("Nghỉ nhiều lần thì mất gì", [
    "Ba lần đọc, ba lần dựng lại mạch",
    "Càng dựng lại, càng dễ bỏ dở",
    "Đọc xong không kể lại được gì"], None),
   "Chia ba lần là ba lần dựng lại mạch. Càng dựng lại, bạn càng dễ bỏ dở, và đọc xong không kể lại được gì."),
  ("list", 14.0, ("Việc cần làm · đọc liền 25 phút", [
    "Đọc liền hai mươi lăm phút",
    "Nghỉ năm phút, không hơn",
    "Đặt hẹn giờ để không tự ngắt"], None),
   "Cách sửa: đọc liền hai mươi lăm phút, nghỉ năm phút thôi. Đặt hẹn giờ để không tự ngắt giữa chừng."),
  ("list", 14.0, ("Việc cần làm · ghi một câu chốt", [
    "Trước khi nghỉ, ghi một câu chốt",
    "Câu chốt là ý chính vừa đọc",
    "Quay lại đọc tiếp từ câu chốt đó"], None),
   "Trước khi nghỉ, ghi một câu chốt lại ý chính vừa đọc. Quay lại thì bắt đầu từ câu chốt đó mà đọc tiếp."),
  ("h1", 13.0, ("Thông điệp",
    "Đọc liền mạch<br>nhớ được <span class=\"hl\">cả bài</span>",
    "Đọc ngắt quãng thì chỉ nhớ đoạn cuối."),
   "Thông điệp: giữ mạch hiểu liền mạch thì nhớ được cả bài, chứ không chỉ đoạn cuối."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom", [
    "Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
    "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
    "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Giữ mạch hiểu là nguyên tắc thứ ba trong khoá. Khoá bảy buổi Zoom, học phí chín trăm tám mươi nghìn đồng, hoàn phí sau buổi một nếu bạn thấy không hợp."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

# ------------------------------------------------- TẬP 12 — Đọc nhanh gấp 2–3 lần
T12 = dua_tap(
 "12_gap-2-3-lan", "Đọc nhanh gấp 2–3 lần", [
  ("h1", 9.0, ("Đọc nhanh gấp 2–3 lần",
    "Mắt không chậm<br>Bạn chưa có <span class=\"hl\">phương pháp</span>",
    "Khác biệt nằm ở cách đọc, không ở con mắt."),
   "Mắt bạn không chậm. Bạn chỉ chưa có phương pháp."),
  ("list", 13.0, ("Đúng phương pháp thì được gì", [
    "Đọc gấp hai, hướng tới gấp ba",
    "Hiểu vẫn giữ nguyên, không lướt",
    "Ba việc cụ thể, không bí quyết chung chung"], None),
   "Đúng phương pháp, mục tiêu buổi đầu là gấp đôi, hướng tới gấp ba, mà hiểu vẫn giữ nguyên."),
  ("thanh", 13.0, ("Mắt đủ sức — nhưng bạn đang đọc", [
    ("Đang đọc", "khoảng hai trăm từ/phút"),
    ("Mắt đủ sức nhận", "khoảng năm trăm từ/phút")],
    "Số trên hình là minh hoạ."),
   "Mắt đủ sức nhận khoảng năm trăm từ một phút, nhưng bạn đang đọc khoảng hai trăm. Khoảng trống đó là do cách đọc."),
  ("h1", 14.0, ("Vì sao bạn đang đọc chậm",
    "Không phải mắt<br>mà là <span class=\"hl\">cách đọc</span>",
    "Ba thói quen cũ giữ tốc độ ở mức hai trăm."),
   "Mắt nhận chữ rất nhanh. Nhưng có ba thói quen cũ đang giữ tốc độ của bạn ở mức thấp."),
  ("list", 14.0, ("Ba thói quen giữ mắt lại", [
    "Đọc từng chữ, dừng quá nhiều",
    "Phát âm trong đầu từng từ",
    "Không có gì dẫn nhịp đọc"], None),
   "Đọc từng chữ nên dừng quá nhiều, phát âm từng từ trong đầu, và không có gì dẫn nhịp đọc."),
  ("list", 14.0, ("Việc cần làm · ba việc tạo tốc độ", [
    "Đọc theo cụm ba đến năm từ",
    "Bỏ phát âm trong đầu",
    "Để ngón tay dẫn mắt"], None),
   "Ba việc tạo ra tốc độ: đọc theo cụm ba đến năm từ, bỏ phát âm trong đầu, và để ngón tay dẫn mắt."),
  ("list", 14.0, ("Việc cần làm · ba chặng buổi đầu", [
    "Chặng một: đọc cụm",
    "Chặng hai: bỏ phát âm",
    "Chặng ba: tăng nhịp"], None),
   "Ba chặng trong buổi đầu: đọc cụm, rồi bỏ phát âm, rồi tăng nhịp. Số trên hình là minh hoạ."),
  ("h1", 13.0, ("Thông điệp",
    "Mục tiêu buổi đầu<br>là <span class=\"hl\">gấp đôi</span>",
    "Gấp ba là chặng sau, khi ba việc kia đã thành nếp."),
   "Thông điệp: mục tiêu của buổi đầu là gấp đôi. Gấp ba là chặng sau."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom", [
    "Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
    "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
    "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Ba việc này là nội dung buổi đầu của khoá. Lớp bảy buổi, học phí chín trăm tám mươi nghìn đồng, hoàn phí sau buổi một nếu bạn thấy không hợp."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

# ------------------------------------------------- TẬP 13 — chọn sách: đọc tiêu đề chính phụ trước
T13 = dua_tap(
 "13_tieude-chinh-phu", "Đọc tiêu đề chính phụ trước", [
  ("h1", 9.0, ("Chọn sách · bước đầu tiên",
    'Đọc hết cuốn sách<br>vẫn <span class="hl">không biết nó nói gì</span>',
    "Không phải bạn đọc chậm — bạn mở sách sai cửa."),
   "Bạn đọc hết một cuốn sách mà vẫn không biết nó nói về cái gì."),
  ("list", 12.0, ("Điều ai cũng gặp", [
    "Mở trang đầu và đọc từ đầu tới cuối",
    "Hết chương một vẫn chưa rõ sách nói gì",
    "Đọc tới nửa cuốn thì bỏ dở"], None),
   "Bạn mở trang đầu và đọc từ đầu tới cuối. Hết chương một vẫn chưa rõ cuốn sách nói gì. Đọc tới nửa cuốn thì bỏ dở."),
  ("list", 13.0, ("Đọc tiêu đề trước được gì", [
    "Biết cuốn sách nói gì trong khoảng năm phút",
    "Không đọc những chương mình không cần",
    "Quyết định mua hay để lại trước khi trả tiền"],
    "Ba bước · một lượt nhìn · chưa cần đọc chữ nào."),
   "Đọc tiêu đề trước cho bạn biết cuốn sách nói về cái gì trong khoảng năm phút, để bạn khỏi đọc những chương mình không cần."),
  ("h1", 13.0, ("Vì sao đọc tiêu đề lại đủ",
    'Tiêu đề chương là<br><span class="hl">bản tóm tắt viết sẵn</span>',
    "Tác giả đã tóm ý từng chương ngay ở dòng tiêu đề."),
   "Tiêu đề chương là bản tóm tắt mà tác giả đã viết sẵn. Đọc tiêu đề liền mạch là đọc lại bản tóm tắt của cả cuốn sách."),
  ("list", 13.0, ("Nhìn một trang sách từ xa", [
    "Dòng tiêu đề <b>đậm</b> — ý chính của chương",
    "Chữ nhỏ bên dưới — phần <b>chứng minh</b>",
    "Muốn biết sách nói gì, nhìn <b>phần đậm</b> trước"], None),
   "Nhìn một trang sách từ xa, bạn thấy những dòng tiêu đề đậm và phần chữ nhỏ bên dưới. Dòng đậm là ý chính, chữ nhỏ là phần chứng minh."),
  ("thanh", 13.0, ("Hai cách mở một cuốn sách", [
    ("Mở trang đầu đọc liền", "đọc theo dòng chữ"),
    ("Đọc tiêu đề trước", "nắm khung trước")],
    "Cùng năm phút, khác chỗ nhìn là khác kết quả."),
   "Mở trang đầu và đọc liền thì bạn đọc theo dòng chữ. Đọc tiêu đề trước thì bạn nắm cái khung của cuốn sách trước đã."),
  ("list", 13.0, ("Bước một và hai", [
    "Bìa và lời giới thiệu — sách hứa điều gì",
    "Mục lục — cuốn sách gồm chương nào",
    "Hai bước này bạn đã có khung cuốn sách"], None),
   "Bước một: đọc bìa và lời giới thiệu để biết sách hứa điều gì. Bước hai: xem mục lục để biết cuốn sách gồm những chương nào."),
  ("list", 13.0, ("Bước ba · đọc tiêu đề liền mạch", [
    "Lật từng chương, chỉ đọc dòng tiêu đề",
    "Đọc liền một mạch, không dừng ở chữ nhỏ",
    "Hết lượt, bạn có bản đồ nội dung cuốn sách"], None),
   "Bước ba: lật từng chương và chỉ đọc dòng tiêu đề, đọc liền một mạch, không dừng lại ở phần chữ nhỏ bên dưới."),
  ("h1", 13.0, ("Thông điệp",
    'Đọc tiêu đề trước là<br>đọc <span class="hl">bản đồ</span> trước',
    "Năm phút đọc tiêu đề thay cho hàng giờ đọc nhầm."),
   "Thông điệp: năm phút đọc tiêu đề cho bạn tấm bản đồ của cuốn sách, thay vì lạc trong đó hàng giờ."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom", [
    "Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
    "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
    "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Đọc tiêu đề trước là bước chọn sách trong khoá. Khoá có bảy buổi Zoom, học phí chín trăm tám mươi nghìn đồng, hoàn phí nếu sau buổi một bạn thấy không hợp."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

# ------------------------------------------------- TẬP 14 — bản đồ bốn lớp của một chương
T14 = dua_tap(
 "14_ban-do-4-lop", "Bản đồ 4 lớp của một chương", [
  ("h1", 9.0, ("Bốn lớp của một cuốn sách",
    'Sách có <span class="hl">bốn lớp</span><br>đa số chỉ chạm lớp cuối',
    "Đọc từ lớp ngoài vào, mười phút là biết có ích hay không."),
   "Một cuốn sách có bốn lớp. Nhưng đa số người đọc chỉ chạm tới lớp cuối cùng."),
  ("list", 12.0, ("Vì sao đọc hoài không vào", [
    "Đọc hai trăm trang rồi mới thấy <b>không dùng được</b>",
    "Cứ đọc từ trang một — <b>chưa nhìn cấu trúc</b>",
    "Bỏ cả tuần cho cuốn sách <b>không hợp</b>"], None),
   "Bạn đọc hai trăm trang rồi mới thấy cuốn sách không dùng được. Vì bạn cứ đọc từ trang một mà chưa nhìn cấu trúc."),
  ("list", 13.0, ("Bốn lớp cho bạn gì", [
    "Mười phút biết cuốn sách có ích hay không",
    "Chỉ đọc kỹ phần bạn cần dùng ngay",
    "Không tiếc một cuốn sách đã đọc dở"],
    "Ba lớp ngoài để quyết định · lớp trong để dùng."),
   "Bốn lớp này cho bạn biết trong mười phút cuốn sách có ích hay không, và chỉ đọc kỹ phần bạn cần dùng ngay."),
  ("h1", 13.0, ("Bốn lớp từ ngoài vào",
    'Ngoài là <span class="hl">quyết định</span><br>trong mới là chi tiết',
    "Bìa và lời giới thiệu, mục lục, tiêu đề chương, rồi mới tới chi tiết."),
   "Bốn lớp từ ngoài vào: bìa và lời giới thiệu, mục lục, tiêu đề từng chương, rồi mới tới chi tiết."),
  ("list", 13.0, ("Ba lớp đầu để quyết định", [
    "Bìa và lời giới thiệu — sách hứa gì",
    "Mục lục — các chương nói về việc gì",
    "Tiêu đề chương — bạn có cần không"], None),
   "Ba lớp đầu để bạn quyết định: cuốn sách hứa gì, các chương nói về việc gì, và bạn có cần nó hay không."),
  ("thanh", 13.0, ("Lớp ngoài và lớp trong", [
    ("Ba lớp ngoài", "đọc trước, quyết định nhanh"),
    ("Lớp chi tiết", "chỉ đọc phần cần dùng")],
    "Lớp trong là chỗ tốn thời gian nhất, nên để đọc sau cùng."),
   "Ba lớp ngoài đọc trước để quyết định nhanh. Lớp chi tiết là chỗ tốn thời gian nhất, nên chỉ đọc phần bạn cần dùng ngay."),
  ("list", 13.0, ("Đọc ba lớp ngoài trước", [
    "Lớp một: bìa và lời giới thiệu",
    "Lớp hai: mục lục, đọc hết một lượt",
    "Lớp ba: tiêu đề từng chương, đọc liền mạch"], None),
   "Đọc ba lớp ngoài trước: lớp một là bìa và lời giới thiệu, lớp hai là mục lục đọc hết một lượt, lớp ba là tiêu đề từng chương."),
  ("list", 13.0, ("Rồi mới tới lớp chi tiết", [
    "Chỉ mở phần bạn cần dùng ngay",
    "Đọc kỹ một đoạn, gấp sách kể lại",
    "Phần không cần thì để đó, không đọc"], None),
   "Rồi mới tới lớp chi tiết: chỉ mở phần bạn cần dùng ngay, đọc kỹ một đoạn rồi gấp sách kể lại. Phần không cần thì để đó."),
  ("h1", 13.0, ("Thông điệp",
    'Đọc từ ngoài vào<br>là <span class="hl">tiết kiệm thời gian</span>',
    "Mười phút ngoài lớp bìa rẻ hơn hai trăm trang đọc nhầm."),
   "Thông điệp: mười phút đọc từ lớp ngoài vào rẻ hơn nhiều so với đọc hai trăm trang rồi mới tiếc."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom", [
    "Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
    "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
    "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Bản đồ bốn lớp này là cách chọn sách tôi dạy trong buổi thứ hai của khoá. Khoá có bảy buổi Zoom, học phí chín trăm tám mươi nghìn đồng."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

# ------------------------------------------------- TẬP 15 — đọc nhanh khác đọc lướt
T15 = dua_tap(
 "15_doc-nhanh-vs-doc-luot", "Đọc nhanh khác đọc lướt", [
  ("h1", 9.0, ("Đọc nhanh và đọc lướt",
    'Đọc nhanh<br>không phải <span class="hl">đọc lướt</span>',
    "Hai cách này khác nhau ở một chỗ: còn hiểu hay không."),
   "Đọc nhanh và đọc lướt nhìn thì giống nhau, nhưng khác một chỗ: còn hiểu nội dung hay không."),
  ("list", 12.0, ("Cả hai đều nhanh hơn", [
    "Đọc nhanh — <b>vẫn kể được ý chính</b>",
    "Đọc lướt — <b>gấp lại là quên</b>",
    "Nhìn thì giống, kết quả khác hẳn"], None),
   "Cả hai cách đều nhanh hơn. Nhưng đọc nhanh thì gấp sách vẫn kể được ý chính, còn đọc lướt thì gấp lại là quên."),
  ("list", 13.0, ("Phân biệt được để làm gì", [
    "Biết mình đang đọc nhanh hay đang lướt",
    "Tăng tốc mà không mất nội dung",
    "Tự kiểm được ngay, không cần ai chấm"], None),
   "Phân biệt hai cách này giúp bạn biết mình đang đọc nhanh hay đang lướt, để tăng tốc mà không mất nội dung."),
  ("h1", 13.0, ("Vì sao chúng khác nhau",
    'Lướt thì <span class="hl">bỏ sót</span><br>nhanh thì <span class="hl">giữ nguyên ý</span>',
    "Đọc lướt bỏ ý chính. Đọc nhanh có phương pháp giữ nguyên ý, chỉ tăng tốc."),
   "Đọc lướt thì bỏ sót ý chính. Đọc nhanh có phương pháp thì giữ nguyên ý, chỉ tăng tốc độ."),
  ("list", 13.0, ("Cùng tăng tốc, khác kết quả", [
    "Đọc lướt: mắt chạy, não <b>không theo</b>",
    "Đọc nhanh: mắt chạy, não <b>vẫn bắt ý</b>",
    "Khác ở chỗ não có bám theo hay không"], None),
   "Khi lướt, mắt chạy nhanh nhưng não không theo kịp. Khi đọc nhanh, mắt cũng chạy nhưng não vẫn bắt được ý."),
  ("thanh", 13.0, ("Đọc lướt và đọc nhanh", [
    ("Đọc lướt", "nhanh nhưng trống"),
    ("Đọc nhanh", "nhanh mà vẫn hiểu")],
    "Hình minh hoạ định tính — khác nhau ở phần hiểu, không ở tốc độ."),
   "Đọc lướt thì nhanh nhưng trống. Đọc nhanh thì nhanh mà vẫn hiểu. Khác nhau ở phần hiểu, không phải ở tốc độ."),
  ("list", 13.0, ("Phép thử trong một phút", [
    "Đọc xong, gấp sách lại",
    "Kể ba ý chính, không nhìn sách",
    "Không kể được ba ý là bạn đang lướt"], None),
   "Đây là phép thử: đọc xong, gấp sách lại và kể ba ý chính. Không kể được ba ý là bạn đang lướt, không phải đọc nhanh."),
  ("list", 13.0, ("Quy tắc tự kiểm", [
    "Nhanh hơn mà <b>hiểu như cũ</b> — được",
    "Nhanh hơn mà <b>hiểu giảm</b> — đã lướt",
    "Hiểu giảm thì chậm lại, đọc lại đoạn đó"], None),
   "Quy tắc tự kiểm rất đơn giản: nhanh hơn mà hiểu như cũ thì được. Hễ hiểu giảm là bạn đã lướt, chậm lại một chút là về đúng."),
  ("h1", 13.0, ("Thông điệp",
    'Nhanh hơn<br>mà vẫn <span class="hl">hiểu như cũ</span>',
    "Đó là đường ranh giữa đọc nhanh và đọc lướt."),
   "Thông điệp: nhanh hơn mà vẫn hiểu như cũ thì là đọc nhanh. Hễ hiểu giảm thì đã lướt."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom", [
    "Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
    "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
    "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Phân biệt được hai cách này là điều kiện đầu tiên để luyện đọc nhanh. Khoá có bảy buổi Zoom, học phí chín trăm tám mươi nghìn đồng, hoàn phí sau buổi một."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

# ------------------------------------------------- TẬP 16 — năm câu hỏi trước khi mở sách
T16 = dua_tap(
 "16_nam-cau-hoi", "Năm câu hỏi trước khi mở sách", [
  ("h1", 9.0, ("Trước khi mở sách",
    'Đọc mà không có câu hỏi<br>thì <span class="hl">não không giữ gì</span>',
    "Não chỉ giữ lại thứ nó đang đi tìm."),
   "Đọc mà không có câu hỏi thì não không biết giữ lại gì. Não chỉ giữ thứ nó đang tìm."),
  ("list", 12.0, ("Đọc xong mà không nhớ", [
    "Đọc hết một chương, <b>gấp lại là trống</b>",
    "Không biết phải <b>giữ lại đoạn nào</b>",
    "Nhớ được vài chỗ, <b>không phải chỗ cần</b>"], None),
   "Bạn đọc hết một chương mà gấp lại là trống, vì không biết phải giữ lại đoạn nào. Cái nhớ được lại không phải chỗ cần."),
  ("list", 13.0, ("Năm câu hỏi cho bạn gì", [
    "Não biết phải giữ lại cái gì",
    "Đọc xong còn nhớ, không phải đọc lại",
    "Đặt câu hỏi xong chỉ mất hai phút"], None),
   "Năm câu hỏi này cho não biết phải giữ lại cái gì, nên đọc xong bạn còn nhớ thay vì phải đọc lại."),
  ("h1", 13.0, ("Vì sao câu hỏi lại quan trọng",
    'Não giữ lại<br>thứ nó <span class="hl">đang đi tìm</span>',
    "Có câu hỏi thì lúc đọc, não và trang sách cùng tìm một thứ."),
   "Não giữ lại thứ nó đang đi tìm. Khi bạn có câu hỏi, não và trang sách cùng đi tìm một thứ, nên nhớ lâu hơn."),
  ("list", 13.0, ("Năm câu hỏi đó là gì", [
    "Tôi cần gì ở sách này?",
    "Tác giả là ai?",
    "Sách trả lời câu hỏi nào?",
    "Chỗ nào đọc kỹ?",
    "Chỗ nào bỏ qua?"], None),
   "Năm câu hỏi đó là: tôi cần gì, tác giả là ai, sách trả lời câu hỏi nào, chỗ nào đọc kỹ, chỗ nào bỏ qua."),
  ("thanh", 13.0, ("Đọc có câu hỏi và không", [
    ("Đọc không câu hỏi", "giữ tuỳ hứng"),
    ("Đọc có câu hỏi", "giữ đúng chỗ cần")],
    "Cùng một cuốn sách, khác chỗ đặt câu hỏi là khác phần còn lại."),
   "Đọc không có câu hỏi thì não giữ tuỳ hứng. Đọc có câu hỏi thì não giữ đúng chỗ bạn cần."),
  ("list", 13.0, ("Ghi năm câu ra giấy", [
    "Mỗi câu một dòng, viết trước khi đọc",
    "Đọc để đi tìm câu trả lời cho từng câu",
    "Đặt câu hỏi xong mất chưa tới hai phút"], None),
   "Việc cần làm: ghi năm câu hỏi đó ra giấy, mỗi câu một dòng, rồi đọc để tìm câu trả lời. Việc này mất chưa tới hai phút."),
  ("list", 13.0, ("Đọc theo câu hỏi", [
    "Câu nào trả lời được thì gạch một dấu",
    "Chỗ nào đọc kỹ, chỗ nào bỏ qua",
    "Đọc xong, nhìn lại năm dòng đã ghi"], None),
   "Khi đọc, câu nào tìm được câu trả lời thì gạch một dấu, chỗ nào đọc kỹ chỗ nào bỏ qua. Đọc xong thì nhìn lại năm dòng đã ghi."),
  ("h1", 13.0, ("Thông điệp",
    'Đọc có câu hỏi<br>thì <span class="hl">mới còn nhớ</span>',
    "Não giữ lại thứ nó đang đi tìm — câu hỏi là cái bạn đang tìm."),
   "Thông điệp: não giữ lại thứ nó đang đi tìm. Đọc có câu hỏi thì đọc xong bạn vẫn còn nhớ."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom", [
    "Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
    "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
    "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Cách đặt câu hỏi này tôi dạy ngay buổi đầu của khoá. Khoá có bảy buổi Zoom, học phí chín trăm tám mươi nghìn đồng, hoàn phí sau buổi một."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

# ------------------------------------------------- TẬP 17 — ghi chép đúng cách
T17 = dua_tap(
 "17_ghi-chep-dung", "Ghi chép đúng cách", [
  ("h1", 9.0, ("Ghi chép khi đọc",
    'Ghi cả trang<br>mà <span class="hl">không nhớ gì</span>',
    "Vì não không nhớ chữ — não nhớ cấu trúc."),
   "Bạn ghi cả một trang mà đọc lại không nhớ gì. Vì não không nhớ chữ."),
  ("list", 12.0, ("Trang vở hay gặp", [
    "Mười lăm dòng chữ nhỏ, <b>chép nguyên câu</b>",
    "Đọc lại trang vở <b>chẳng vào đầu</b>",
    "Càng ghi nhiều, <b>càng ít nhớ</b>"], None),
   "Trang vở của bạn có mười lăm dòng chữ nhỏ, chép nguyên câu trong sách. Càng ghi nhiều, càng ít nhớ."),
  ("list", 13.0, ("Ghi đúng cách được gì", [
    "Trang ghi ba dòng lớn, liếc một lần là nhớ",
    "Ôn lại nhanh, không phải đọc lại cả sách",
    "Thấy ngay chỗ mình còn chưa hiểu"], None),
   "Ghi đúng cách cho bạn một trang chỉ ba dòng lớn, liếc một lần là nhớ, và ôn lại nhanh hơn hẳn."),
  ("h1", 13.0, ("Vì sao chép cả câu là vô ích",
    'Não nhớ <span class="hl">cấu trúc</span><br>không nhớ chữ',
    "Một trang ba dòng lớn dễ nhớ hơn một trang đầy chữ."),
   "Não nhớ cấu trúc, không nhớ chữ. Một trang ba dòng lớn dễ nhớ hơn một trang đầy chữ."),
  ("list", 13.0, ("Lúc chép là lúc không học", [
    "Chép nguyên câu — tay viết, não nghỉ",
    "Chép xong, đoạn đó <b>chưa hề vào đầu</b>",
    "Ghi ít mà đúng chỗ thì nhớ hơn"], None),
   "Lúc bạn chép nguyên câu là lúc tay viết mà não nghỉ. Chép xong, đoạn đó chưa hề vào đầu."),
  ("thanh", 13.0, ("Hai kiểu trang vở", [
    ("Ghi chi tiết, nhiều dòng", "dày mà trống"),
    ("Ghi tiêu đề, ý chính", "thưa mà nhớ")],
    "Hình minh hoạ định tính — không phải số đo của ai."),
   "Trang ghi chi tiết thì dày chữ mà trống. Trang ghi tiêu đề và ý chính thì thưa mà liếc một lần là nhớ."),
  ("list", 13.0, ("Ba nguyên tắc ghi chép", [
    "Chỉ ghi <b>tiêu đề và ý chính</b>",
    "Mỗi ý <b>một dòng</b>, không viết câu dài",
    "Chỗ chưa hiểu thì <b>đánh dấu</b>, đừng chép lại"], None),
   "Ba nguyên tắc: chỉ ghi tiêu đề và ý chính, mỗi ý một dòng, và đánh dấu chỗ chưa hiểu thay vì chép lại."),
  ("list", 13.0, ("Áp vào buổi đọc hôm nay", [
    "Đọc xong một mục, ghi một dòng chốt",
    "Cuối buổi: đọc lại trang ghi, tự kể lại",
    "Chỗ đánh dấu chưa hiểu thì mở lại sách"], None),
   "Áp vào hôm nay: đọc xong một mục thì ghi một dòng chốt. Cuối buổi, đọc lại trang ghi và tự kể lại."),
  ("h1", 13.0, ("Thông điệp",
    'Ghi chép là ghi <span class="hl">cấu trúc</span><br>không phải chép chữ',
    "Ghi ít mà đúng chỗ thì nhớ lâu hơn ghi nhiều."),
   "Thông điệp: ghi chép là ghi lại cấu trúc, không phải chép lại chữ. Ghi ít mà đúng chỗ thì nhớ lâu hơn."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom", [
    "Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
    "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
    "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Đây là cách ghi chép trong buổi thứ tư của khoá. Khoá có bảy buổi Zoom, học phí chín trăm tám mươi nghìn đồng, hoàn phí sau buổi một."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

# Nhóm D — bốn tập dựng sẵn theo định dạng sáu phần (bộ dựng dua_tap)
# T18 Sơ đồ một trang · T19 Lịch ôn 1-3-6 · T20 Tựa sách đánh lừa · T21 Lướt có cấu trúc

T18 = dua_tap(
 "18_so-do-1-trang", "Sơ đồ một trang cho một quyển sách", [
  ("h1", 9.0, ("Đọc xong cả quyển",
    "Thứ đọng lại<br>chỉ một <span class=\"hl\">trang giấy</span>",
    "Một trang thay cho cả quyển sách."),
   "Đọc xong cả một quyển sách, thứ còn đọng lại chỉ cần một trang giấy."),
  ("list", 12.0, ("Ba tình huống quen",
    ["Đọc xong vài ngày — mở lại chẳng nhớ gì",
     "Muốn ôn — phải đọc lại từ trang đầu",
     "Cần kể lại nội dung — không biết bắt đầu từ đâu"], None),
   "Đọc xong mấy ngày, mở lại bạn chẳng nhớ gì. Muốn ôn thì phải đọc lại từ trang đầu."),
  ("list", 13.0, ("Một trang giấy cho bạn gì",
    ["Nhìn một trang, nhớ cả quyển",
     "Ôn nhanh hơn đọc lại hai trăm trang",
     "Lần ôn nào cũng vào đúng chỗ còn yếu"],
    "Một trang thay cho đọc lại cả quyển."),
   "Trang sơ đồ cho bạn ba thứ: nhìn vào là nhớ cả quyển, ôn nhanh hơn đọc lại hai trăm trang, và luôn vào đúng chỗ còn yếu."),
  ("h1", 14.0, ("Vì sao một trang lại đủ",
    "Não nhớ <span class=\"hl\">cấu trúc</span><br>không nhớ chữ",
    "Cả quyển là một mạng ý, không phải một chuỗi câu."),
   "Não bạn nhớ cấu trúc, không nhớ từng câu chữ. Cả quyển sách, chỗ đọng lại là mạng ý chính và cách chúng nối với nhau."),
  ("list", 13.0, ("Đọc lại hai trăm trang",
    ["Đọc lại cho cảm giác quen mặt chữ",
     "Quen mặt chữ chưa phải là nhớ",
     "Một trang buộc bạn tự kể lại"], None),
   "Đọc lại hai trăm trang chỉ cho cảm giác quen mặt chữ. Quen chưa phải là nhớ. Nhìn sơ đồ, bạn phải tự kể lại nên biết mình thiếu gì."),
  ("list", 13.0, ("Sơ đồ lớn dần theo chương",
    ["Đọc xong chương nào — thêm một nhánh",
     "Nhánh nào quên — mở lại đúng chỗ đó",
     "Càng đọc, sơ đồ càng đầy"], None),
   "Sơ đồ lớn dần theo từng chương. Đọc xong chương nào, thêm một nhánh cho chương đó. Nhánh nào bạn quên thì mở lại đúng chỗ đó."),
  ("list", 14.0, ("Trang sơ đồ gồm gì",
    ["<b>Chủ đề chính</b> — gói trong một câu",
     "<b>Bốn ý lớn nhất</b> của quyển",
     "<b>Ví dụ đáng nhớ</b> nhất",
     "<b>Việc áp dụng được</b> ngay",
     "<b>Chỗ còn chưa hiểu</b>"], None),
   "Trang sơ đồ gồm năm phần: chủ đề chính gói trong một câu, bốn ý lớn nhất, một ví dụ đáng nhớ, việc áp dụng được, và chỗ bạn còn chưa hiểu."),
  ("list", 14.0, ("Làm ngay trong mười phút",
    ["Lấy một tờ giấy, ghi chủ đề ở giữa",
     "Đọc chương nào, thêm một nhánh",
     "Chỗ chưa hiểu — khoanh lại, mở sau"], None),
   "Bắt đầu ngay: lấy một tờ giấy, ghi chủ đề chính ở giữa. Đọc xong chương nào thì thêm một nhánh. Chỗ nào chưa hiểu thì khoanh lại để mở sau."),
  ("h1", 13.0, ("Thông điệp",
    "Một trang<br>thay <span class=\"hl\">cả quyển</span>",
    "Sơ đồ một trang là bước cuối của mỗi buổi học."),
   "Thông điệp: một trang sơ đồ thay cho việc đọc lại cả quyển. Đây là bước cuối của mỗi buổi học trong khoá."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom",
    ["Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
     "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
     "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Sơ đồ một trang này là bước cuối của mỗi buổi học trong khoá. Khoá bảy buổi Zoom, học phí chín trăm tám mươi nghìn đồng, hoàn phí nếu sau buổi một bạn thấy không hợp."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

T19 = dua_tap(
 "19_lich-on-1-3-6", "Lịch ôn ngày 1-3-6", [
  ("h1", 9.0, ("Ôn tập · mốc 1–3–6",
    "Không ôn —<br>một ngày mất <span class=\"hl\">một nửa</span>",
    "Vừa học xong, chưa kịp dùng đã bay mất một nửa."),
   "Không ôn, sau một ngày bạn mất một nửa những gì vừa học."),
  ("list", 12.0, ("Chuyện ai cũng gặp",
    ["Học tối nay, tuần sau quên sạch",
     "Đọc lại mới nhớ — mà lâu rồi không đọc",
     "Cảm giác đã thuộc, tới lúc cần lại không có"], None),
   "Học xong tối nay, tuần sau bạn quên gần hết. Có lúc thấy như đã thuộc, tới lúc cần dùng thì không kể lại được."),
  ("list", 13.0, ("Ba mốc ôn cho bạn gì",
    ["Mức nhớ giữ chín mươi phần trăm trở lên",
     "Mỗi lần ôn chỉ năm phút",
     "Không phải học lại từ đầu"],
    "Ba mốc: ngày một, ngày ba, ngày sáu."),
   "Ôn đúng ba mốc, mức nhớ giữ ở chín mươi phần trăm trở lên, và mỗi lần chỉ năm phút. Bạn không phải học lại từ đầu."),
  ("h1", 14.0, ("Vì sao trí nhớ rơi",
    "Mất mát tính<br>theo <span class=\"hl\">ngày</span>",
    "Không ôn thì đường nhớ chỉ có một chiều: đi xuống."),
   "Trí nhớ rơi theo thời gian, không theo việc bạn thông minh hay không. Không ôn thì đường nhớ chỉ đi xuống, và rơi nhanh nhất là ngày đầu."),
  ("list", 13.0, ("Đường rơi của trí nhớ",
    ["Học xong: một trăm phần trăm",
     "Một ngày: còn năm mươi",
     "Ba ngày: ba mươi bảy",
     "Sáu ngày: mười tám"],
    "Số minh hoạ cho đường cong trí nhớ."),
   "Nhìn con số: học xong là một trăm phần trăm. Sau một ngày còn năm mươi. Sau ba ngày còn ba mươi bảy. Sau sáu ngày chỉ còn mười tám."),
  ("h1", 13.0, ("Ôn đúng lúc thì sao",
    "Ba mốc chặn<br><span class=\"hl\">đường rơi</span>",
    "Ôn ở ngày một, ba, sáu — mức nhớ giữ trên chín mươi phần trăm."),
   "Ôn đúng lúc thì đường rơi bị chặn. Ôn ở ngày một, ngày ba và ngày sáu, mức nhớ giữ trên chín mươi phần trăm. Đó là toàn bộ mẹo."),
  ("list", 14.0, ("Lịch ôn cụ thể",
    ["Ngày một sau buổi học — năm phút",
     "Ngày ba — năm phút",
     "Ngày sáu — năm phút",
     "Ghi vào lịch ngay khi học xong"], None),
   "Lịch cụ thể: ngày một sau buổi học, năm phút. Ngày ba, năm phút. Ngày sáu, năm phút. Ghi ngay vào lịch khi vừa học xong."),
  ("list", 14.0, ("Ôn cho đúng cách",
    ["Gấp tài liệu, tự kể lại trước",
     "Chỗ nào không kể được — mở đúng chỗ đó",
     "Mỗi lần chỉ cần năm phút"], None),
   "Cách ôn cũng quan trọng: gấp tài liệu lại, tự kể trước. Chỗ nào không kể được thì mở đúng chỗ đó đọc lại."),
  ("h1", 13.0, ("Thông điệp",
    "Ôn <span class=\"hl\">ít</span>, đúng lúc<br>nhớ lâu",
    "Ba lần năm phút thay cho một lần đọc lại cả buổi."),
   "Thông điệp: ôn ít nhưng đúng lúc thì nhớ lâu. Ba lần năm phút đủ thay cho một lần đọc lại cả buổi tối."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom",
    ["Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
     "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
     "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Lịch ôn một, ba, sáu này đi kèm theo từng buổi học trong khoá. Khoá bảy buổi Zoom, học phí chín trăm tám mươi nghìn đồng, hoàn phí nếu sau buổi một bạn thấy không hợp."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

T20 = dua_tap(
 "20_tua-sach-danh-lua", "Tựa sách chưa chắc đúng nội dung", [
  ("h1", 9.0, ("Chọn sách · đừng mua theo tựa",
    "Tựa sách viết để <span class=\"hl\">bán</span><br>không phải để đúng",
    "Một tựa hay chưa nói gì về nội dung bên trong."),
   "Tựa sách được viết để bán sách, không phải để nói đúng nội dung."),
  ("list", 12.0, ("Hai quyển trên cùng một kệ",
    ["Quyển tựa rất hay — mục lục chung chung",
     "Quyển tựa thường — đúng việc bạn cần",
     "Mua theo tựa — dễ rước quyển rỗng về"], None),
   "Hai quyển đứng cạnh nhau: một quyển tựa rất hay nhưng mục lục chung chung, một quyển tựa thường mà có đúng việc bạn cần."),
  ("list", 13.0, ("Đọc mục lục trước được gì",
    ["Biết sách có đúng việc bạn cần không",
     "Không mua quyển chỉ hay ở bìa",
     "Tiền và thời gian vào đúng quyển"],
    "Ba bước, làm được ngay tại kệ sách."),
   "Đọc mục lục trước giúp bạn biết quyển sách có đúng việc mình cần không, và tránh mua quyển chỉ hay ở bìa."),
  ("h1", 14.0, ("Vì sao tựa hay vẫn lừa được",
    "Tựa là <span class=\"hl\">quảng cáo</span><br>mục lục là sự thật",
    "Người làm sách chăm cái tựa nhất — vì tựa bán được sách."),
   "Người làm sách chăm chút cái tựa nhất, vì tựa là thứ bán được sách. Còn mục lục thì khó làm đẹp giả, nên nó nói thật hơn."),
  ("list", 13.0, ("Cách thử nhanh",
    ["Mở mục lục, đọc từng tên chương",
     "Đếm số chương đúng việc bạn cần",
     "Không có chương nào dùng được — để lại"], None),
   "Mở mục lục và đọc từng tên chương. Đếm xem có bao nhiêu chương đúng với việc bạn đang cần. Không có chương nào dùng được thì để lại."),
  ("h1", 13.0, ("Tựa hứa — mục lục trả",
    "Đếm chương dùng được<br>là <span class=\"hl\">cách chắc nhất</span>",
    "Một quyển hữu ích có ít nhất hai chương đúng nhu cầu."),
   "Quy tắc đơn giản: một quyển đáng mua phải có ít nhất hai chương đúng nhu cầu của bạn. Ít hơn thì để lại."),
  ("list", 14.0, ("Ba bước trước khi trả tiền",
    ["Một: đọc mục lục, đọc tên từng chương",
     "Hai: đếm chương đúng nhu cầu",
     "Ba: chỉ mua khi có ít nhất hai chương"], None),
   "Ba bước trước khi trả tiền. Một, đọc mục lục và tên từng chương. Hai, đếm số chương đúng nhu cầu. Ba, chỉ mua khi có ít nhất hai chương."),
  ("list", 14.0, ("Áp dụng ngay lần sau",
    ["Mở mục lục trước khi nhìn bìa",
     "Một quyển dùng hai chương hơn mười quyển để đó",
     "Mua ít, dùng hết"],
    "Một quyển dùng được hai chương vẫn hơn mười quyển đọc xong để đó."),
   "Lần sau vào nhà sách, mở mục lục trước khi nhìn bìa. Một quyển dùng được hai chương vẫn hơn mười quyển đọc xong rồi để đó."),
  ("h1", 13.0, ("Thông điệp",
    "Đừng mua theo tựa —<br>mua theo <span class=\"hl\">mục lục</span>",
    "Tựa để bán, mục lục để bạn chọn đúng."),
   "Thông điệp: đừng mua theo tựa, hãy mua theo mục lục. Tựa được viết để bán, mục lục mới nói quyển sách có gì cho bạn."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom",
    ["Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
     "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
     "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Cách chọn sách này nằm trong buổi thứ hai của khoá. Khoá bảy buổi Zoom, học phí chín trăm tám mươi nghìn đồng, hoàn phí nếu sau buổi một bạn thấy không hợp."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

T21 = dua_tap(
 "21_skim-co-cau-truc", "Lướt có cấu trúc: 300 trang trong 15 phút", [
  ("h1", 9.0, ("Lướt có cấu trúc",
    "Ba trăm trang<br>trong <span class=\"hl\">mười lăm phút</span>",
    "Không phải đọc hết — mà là biết chỗ nào đáng đọc trước."),
   "Ba trăm trang trong mười lăm phút. Không phải đọc hết, mà là biết chỗ nào đáng đọc trước."),
  ("list", 12.0, ("Vì sao mở ra là ngộp",
    ["Ba trăm trang, không biết bắt đầu từ đâu",
     "Đọc từ trang đầu — hết buổi được vài chục trang",
     "Đọc xong cũng không biết chỗ nào đáng đọc"], None),
   "Mở một quyển dày ba trăm trang, bạn không biết bắt đầu từ đâu. Đọc từ trang đầu thì hết buổi mới được vài chục trang."),
  ("list", 13.0, ("Lướt đúng cách được gì",
    ["Nắm cả quyển trong mười lăm phút",
     "Biết trước khoảng hai mươi phần trăm đáng đọc kỹ",
     "Không đọc dàn đều cả ba trăm trang"],
    "Hai mươi phần trăm đọc kỹ — phần còn lại chỉ lướt."),
   "Lướt đúng cách cho bạn nắm cả quyển trong mười lăm phút, và biết trước khoảng hai mươi phần trăm là chỗ đáng đọc kỹ."),
  ("h1", 14.0, ("Vì sao lướt vẫn hiểu",
    "Sách đã có sẵn<br><span class=\"hl\">bản đồ</span>",
    "Tác giả xếp ý theo lớp — bạn chỉ cần đọc theo lớp đó."),
   "Tác giả đã xếp ý trong sách thành lớp sẵn. Bìa và mục lục cho biết sách nói về gì. Tiêu đề chương là bản đồ cả quyển."),
  ("list", 13.0, ("Bốn lớp để lướt",
    ["<b>Bìa và mục lục</b> — sách nói về gì",
     "<b>Tiêu đề chương</b> — bản đồ cuốn sách",
     "<b>Câu đầu, câu cuối</b> mỗi đoạn — ý chính",
     "<b>Chữ in đậm</b> — chỗ tác giả nhấn"], None),
   "Bốn lớp để lướt: bìa và mục lục, tiêu đề chương, câu đầu câu cuối mỗi đoạn, và chữ in đậm là chỗ tác giả nhấn."),
  ("list", 13.0, ("Lượt đầu chỉ để đánh dấu",
    ["Lướt hết ba trăm trang, tay đánh dấu",
     "Đánh dấu chỗ có vẻ liên quan",
     "Chưa đọc kỹ gì ở lượt này"], None),
   "Lượt đầu bạn lướt hết ba trăm trang và đánh dấu chỗ liên quan. Chưa đọc kỹ gì — chỉ khoảng hai mươi phần trăm sẽ được đọc kỹ."),
  ("list", 14.0, ("Ba lượt, mười lăm phút",
    ["Lượt một — hai phút: mục lục và tiêu đề",
     "Lượt hai — năm phút: câu đầu, câu cuối",
     "Lượt ba — tám phút: phần đáng đọc"],
    "Hai cộng năm cộng tám là mười lăm phút."),
   "Ba lượt cho mười lăm phút. Lượt một: hai phút cho mục lục và tiêu đề. Lượt hai: năm phút cho câu đầu, câu cuối. Lượt ba: tám phút cho phần đáng đọc."),
  ("list", 14.0, ("Áp dụng vào quyển đang đọc",
    ["Lấy một quyển đang đọc dở",
     "Đặt đồng hồ: hai, năm, tám phút",
     "Đánh dấu xong mới đọc kỹ phần đã chọn"], None),
   "Lấy một quyển đang đọc dở và đặt đồng hồ: hai phút, năm phút, tám phút. Lượt đánh dấu xong rồi mới đọc kỹ phần bạn đã chọn."),
  ("h1", 13.0, ("Thông điệp",
    "Biết chỗ đáng đọc<br>trước khi <span class=\"hl\">đọc</span>",
    "Lướt có cấu trúc để không phí ba trăm trang."),
   "Thông điệp: biết chỗ đáng đọc trước khi đọc. Lướt có cấu trúc giúp bạn không phí ba trăm trang vào những chỗ không cần."),
  ("list", 16.0, ("Khoá đọc hiệu quả · 7 buổi Zoom",
    ["Buổi đầu: luyện mắt theo kỹ thuật 3-2-1",
     "Buổi hai: đọc cụm 3–5 từ, bỏ đọc thầm",
     "Các buổi sau: quy trình đọc, ghi chép, ôn theo mốc"],
    "980.000đ · hoàn phí sau buổi 1 nếu không hợp."),
   "Cách lướt ba lượt này tôi dạy kèm trong từng buổi học. Khoá bảy buổi Zoom, học phí chín trăm tám mươi nghìn đồng, hoàn phí nếu sau buổi một bạn thấy không hợp."),
  ("cta", 8.0, None, "Quét mã trên màn hình để xem bảy buổi và giữ chỗ."),
 ])

# ---------------------------------------------------------------- TẬP 22 — bài test tốc độ đọc, bản đầy đủ
# Các tập đứng trước theo đúng thứ tự đăng — văn bản cho bài test lấy từ chính lời đọc của chúng.
_DS_TAP = [EP7, T02, T03, T04, T08, T09, T06, T05, T10, T11, T12, T13, T14, T15, T16, T17, T18, T19, T20, T21, EP20_11]

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


EPISODES = _DS_TAP + [EP22, EP23, EP24, EP25, EP26, EP27, EP28, EP29, EP30, EP31, EP_AI_AGENT]
