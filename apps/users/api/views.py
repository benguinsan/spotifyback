from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from djoser.social.views import ProviderAuthView
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status, views
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from apps.core import pagination
from apps.core.permissions import IsOwnerUserPermission
from apps.users.api.serializers import (
    CustomUserUpdateSerializer,
    ShortCustomUserSerializer,
    UpdateUserProfileImageSerializer,
)

User = get_user_model()

def set_cookie(response: Response, access_token: str = None, refresh_token: str = None) -> None:
    """
    Set cookies for access and refresh tokens
    """

    if access_token:
        response.set_cookie(
            "access",
            access_token,
            max_age=settings.SIMPLE_JWT["AUTH_COOKIE_MAX_AGE"],
            path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
    
    if refresh_token:
        response.set_cookie(
            "refresh",
            refresh_token,
            max_age=settings.SIMPLE_JWT["AUTH_COOKIE_MAX_AGE"],
            path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    Customize TokenObtainPairView to set cookies for access and refresh tokens
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)

        try:
            email_ = request.data["email"]
            password = request.data["password"]
        except KeyError:
            return Response({"detail": "email and/or password not provided."}, status=status.HTTP_400_BAD_REQUEST)

        if authenticate(email=email_, password=password) is None:
            user = get_object_or_404(User, email=email_)

            if not user.is_active:
                return Response({"detail": "user is not active."}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({"detail": "user password wrong."}, status=status.HTTP_401_UNAUTHORIZED)

        if response.status_code == 200:
            access_token = response.data.get("access")
            refresh_token = response.data.get("refresh")

            set_cookie(response, access_token, refresh_token)

        return response
    
class LogoutView(views.APIView):
    """
    Extend Djoser's LogoutView to delete cookies for access and refresh tokens
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = None

    def post(self, request: Request) -> Response:
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("access")
        response.delete_cookie("refresh")

        return response

class CustomTokenRefreshView(TokenRefreshView):
    """
    Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid.
    Customize TokenRefreshView to set cookies for access and refresh tokens
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        refresh_token = request.COOKIES.get("refresh")

        if request.data.get("refresh"):
            pass
        elif refresh_token:
            request.data["refresh"] = refresh_token
        else:
            return Response({"detail": "refresh token not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get("access")
            refresh_token = response.data.get("refresh")

            set_cookie(response, access_token, refresh_token)

        return response

class CustomTokenVerifyView(TokenVerifyView):
    """
    Takes a token and indicates if it is valid.
    This view provides no information about a token's fitness for a particular use.
    Customize TokenVerifyView to set cookies for access and refresh tokens
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        access_token = request.COOKIES.get("access")

        if request.data.get("token"):
            pass
        elif access_token:
            request.data["token"] = access_token
        else:
            return Response({"detail": "access token not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        return super().post(request, *args, **kwargs)

@extend_schema(tags=["User Following"])
class UserFollowAPIView(views.APIView):
    """
    Follow users. Only users who have not followed can follow.
    1. Check if user is following yourself. If yes, return an error message `HTTP_400_BAD_REQUEST`.
    2. Check if user has already followed. If yes, return an error message `HTTP_400_BAD_REQUEST`.
    3. Follow user `HTTP_200_OK`.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None

    def post(self, request, user_id) -> Response:
        user = request.user
        user_to_follow = get_object_or_404(User, id=user_id)

        if user == user_to_follow:
            return Response({"msg": "You can not follow yourself"}, status.HTTP_400_BAD_REQUEST)

        if user_to_follow.check_following(user.id):
            return Response({"msg": "You have already followed this user"}, status.HTTP_400_BAD_REQUEST)

        user_to_follow.follow(user)
        return Response({"msg": "You have followed this user"}, status.HTTP_200_OK)

@extend_schema(tags=["User Following"])
class UserUnfollowAPIView(views.APIView):
    """
    Unfollow users. Only users who have followed can unfollow.
    1. Check if user is following yourself. If yes, return an error message `HTTP_400_BAD_REQUEST`.
    2. Check if user has already unfollowed. If yes, return an error message `HTTP_400_BAD_REQUEST`.
    3. Unfollow user `HTTP_200_OK`.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None

    def post(self, request, user_id) -> Response:
        user = request.user
        user_to_unfollow = get_object_or_404(User, id=user_id)

        if user == user_to_unfollow:
            return Response({"msg": "You can not unfollow yourself"}, status.HTTP_400_BAD_REQUEST)

        if not user_to_unfollow.check_following(user.id):
            return Response({"msg": "You have not followed this user"}, status.HTTP_400_BAD_REQUEST)

        user_to_unfollow.unfollow(user)
        return Response({"msg": "You have unfollowed this user"}, status.HTTP_200_OK)

@extend_schema(tags=["User Following"])
class ListUserFollowersAPIView(generics.ListAPIView):
    """
    List followers of a user. Public users can see their followers.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = ShortCustomUserSerializer
    pagination_class = None
    lookup_field = "id"

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs["user_id"])
        return user.get_followers()


@extend_schema(tags=["User Following"])
class ListUserFollowingAPIView(generics.ListAPIView):
    """
    List following of a user. Public users can see their following.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = ShortCustomUserSerializer
    pagination_class = None
    lookup_field = "id"

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs["user_id"])
        return user.get_following()


@extend_schema(tags=["User Profile"])
class ListUsersProfileAPIView(generics.ListAPIView):
    """
    List User Profile. Public users can see other profile.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = ShortCustomUserSerializer
    pagination_class = pagination.StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["display_name", "playlists__title"]
    ordering_fields = ["created_at", "followers_count"]

    def get_queryset(self):
        return User.objects.filter(type_profile="user", is_staff=False, is_superuser=False, is_active=True)

@extend_schema(tags=["User Profile"])
class DetailMyUserProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    Retrieve user profile. Only users can see their profile.
    """

    permission_classes = [IsOwnerUserPermission]
    serializer_class = CustomUserUpdateSerializer

    def get_object(self):
        return self.request.user


@extend_schema(tags=["User Profile"])
class MyUserProfileImageAPIView(generics.UpdateAPIView):
    """
    Update user profile image. Only users can update their profile image.
    """

    permission_classes = [IsOwnerUserPermission]
    serializer_class = UpdateUserProfileImageSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user

# login with google
@extend_schema(tags=["Oauth2"])
class CustomProviderAuthView(ProviderAuthView):
    """
    Extend Djoser's ProviderAuthView to set cookies for access and refresh tokens.
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)

        if response.status_code == 201:
            access_token = response.data.get("access")
            refresh_token = response.data.get("refresh")

            set_cookie(response, access_token, refresh_token)

        return response
