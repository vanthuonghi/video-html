#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chọn tập cần dựng: chỉ tập vừa đổi, không dựng lại tập đã xong.

Video đã dựng rồi thì không đụng tới nữa. Mỗi lần đẩy, bước này xem tập nào thật
sự đổi rồi trả danh sách cho ma trận job. Dựng lại 20 tập chỉ vì một tập mới là
thứ bỏ được.

Tín hiệu thay đổi (lấy hợp của hai nguồn):
  1. trang HTML đổi so với commit trước (git diff TRUOC HEAD -- do-hoa)
  2. bản sinh lại khác bản đang có (bắt trường hợp sửa khung dựng mà quên sinh lại)

Dùng trong CI (đọc biến môi trường IN, TRUOC, GITHUB_OUTPUT).
Dùng ở máy: python3 chon-tap.py --in "05_phuhuynh-con-bo-sach"
           python3 chon-tap.py --truoc HEAD~1
"""
import glob, json, os, re, subprocess, sys

BASE = os.environ.get("VH_BASE") or os.path.dirname(os.path.abspath(__file__))


def git(*a):
    r = subprocess.run(["git", "-C", BASE, *a], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def co_commit(rev):
    """Commit có thật không. Phải xem mã thoát: `git cat-file -e` không in gì cả."""
    return subprocess.run(["git", "-C", BASE, "cat-file", "-e", f"{rev}^{{commit}}"],
                          capture_output=True).returncode == 0


def ds_tap():
    """Slug của các tập gốc trong do-hoa/ (bỏ bản _WxH của khung khác)."""
    co = sorted(os.path.basename(p)[:-5] for p in glob.glob(f"{BASE}/do-hoa/*.html"))
    return [s for s in co if not re.search(r"_[0-9]+x[0-9]+$", s)]


def slug_tu_tep(dong):
    """Đọc đầu ra `git status --porcelain` hoặc `git diff --name-only` → slug tập."""
    ra = set()
    for d in dong.splitlines():
        # `status --porcelain` có mã 2 ký tự đứng trước, `diff --name-only` thì không;
        # tên tệp không có dấu cách nên lấy mảnh cuối là đủ cho cả hai
        tep = d.split()[-1] if d.split() else ""
        m = re.match(r"do-hoa/(.+?)(?:_[0-9]+x[0-9]+)?\.html$", tep)
        if m:
            ra.add(m.group(1))
    return ra


def main():
    argv = sys.argv[1:]
    env_in = os.environ.get("IN", "")
    env_truoc = os.environ.get("TRUOC", "")
    for i, a in enumerate(argv):
        if a == "--in" and i + 1 < len(argv):
            env_in = argv[i + 1]
        if a == "--truoc" and i + 1 < len(argv):
            env_truoc = argv[i + 1]

    co = ds_tap()
    if not co:
        raise SystemExit("Chưa có trang nào trong do-hoa/. Chạy: python3 dung-tap-do-hoa.py")

    tay = [t for t in env_in.replace(",", " ").split() if t]
    if tay:
        chon, nguon = tay, "chọn tay"
    elif not env_truoc or set(env_truoc) == {"0"}:
        chon, nguon = co, "không có commit trước để so → dựng tất cả"
    elif not co_commit(env_truoc):
        chon, nguon = co, f"không thấy commit {env_truoc[:8]} → dựng tất cả"
    else:
        doi = slug_tu_tep(git("diff", "--name-only", env_truoc, "HEAD", "--", "do-hoa"))
        # sinh lại trang rồi xem còn tệp nào khác bản đang có (sửa khung mà quên sinh lại)
        r = subprocess.run([sys.executable, f"{BASE}/dung-tap-do-hoa.py"],
                           cwd=BASE, capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit("Không sinh lại được trang HTML:\n" + (r.stderr or "")[-500:])
        doi |= slug_tu_tep(git("status", "--porcelain", "--", "do-hoa"))
        chon, nguon = [s for s in co if s in doi], "trang HTML đổi"

    thieu = [t for t in chon if t not in co]
    if thieu:
        raise SystemExit("Không có tập: " + ", ".join(thieu))

    print(f"nguồn: {nguon}")
    print("sẽ dựng: " + (", ".join(chon) if chon else "(không tập nào — bỏ qua bước dựng)"))
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write("tap=" + json.dumps(chon) + "\n")
            f.write("co=" + ("1" if chon else "0") + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
