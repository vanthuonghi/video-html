#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sinh nhạc nền bằng Python — repo không cần kèm tệp âm thanh nào.

Ra: .thu-nghiem/audio/pad.wav   — 115,2 giây (12 đoạn × 4 ô nhịp), lặp được, không tiếng ù
    .thu-nghiem/audio/swell.wav — tiếng chuông ngắn ở mốc chuyển cảnh

Vì sao không dùng ffmpeg như bản đầu: bản cũ là hai sin 110 Hz + 163 Hz chồng nhau,
chênh 53 Hz nên tạo nhịp phách rất chậm rồi lọc thấp 420 Hz — nghe thành tiếng "è è"
ù suốt video. Ở đây nhạc được viết bằng nốt thật (hợp âm Am–F–C–G, chuông + bass
êm) nên không có phách ù nào; mọi thứ là sin có bao hình tắt dần nên vẫn sạch.

Vì sao không còn là một vòng 9,6 giây lặp 6 lần: tập dài (tập 23 dài 99 giây) nghe
lặp y nguyên một lần, rất dễ lộ. Nay bốn kiểu đoạn A/B/C/D khác nhau (quãng tám của
chuông, độ dày nốt, nốt quãng tám trong hợp âm) xếp thành một hình thức 115,2 giây —
dài hơn tập dài nhất hiện có, và hai chặng liền nhau không còn trùng nhau.

