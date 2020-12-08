from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
MAX_LENGTH = 255

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
	"""
	Storage for uploaded static CV/Resume.
	"""
	user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
	cv = models.FileField(upload_to='cvs/%Y/%m/%d/')
	resume = models.FileField(upload_to='resumes/%Y/%m/%d/')


class Education(models.Model):
	"""
	User education in their CV/Resume.
	"""
	user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	school_name = models.CharField(max_length=MAX_LENGTH)
	course_name = models.CharField(max_length=MAX_LENGTH)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField(null=True)
	grade_obtained = models.CharField(max_length=MAX_LENGTH, blank=True)


class Experience(models.Model):
	"""
	User experience(previous work) in their dynamic CV/Resume.
	"""
	user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	job_title = models.CharField(max_length=MAX_LENGTH)
	organisation_name = models.CharField(max_length=MAX_LENGTH)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField(null=True)
	job_description = models.TextField(blank=True)


class Organisation(models.Model):
	"""
	Organisation to associate 'posted' jobs with.
	"""
	user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
	logo = models.ImageField(upload_to='images/logos/%Y/%m/%d')
	name = models.CharField(max_length=MAX_LENGTH)
	description = models.TextField()