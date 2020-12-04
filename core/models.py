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


class Education(models.Model):
	user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	school_name = models.CharField(max_length=255)
	course_name = models.CharField(max_length=255)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField(null=True)
	grade_obtained = models.CharField(max_length=255, blank=True)