from django.contrib import admin

from chat_app.models import Message, User

admin.site.register(Message)
admin.site.register(User)
