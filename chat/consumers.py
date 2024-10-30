import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from .models import Message, PrivateChat



class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.other_username = self.scope['url_route']['kwargs']['username']

		self.current_username = self.scope['user'].username

		self.chat_name = f'chat_{min(self.current_username, self.other_username)}_{max(self.current_username, self.other_username)}'

		await self.channel_layer.group_add(self.chat_name, self.channel_name)

		await self.accept()


	async def disconnect(self, close_code):
		# leave the group
		await self.channel_layer.group_discard(
			self.chat_name, self.channel_name	
		)


	async def receive(self, text_data):
		data = json.loads(text_data)
		message = data['message']
		sender = data['sender']

		print("Recieveing chat..")
		print(data)

		await self.save_message(sender, message)

		await self.channel_layer.group_send(
			self.chat_name,
			{
				'type': 'send_message',
				'message': message,
				'sender': sender
			}
		)
		

	async def send_message(self, event):
		sender = event['sender']
		message = event['message']

		await self.send(json.dumps({
			'sender': sender,
			'message': message
		}))


	async def save_message(self, sender, message):
		sender = await self.get_user(sender)
		user2 = await self.get_user(self.scope['url_route']['kwargs']['username'])
		room = await database_sync_to_async(PrivateChat.get_or_create_private_chat)(sender, user2)
		await database_sync_to_async(Message.objects.create)(room=room, sender=sender, message=message)


	@database_sync_to_async
	def get_user(self, username):
		return User.objects.get(username=username)
