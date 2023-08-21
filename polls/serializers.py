from rest_framework import serializers

from .models import Polls



class PollsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polls
        fields = [
            'question', 'author', 'option1',
            'option2', 'option3', 'status'
        ]

        