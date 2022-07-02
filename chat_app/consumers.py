import json
from datetime import datetime

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat_app.models import Message, User


class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_group_name = f'general_chat'
		self.user = self.scope['user']
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)
		await self.accept()

	async def disconnect(self, code):
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)
	
	async def receive(self, text_data=None, bytes_data=None):
		text_data_json = json.loads(text_data)
		user = self.user
		message = text_data_json['message']
		date_time = datetime.now()
		await self.save_message(user=user, message=message, date_time=date_time)
		await self.channel_layer.group_send(
			self.room_group_name,
			{	
				'type': 'chat_message',
				'username': user.username,
				'message': message,
				'date_time': date_time.strftime('%H:%M; %Y.%m.%d')
			}
		)
	
	async def chat_message(self, event):
		username = event['username']
		message = event['message']
		date_time = event['date_time']
		await self.send(text_data=json.dumps({
			'username': username,
			'message': message,
			'date_time': date_time
		}))

	@database_sync_to_async
	def save_message(self, user, message, date_time):
		Message.objects.create(author=user, message=message, created_at=date_time)
