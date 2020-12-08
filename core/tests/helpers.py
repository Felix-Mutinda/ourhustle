from core.models import User, UserProfile


def create_user_profile():
	"""
	Helper to create a user and a corresponding
	user_profile.
	"""
	user = User.objects.create_user(
		username='user',
		password='pass'
	)

	return UserProfile.objects.create(
		user=user
	)