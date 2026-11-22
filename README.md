# video-html — video đồ hoạ giải thích dựng bằng HTML

Video dọc 9:16 (1080×1920) cho kênh **Speed Reading Việt Nam** — hình động vẽ bằng
HTML/CSS/JS, chụp khung bằng Chromium headless, ghép lời đọc + nhạc nền bằng ffmpeg,
**dựng trên GitHub Actions**. Không quay, không footage, không khoá API bắt buộc.

Cách này chọn vì **HTML đa dạng hơn khuôn có sẵn**: mỗi tập có thể vẽ một hình khác hẳn
(biểu đồ cột rơi dần, lưới ô nhớ tràn, vòng trường nhìn, chữ nhấp nháy theo nhịp…),
không bị gò vào vài loại hình của một thư viện dựng sẵn.

## Đường ống

```
kich-ban.py          kịch bản từng tập: cảnh, HTML cảnh, hàm vẽ theo thời gian, lời đọc
dung-tap-do-hoa.py   khung dựng: CSS, JS __seek, phụ đề, thẻ kết thúc, tỉ lệ khung
      ├─ sinh-nhac.py        nhạc nền + tiếng vút (sinh bằng ffmpeg, không kèm tệp)
      ├─ sinh-giong-edge.py  lời đọc bằng edge-tts (Microsoft, miễn phí)
      ├─ chup-nhanh.py       chụp N khung song song qua CDP (N tiến trình Chrome)
      ├─ ffmpeg              mã hoá thành mp4
      └─ ghep-tieng-tap.py   ghép lời đọc + nhạc nền, xuất bản có tiếng
             └─ kiem-tra.py  chặn lỗi thật: sai thời lượng, sai khung, tiếng câm
```

`kich-ban.py` là **nguồn duy nhất** mô tả nội dung, `dung-tap-do-hoa.py` là khung dựng. Sửa
kịch bản ở `kich-ban.py` rồi đẩy lên là máy tự dựng.

## Thư mục

| Tệp | Việc |
|---|---|
| `kich-ban.py` | kịch bản 20 tập: cảnh, mốc thời gian, HTML cảnh, hàm vẽ, lời đọc |
| `dung-tap-do-hoa.py` | khung dựng trang HTML: CSS, `__seek`, phụ đề, thẻ kết thúc, `--size` |
| `chup-nhanh.py` | chụp khung hình; chia việc ra nhiều tiến trình; tự dò độ dài trang |
| `ghep-tieng-tap.py` | đặt lời đọc vào đúng cảnh, thêm nhạc nền, ép tốc độ nếu lời quá dài |
| `sinh-giong-edge.py` | sinh lời đọc bằng edge-tts, có thử lại (dịch vụ hay chập chờn) |
| `sinh-nhac.py` | sinh nhạc nền và tiếng vút bằng ffmpeg |
| `kiem-tra.py` | kiểm tra đầu ra, mã thoát 1 nếu lỗi |
| `sinh-phu-de.py` | sinh phụ đề `.srt` từ lời đọc và mốc từng từ (không có thì theo mốc cảnh) |
| `sinh-qr.py` | sinh mã QR đăng ký (`do-hoa/assets/qr.svg`) từ `noi-dung.json` |
| `sinh-poster.py` | chụp ảnh bìa 1080×1920 tại mốc `cover_at` của từng tập |
| `sinh-metadata.py` | sinh `metadata.json`: tiêu đề, mô tả, hashtag, chương, `?v=<sha8>` |
| `kiem-tra-kich-ban.py` | validator: cấu trúc tập, cảnh liền mạch, ngân sách lời đọc |
| `kiem-tra-hop-dong.py` | cùng một mốc `t` ở hai phiên trình duyệt phải ra cùng khung (PSNR ≥ 45 dB) |
| `dung-ti-le-khac.py` | dựng trọn một tập ở khung 1:1 / 16:9: HTML → khung → mp4 → ghép tiếng |
| `chon-tap.py` | chọn tập cần dựng theo thay đổi, để không dựng lại video đã xong |
| `noi-dung.json` | link đăng ký, câu mời quét mã, hashtag dùng chung |
| `soat-do-hoa.py` | quét theo thời gian, tìm chữ tràn khỏi vùng an toàn 9:16; `--fail` để dùng làm cổng CI |
| `dung-video-do-hoa.sh` | một lệnh dựng trọn một tập ở máy |
| `dung-ti-le-khac.py` | dựng trọn một tập ở tỉ lệ khung khác 9:16 (1:1, 16:9) |
| `tai-font-inter.py` | tải font Inter (font thương hiệu) vào `do-hoa/fonts/` |
| `kiem-qr.py` | giải mã mã QR trong thẻ kết thúc của video đã dựng |
| `kiem-bai-test.py` | đối chiếu cụm từ hiện ở mốc `t` của bài test tốc độ với kịch bản |
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

