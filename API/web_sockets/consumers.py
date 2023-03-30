import json

from channels.generic.websocket import WebsocketConsumer
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from API.models import *


class ClientNotificationConsumer(WebsocketConsumer):
    

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.client_id = None

    def connect(self):

        user = self.get_connection_user()
        if not hasattr(user, 'client'):
            self.accept()
            self.send(text_data="Invalid/No Token")
            self.close()
            return

        self.client_id = user.client.id
        print(f"Client ({self.client_id}) just connected")
        
        @receiver(post_save, sender=ClientNotification, dispatch_uid=f"client_{self.client_id}")
        def notification_sender(sender, instance: ClientNotification=None, created=False, **kwargs):

            if created and instance.client_id==self.client_id:

                data_to_send = {"notification": instance.to_dict()}

                print(f"{data_to_send=}")
                self.send(text_data=json.dumps(data_to_send))
        
        self.accept()
        self.send(text_data=f"helloooo, you are client ({self.client_id})")

    def disconnect(self, close_code):
        print(f"{close_code=}")

    def receive(self, text_data=None, bytes_data=None):

        print(f"Client ({self.client_id}) just sent:")
        try:
            text_data_json = json.loads(text_data)
            print(text_data_json)
        except Exception as e:
            print(text_data)

    def get_connection_user(self):

        headers = self.scope.get('headers')
        headers = list(map(lambda el: (el[0].decode("ascii"), el[1].decode("ascii")), headers))
        headers = dict(headers)

        token = headers.get("authorization")
        if token is None:
            return
        
        token = token.lstrip("Token ")
        token = Token.objects.filter(key=token).first()
        if token is None:
            return

        return token.user



class StoreNotificationConsumer(WebsocketConsumer):
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.store_id = None

    def connect(self):

        user = self.get_connection_user()
        if not hasattr(user, 'store'):
            self.accept()
            self.send(text_data="Invalid/No Token")
            self.close()
            return

        self.store_id = user.store.id
        print(f"Store ({self.store_id}) just connected")
        
        @receiver(post_save, sender=StoreNotification, dispatch_uid=f"store_{self.store_id}")
        def notification_sender(sender, instance: StoreNotification=None, created=False, **kwargs):

            if created and instance.store_id==self.store_id:

                data_to_send = {"notification": instance.to_dict()}

                print(f"{data_to_send=}")
                self.send(text_data=json.dumps(data_to_send))
        
        self.accept()
        self.send(text_data=f"helloooo, you are store ({self.store_id})")

    def disconnect(self, close_code):
        print(f"{close_code=}")

    def receive(self, text_data=None, bytes_data=None):

        print(f"Store ({self.store_id}) just sent:")
        try:
            text_data_json = json.loads(text_data)
            print(text_data_json)
        except Exception as e:
            print(text_data)

    def get_connection_user(self):

        headers = self.scope.get('headers')
        headers = list(map(lambda el: (el[0].decode("ascii"), el[1].decode("ascii")), headers))
        headers = dict(headers)

        token = headers.get("authorization")
        if token is None:
            return
        
        token = token.lstrip("Token ")
        token = Token.objects.filter(key=token).first()
        if token is None:
            return

        return token.user

