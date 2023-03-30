from django.urls import path

from API.web_sockets import consumers

websocket_urlpatterns = [
    path("client_notification/", consumers.ClientNotificationConsumer.as_asgi()),
    path("store_notification/", consumers.StoreNotificationConsumer.as_asgi()),
]