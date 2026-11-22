#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sinh nhạc nền bằng Python — repo không cần kèm tệp âm thanh nào.

Ra: .thu-nghiem/audio/pad.wav   — bản nhạc nhẹ 57,6 giây (lặp được, không tiếng ù)
    .thu-nghiem/audio/swell.wav — tiếng chuông ngắn ở mốc chuyển cảnh

Vì sao không dùng ffmpeg như bản đầu: bản cũ là hai sin 110 Hz + 163 Hz chồng nhau,
chênh 53 Hz nên tạo nhịp phách rất chậm rồi lọc thấp 420 Hz — nghe thành tiếng "è è"
ù suốt video. Ở đây nhạc được viết bằng nốt thật (hợp âm Am–F–C–G, chuông + bass
êm) nên không có phách ù nào; mọi thứ là sin có bao hình tắt dần nên vẫn sạch,
không ồn.

Dùng: python3 sinh-nhac.py
"""
import array, math, os, sys, wave

BASE = os.environ.get("VH_BASE") or os.path.dirname(os.path.abspath(__file__))
AUD = f"{BASE}/.thu-nghiem/audio"
SR = 48000
BAR = 2.4                     # 100 BPM, 4 phách/ô nhịp
SO_O = 24                     # 24 ô = 57,6 giây
FADE = 0.25                   # làm mờ hai đầu để lặp không kêu "tách"

# Am – F – C – G, mỗi hợp âm một ô nhịp. Số là nốt MIDI (La2 = 45).
VONG = ["Am", "F", "C", "G"]
HOP_AM = {"Am": [45, 48, 52], "F": [41, 45, 48], "C": [48, 52, 55], "G": [43, 47, 50]}
# thứ tự quét của tiếng chuông trong mỗi ô: trầm → cao → về giữa
QUET = [0, 1, 2, 1, 0, 2, 1, 2]


def tan_so(midi):
    return 440.0 * 2 ** ((midi - 69) / 12.0)


def them_chuong(buf, t0, f, bien_do, tau=0.55, hai=0.22):
    """Một nốt chuông: sin tắt dần + hơi có hoạ âm bậc hai cho ấm, không chói."""
    i0 = int(t0 * SR)
    n = int(min(1.6, 4 * tau) * SR)
    for i in range(n):
        j = i0 + i
        if j >= len(buf):
            break
        t = i / SR
        bao = math.exp(-t / tau) * (1.0 - math.exp(-t / 0.006))
        buf[j] += bien_do * bao * (math.sin(2 * math.pi * f * t)
                                   + hai * math.sin(4 * math.pi * f * t) * math.exp(-t / (tau * 0.45)))


def them_bass(buf, t0, f, bien_do, dai=BAR):
    """Nốt bass êm: vào chậm, giữ, ra chậm — chỉ sin nên không có tiếng rè."""
    i0 = int(t0 * SR)
    n = int(dai * SR)
    vao, ra = 0.35, 0.55
    for i in range(n):
        j = i0 + i
        if j >= len(buf):
            break
        t = i / SR
        bao = min(1.0, t / vao, (dai - t) / ra) if dai - t > 0 else 0.0
        if bao < 0:
            bao = 0.0
        buf[j] += bien_do * bao * math.sin(2 * math.pi * f * t)


def ghi_wav(ten, mau, dinh=0.55):
    """Chuẩn hoá tới đỉnh `dinh` (0..1) rồi ghi WAV 16-bit mono."""
    lon = max((abs(v) for v in mau), default=0.0) or 1.0
    k = dinh / lon
    pcm = array.array("h", (int(max(-32767, min(32767, v * k * 32767))) for v in mau))
    with wave.open(ten, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    return len(mau) / SR


def nhac_nen():
    n = int(SO_O * BAR * SR)
    buf = [0.0] * n
    for o in range(SO_O):
        ten = VONG[o % len(VONG)]
        hop = HOP_AM[ten]
        t_o = o * BAR
        # bass: nốt gốc, nhẹ và dài hết ô nhịp
        them_bass(buf, t_o, tan_so(hop[0]), 0.085)
        # chuông: 8 nốt mỗi ô, nốt gốc lên quãng tám cho sáng mà vẫn dịu
        for k, chi in enumerate(QUET):
            midi = hop[chi] + 12 + (12 if k % 4 == 2 else 0)
            # nốt 1 và 5 của ô nhấn hơn một chút để có nhịp, không đều đều
            bien_do = 0.15 if k in (0, 4) else 0.095
            them_chuong(buf, t_o + k * (BAR / len(QUET)), tan_so(midi), bien_do,
                        tau=0.5 if k in (0, 4) else 0.38,
                        hai=0.18 if k in (0, 4) else 0.10)
    # làm mờ hai đầu: bản nhạc được lặp bằng -stream_loop nên mối nối phải êm
    m = int(FADE * SR)
    for i in range(m):
        buf[i] *= i / m
        buf[n - 1 - i] *= i / m
    return buf


def tieng_chuyen_canh():
    """Chuông hai nốt (quãng năm) thay cho tiếng nhiễu gió cũ."""
    n = int(1.2 * SR)
    buf = [0.0] * n
    them_chuong(buf, 0.0, tan_so(81), 0.5, tau=0.42, hai=0.25)   # La5
    them_chuong(buf, 0.06, tan_so(88), 0.32, tau=0.34, hai=0.18)  # Mi6
    return buf


def main():
    os.makedirs(AUD, exist_ok=True)
    pad, swell = f"{AUD}/pad.wav", f"{AUD}/swell.wav"
    d1 = ghi_wav(pad, nhac_nen(), dinh=0.55)
    d2 = ghi_wav(swell, tieng_chuyen_canh(), dinh=0.40)
    for f, d in ((pad, d1), (swell, d2)):
        print(f"  {os.path.basename(f):10s} {d:.2f}s  {os.path.getsize(f)//1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
