#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sinh metadata.json cho từng tập: tiêu đề, mô tả, hashtag, chương.

Nội dung lấy từ chính kịch bản (ten, narration) và noi-dung.json, nên sửa kịch bản
là metadata đổi theo. Ra: video-do-hoa/<slug>.json

Dùng: python3 sinh-metadata.py [slug ...]
"""
import hashlib, importlib.util, json, os, sys

BASE = os.environ.get("VH_BASE") or os.path.dirname(os.path.abspath(__file__))
OUT = f"{BASE}/video-do-hoa"
LINK_VIDEO = ("https://github.com/vanthuonghi/video-html/releases/download/"
              "moi-nhat/{slug}_co-tieng.mp4")


def nap(ten_tep, ten):
    sp = importlib.util.spec_from_file_location(ten, os.path.join(BASE, ten_tep))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


dt = nap("dung-tap-do-hoa.py", "dt")


def _phien_ban(slug):
    """?v=<8 ký tự sha256> để Buffer/CDN không dùng bản video cũ trong bộ nhớ đệm."""
    f = f"{OUT}/{slug}_co-tieng.mp4"
    if not os.path.exists(f):
        return ""
    h = hashlib.sha256()
    with open(f, "rb") as fh:
        for khoi in iter(lambda: fh.read(1 << 20), b""):
            h.update(khoi)
    return "?v=" + h.hexdigest()[:8]


def gio(t):
    m, s = divmod(int(round(t)), 60)
    return f"{m}:{s:02d}"


def tao(i, ep, cfg):
    so, tong = i + 1, len(dt.EPISODES)
    ten = ep.get("ten", ep["slug"])
    cau_dau = dict(ep["narration"]).get(0, "")
    sau = dt.EPISODES[i + 1] if i + 1 < len(dt.EPISODES) else None
    tieu_de = f"{ten} | Đọc hiệu quả #{so:02d}"
    # Phong cách đỏ–trắng trỏ về trang lớp Zoom online, khớp với thẻ kết thúc của video
    do_trang = ep.get("phong_cach") == "do-trang"
    mo_ta = "\n".join(x for x in [
        f"Tập {so}/{tong}: {ten}.",
        cau_dau,
        "",
        cfg.get("mo_ta_cuoi_online") if do_trang else cfg["mo_ta_cuoi"],
        f"Đăng ký lớp gần nhất: {cfg.get('dang_ky_online') if do_trang else cfg['dang_ky']}",
        ("Tập sau: " + sau.get("ten", "")) if sau else "Đây là tập cuối chuỗi.",
    ] if x is not None)
    nhan = list(cfg.get("hashtag", []))
    nhan.append("#docnhanh")
    return {
        "slug": ep["slug"],
        "so_tap": so,
        "tong_so_tap": tong,
        "tieu_de": tieu_de,
        "mo_ta": mo_ta,
        "hashtag": nhan,
        "thoi_luong_giay": ep["total"],
        "poster": f"{ep['slug']}_poster.png",
        "thumb": f"{ep['slug']}_thumb.png",
        "video": LINK_VIDEO.format(slug=ep["slug"]) + _phien_ban(ep["slug"]),
        "chuong": [{"ten": f"Cảnh {k + 1}", "bat_dau": gio(a)} for k, (a, _) in enumerate(ep["scenes"])],
    }


def main():
    with open(f"{BASE}/noi-dung.json", encoding="utf-8") as f:
        cfg = json.load(f)
    os.makedirs(OUT, exist_ok=True)
    chon = sys.argv[1:] or [e["slug"] for e in dt.EPISODES]
    for i, ep in enumerate(dt.EPISODES):
        if ep["slug"] not in chon:
            continue
        p = f"{OUT}/{ep['slug']}.json"
        with open(p, "w", encoding="utf-8") as f:
            json.dump(tao(i, ep, cfg), f, ensure_ascii=False, indent=1)
        print(f"  {ep['slug']}: {p}")


if __name__ == "__main__":
    main()
