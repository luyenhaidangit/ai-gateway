# AI Gateway

`AI Gateway` là một service FastAPI cung cấp API suy luận sentiment cho dữ liệu text.
Ứng dụng nạp model giả lập khi khởi động, hỗ trợ kiểm tra trạng thái hệ thống và có thể lưu lịch sử suy luận vào Oracle Database.

## Mục tiêu repo

Repo này dùng để triển khai một API service đơn giản theo hướng production-ready ở mức cơ bản:

- khởi động ứng dụng qua FastAPI lifespan
- kết nối Oracle Database bằng SQLAlchemy async
- cung cấp endpoint suy luận và tra cứu lịch sử
- mở tài liệu Swagger để test nhanh
- đóng gói chạy bằng Docker

## Công nghệ sử dụng

- Python `3.11+`
- FastAPI
- Uvicorn
- SQLAlchemy `2.x`
- OracleDB driver (`oracledb`)
- Pydantic Settings
- Structlog
- Docker

## Cấu trúc thư mục

```text
flex-ai-gateway/
|-- app/
|   |-- main.py                # Entry point FastAPI
|   |-- config.py              # Đọc cấu hình từ .env
|   |-- database.py            # Engine, session, init_db, get_db
|   |-- routers/
|   |   `-- api.py             # API routes và health check
|   |-- services/
|   |   |-- core.py            # Model giả lập và logic inference
|   |   `-- inference_service.py
|   |-- models/
|   |   |-- database.py        # SQLAlchemy models
|   |   `-- schemas.py         # Request/response schemas
|   |-- core/
|   |   |-- config.py
|   |   |-- dependencies.py
|   |   |-- exceptions.py
|   |   |-- logging.py
|   |   `-- security.py
|   |-- db/
|   |   |-- base.py
|   |   `-- session.py
|   |-- repositories/
|   |   `-- inference_repository.py
|   `-- schemas/
|       `-- inference_schema.py
|-- secrets/
|   `-- oracle-wallet/
|-- .env.example
|-- Dockerfile
|-- pyproject.toml
|-- README.md
```

## Các endpoint chính

- `POST /api/infer`: gửi text để suy luận sentiment
- `GET /api/infer/{infer_id}`: lấy lại kết quả suy luận theo ID
- `GET /health`: kiểm tra trạng thái model và database
- `GET /docs`: Swagger UI

## Yêu cầu môi trường

Trước khi chạy, cần có:

- Python `3.11` trở lên
- `pip` mới
- Oracle Database nếu muốn lưu lịch sử xuống DB
- Oracle Wallet nếu môi trường của bạn yêu cầu kết nối wallet

Lưu ý:

- Service vẫn có thể khởi động nếu database chưa sẵn sàng
- Khi database lỗi, một số chức năng lưu lịch sử sẽ degrade thay vì làm sập toàn bộ app

## Cấu hình môi trường

Project đọc biến môi trường từ file `.env`.

Tạo file `.env` từ mẫu:

```powershell
Copy-Item .env.example .env
```

Các biến cấu hình quan trọng:

- `DATABASE_URL`: chuỗi kết nối Oracle
- `ORACLE_WALLET_DIR`: đường dẫn tới thư mục wallet
- `ORACLE_WALLET_PASSWORD`: mật khẩu wallet nếu có
- `MODEL_NAME`: tên model đang dùng
- `CONFIDENCE_THRESHOLD`: ngưỡng cấu hình cho model
- `ALLOWED_ORIGINS`: danh sách origin CORS, phân tách bằng dấu phẩy

Khuyến nghị:

- không dùng nguyên secret trong `.env.example` cho môi trường thật
- thay toàn bộ thông tin user/password thật bằng giá trị riêng của môi trường của bạn

## Cài đặt local

### 1. Tạo virtual environment

```powershell
python -m venv .venv
```

### 2. Kích hoạt virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Cài đặt dependencies

```powershell
pip install --upgrade pip
pip install -e .
```

## Chạy ứng dụng local

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Sau khi chạy thành công:

- API base URL: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/health`

## Chạy bằng Docker

### Build image

```powershell
docker build -t ai-gateway .
```

### Run container

```powershell
docker run --rm -p 8000:8000 --env-file .env ai-gateway
```

## Test nhanh API

### Health check

```powershell
curl http://localhost:8000/health
```

### Gọi suy luận

```powershell
curl -X POST http://localhost:8000/api/infer `
  -H "Content-Type: application/json" `
  -d '{"text":"This application works amazingly well"}'
```

### Lấy lịch sử theo ID

```powershell
curl http://localhost:8000/api/infer/1
```

## Luồng khởi động ứng dụng

Entry point của service là [`app/main.py`](C:\Workspace\Personal\flex-ai-gateway\app\main.py).

Khi service khởi động:

1. FastAPI tạo app instance
2. `lifespan()` chạy `init_db()` để kiểm tra hoặc tạo bảng
3. `lifespan()` chạy `ml_model.load_model()` để nạp model giả lập
4. middleware CORS được đăng ký
5. routers API và health được mount

## Ghi chú phát triển

- Entry point runtime: `app.main:app`
- Package management hiện dùng `pyproject.toml`
- Dockerfile hiện chạy service bằng Uvicorn trên cổng `8000`
- Nếu muốn chuẩn hóa hơn nữa, có thể tiếp tục gom cấu hình, DB session và logging về các module `app/core` và `app/db`
