#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Giải mã mã QR trong thẻ kết thúc để chắc chắn nó quét ra đúng trang.

Mã QR là thứ duy nhất trong video người xem phải "dùng" — dựng bằng mắt không kiểm được.
Tệp này cắt vùng mã QR ở khung cuối rồi giải mã thật bằng OpenCV.

Dùng: python3 kiem-qr.py <video.mp4> <giây> [<trang mong đợi>]
"""
import re, subprocess, sys, tempfile, os

import cv2


def giai(duong):
    anh = cv2.imread(duong)
    if anh is None:
        return None, None
    det = cv2.QRCodeDetector()
    chu, diem, _ = det.detectAndDecode(anh)
    return chu, diem


def main():
    if len(sys.argv) < 3:
        raise SystemExit("dùng: python3 kiem-qr.py <video.mp4> <giây> [<trang mong đợi>]")
    video, giay = sys.argv[1], sys.argv[2]
    mong_doi = sys.argv[3] if len(sys.argv) > 3 else None
    with tempfile.TemporaryDirectory() as td:
        khung = os.path.join(td, "khung.jpg")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", giay, "-i", video,
                        "-frames:v", "1", khung], check=True)
        # thẻ kết thúc: mã QR nằm nửa dưới khung, cắt ra cho chắc
        anh = cv2.imread(khung)
        cao = anh.shape[0]
        vung = os.path.join(td, "qr.jpg")
        cv2.imwrite(vung, anh[int(cao * 0.55):, :])
        ket = []
        for ten, duong in (("cả khung", khung), ("nửa dưới", vung)):
            chu, diem = giai(duong)
            if chu:
                ket.append((ten, chu, None if diem is None else len(diem)))
        for ten, chu, _n in ket:
            print(f"  {ten}: “{chu}”")
        if not ket:
            print("  KHÔNG giải được mã QR nào trong khung này")
            return 1
        ra = ket[0][1]
        if mong_doi:
            print(f"  mong đợi: “{mong_doi}” → {'ĐÚNG' if ra.rstrip('/') == mong_doi.rstrip('/') else 'SAI'}")
            return 0 if ra.rstrip('/') == mong_doi.rstrip('/') else 1
        return 0


if __name__ == "__main__":
    sys.exit(main())
