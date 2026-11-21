# video-html — video đồ hoạ giải thích dựng bằng HTML

Video dọc 9:16 (1080×1920) cho kênh **Speed Reading Việt Nam** — hình động vẽ bằng
HTML/CSS/JS, chụp khung bằng Chromium headless, ghép lời đọc + nhạc nền bằng ffmpeg,
**dựng trên GitHub Actions**. Không quay, không footage, không khoá API bắt buộc.

Cách này chọn vì **HTML đa dạng hơn khuôn có sẵn**: mỗi tập có thể vẽ một hình khác hẳn
(biểu đồ cột rơi dần, lưới ô nhớ tràn, vòng trường nhìn, chữ nhấp nháy theo nhịp…),
không bị gò vào vài loại hình của một thư viện dựng sẵn.

## Đường ống

```
dung-tap-do-hoa.py   kịch bản từng tập: cảnh, hàm vẽ theo thời gian, lời đọc
      ├─ sinh-nhac.py        nhạc nền + tiếng vút (sinh bằng ffmpeg, không kèm tệp)
      ├─ sinh-giong-edge.py  lời đọc bằng edge-tts (Microsoft, miễn phí)
      ├─ chup-nhanh.py       chụp N khung song song qua CDP (N tiến trình Chrome)
      ├─ ffmpeg              mã hoá thành mp4
      └─ ghep-tieng-tap.py   ghép lời đọc + nhạc nền, xuất bản có tiếng
             └─ kiem-tra.py  chặn lỗi thật: sai thời lượng, sai khung, tiếng câm
```

`dung-tap-do-hoa.py` là **nguồn duy nhất** mô tả nội dung. Sửa ở đó rồi đẩy lên là máy tự dựng.

## Thư mục

| Tệp | Việc |
|---|---|
| `dung-tap-do-hoa.py` | kịch bản 8 tập: cảnh, mốc thời gian, hàm vẽ, lời đọc |
| `chup-nhanh.py` | chụp khung hình; chia việc ra nhiều tiến trình; tự dò độ dài trang |
| `ghep-tieng-tap.py` | đặt lời đọc vào đúng cảnh, thêm nhạc nền, ép tốc độ nếu lời quá dài |
| `sinh-giong-edge.py` | sinh lời đọc bằng edge-tts, có thử lại (dịch vụ hay chập chờn) |
| `sinh-nhac.py` | sinh nhạc nền và tiếng vút bằng ffmpeg |
| `kiem-tra.py` | kiểm tra đầu ra, mã thoát 1 nếu lỗi |
| `sinh-phu-de.py` | sinh phụ đề `.srt` từ lời đọc và mốc cảnh |
| `sinh-qr.py` | sinh mã QR đăng ký (`do-hoa/assets/qr.svg`) từ `noi-dung.json` |
| `sinh-poster.py` | chụp ảnh bìa 1080×1920 tại mốc `cover_at` của từng tập |
| `sinh-metadata.py` | sinh `metadata.json`: tiêu đề, mô tả, hashtag, chương |
| `noi-dung.json` | link đăng ký, câu mời quét mã, hashtag dùng chung |
| `soat-do-hoa.py` | quét theo thời gian, tìm chữ tràn khỏi vùng an toàn 9:16; `--fail` để dùng làm cổng CI |
| `dung-video-do-hoa.sh` | một lệnh dựng trọn một tập ở máy |
| `do-hoa/*.html` | trang HTML sinh ra (commit lại để xem được trong repo) |
| `do-hoa/fonts/` | font Noto Sans tải sẵn — mọi máy dựng ra cùng một bố cục chữ |

Vùng an toàn của trang là **x ∈ [96, 984], y ∈ [220, 1580]** (1080×1920): đỉnh chừa thanh
_trạng thái, đáy chừa caption và nút của TikTok/Reels/Shorts. Dòng thương hiệu nằm ở dải
trên cùng. Mỗi lần đẩy lên, job `soat-bo-cuc` dựng lại HTML và chặn nếu có phần tử tràn.
Chữ dùng font đóng gói trong `do-hoa/fonts/` (không phụ thuộc font của máy dựng), nên số đo
ở máy và trên CI trùng nhau.

Âm thanh: nhạc nền tự hạ dưới giọng đọc (`sidechaincompress`), mỗi tập được đo độ to thật
rồi đưa về **−16 LUFS, đỉnh −1,5 dBTP** để các tập nghe đều nhau.

