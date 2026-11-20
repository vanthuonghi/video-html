#!/usr/bin/env bash
# Dựng một video đồ hoạ từ file HTML: chụp khung song song → mã hoá → ghép tiếng (nếu có).
# Dùng: bash dung-video-do-hoa.sh <file.html> <ten-video> [<thư-mục-tiếng>]
set -euo pipefail
BASE=/home/vider/speedreading-90days
HTML="${1:?cần đường dẫn file html}"
NAME="${2:?cần tên video}"
VOICE="${3:-}"

PY="$BASE/.venv-video/bin/python"
FRAMES="$BASE/.thu-nghiem/frames-$NAME"
OUT="$BASE/video-do-hoa"
WORKERS="${WORKERS:-6}"
FPS="${FPS:-24}"

# đưa file html ra qua máy chủ tạm để trình duyệt mở được
if ! curl -s -o /dev/null "http://127.0.0.1:8899/$HTML"; then
  echo "!! máy chủ 8899 chưa chạy. Mở trước: cd $BASE && python3 -m http.server 8899"
  exit 1
fi
URL="http://127.0.0.1:8899/$HTML"

echo "=== 1. Chụp khung hình ($WORKERS tiến trình, $FPS khung/giây) ==="
T0=$(date +%s)
rm -rf "$FRAMES"; mkdir -p "$FRAMES"
"$PY" "$BASE/chup-nhanh.py" "$URL" "$FRAMES" --workers "$WORKERS" --fps "$FPS" --port 9400 2>&1 | tail -2
T1=$(date +%s)
echo "    chụp xong sau $((T1-T0)) giây"

echo "=== 2. Mã hoá thành video ==="
mkdir -p "$OUT"
ffmpeg -v error -y -framerate "$FPS" -i "$FRAMES/%05d.jpg" \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -movflags +faststart -r "$FPS" \
  "$OUT/$NAME.mp4"
T2=$(date +%s)
echo "    mã hoá xong sau $((T2-T1)) giây"

if [ -n "$VOICE" ] && [ -d "$VOICE" ]; then
  echo "=== 3. Ghép lời đọc từ $VOICE ==="
  python3 "$BASE/ghep-tieng.py" 2>/dev/null || true
  T3=$(date +%s); echo "    ghép tiếng sau $((T3-T2)) giây"
fi

echo "=== KẾT QUẢ ==="
ffprobe -v error -show_entries format=duration,size:stream=codec_type,width,height \
  -of default=nw=1 "$OUT/$NAME.mp4" | sed 's/^/    /'
echo "    tổng thời gian máy chạy: $(( $(date +%s)-T0 )) giây"
