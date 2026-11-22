#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kiểm bài test tốc độ: ở mốc t bất kỳ, từ hiện trên màn hình phải đúng từ trong kịch bản.

In ra cụm từ đáng lẽ hiện ở mốc t (theo đúng công thức trong trang) để đối chiếu với
khung hình thật lấy từ video. Dùng: python3 kiem-bai-test.py 121 25.0 45.0
"""
import importlib.util, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "22_bai-test-toc-do-day-du"


def nap(ten, duong):
    sp = importlib.util.spec_from_file_location(ten, os.path.join(BASE, duong))
    if sp is None:
        raise SystemExit(f"không nạp được {duong}")
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def main():
    kb = nap("kb", "kich-ban.py")
    dt = nap("dt", "dung-tap-do-hoa.py")

    # chuỗi từ của từng mốc, cộng dồn đúng như lúc dựng trang
    van_ban = kb._van_ban_test(sum(kb.so_tu_moc(w, c) for w, c, _g in kb.MOC_TEST))
    moc, vt = [], 0
    for k, (wpm, c, _g) in enumerate(kb.MOC_TEST):
        n = kb.so_tu_moc(wpm, c)
        moc.append({"k": k, "wpm": wpm, "c": c, "n": n, "doan": van_ban[vt:vt + n]})
        vt += n

    for arg in (sys.argv[1:] or ["121", "25", "45"]):
        t = float(arg)
        for m in moc:
            a = kb.GIAI_THICH + m["k"] * kb.CHAY
            t0 = a + 0.45
            if not (t0 <= t < a + kb.CHAY):
                continue
            j = int((t - t0) // (m["c"] * 60 / m["wpm"]))
            hien = m["doan"][j * m["c"]:(j + 1) * m["c"]] if j * m["c"] < m["n"] else []
            print(f"  t={t:6.2f}s · mốc {m['k']+1}/12 ({m['wpm']} từ/phút, {m['c']} từ mỗi lần)")
            print(f"     cụm thứ {j+1}/{m['n']//m['c']} · phải hiện: “{' '.join(hien)}”")
            print(f"     quầy phải ghi: {min((j+1)*m['c'], m['n'])}/{m['n']} từ")

    # đối chiếu chéo: chuỗi từ trong trang HTML phải trùng chuỗi vừa dựng lại
    html = open(os.path.join(BASE, f"do-hoa/{SLUG}.html"), encoding="utf-8").read()
    trung = all(f'data-words="{"|".join(m["doan"])}"' in html for m in moc)
    print(f"\n  chuỗi từ trong trang HTML trùng kịch bản: {'ĐÚNG' if trung else 'KHÁC'}")


if __name__ == "__main__":
    main()
