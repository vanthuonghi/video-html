#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sinh phụ đề .srt cho từng tập từ chính lời đọc trong kịch bản.

Mỗi lời đọc thành một dòng phụ đề: bắt đầu sau khi cảnh đã hiện (OFFSET), kết thúc
khi đọc xong (đo từ tệp mp3) nhưng không quá cuối cảnh (chừa GAP). Chưa dùng tới
WordBoundary của edge-tts — bản từng từ để dành cho phần phụ đề burn-in.

Dùng: python3 sinh-phu-de.py [slug ...]
Ra:   video-do-hoa/<slug>.srt
"""
import importlib.util, os, subprocess, sys

BASE = os.environ.get("VH_BASE") or os.path.dirname(os.path.abspath(__file__))
OUT = f"{BASE}/video-do-hoa"
GIONG = f"{BASE}/.thu-nghiem/giong"
OFFSET = 0.35
GAP = 0.5
RONG_DONG = 42


def dur(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", f], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def gio(t):
    ms = int(round(max(0.0, t) * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def ngat_dong(text):
    """Ngắt dòng ở ~42 ký tự, trả về danh sách dòng (không cắt bớt chữ)."""
    dong, ket = [], []
    for tu in text.split():
        if dong and len(" ".join(dong + [tu])) > RONG_DONG:
            ket.append(" ".join(dong))
            dong = [tu]
        else:
            dong.append(tu)
    if dong:
        ket.append(" ".join(dong))
    return ket or [text]


def chia_cue(dong, start, end):
    """Chia lời đọc dài thành nhiều cue, mỗi cue tối đa 2 dòng, chia thời gian theo số chữ."""
    nhom = [dong[i:i + 2] for i in range(0, len(dong), 2)]
    # tránh cue cuối còn đúng một chữ (hiện ra rất nhanh, khó đọc)
    if len(nhom) > 1 and len(nhom[-1]) == 1 and len(nhom[-2]) == 2:
        nhom[-1] = [nhom[-2].pop()] + nhom[-1]
    tong = sum(len(" ".join(g)) for g in nhom) or 1
    out, t = [], start
    for g in nhom:
        d = (end - start) * len(" ".join(g)) / tong
        out.append((t, min(end, t + d), "\n".join(g)))
        t += d
    return out


def tao(slug, ep):
    # Có mốc từng từ thì dùng đúng các dòng phụ đề đã cháy vào hình, để bản .srt
    # tải về khớp từng chữ và từng nhịp với video.
    try:
        sp = importlib.util.spec_from_file_location("dt", f"{BASE}/dung-tap-do-hoa.py")
        dt = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(dt)
        cue = dt.captions(ep)
    except Exception:
        cue = []
    if cue:
        return "\n".join(f"{k+1}\n{gio(a)} --> {gio(b)}\n{chu}\n"
                         for k, (a, b, chu) in enumerate(cue))
    dong = []
    for idx, text in sorted(ep["narration"]):
        if idx >= len(ep["scenes"]):
            continue
        a, b = ep["scenes"][idx]
        start, end = a + OFFSET, b - GAP
        f = f"{GIONG}/{slug}-sc{idx+1}.mp3"
        if os.path.exists(f) and os.path.getsize(f) > 4000:
            end = min(end, start + dur(f) + 0.30)
        if end - start < 0.4:
            end = start + 0.4
        for a2, b2, chu in chia_cue(ngat_dong(text), start, end):
            dong.append(f"{len(dong)+1}\n{gio(a2)} --> {gio(b2)}\n{chu}\n")
    return "\n".join(dong)


def main():
    sp = importlib.util.spec_from_file_location("dt", f"{BASE}/dung-tap-do-hoa.py")
    dt = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(dt)
    chon = sys.argv[1:] or [e["slug"] for e in dt.EPISODES]
    os.makedirs(OUT, exist_ok=True)
    for ep in dt.EPISODES:
        if ep["slug"] not in chon:
            continue
        p = f"{OUT}/{ep['slug']}.srt"
        open(p, "w", encoding="utf-8").write(tao(ep["slug"], ep))
        so_dong = open(p, encoding="utf-8").read().count(" --> ")
        print(f"  {ep['slug']}: {so_dong} dòng phụ đề · {p}")


if __name__ == "__main__":
    main()
