from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()

class Notification(models.Model):
	user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name='notifications')
	message = models.CharField(max_length=255, help_text="Notification text")
	url = models.URLField(blank=True, null=True, help_text="Optional link to relevant page/item")
	created_at = models.DateTimeField(auto_now_add=True)
	read = models.BooleanField(default=False, help_text="Whether the user has viewed this notification")

	def __str__(self):
		return f'Notification for {self.user.user.username}: {self.message[:30]}'
