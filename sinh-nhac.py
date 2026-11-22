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
QUET = [0, 1, 2, 1]


def tan_so(midi):
    return 440.0 * 2 ** ((midi - 69) / 12.0)


def cong_vong(buf, t0, mau):
    """Cộng một nốt đã dựng sẵn vào vòng nhạc, quấn vòng ở cuối.

    Vòng nhạc dài 9,6 giây và được lặp 6 lần thành 57,6 giây, nên đuôi nốt của ô
    nhịp cuối phải chảy sang đầu vòng chứ không bị cắt (cắt là nghe "tách").
    """
    n = len(buf)
    i0 = int(t0 * SR)
    for i, v in enumerate(mau):
        buf[(i0 + i) % n] += v


def not_chuong(f, bien_do, tau=0.55, hai=0.22):
    """Mẫu của một nốt chuông: sin tắt dần + hoạ âm bậc hai cho ấm."""
    n = int(min(1.6, 4 * tau) * SR)
    ra = []
    for i in range(n):
        t = i / SR
        bao = math.exp(-t / tau) * (1.0 - math.exp(-t / 0.006))
        ra.append(bien_do * bao * (math.sin(2 * math.pi * f * t)
                                   + hai * math.sin(4 * math.pi * f * t) * math.exp(-t / (tau * 0.45))))
    return ra


def not_bass(f, bien_do, dai=BAR):
    """Một ô bass êm: vào chậm, giữ, ra chậm — chỉ sin nên không có tiếng rè."""
    n = int(dai * SR)
    vao, ra_o = 0.35, 0.55
    return [bien_do * max(0.0, min(1.0, (i / SR) / vao, (dai - i / SR) / ra_o))
            * math.sin(2 * math.pi * f * (i / SR)) for i in range(n)]


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
    """Dựng MỘT vòng 4 ô nhịp (9,6 giây) rồi lặp 6 lần.

    Vòng hợp âm lặp y hệt nhau, nên dựng từng ô 24 lần là phí: mỗi nốt chỉ viết
    một lần rồi nhân bản. Bản viết thẳng ra 57,6 giây mất 23 giây mỗi job — quá
    đắt, trong khi cách này dưới 3 giây và ra đúng cùng một bản nhạc.
    """
    vong = [0.0] * int(BAR * len(VONG) * SR)
    for o, ten in enumerate(VONG):
        hop = HOP_AM[ten]
        t_o = o * BAR
        # bass: nốt gốc, nhẹ và dài hết ô nhịp
        cong_vong(vong, t_o, not_bass(tan_so(hop[0]), 0.085))
        # chuông: 4 nốt mỗi ô, nốt gốc lên quãng tám cho sáng mà vẫn dịu
        for k, chi in enumerate(QUET):
            midi = hop[chi] + 12 + (12 if k == 2 else 0)
            nhan = k == 0            # nốt đầu ô nhấn hơn để có nhịp, không đều đều
            cong_vong(vong, t_o + k * (BAR / len(QUET)),
                      not_chuong(tan_so(midi), 0.15 if nhan else 0.095,
                                 tau=0.50 if nhan else 0.38,
                                 hai=0.18 if nhan else 0.10))
    buf = vong * int(round(SO_O / len(VONG)))
    # làm mờ hai đầu: bản nhạc được lặp bằng -stream_loop nên mối nối phải êm
    n = len(buf)
    m = int(FADE * SR)
    for i in range(m):
        buf[i] *= i / m
        buf[n - 1 - i] *= i / m
    return buf


def tieng_chuyen_canh():
    """Chuông hai nốt (quãng năm) thay cho tiếng nhiễu gió cũ."""
    buf = [0.0] * int(1.2 * SR)
    cong_vong(buf, 0.0, not_chuong(tan_so(81), 0.5, tau=0.42, hai=0.25))   # La5
    cong_vong(buf, 0.06, not_chuong(tan_so(88), 0.32, tau=0.34, hai=0.18))  # Mi6
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
