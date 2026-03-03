# AVOIDANCE_TABLE — Proof of Avoiding Common Mistakes (MLOps Ver)

Tôi đã tránh đủ **8/8 lỗi** phổ biến trong bảng lỗi buổi 1. Dưới đây là chi tiết cách xử lý:

---

## ✅ Lỗi #1 — Base image `python:latest`

**Cách xử lý:** Dùng image `python:3.11-slim` cho cả builder stage và runtime stage, tiết kiệm hơn 800MB.

```dockerfile
# Stage 1
FROM python:3.11-slim AS builder
...
# Stage 2
FROM python:3.11-slim
COPY --from=builder /install /usr/local
```

---

## ✅ Lỗi #2 — Không có `.dockerignore`

**Cách xử lý:** Đã tạo `.dockerignore` giúp loại bỏ toàn bộ file code Python thừa, biến môi trường `.env`, folder virtualenv, file markdown.

```
__pycache__/
*.pyc
.venv/
.env
*.md
!README.md
```

---

## ✅ Lỗi #3 — Hardcode kết nối DB hay biến bí mật

**Cách xử lý:** Tất cả biến như URL kết nối DB, tên Model, Allowed Origins đều được đọc qua class `Settings` chạy bằng `pydantic-settings`.

```python
# app/config.py
class Settings(BaseSettings):
    DATABASE_URL: str = "oracle+oracledb://.../@db:1521/..."
    MODEL_NAME: str = "sentiment-analysis-v1"
```

---

## ✅ Lỗi #4 — DB không có healthcheck

**Cách xử lý:** Cấu hình `docker-compose.yml` service Oracle XE với healthcheck script `healthcheck.sh`, sau đó bắt API chờ Db chạy xong `depends_on: condition: service_healthy`.

```yaml
db:
  healthcheck:
    test: ["CMD", "healthcheck.sh"]
    interval: 10s
api:
  depends_on:
    db:
      condition: service_healthy
```

---

## ✅ Lỗi #5 — Nhét hết code vào `main.py`

**Cách xử lý:** Tách codebase ra thành các file xử lý độc lập, đặc biệt mô hình ML được tải lên bằng Singleton tách biệt trong `core.py`:
- `config.py`
- `database.py` (SQL engine)
- `routers/api.py` (HTTP endpoints)
- `models/schemas.py` & `models/database.py`
- `services/core.py` (Inference Logic & MLOps object)

---

## ✅ Lỗi #6 — Không dùng Pydantic validate request

**Cách xử lý:** Data đẩy vào MLOps model phải qua filter chữ nghiêm ngặt:

```python
class InferenceRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
```
API tự động chặn chuỗi rỗng và chuỗi siêu dài để tránh overload inference. Trả về `422 Unprocessable Entity` với JSON chỉ rõ lỗi.

---

## ✅ Lỗi #7 — CORS `*` làm tăng rủi ro security

**Cách xử lý:** Frontend truyền danh sách URL bằng file `.env` qua biến `ALLOWED_ORIGINS` thay vì dùng string wildcard `["*"]` cẩu thả.

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins, 
)
```

---

## ✅ Lỗi #8 — Chạy worker ở quyền root

**Cách xử lý:** Trong `Dockerfile`, sau khi cài đặt package xong, app được set qua tài khoản linux thường mang tính an toàn cao:

```dockerfile
# Create non-root user
RUN useradd -m -r aiuser && chown -R aiuser:aiuser /app

USER aiuser
CMD ["uvicorn", "app.main:app", ..., "--workers", "4"]
```
Đặc biệt app đã bật thêm `--workers 4` chuyên biệt phục vụ server ML chịu tải dự đoán văn bản để không nghẽn cổ chai.