Cảnh cuối của mọi tập được thay bằng **thẻ kết thúc dùng chung**: số tập `n/tổng`, teaser
tập sau, mã QR đăng ký và dải chấm tiến độ. Link và câu mời nằm trong `noi-dung.json`,
sửa một chỗ là toàn bộ tập đổi theo. Mỗi tập sinh kèm `_poster.png` (ảnh bìa) và
`.json` (tiêu đề, mô tả, hashtag) — cả hai cùng `.srt` được đẩy lên release `moi-nhat`.
Mốc chụp ảnh bìa đặt riêng được bằng khoá `cover_at` trong tập đó.

## Dựng trên GitHub

- Vào **Actions → Dựng video đồ hoạ → Run workflow**. Ô `tap` để trống là dựng tất cả;
  muốn một tập thì ghi mã tập, ví dụ `03_bieu-tri-quen`.
- Mỗi tập chạy trên **một máy riêng, song song** (tối đa 8). Máy chuẩn của repo công khai:
  4 lõi / 16 GB, **miễn phí và không giới hạn phút**.
- Video được đăng vào release **`moi-nhat`** với **URL cố định theo từng tập**, thay mới tại chỗ:

  ```
  https://github.com/vanthuonghi/video-html/releases/download/moi-nhat/<mã-tập>_co-tieng.mp4
  ```

  URL cố định là điểm quan trọng: Buffer chỉ nhận media qua URL công khai, nên nối thẳng được.
- Bản dựng cũng nằm trong mục **Artifacts** của lần chạy (giữ 14 ngày).

## Thêm một tập mới

1. Mở `dung-tap-do-hoa.py`, thêm một khối như các khối `EP7`, `EP9`:
   - `scenes`: danh sách `(giây bắt đầu, giây kết thúc)` cho từng cảnh;
   - `html`: phần HTML mỗi cảnh (dùng các lớp CSS có sẵn: `.race`, `.chart`, `.grid`, `.flash`, `.cluster`, `.stack`…);
   - `anim`: hàm `function(t, el)` vẽ theo thời gian, **chạy được ở mọi mốc t** (không dựa vào khung trước);
   - `narration`: `(số thứ tự cảnh, lời đọc)` — cảnh nào không có thì bỏ trống.
2. Thêm tên tập vào danh sách `EPISODES`.
3. Đẩy lên GitHub, hoặc thử ở máy: `bash dung-video-do-hoa.sh do-hoa/<mã-tập>.html <mã-tập>`.

## Dựng ở máy

```bash
python3 -m http.server 8899 &          # để Chromium mở được trang
python3 dung-tap-do-hoa.py             # sinh trang HTML
python3 sinh-nhac.py                   # sinh nhạc nền
python3 sinh-giong-edge.py <mã-tập>    # sinh lời đọc
bash dung-video-do-hoa.sh do-hoa/<mã-tập>.html <mã-tập>
python3 kiem-tra.py <mã-tập>
```

Máy 8 luồng: một tập 42 giây dựng hết **khoảng 60 giây** (chụp 46 giây + mã hoá 14 giây).

## Vài điều đã trả giá để biết

- **Khâu chụp khung là nút cổng, không phải phần tính toán.** Mỗi khung tốn ~156 ms ở khâu
  chụp và ~1 ms ở khâu tính. Nên cách duy nhất để nhanh là **chạy nhiều tiến trình song song**
  (6 tiến trình: nhanh 3,4 lần). Bật card đồ hoạ và hạ chất lượng ảnh đều **không** giúp gì.
- **Không được để script tự đoán độ dài video.** Từng có lần mặc định 40 giây làm cả loạt
  bị cụt mất đoạn kết. Giờ trang tự khai `window.__total`, script dò lại rồi mới chụp, và có
  phép kiểm số khung chụp được so với số khung cần.
- **Phần tử định vị theo toạ độ đo được phải có `top:0;left:0`**, nếu không nó giữ vị trí tĩnh
  trong cột flex và bay ra ngoài khung — lỗi chỉ thấy ở khung giữa phim, không thấy ở giây 0.
- **Kiểm bố cục bằng DOM, đừng chỉ nhìn ảnh:** quét mọi khung, so từng hình chữ nhật với vùng
  an toàn. Cách này bắt được chữ tràn, phần tử nằm ngoài khung và nhãn không khớp số.
- **edge-tts hay trả về file rỗng (`NoAudioReceived`)** — luôn thử lại 3–5 lần, và lùi về
  cách gọi dòng lệnh khi cách gọi thư viện thất bại.
