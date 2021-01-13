from django.db import models
from django.contrib.auth import get_user_model

from .managers import UserProfileManager


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

	# Use a custome manager
	objects = UserProfileManager()


class CVResume(models.Model):
	"""
	Storage for uploaded static CV/Resume.
	"""
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	cv = models.FileField(upload_to='cvs/%Y/%m/%d/', null=True, blank=True)
	resume = models.FileField(upload_to='resumes/%Y/%m/%d/', null=True, blank=True)


class Education(models.Model):
	"""
	User education in their CV/Resume.
	"""
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	school_name = models.CharField(max_length=MAX_LENGTH)
	course_name = models.CharField(max_length=MAX_LENGTH)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField(null=True, blank=True)
	grade_obtained = models.CharField(max_length=MAX_LENGTH, blank=True)


class Experience(models.Model):
	"""
	User experience(previous work) in their dynamic CV/Resume.
	"""
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	job_title = models.CharField(max_length=MAX_LENGTH)
	organisation_name = models.CharField(max_length=MAX_LENGTH)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField(null=True, blank=True)
	job_description = models.TextField(blank=True)


class Organisation(models.Model):
	"""
	Organisation to associate 'posted' jobs with.
	"""
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	logo = models.ImageField(upload_to='images/logos/%Y/%m/%d', null=True, blank=True)
	name = models.CharField(max_length=MAX_LENGTH)
	description = models.TextField()


class Skill(models.Model):
	"""
	User skills for their dynamic CV/Resume.
	"""
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	tag = models.CharField(max_length=MAX_LENGTH)


class JobCategory(models.Model):
	"""
	Job category.
	"""
	category = models.CharField(max_length=MAX_LENGTH)

class Job(models.Model):
	"""
	Represents a job item/object.
	"""
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)
	organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
	category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
	title = models.CharField(max_length=MAX_LENGTH)
	description = models.TextField()
	allow_comments = models.BooleanField(default=True)
	start_accepting_applications_at = models.DateTimeField()
	stop_accepting_applications_at = models.DateTimeField()
	employment_term = models.CharField(max_length=MAX_LENGTH, blank=True)
	seniority_level = models.CharField(max_length=MAX_LENGTH, blank=True)
	location = models.CharField(max_length=MAX_LENGTH, blank=True)


class JobComment(models.Model):
	"""
	Comments for a given job.
	"""
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)
	job = models.ForeignKey(Job, on_delete=models.CASCADE)
	text = models.CharField(max_length=MAX_LENGTH)
	heart = models.BooleanField(default=False)


class AppliedJob(models.Model):
	"""
	Jobs applied by a user.
	"""
	applied_by = models.ForeignKey(User, on_delete=models.CASCADE)
	job = models.ForeignKey(Job, on_delete=models.CASCADE)
	date_applied = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=MAX_LENGTH, default='Applied')