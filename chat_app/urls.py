from django.urls import path
from django.contrib.auth.views import LogoutView

from chat_app.views import ChatroomView, EnterView

urlpatterns = [
	path('chat/', ChatroomView.as_view(), name='chatroom'),
	path('', EnterView.as_view(), name='enter'),
	path('logout/', LogoutView.as_view(next_page='/'), name='logout')
]