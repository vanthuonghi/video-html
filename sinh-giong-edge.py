#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sinh lời đọc cho từng tập bằng edge-tts (giọng Microsoft, miễn phí, không cần khoá API).
Dùng: python3 sinh-giong-edge.py [slug ...] [--giong vi-VN-NamMinhNeural] [--ep N]
"""
import asyncio, importlib.util, os, subprocess, sys, time

BASE = os.path.dirname(os.path.abspath(__file__))
GIONG = f"{BASE}/.thu-nghiem/giong"
VOICE = "vi-VN-NamMinhNeural"


def load_episodes():
    spec = importlib.util.spec_from_file_location("dt", f"{BASE}/dung-tap-do-hoa.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.EPISODES


async def sinh_co_moc(text, voice, out):
    """Ghi mp3 và mốc từng từ (WordBoundary) để dựng phụ đề bám theo giọng."""
    import edge_tts
    words = []
    with open(out, "wb") as f:
        async for ch in edge_tts.Communicate(text, voice, boundary="WordBoundary").stream():
            if ch["type"] == "audio":
                f.write(ch["data"])
            elif ch["type"] == "WordBoundary":
                a = ch["offset"] / 1e7
                words.append([round(a, 3), round(a + ch["duration"] / 1e7, 3), ch["text"]])
    if words:
        import json as _json
        with open(out.replace(".mp3", ".words.json"), "w", encoding="utf-8") as fh:
            _json.dump({"voice": voice, "words": words}, fh, ensure_ascii=False)


def sinh(text, out, voice):
    """edge-tts hay chập chờn (NoAudioReceived) nên thử lại nhiều lần, và lùi về dòng lệnh.
    Ghi lại giọng đã dùng cho từng tệp: đổi giọng là sinh lại, không dùng nhầm tệp cũ."""
    os.makedirs(os.path.dirname(out), exist_ok=True)
    import json as _json
    man_path = os.path.join(os.path.dirname(out), "manifest.json")
    try:
        man = _json.load(open(man_path, encoding="utf-8"))
    except Exception:
        man = {}
    ten = os.path.basename(out)
    moc = out.replace(".mp3", ".words.json")
    if (os.path.exists(out) and os.path.getsize(out) > 4000 and man.get(ten) == voice
            and os.path.exists(moc)):
        return True, f"đã có sẵn đúng giọng + mốc từ ({os.path.getsize(out)//1024} KB)"
    err = ""

    def xong(ten_lan):
        man[ten] = voice
        _json.dump(man, open(man_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        co_moc = " + mốc từ" if os.path.exists(moc) else " (không có mốc từ)"
        return True, f"{ten_lan} · giọng {voice.split('-')[-1]} · {os.path.getsize(out)//1024} KB{co_moc}"

    # 1) đường có mốc từng từ (WordBoundary) — dịch vụ hay trả NoAudioReceived nên thử vài lần
    for lan in range(1, 4):
        try:
            import edge_tts
            asyncio.run(sinh_co_moc(text, voice, out))
        except Exception as e:
            err = f"{type(e).__name__}: {str(e)[:50]}"
        if os.path.exists(out) and os.path.getsize(out) > 4000 and os.path.exists(moc):
            return xong(f"lần {lan}")
        time.sleep(2 + lan)

    # 2) lùi về dòng lệnh: vẫn ra mp3, chỉ mất mốc từ (phụ đề quay về mức cảnh)
    for lan in range(1, 7):
        r = subprocess.run(["edge-tts", "--voice", voice, "--text", text, "--write-media", out],
                           capture_output=True, text=True)
        if os.path.exists(out) and os.path.getsize(out) > 4000:
            return xong(f"lần {lan} (dòng lệnh)")
        err = (r.stderr or err)[-80:]
        time.sleep(3 + lan)          # dịch vụ hay chặn tạm, lùi dần rồi thử lại
    return False, f"thất bại sau 9 lần: {err}"


def main():
    global VOICE
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--giong" in sys.argv:
        VOICE = sys.argv[sys.argv.index("--giong") + 1]
        args = [a for a in args if a != VOICE]
    eps = load_episodes()
    if args:
        eps = [e for e in eps if e["slug"] in args]
    print(f"giọng: {VOICE}")
    loi, hong = 0, 0
    for ep in eps:
        print(f"\n{ep['slug']}  ({len(ep['narration'])} cảnh có lời)")
        for idx, text in ep["narration"]:
            out = f"{GIONG}/{ep['slug']}-sc{idx+1}.mp3"
            ok, msg = sinh(text, out, VOICE)
            print(f"   cảnh {idx+1}: {'OK ' if ok else 'LỖI'} {msg}")
            loi += ok
            hong += (not ok)
            time.sleep(1.2)          # giãn nhịp, tránh bị dịch vụ chặn tạm
    print(f"\nXONG: {loi} đoạn ok, {hong} đoạn lỗi")
    return 1 if hong else 0


if __name__ == "__main__":
    sys.exit(main())