## Phụ đề

`edge-tts` trả về **mốc từng từ**; `sinh-giong-edge.py` lưu mốc đó cạnh mp3
(`<slug>-scN.words.json`). Nhờ vậy:

- phụ đề **cháy thẳng vào khung hình** ngay lúc chụp (không phải mã hoá lại video):
  4 từ một dòng, nền tối bo góc, nằm ở y≈1485–1540, trong vùng an toàn;
- `.srt` xuất ra dùng **đúng các dòng đó**, nên bản tải về khớp từng chữ với video;
- không có mốc từ (ví dụ máy không cài `edge-tts`) thì trang tự bỏ phụ đề và `.srt`
  quay về bản theo mốc cảnh — không vỡ bản dựng.

**Quy ước khi commit `do-hoa/*.html`:** bản đem commit phải là bản dựng khi **chưa có tệp
lời đọc** trong `.thu-nghiem/giong` (nên `CUES` rỗng), vì CI kiểm "do-hoa/\*.html khớp
generator" trên một máy không có tệp lời đọc. Dựng trang trong lúc đã sinh giọng thì trang
có nhúng mốc từ, CI sẽ báo lệch generator — máy chủ vẫn dựng lại trang có phụ đề đầy đủ
trước khi chụp, nên bản commit không ảnh hưởng phụ đề của video. `dung-tap-do-hoa.py` in
một dòng nhắc khi trang vừa dựng có nhúng mốc từ.

## Dùng repo này cho kênh của bạn

1. Fork repo, sửa `noi-dung.json` (link đăng ký, hashtag, câu mời) và màu trong `CSS`
   của `dung-tap-do-hoa.py`.
2. Viết tập mới: thêm một dict vào `EPISODES` (slug, `ten`, `total`, `scenes`,
   `html`, `anim`, `narration`) rồi chạy `python3 kiem-tra-kich-ban.py`.
3. Đẩy lên `main` — Actions dựng, soát bố cục, rồi đăng video + `.srt` + poster +
   thumbnail + `metadata.json` lên release `moi-nhat`.

Giấy phép: MIT (xem `LICENSE`).

## Xem trước cả bộ tập

`python3 sinh-gallery.py` sinh `gallery/index.html`: lưới 16 thẻ (ảnh bìa lấy từ
release), bấm một thẻ mở trình xem 1080×1920 thu nhỏ, có thanh tua và nút phát gọi
thẳng `contentWindow.__seek(t)` — không render lại gì. Mở bằng
`python3 -m http.server` ở gốc repo rồi vào `/gallery/`, hoặc bật GitHub Pages:
Settings → Pages → Source: **GitHub Actions**. Sau đó workflow `pages.yml` tự đăng
thư mục `gallery/` mỗi khi nó đổi; khi Pages chưa bật, workflow đó tự bỏ qua nên
không làm đỏ lần đẩy nào.

## Hai bộ màu trình bày

**Bộ màu chuẩn từ tập 21 trở đi là đỏ–trắng** (thương hiệu `speedreading.vn/sp-online`);
các tập 01–20 giữ nguyên nền tối xanh ngọc như đã đăng. Tập mới thêm khoá này vào dict
của tập đó trong `kich-ban.py`:

```python
"phong_cach": "do-trang",
```

Khi bật, tập đó dùng: nền trắng, đỏ thương hiệu `#dc2626` / `#b91c1c` / `#991b1b`, chữ xám
đậm, font **Inter** (tải sẵn trong `do-hoa/fonts/`, sinh bằng `tai-font-inter.py`), ô phụ đề
đỏ sẫm chữ trắng — và **thẻ kết thúc trỏ về `speedreading.vn/sp-online`** kèm mã QR riêng
(`assets/qr-sp-online.svg`, `sinh-qr.py` sinh cùng mã cũ). Mô tả trong `metadata.json` cũng
đổi theo link đó.

Đổi font thì bề ngang chữ đổi theo, nên sau khi bật bộ màu mới **phải chạy lại
`soat-do-hoa.py <slug> --fail`** trước khi dựng — đây là cổng bắt lỗi chữ tràn.

## Đa tỉ lệ khung (một kịch bản, ba đầu ra)

Cùng một kịch bản dựng được cho Reels/TikTok (9:16), feed vuông (1:1) và YouTube
ngang (16:9):

Trọn một tập, từ trang HTML tới video có tiếng:

