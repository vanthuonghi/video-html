#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kiểm tra một tập đã dựng: đúng thời lượng, có hình, có tiếng, và tiếng không bị câm.
Dùng: python3 kiem-tra.py <slug> [<slug> ...]      (mã thoát 1 nếu có tập lỗi)
      python3 kiem-tra.py <slug> --size 1080x1080  (bản khung khác: <slug>_1080x1080_co-tieng.mp4)
"""
import importlib.util, json, os, subprocess, sys

BASE = os.environ.get("VH_BASE") or os.path.dirname(os.path.abspath(__file__))
OUT = f"{BASE}/video-do-hoa"


def load_episodes():
    sp = importlib.util.spec_from_file_location("dt", f"{BASE}/dung-tap-do-hoa.py")
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    return {e["slug"]: e for e in m.EPISODES}


def probe(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration,size:stream=codec_type,codec_name,width,height",
                        "-of", "json", f], capture_output=True, text=True)
    return json.loads(r.stdout)


def do_muc(f):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    mean = peak = None
    for line in r.splitlines():
        if "mean_volume:" in line:
            mean = float(line.split("mean_volume:")[-1].strip().split()[0])
        if "max_volume:" in line:
            peak = float(line.split("max_volume:")[-1].strip().split()[0])
    return mean, peak


def co_tieng_noi(f, moc, cua_so=0.5, tre=0.4):
    """Đo mức âm thanh trong đoạn đầu mỗi lời đọc, so với mức nền của cả video.
    Trả về danh sách (số cảnh, mức đo) và mức nền."""
    import array, math, wave
    tam = f + ".kiem-tra.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f, "-ac", "1", "-ar", "16000", tam], check=True)
    with wave.open(tam, "rb") as w:
        sr = w.getframerate()
        frames = w.readframes(w.getnframes())
    x = array.array("h"); x.frombytes(frames)
    n = max(1, int(sr * 0.05))
    muc = []
    for i in range(0, len(x) - n, n):
        doan = x[i:i+n]
        rms = (sum(float(v)*v for v in doan) / len(doan)) ** 0.5
        muc.append(20 * math.log10(rms / 32768 + 1e-9))
    muc_sap = sorted(muc)
    nen = muc_sap[int(len(muc_sap) * 0.2)]        # mức nhạc nền
    ket = []
    for c in moc:
        a = int((c + tre) / 0.05); b = int((c + tre + cua_so) / 0.05)
        doan = muc[a:b] or [nen]
        ket.append((round(max(doan), 1), round(max(doan) - nen, 1)))
    os.remove(tam)
    return ket, round(nen, 1)


def main():
    eps = load_episodes()
    args = sys.argv[1:]
    # --size WxH: kiểm bản dựng khung khác; mặc định là bản dọc 9:16
    khung = None
    con = []
    i = 0
    while i < len(args):
        if args[i] == "--size" and i + 1 < len(args):
            try:
                khung = tuple(int(x) for x in args[i + 1].lower().split("x"))
            except Exception:
                raise SystemExit(f"--size phải có dạng WxH (nhận: {args[i + 1]})")
            i += 2
            continue
        con.append(args[i]); i += 1
    if not con:
        con = list(eps)
    rong, cao = khung or (1080, 1920)
    hau = f"_{rong}x{cao}" if khung else ""
    loi = 0
    for slug in con:
        ep = eps[slug]
        f = f"{OUT}/{slug}{hau}_co-tieng.mp4"
        print(f"\n=== {slug}")
        if not os.path.exists(f):
            print("  LỖI: chưa có tệp video"); loi += 1; continue
        d = probe(f)
        dur = float(d["format"]["duration"]); size = int(d["format"]["size"])
        vs = [s for s in d["streams"] if s["codec_type"] == "video"]
        aud = [s for s in d["streams"] if s["codec_type"] == "audio"]
        ok = True
        if abs(dur - ep["total"]) > 0.15:
            print(f"  LỖI: thời lượng {dur:.2f}s lệch so với kịch bản {ep['total']}s"); ok = False
        else:
            print(f"  thời lượng {dur:.2f}s khớp kịch bản")
        if not vs:
            print("  LỖI: không có luồng hình"); ok = False
        elif vs[0]["width"] != rong or vs[0]["height"] != cao:
            print(f"  LỖI: khung {vs[0]['width']}x{vs[0]['height']}, phải là {rong}x{cao}"); ok = False
        else:
            print(f"  khung {vs[0]['width']}x{vs[0]['height']} đúng")
        if not aud:
            print("  LỖI: không có luồng tiếng"); ok = False
        else:
            mean, peak = do_muc(f)
            if mean is None or mean < -40:
                print(f"  LỖI: tiếng gần như câm (trung bình {mean} dB)"); ok = False
            else:
                print(f"  tiếng: trung bình {mean} dB · đỉnh {peak} dB")
            # từng lời đọc phải thật sự xuất hiện trong video
            moc, t = [], 0.0
            for a, b in ep["scenes"]:
                moc.append(round(t, 2)); t = b
            co = [moc[i] for i, _ in ep.get("narration", [])
                  if i < len(moc) and os.path.exists(f"{BASE}/.thu-nghiem/giong/{slug}-sc{i+1}.mp3")]
            if co:
                ket, nen = co_tieng_noi(f, co, cua_so=1.0)
                for c, (m, hon) in zip(co, ket):
                    if hon < 6:
                        print(f"  LỖI: cảnh mốc {c}s gần như không có tiếng nói (chỉ hơn nền {hon} dB)")
                        ok = False
                print(f"  lời đọc: {len(co)} đoạn, hơn nền " + ", ".join(f"{h:+.1f} dB" for _m, h in ket))
        print(f"  dung lượng {size/1048576:.1f} MB · số cảnh {len(ep['scenes'])}")
        loi += (not ok)
    print(f"\nKẾT LUẬN: {'TẤT CẢ ĐẠT' if loi == 0 else str(loi) + ' tập LỖI'}")
    return 1 if loi else 0


if __name__ == "__main__":
    sys.exit(main())
