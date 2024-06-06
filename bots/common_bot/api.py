from rest_framework import serializers
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

# owerwrite the ListAPIView class to authenticate the user
from .apps import BotConfig
from .models import User, Location, Channel, MovieTrailer, Movie, MovieChannel, Unnecessary_word_filter

app_name = BotConfig.app_url


class ListAPIAuthView(ListAPIView):
    permission_classes = [IsAuthenticated]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        ref_name = f"{app_name}_user"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        ref_name = f"{app_name}_location"


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'
        ref_name = f"{app_name}_channel"


class MovieTrailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieTrailer
        fields = '__all__'
        ref_name = f"{app_name}_movie_trailer"


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        ref_name = f"{app_name}_movie"


class MovieChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieChannel
        fields = '__all__'
        ref_name = f"{app_name}_movie_channel"


class Unnecessary_word_filterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unnecessary_word_filter
        fields = '__all__'
        ref_name = f"{app_name}_unnecessary_word_filter"


class UserApi(ListAPIAuthView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LocationApi(ListAPIAuthView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class ChannelApi(ListAPIAuthView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class MovieTrailerApi(ListAPIAuthView):
    queryset = MovieTrailer.objects.all()
    serializer_class = MovieTrailerSerializer


class MovieApi(ListAPIAuthView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieChannelApi(ListAPIAuthView):
    queryset = MovieChannel.objects.all()
    serializer_class = MovieChannelSerializer


class UnnecessaryWordFilterApi(ListAPIAuthView):
    queryset = Unnecessary_word_filter.objects.all()
    serializer_class = Unnecessary_word_filterSerializer
