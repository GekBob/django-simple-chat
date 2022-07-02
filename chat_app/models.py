from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager


class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(unique=True, db_index=True, max_length=25)
	email = models.EmailField(unique=True, blank=True, null=True)

	is_staff = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'username'

	def __str__(self) -> str:
		return self.username


class Message(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	message = models.TextField()
	created_at = models.DateTimeField()

	class Meta:
		ordering = ['created_at']

	def __str__(self) -> str:
		return str(self.id)