Dùng: python3 sinh-nhac.py
"""
import array, math, os, sys, wave

BASE = os.environ.get("VH_BASE") or os.path.dirname(os.path.abspath(__file__))
AUD = f"{BASE}/.thu-nghiem/audio"
SR = 48000
BAR = 2.4                     # 100 BPM, 4 phách/ô nhịp
DUOI = 1.2                    # đuôi vang: nốt cuối đoạn ngân sang đầu đoạn sau
FADE = 0.25                   # làm mờ hai đầu bản nhạc để lặp không kêu "tách"

# Am – F – C – G, mỗi hợp âm một ô nhịp. Bốn số là nốt MIDI (La2 = 45):
# gốc, quãng ba, quãng năm, quãng tám.
VONG = ["Am", "F", "C", "G"]
HOP_AM = {"Am": [45, 48, 52, 57], "F": [41, 45, 48, 53],
          "C": [48, 52, 55, 60], "G": [43, 47, 50, 55]}

# Bốn kiểu đoạn. `quet` là các bậc hợp âm đánh trong một ô nhịp (chia đều số phách);
# `quang` dịch chuông lên quãng tám; `cao` là vị trí trong `quet` được nhấc thêm một
# quãng tám cho sáng; `dam` là hệ số âm lượng chuông của đoạn đó.
KIEU = {
    "A": dict(quet=[0, 1, 2, 1], quang=12, cao=2, dam=1.00),    # gốc: quét 4 nốt/ô
    "B": dict(quet=[0, 2, 1, 2], quang=24, cao=3, dam=0.55),    # sáng: chuông cao quãng tám
    "C": dict(quet=[0, 2],       quang=12, cao=None, dam=1.20),  # thưa: 2 nốt/ô, ngân dài
    "D": dict(quet=[0, 1, 2, 3], quang=12, cao=None, dam=0.80),  # dày: 4 nốt/ô, có nốt quãng tám
}
# Hình thức 12 đoạn = 115,2 giây. Đoạn đầu và đoạn cuối đều là A nên chỗ nối khi
# -stream_loop quay lại đầu nghe như A chạy tiếp chứ không "nhảy" sang đoạn khác.
HINH_THUC = ["A", "B", "A", "C", "A", "B", "D", "C", "A", "B", "D", "A"]

TAU, HAI = 0.45, 0.15         # độ ngân và lượng hoạ âm bậc hai của chuông
_mau = {}                     # mẫu từng nốt chỉ dựng một lần rồi dùng lại


def tan_so(midi):
    return 440.0 * 2 ** ((midi - 69) / 12.0)


def mau_chuong(midi):
    """Mẫu một nốt chuông (biên độ 1): sin tắt dần + hoạ âm bậc hai cho ấm."""
    if midi in _mau:
        return _mau[midi]
    f = tan_so(midi)
    n = int(min(1.3, 3 * TAU) * SR)
    mau = array.array("d", bytes(8 * n))
    for i in range(n):
        t = i / SR
        bao = math.exp(-t / TAU) * (1.0 - math.exp(-t / 0.006))
        mau[i] = bao * (math.sin(2 * math.pi * f * t)
                        + HAI * math.sin(4 * math.pi * f * t) * math.exp(-t / (TAU * 0.45)))
    _mau[midi] = mau
    return mau


def mau_bass(midi):
    """Một ô bass êm (biên độ 1): vào chậm, giữ, ra chậm — chỉ sin nên không rè."""
    if ("bass", midi) in _mau:
        return _mau[("bass", midi)]
    f = tan_so(midi)
    n = int(BAR * SR)
    vao, ra_o = 0.35, 0.55
    mau = array.array("d", bytes(8 * n))
    for i in range(n):
        t = i / SR
        bao = max(0.0, min(1.0, t / vao, (BAR - t) / ra_o))
        mau[i] = bao * math.sin(2 * math.pi * f * t)
    _mau[("bass", midi)] = mau
    return mau


def cong(buf, t0, mau, k=1.0):
    """Cộng một mẫu nốt vào vị trí t0 (giây), cắt ở cuối bộ đệm."""
    i0 = int(t0 * SR)
    m = min(len(mau), len(buf) - i0)
    for j in range(m):
        buf[i0 + j] += mau[j] * k


def doan(ten):
    """Dựng một đoạn 4 ô nhịp (9,6 giây) theo kiểu `ten`, kèm đuôi vang."""
    p = KIEU[ten]
    buf = [0.0] * int((4 * BAR + DUOI) * SR)
    for o, ten_hop in enumerate(VONG):
        hop = HOP_AM[ten_hop]
        t_o = o * BAR
        # bass: nốt gốc, nhẹ và dài hết ô nhịp
        cong(buf, t_o, mau_bass(hop[0]), 0.085)
        chia = len(p["quet"])
        for k, chi in enumerate(p["quet"]):
            midi = hop[chi] + p["quang"] + (12 if k == p["cao"] else 0)
            nhan = k == 0                    # nốt đầu ô nhấn hơn để có nhịp
            cong(buf, t_o + k * (BAR / chia), mau_chuong(midi),
                 (0.15 if nhan else 0.095) * p["dam"])
    return buf


def nhac_nen():
    """Ghép 12 đoạn theo HINH_THUC thành bản 115,2 giây.

    Chỉ có bốn kiểu đoạn nên mỗi kiểu dựng một lần rồi chép sang các chỗ dùng lại;
    nốt cũng chỉ dựng một mẫu cho mỗi cao độ. Đuôi vang của đoạn trước được cộng
    vào đầu đoạn sau để nốt cuối đoạn không bị cắt cụt.
    """
    L = int(4 * BAR * SR)
    da_dung = {ten: doan(ten) for ten in KIEU}
    buf = array.array("d", bytes(8 * L * len(HINH_THUC)))
    duoi = int(DUOI * SR)
    for i, ten in enumerate(HINH_THUC):
        dau = i * L
        buf[dau:dau + L] = array.array("d", da_dung[ten][:L])
        if i:                                # đuôi vang của đoạn trước chảy vào đầu đoạn này
            truoc = da_dung[HINH_THUC[i - 1]]
            for j in range(min(duoi, L, len(truoc) - L)):
                buf[dau + j] += truoc[L + j]
    # làm mờ hai đầu: bản nhạc được lặp bằng -stream_loop nên mối nối phải êm
    n = len(buf)
    m = int(FADE * SR)
    for i in range(m):
        buf[i] *= i / m
        buf[n - 1 - i] *= i / m
    return buf


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


def tieng_chuyen_canh():
    """Chuông hai nốt (quãng năm) thay cho tiếng nhiễu gió cũ."""
    buf = [0.0] * int(1.2 * SR)
    cong(buf, 0.0, mau_chuong(81), 0.5)      # La5
    cong(buf, 0.06, mau_chuong(88), 0.32)    # Mi6
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
