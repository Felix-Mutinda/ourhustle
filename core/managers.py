from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class UserProfileManager(models.Manager):
	"""
	Overides the default manager with extra fields.
	"""
	def create_user(self, **kwargs):
		"""
		Create a user instance with the given kwargs and
		associate it with profile instance.
		"""
		user = User.objects.create_user(**kwargs)
		user_profile = self.create(
			user=user
		)

		return user
