#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sinh mã QR trỏ tới link đăng ký, để dán vào thẻ kết thúc của mọi tập.

Link lấy từ noi-dung.json (khoá "dang_ky") — sửa một chỗ là mọi tập đổi theo.
Ra: do-hoa/assets/qr.svg

Dùng: python3 sinh-qr.py
"""
import json, os, sys

import qrcode
import qrcode.image.svg

BASE = os.environ.get("VH_BASE") or os.path.dirname(os.path.abspath(__file__))
RA = f"{BASE}/do-hoa/assets/qr.svg"


def sinh(url, ra):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
    os.makedirs(os.path.dirname(ra), exist_ok=True)
    img.save(ra)
    print(f"  QR: {url} → {os.path.basename(ra)} ({os.path.getsize(ra)} byte)")


def main():
    with open(f"{BASE}/noi-dung.json", encoding="utf-8") as f:
        cfg = json.load(f)
    sinh(cfg["dang_ky"], RA)
    # Phong cách đỏ–trắng (đồng bộ với speedreading.vn/sp-online) dùng mã riêng
    if cfg.get("dang_ky_online"):
        sinh(cfg["dang_ky_online"], f"{BASE}/do-hoa/assets/qr-sp-online.svg")
    if "speedreading.vn" in cfg["dang_ky"]:
        print("  !! link này là giá trị mẫu trong noi-dung.json — thay bằng link đăng ký thật")


if __name__ == "__main__":
    sys.exit(main())
