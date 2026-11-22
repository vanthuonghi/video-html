#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tải font Inter (font thương hiệu của speedreading.vn) về do-hoa/fonts để bản dựng
không phụ thuộc mạng và mọi máy ra cùng một bố cục chữ.

Chỉ lấy ba tập ký tự cần cho tiếng Việt: vietnamese, latin-ext, latin.
Ra: do-hoa/fonts/inter-<tập>-<độ đậm>.woff2 và do-hoa/fonts/inter.css

Dùng: python3 tai-font-inter.py
"""
import os, re, subprocess, sys, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
FONTS = f"{BASE}/do-hoa/fonts"
NGUON = "https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap"
CHON = ("vietnamese", "latin-ext", "latin")
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/126.0 Safari/537.36")


def main():
    os.makedirs(FONTS, exist_ok=True)
    req = urllib.request.Request(NGUON, headers={"User-Agent": UA})
    css = urllib.request.urlopen(req, timeout=60).read().decode()

    khoi = re.findall(r"/\* ([a-z-]+) \*/\s*@font-face \{(.*?)\}", css, re.S)
    ra, so = [], 0
    for tap, than in khoi:
        if tap not in CHON:
            continue
        url = re.search(r"url\((https://[^)]+)\)", than).group(1)
        do = re.search(r"font-weight: (\d+)", than).group(1)
        ur = re.search(r"unicode-range: ([^;]+);", than).group(1)
        ten = f"inter-{tap}-{do}.woff2"
        duong = f"{FONTS}/{ten}"
        if not os.path.exists(duong):
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}),
                                        timeout=60) as r, open(duong, "wb") as f:
                f.write(r.read())
        so += 1
        ra.append(f"""/* {tap} · {do} */
@font-face {{
  font-family: 'VH Inter';
  font-style: normal;
  font-weight: {do};
  font-display: swap;
  src: url({ten}) format('woff2');
  unicode-range: {ur};
}}""")

    open(f"{FONTS}/inter.css", "w", encoding="utf-8").write(
        "/* Inter (font thương hiệu speedreading.vn), tải sẵn — mọi máy dựng ra cùng một bố cục chữ. */\n"
        + "\n".join(ra) + "\n")
    tong = sum(os.path.getsize(f"{FONTS}/{f}") for f in os.listdir(FONTS)
               if f.startswith("inter-") and f.endswith(".woff2"))
    print(f"  {so} @font-face · {tong // 1024} KB woff2 · {FONTS}/inter.css")


if __name__ == "__main__":
    sys.exit(main())
