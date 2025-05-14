from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from django.db.models import Count
from apps.audio.models import Track
from apps.users.models import User
from apps.artists.models import Artist
from apps.albums.models import Album
from apps.genre.models import Genre
from apps.playlists.models import Playlist

# Tạo ứng dụng FastAPI
chatbot_app = FastAPI()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    message: str
    suggestions: Optional[List[str]] = None

@chatbot_app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> Dict[str, Any]:
    user_message = request.message.lower()
    
    # Xử lý chào hỏi
    greetings = ["xin chào", "chào", "hello", "hi", "hey"]
    if any(greeting in user_message for greeting in greetings):
        return {
            "message": "Xin chào! Tôi là trợ lý ảo của Spotify-Clone. Tôi có thể giúp bạn:",
            "suggestions": [
                "Gợi ý bài hát theo thể loại",
                "Thống kê hệ thống",
                "Tìm nghệ sĩ nổi tiếng"
            ]
        }
    
    # Xử lý gợi ý bài hát theo thể loại
    if ("gợi ý" in user_message or "đề xuất" in user_message) and ("bài hát" in user_message or "nhạc" in user_message):
        # Trích xuất thể loại từ tin nhắn
        genre_name = extract_genre(user_message)
        
        try:
            # Tìm thể loại trong database
            genre = Genre.objects.filter(name__icontains=genre_name).first()
            
            if not genre:
                return {
                    "message": f"Xin lỗi, tôi không tìm thấy thể loại '{genre_name}'. Bạn có thể thử các thể loại khác như pop, rock, jazz...",
                    "suggestions": ["Gợi ý bài hát thể loại pop", "Gợi ý bài hát thể loại rock", "Thống kê hệ thống"]
                }
            
            # Lấy các bài hát theo thể loại
            tracks = Track.objects.filter(genre=genre, is_private=False).order_by('-plays_count')[:5]
            
            if not tracks:
                return {
                    "message": f"Hiện tại không có bài hát nào thuộc thể loại {genre.name}.",
                    "suggestions": ["Gợi ý bài hát thể loại pop", "Thống kê hệ thống"]
                }
            
            response = f"Đây là một số bài hát thể loại {genre.name} được yêu thích:\n\n"
            for i, track in enumerate(tracks, 1):
                response += f"{i}. {track.title} - {track.artist.display_name}\n"
            
            return {
                "message": response,
                "suggestions": ["Thống kê hệ thống", f"Tìm nghệ sĩ {tracks[0].artist.display_name}"]
            }
            
        except Exception as e:
            return {
                "message": "Xin lỗi, có lỗi xảy ra khi tìm kiếm bài hát.",
                "suggestions": ["Thống kê hệ thống", "Gợi ý bài hát thể loại pop"]
            }
    
    # Xử lý tìm nghệ sĩ
    if "tìm nghệ sĩ" in user_message or "nghệ sĩ" in user_message:
        try:
            # Tìm tên nghệ sĩ trong tin nhắn
            artist_name = extract_artist_name(user_message)
            
            if not artist_name:
                # Lấy các nghệ sĩ nổi tiếng nhất
                artists = Artist.objects.all().order_by('-created_at')[:5]
                
                if not artists:
                    return {
                        "message": "Hiện tại không có nghệ sĩ nào trong hệ thống.",
                        "suggestions": ["Thống kê hệ thống", "Gợi ý bài hát thể loại pop"]
                    }
                
                response = "Đây là một số nghệ sĩ nổi tiếng trên Spotify-Clone:\n\n"
                for i, artist in enumerate(artists, 1):
                    response += f"{i}. {artist.display_name}\n"
                
                return {
                    "message": response,
                    "suggestions": ["Thống kê hệ thống", f"Tìm bài hát của {artists[0].display_name}"]
                }
            
            # Tìm nghệ sĩ theo tên
            artist = Artist.objects.filter(display_name__icontains=artist_name).first()
            
            if not artist:
                return {
                    "message": f"Xin lỗi, tôi không tìm thấy nghệ sĩ '{artist_name}'.",
                    "suggestions": ["Thống kê hệ thống", "Gợi ý bài hát thể loại pop"]
                }
            
            # Lấy các bài hát của nghệ sĩ
            tracks = Track.objects.filter(artist=artist, is_private=False).order_by('-plays_count')[:5]
            
            response = f"Thông tin về nghệ sĩ {artist.display_name}:\n\n"
            if artist.is_verify:
                response += "✓ Đã xác thực\n\n"
            
            if tracks:
                response += "Các bài hát nổi tiếng:\n"
                for i, track in enumerate(tracks, 1):
                    response += f"{i}. {track.title}\n"
            else:
                response += "Hiện tại nghệ sĩ này chưa có bài hát nào."
            
            return {
                "message": response,
                "suggestions": ["Thống kê hệ thống", "Gợi ý bài hát thể loại pop"]
            }
            
        except Exception as e:
            return {
                "message": "Xin lỗi, có lỗi xảy ra khi tìm kiếm nghệ sĩ.",
                "suggestions": ["Thống kê hệ thống", "Gợi ý bài hát thể loại pop"]
            }
    
    # Xử lý thống kê
    if "thống kê" in user_message or "tổng số" in user_message:
        try:
            total_songs = Track.objects.count()
            total_users = User.objects.count()
            total_artists = Artist.objects.count()
            total_albums = Album.objects.count()
            total_playlists = Playlist.objects.count()
            
            response = "📊 Thống kê hệ thống:\n\n"
            response += f"🎵 Tổng số bài hát: {total_songs}\n"
            response += f"👤 Tổng số người dùng: {total_users}\n"
            response += f"🎤 Tổng số nghệ sĩ: {total_artists}\n"
            response += f"💿 Tổng số album: {total_albums}\n"
            response += f"📋 Tổng số playlist: {total_playlists}\n"
            
            # Thêm thống kê về thể loại phổ biến nhất
            top_genres = Genre.objects.annotate(track_count=Count('tracks')).order_by('-track_count')[:3]
            if top_genres:
                response += "\n🏆 Thể loại phổ biến nhất:\n"
                for i, genre in enumerate(top_genres, 1):
                    response += f"{i}. {genre.name} ({genre.track_count} bài hát)\n"
            
            return {
                "message": response,
                "suggestions": ["Gợi ý bài hát thể loại pop", "Tìm nghệ sĩ nổi tiếng"]
            }
            
        except Exception as e:
            return {
                "message": "Xin lỗi, có lỗi xảy ra khi lấy thống kê hệ thống.",
                "suggestions": ["Gợi ý bài hát thể loại pop", "Tìm nghệ sĩ nổi tiếng"]
            }
    
    # Phản hồi mặc định
    return {
        "message": "Xin lỗi, tôi không hiểu yêu cầu của bạn. Tôi có thể giúp bạn gợi ý bài hát theo thể loại, tìm nghệ sĩ hoặc xem thống kê hệ thống.",
        "suggestions": ["Gợi ý bài hát thể loại pop", "Thống kê hệ thống", "Tìm nghệ sĩ nổi tiếng"]
    }

def extract_genre(message):
    # Lấy danh sách thể loại từ database
    genres = Genre.objects.values_list('name', flat=True)
    
    # Tìm thể loại trong tin nhắn
    for genre in genres:
        if genre.lower() in message.lower():
            return genre
    
    # Nếu không tìm thấy, trả về thể loại mặc định
    return "pop"

def extract_artist_name(message):
    # Tách các từ trong tin nhắn
    words = message.split()
    
    # Tìm vị trí của từ "nghệ sĩ" hoặc "ca sĩ"
    artist_index = -1
    for i, word in enumerate(words):
        if word in ["nghệ sĩ", "ca sĩ", "artist", "singer"]:
            artist_index = i
            break
    
    # Nếu tìm thấy và có từ tiếp theo
    if artist_index != -1 and artist_index < len(words) - 1:
        # Lấy tất cả các từ sau từ "nghệ sĩ"
        return " ".join(words[artist_index + 1:])
    
    return None
