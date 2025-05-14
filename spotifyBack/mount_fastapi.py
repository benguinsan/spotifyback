from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.chatbot.api.views import chatbot_app

# Tạo ứng dụng FastAPI chính
main_app = FastAPI()

# Thêm CORS middleware
main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong môi trường production, hãy giới hạn origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount ứng dụng chatbot
main_app.mount("/api/v1/chatbot", chatbot_app) 