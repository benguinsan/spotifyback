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
# DJANGO
DEBUG=True
SECRET_KEY=change_this_to_a_secure_random_string
INTERNAL_IPS=127.0.0.1
ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_SETTINGS_MODULE=spotifyBack.settings
DOMAIN=localhost:8080

# DATABASE
DB_NAME=spotify_clone
DB_USER=ben
DB_PASSWORD=change_this_password
DB_HOST=db
DB_PORT=3306

# JWT
AUTH_COOKIE_SECURE=False
SIGNING_KEY=change_this_to_a_secure_random_string
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