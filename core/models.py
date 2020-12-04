from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class UserProfile(models.Model):
	"""
	Extends the default user with extra fields.
	"""

	user = models.OneToOneField(
		User,
		on_delete=models.CASCADE,
		primary_key=True,
		related_name='profile'
	)

class CVResume(models.Model):
	user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
	cv = models.FileField(upload_to='cvs/%Y/%m/%d/')
	resume = models.FileField(upload_to='resumes/%Y/%m/%d/')