```bash
python3 -m http.server 8899 &
python3 dung-ti-le-khac.py 02_noi-tham-trong-dau --size 1080x1080    # vuông
python3 dung-ti-le-khac.py 02_noi-tham-trong-dau --size 1920x1080    # ngang
python3 soat-do-hoa.py 02_noi-tham-trong-dau --size 1080x1080 --fail
```

Số đo thật của hai bản dựng đó (1008 khung, 4 tiến trình): hình 42,00s, tiếng
−16,1 LUFS đỉnh −1,5 dB, dung lượng 3,1 MB (1:1) và 3,7 MB (16:9); chụp 1008 khung
mất 37,9s (26,6 khung/giây tổng).

Cách làm: giữ nguyên khung thiết kế 1080×1920 rồi **thu phóng vừa khung đích**
(`transform: scale`), nới cột nội dung lên tối đa 1320px thiết kế cho khung
vuông/ngang. Nhờ vậy các cảnh đã soát không phải dựng lại, chữ vẫn đúng tỉ lệ, còn
phần thừa hai bên là nền `#bg` phủ kín chứ không phải dải đen.

Bản khác tỉ lệ ghi thành `do-hoa/<slug>_WxH.html`, không lẫn với tập gốc; cổng
`soat-do-hoa.py --size ...` tự dịch vùng an toàn theo phép thu phóng đó. Mới làm
cho **một tập mẫu** (02) — cố ý, để chứng minh trước khi nhân ra cả chuỗi.

## Tốc độ (số đo thật)

Một lần đẩy `main` dựng **cả 16 tập song song** trên GitHub Actions:

| Hạng mục | Số đo |
| --- | --- |
| Toàn bộ lần chạy (16 tập + soát bố cục, kể cả xếp hàng) | **6 phút 12 giây** |
| Tập nhanh nhất / chậm nhất | 1 phút 59 giây / 3 phút 8 giây |
| Soát bố cục 16 tập (`soat-do-hoa.py`) | 27 giây |
| Chụp khung trên máy (1008 khung, 4 tiến trình, Chrome 126) | 8,9 khung/giây |
| Chụp khung 1080×1080 (1008 khung, 4 tiến trình) | 32,1 khung/giây (ít điểm ảnh hơn nên nhanh gần 4 lần) |
| Độ to sau khi ghép | −16,0 … −16,2 LUFS, đỉnh −1,2 … −1,5 dBFS |

Thời gian gần như không đổi so với trước khi có phụ đề vì phụ đề được cháy vào khung
ngay lúc chụp — không có bước mã hoá lại video.

## Dựng trên GitHub

- **Đẩy lên `main`**: chỉ tập có trang HTML đổi mới được dựng (`chon-tap.py` so với
  commit trước). Sửa một tập thì một máy chạy, video cũ không bị dựng lại.
- **Chạy tay**: Actions → Dựng video đồ hoạ → Run workflow. Ô `tap` để trống là dựng
  lại tất cả; muốn một tập thì ghi mã tập, ví dụ `05_phuhuynh-con-bo-sach`.
- Không tập nào đổi thì bước dựng được bỏ qua hẳn, lần chạy vẫn xanh.
- Mỗi tập chạy trên **một máy riêng, song song** (tối đa 8). Máy chuẩn của repo công khai:
  4 lõi / 16 GB, **miễn phí và không giới hạn phút**.
- Video được đăng vào release **`moi-nhat`** với **URL cố định theo từng tập**, thay mới tại chỗ:

  ```
  https://github.com/vanthuonghi/video-html/releases/download/moi-nhat/<mã-tập>_co-tieng.mp4
  ```

  URL cố định là điểm quan trọng: Buffer chỉ nhận media qua URL công khai, nên nối thẳng được.
- Bản dựng cũng nằm trong mục **Artifacts** của lần chạy (giữ 14 ngày).

## Thêm một tập mới

1. Mở `kich-ban.py`, thêm một khối như các khối `EP7`, `EP9` (kịch bản nằm riêng, khung dựng ở `dung-tap-do-hoa.py`):
   - `scenes`: danh sách `(giây bắt đầu, giây kết thúc)` cho từng cảnh;
   - `html`: phần HTML mỗi cảnh (dùng các lớp CSS có sẵn: `.race`, `.chart`, `.grid`, `.flash`, `.cluster`, `.stack`…);
   - `anim`: hàm `function(t, el)` vẽ theo thời gian, **chạy được ở mọi mốc t** (không dựa vào khung trước);
   - `narration`: `(số thứ tự cảnh, lời đọc)` — cảnh nào không có thì bỏ trống.
2. Thêm tên tập vào danh sách `EPISODES` (cuối `kich-ban.py`) rồi chạy
   `python3 kiem-tra-kich-ban.py` — bộ kiểm báo lỗi cấu trúc và ngân sách lời đọc
   trước khi tốn một lần dựng.
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
