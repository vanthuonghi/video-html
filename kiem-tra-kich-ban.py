#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kiểm tra kịch bản trước khi dựng: cấu trúc tập và ngân sách lời đọc.

Chặn những lỗi làm hỏng bản dựng mà không ai thấy: cảnh chồng nhau, thiếu hàm vẽ,
mốc lời đọc sai, hoặc lời dài tới mức phải tua nhanh âm thầm.

Dùng: python3 kiem-tra-kich-ban.py [--chat]
Mã thoát 1 nếu có lỗi (dùng làm cổng trong CI).
"""
import importlib.util, os, re, sys

BASE = os.environ.get("VH_BASE") or os.path.dirname(os.path.abspath(__file__))
SO_TU_MOI_GIAY = 4.0      # tốc độ đọc tiếng Việt dùng để tính ngân sách
VUOT_CHO_PHEP = 0.15      # lời dài hơn chỗ trống quá 15% mới coi là lỗi


def nap():
    sp = importlib.util.spec_from_file_location("dt", f"{BASE}/dung-tap-do-hoa.py")
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def nap_kb():
    """Nạp kich-ban.py để lấy hai hằng số dùng chung: CTA và CAU_TRUC_CHUAN."""
    sp = importlib.util.spec_from_file_location("kb", f"{BASE}/kich-ban.py")
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def kiem(ep, dt, kb):
    loi, canh_bao = [], []
    slug = ep.get("slug", "?")
    so_canh, so_html, so_anim = len(ep["scenes"]), len(ep["html"]), len(ep["anim"])
    if not (so_canh == so_html == so_anim):
        loi.append(f"{slug}: scenes={so_canh}, html={so_html}, anim={so_anim} phải bằng nhau")
    if not ep.get("ten"):
        loi.append(f"{slug}: thiếu 'ten' (dùng cho teaser và metadata)")
    a, b = ep["scenes"][0]
    if abs(a) > 0.001:
        loi.append(f"{slug}: cảnh đầu bắt đầu ở {a}s, phải là 0")
    for i, (x, y) in enumerate(ep["scenes"]):
        if y <= x:
            loi.append(f"{slug}: cảnh {i+1} có mốc {x}–{y} không tăng")
        if i and abs(x - ep["scenes"][i - 1][1]) > 0.001:
            loi.append(f"{slug}: cảnh {i+1} bắt đầu {x}s nhưng cảnh trước kết thúc {ep['scenes'][i-1][1]}s")
    if abs(ep["scenes"][-1][1] - ep["total"]) > 0.001:
        loi.append(f"{slug}: total={ep['total']} nhưng cảnh cuối kết thúc {ep['scenes'][-1][1]}")
    for idx, text in ep["narration"]:
        if not (0 <= idx < so_canh):
            loi.append(f"{slug}: lời đọc trỏ tới cảnh {idx} không tồn tại")
            continue
        if not text.strip():
            loi.append(f"{slug}: lời đọc cảnh {idx+1} rỗng")
            continue
        x, y = ep["scenes"][idx]
        trong = y - x - 0.85            # OFFSET + GAP trong ghep-tieng-tap.py
        can = len(text.split()) / SO_TU_MOI_GIAY
        if trong > 0 and can > trong * (1 + VUOT_CHO_PHEP):
            canh_bao.append(f"{slug}: cảnh {idx+1} cần ~{can:.1f}s cho {len(text.split())} từ, "
                            f"chỉ có {trong:.1f}s → sẽ phải tua nhanh")
    c = dt.cover_at(ep)
    if not (0 <= c <= ep["total"]):
        loi.append(f"{slug}: cover_at={c} nằm ngoài video")
    # Bộ màu chuẩn từ tập 21 là đỏ–trắng (thương hiệu speedreading.vn/sp-online).
    # Quên khoá này chỉ nhìn ra khi video đã dựng xong, nên nhắc ngay ở cổng kiểm kịch bản.
    # Tập của dự án khác dùng chung đường ống (khai "dang_ky" riêng, ví dụ AI Agent) không
    # thuộc bộ màu này — bỏ qua, kẻo cổng của dự án này chặn nhầm video của dự án kia.
    sr = not ep.get("dang_ky")
    so_tap = re.match(r"(\d+)", slug)
    if sr and so_tap and int(so_tap.group(1)) >= 21 and ep.get("phong_cach") != "do-trang":
        canh_bao.append(f'{slug}: thiếu "phong_cach": "do-trang" — bộ màu chuẩn từ tập 21')
    # Định dạng nội dung chuẩn từ tập 23: sáu phần hook → giá trị → hiểu biết mới →
    # việc cần làm → thông điệp → giới thiệu khoá 7 buổi. Video 45 giây không đủ chỗ
    # cho sáu phần, nên cổng này cũng chặn luôn các tập quá ngắn.
    if sr and so_tap and int(so_tap.group(1)) >= 23:
        if ep.get("cau_truc") != kb.CAU_TRUC_CHUAN:
            loi.append(f'{slug}: phải khai "cau_truc": CAU_TRUC_CHUAN (6 phần chuẩn)')
        if ep["total"] < 110:
            loi.append(f"{slug}: dài {ep['total']}s — tập theo định dạng mới phải từ 110 giây")
        if so_canh < 9:
            loi.append(f"{slug}: chỉ {so_canh} cảnh — cần tối thiểu 9 cảnh cho đủ 6 phần")
        if ep["html"][-1] != kb.CTA:
            loi.append(f"{slug}: cảnh cuối phải là CTA (thẻ kết thúc + khoá 7 buổi)")
    return loi, canh_bao


def main():
    dt = nap()
    kb = nap_kb()
    slug = [e["slug"] for e in dt.EPISODES]
    trung = {s for s in slug if slug.count(s) > 1}
    loi, canh_bao = [f"slug trùng: {', '.join(sorted(trung))}"] if trung else [], []
    for ep in dt.EPISODES:
        a, b = kiem(ep, dt, kb)
        loi += a
        canh_bao += b
    for c in canh_bao:
        print(f"  CẢNH BÁO {c}")
    for l in loi:
        print(f"  LỖI {l}")
    print(f"KẾT LUẬN: {len(dt.EPISODES)} tập · {len(loi)} lỗi · {len(canh_bao)} cảnh báo")
    return 1 if loi else 0


if __name__ == "__main__":
    sys.exit(main())
