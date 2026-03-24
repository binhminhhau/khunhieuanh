## Web khử nhiễu ảnh bằng Python

App web chạy local để upload ảnh và khử nhiễu bằng các thuật toán OpenCV (Non-Local Means, Bilateral, Median).

### Yêu cầu

- Python 3.10+ (khuyến nghị 3.11)

### Cài đặt

Mở PowerShell tại thư mục dự án `D:\WorkSpace\KhuNhieu` rồi chạy:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Chạy web

```bash
python app.py
```

Sau đó mở link mà terminal in ra (thường là `http://127.0.0.1:7860`).

### Gợi ý tham số

- **Non-Local Means**: tăng `Strength (h)` và `Strength Color (hColor)` nếu còn nhiễu, nhưng quá cao sẽ bệt chi tiết.
- **Median**: hiệu quả với nhiễu muối tiêu; tăng `Window / Kernel`.
- **Bilateral**: giữ biên tốt; thử tăng `sigmaColor`/`sigmaSpace` dần.

