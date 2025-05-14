"""
ASGI config for spotifyBack project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from fastapi.applications import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spotifyBack.settings')

# Khởi tạo ứng dụng Django
django_app = get_asgi_application()

# Import FastAPI app sau khi đã thiết lập Django
from spotifyBack.mount_fastapi import main_app

# Mount Django app dưới đường dẫn "/"
main_app.mount("/", WSGIMiddleware(django_app))

# Đặt application là FastAPI app
application = main_app
