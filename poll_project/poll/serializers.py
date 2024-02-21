from rest_framework import serializers
from .models import PollRoom, PollOption

class PollRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollRoom
        fields = ['id', 'creator', 'title']

class PollOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollOption
        fields = ['id', 'poll_room', 'option_text', 'vote_count']
