# Spotify Clone Backend (Django)


## Giới thiệu
Đây là backend của dự án Spotify Clone, sử dụng Django, Django REST Framework và MySQL.
Frontend của dự án có thể được tìm thấy tại: [Spotify Clone Frontend](https://github.com/benguinsan/spotifyFront)

## Chạy bằng Docker

### 1. Build và chạy bằng docker-compose
```bash
docker-compose up --build
```
- Backend sẽ chạy ở: http://localhost:8000
- Database MySQL sẽ tự động được khởi tạo.

### 2. Dừng dịch vụ
```bash
docker-compose down
```

## Cấu hình biến môi trường
- Sử dụng file `.env` hoặc `.envs` để cấu hình các biến như DB, SECRET_KEY, ...
- Ví dụ:
```
DJANGO_SECRET_KEY=your_secret_key
POSTGRES_DB=spotify
POSTGRES_USER=spotify
POSTGRES_PASSWORD=yourpassword
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

## Các lệnh quản trị Django (nếu không dùng Docker)
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## API endpoint mặc định
- http://localhost:8000/api/v1/