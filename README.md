# 🚀 MLOps Inference Server

FastAPI service đóng vai trò **Inference Server** giả lập trong hệ thống MLOps. Nhận raw text data, chạy phân loại thông qua một (mock) fine-tuned model (được load vào RAM trong lifespan startup). Kết quả dự đoán cùng với model version được lưu trữ lại trên hệ thống Oracle DB để theo dõi và retraining sau này. Scale dự phòng bằng uvicorn workers.

## 📋 Features

- **POST /api/infer** — Gửi text để phân loại (Positive/Negative/Neutral) và lấy độ tin cậy. Dữ liệu được log tự động vào DB.
- **GET /api/infer/{id}** — Xem lại kết quả phân loại từ lịch sử (history logging)
- **GET /health** — Kiểm tra trạng thái Database connection + trạng thái ML model đã được tải vào RAM hay chưa. Trả 503 khi model chưa load xong.
- **Pydantic validation** — Ràng buộc chiều dài text (1 - 5000 ký tự). Trả 422 chi tiết nếu nhập sai.
- **Docker production-ready (Scale)** — Mở sẵn `--workers 4`, tự động non-root, Oracle XE healthcheck.

## 🏗️ Project Structure

```
ai-gateway/                   # Tên repo cũ nhưng sử dụng cho MLOps Server
├── app/
│   ├── main.py              # FastAPI app + lifespan model loading
│   ├── config.py             # Env vars, model configs
│   ├── database.py           # SQLAlchemy async + Oracle
│   ├── routers/
│   │   └── api.py            # /api/infer và /health
│   ├── models/
│   │   ├── schemas.py        # Pydantic (InferenceRequest/Response)
│   │   └── database.py       # SQLAlchemy (InferenceResult table)
│   └── services/
│       └── core.py           # MLModelSingleton + DB methods
├── docker/
│   ├── Dockerfile            # Multi-stage build + workers cmd
│   └── docker-compose.yml    # API + Oracle XE
├── AVOIDANCE_TABLE.md        # Lỗi tránh (multi-stage, non-root...)
└── .env.example
```

## 🚀 Quick Start (Local & Docker)

### Run without Docker (Local Testing)
Do project dùng Oracle database nhưng chạy local có tính năng graceful degraded (bỏ qua cache save DB nếu lỗi DB). Giả lập loading model tốn 2s.
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000
```

### Run using Docker Compose
```bash
cp .env.example .env
cd docker
docker-compose up --build -d
```

## 🧪 Testing the API

```bash
# Health check (will show 'model_loaded': true)
curl http://localhost:8000/health

# Run an Inference prediction
curl -X POST http://localhost:8000/api/infer \
  -H "Content-Type: application/json" \
  -d '{"text": "This application works amazingly well"}'

# Get inference history
curl http://localhost:8000/api/infer/1

# Test validation (text too long or empty)
curl -X POST http://localhost:8000/api/infer \
  -H "Content-Type: application/json" \
  -d '{"text": ""}'
```

### Swagger UI

Mở [http://localhost:8000/docs](http://localhost:8000/docs) để test Swagger UI.

## 🛡️ Best Practices Applied

Xem [AVOIDANCE_TABLE.md](AVOIDANCE_TABLE.md) để thấy chi tiết cách sửa đủ **8 sai lầm phổ biến**.

# pip install fastapi uvicorn
