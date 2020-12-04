import filecmp

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APITestCase

from core.models import (
	CVResume,
	UserProfile
)


User = get_user_model()


class UserProfileTests(APITestCase):
	"""
	Tests UserProfile modle.
	"""
	def setUp(self):
		self.user = User.objects.create_user(
				username='user',
				password='pass'
			)

	def test_user_profile_created(self):
		"""
		Test if a user profile is created successfully.
		"""
		user_profile = UserProfile.objects.create(
			user = self.user
		)
		self.assertEqual(
			user_profile,
			self.user.profile,
			'User profiles don\'t match'
		)

class CVResumeTests(APITestCase):
	"""
	Tests CVResume model.
	"""

	def setUp(self):
		self.user = User.objects.create_user(
			username='user',
			password='pass'
		)
		self.user_profile = UserProfile.objects.create(
			user=self.user
		)

	def test_cv_created(self):
		"""
		Test whether a cv is saved correctly.
		"""

		# Create a file like object representing uploaded data
		# Then pass it to CVResume to save to db/disk
		cv = SimpleUploadedFile('my_cv.pdf', b'Impresive CV')
		CVResume.objects.create(
			user_profile=self.user_profile,
			cv=cv
		)
		cv.open() # Reopen the cv object - set seek to 0
		cv_resume = CVResume.objects.get(pk=1)
		self.assertEqual(
			cv.read(), cv_resume.cv.read(), # Compare file like objects
			'Created cv does not match the provided one.'
		)

	def test_resume_created(self):
		"""
		Test whether a resume is saved correctly.
		"""

		# Create a file like object representing uploaded data
		# Then pass it to CVResume to save to db/disk
		resume = SimpleUploadedFile('my_resume.pdf', b'Impresive Resume')
		CVResume.objects.create(
			user_profile=self.user_profile,
			resume=resume
		)
		resume.open() # Reopen the resume object - set seek to 0
		cv_resume = CVResume.objects.get(pk=1)
		self.assertEqual(
			resume.read(), cv_resume.resume.read(), # Compare file like objects
			'Created reusme does not match the provided one.'
		)

	def test_cv_and_resume_created(self):
		"""
		Test whether both cv and resume are saved correctly.
		"""
		cv = SimpleUploadedFile('my_cv.pdf', b'Impresive CV')
		resume = SimpleUploadedFile('my_resume.pdf', b'Impresive Resume')
		CVResume.objects.create(
			user_profile=self.user_profile,
			cv=cv,
			resume=resume
		)
		# Set file positions to the begining
		cv.open()
		resume.open()

		# Retrieve the saved object
		cv_resume = CVResume.objects.get(pk=1)

		# Check if cv match
		self.assertEqual(
			cv.read(), cv_resume.cv.read(), # Compare file like objects
			'Created cv does not match the provided one.'
		)

		# Check if resume match
		self.assertEqual(
			resume.read(), cv_resume.resume.read(), # Compare file like objects
			'Created reusme does not match the provided one.'
		)
