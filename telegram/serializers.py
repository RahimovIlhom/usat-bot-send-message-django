from rest_framework import serializers
from .models import TelegramUser


class CreateTelegramUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = TelegramUser
        fields = ['tg_id', 'status', 'lang']
