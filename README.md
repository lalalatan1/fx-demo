# Futures Lab — BTC / ETH web bot

Giao diện web mô phỏng giao dịch Futures đa khung **4h + 1h + 15m**.

**Chỉ mô phỏng. Không đặt lệnh trên Binance, không giao dịch tiền thật, không cần API key.** Giá demo được tạo giả lập và tăng tốc; kết quả không phải backtest hay lợi nhuận thực tế.

## Chạy trên Mac

Cài Python 3.10 trở lên, tải repo bằng **Code → Download ZIP**, giải nén. Mở Terminal tại thư mục dự án:

```bash
cd bot
python3 web.py
```

Mở Chrome tại `http://127.0.0.1:8765`. Bấm **Chạy demo** để xem vị thế, nhật ký và đường vốn. **Dừng demo** sẽ tạm dừng, **Đặt lại vốn** bắt đầu lại với 1.000 USDT giả lập. Dừng server bằng `Control + C` trong Terminal.

Có thể chạy bằng `bash bot/start-web.sh` từ thư mục gốc. Không cần cài thư viện pip.

## Windows

Cài Python 3.10+, mở `bot/start-web.bat`, hoặc chạy `python bot/web.py` trong Terminal.

## Kiểm tra

```bash
cd bot
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
```

Nút **Kiểm tra kết nối** thử truy cập API Binance Futures Testnet từ máy chạy web. Truy cập được binance.com không đảm bảo API Testnet cũng truy cập được. Máy cloud dùng để phát triển bị Binance từ chối bằng HTTP 451 (khu vực hạn chế); kết quả trên máy bạn có thể khác.

## Chiến lược và giới hạn

EMA20/EMA50 trên 4h và 1h xác nhận xu hướng; phá vỡ 20 nến trên 15m để tìm điểm vào. Rủi ro mục tiêu 0,5% mỗi lệnh, tối đa hai vị thế; giới hạn giá trị vị thế lúc mở là 2× vốn; dừng mở lệnh khi giảm 2% vốn trong ngày UTC.

Web demo lưu trạng thái trong RAM, mất khi tắt server. Stop-loss mô phỏng không phải lệnh bảo vệ trên sàn. Chưa có backtest, funding, thanh lý, margin isolated hay thực thi lệnh Testnet. Xem [hướng dẫn chi tiết](bot/README.md).

Dự án Java FX demo trước đây vẫn có trong lịch sử Git.
