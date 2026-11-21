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


def main():
    with open(f"{BASE}/noi-dung.json", encoding="utf-8") as f:
        url = json.load(f)["dang_ky"]
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
    os.makedirs(os.path.dirname(RA), exist_ok=True)
    img.save(RA)
    print(f"  QR: {url} → {RA} ({os.path.getsize(RA)} byte)")
    if "speedreading.vn" in url:
        print("  !! link này là giá trị mẫu trong noi-dung.json — thay bằng link đăng ký thật")


if __name__ == "__main__":
    sys.exit(main())
