from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreatePasswordRetypeSerializer, UserSerializer
from django_countries.serializers import CountryFieldMixin

User = get_user_model()


class CustomUserCreatePasswordRetypeSerializer(CountryFieldMixin, UserCreatePasswordRetypeSerializer):
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        model = User
        fields = ("id", "email", "display_name", "gender", "country", "type_profile", "image", "password")

class CustomUserSerializer(CountryFieldMixin, UserSerializer):
    type_profile = serializers.CharField(source="get_type_profile_display", read_only=True)
    gender = serializers.CharField(source="get_gender_display", read_only=True)
    followers_count = serializers.IntegerField(source="followers.count", read_only=True)
    following_count = serializers.IntegerField(source="following.count", read_only=True)
    playlists_count = serializers.IntegerField(source="playlists.count", read_only=True)
    artist_slug = serializers.CharField(source="artist.slug", read_only=True)

    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            "id",
            "email",
            "display_name",
            "gender",
            "image",
            "country",
            "type_profile",
            "artist_slug",
            "followers_count",
            "following_count",
            "playlists_count",
        )
        read_only_fields = ("email", "type_profile", "color")

class CustomUserUpdateSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            "id",
            "email",
            "display_name",
            "gender",
            "image",
            "type_profile",
            "country",
        )
        read_only_fields = ("email", "type_profile")

class ShortCustomUserSerializer(CustomUserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ("id", "display_name", "type_profile", "artist_slug", "image", "followers_count")

class UpdateUserProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("image",)