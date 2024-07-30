import asyncio
from concurrent.futures import ThreadPoolExecutor

from asgiref.sync import sync_to_async, async_to_sync
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import CreateTelegramUserSerializer
from .models import TelegramUser
from .utils import send_message_via_tg_api


class TelegramUserCreateAPIView(generics.CreateAPIView):
    serializer_class = CreateTelegramUserSerializer
    queryset = TelegramUser.objects.all()
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Telegram so'rovini fon jarayonida yuborish
        self.run_in_background(send_message_via_tg_api, serializer)

        return Response({"message": "Message sent successfully"}, status=200, headers=headers)

    def run_in_background(self, func, *args):
        def wrapper():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(func(*args))
            except Exception as e:
                print(f"Error in background task: {e}")
            finally:
                loop.close()

        # ThreadPoolExecutor yordamida yangi ipda vazifani bajarish
        executor = ThreadPoolExecutor(max_workers=1)
        executor.submit(wrapper)
