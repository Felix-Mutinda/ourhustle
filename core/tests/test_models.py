from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

from rest_framework.test import APITestCase

from core.models import (
	CVResume,
	UserProfile,
	Education
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

		# Create a file like objects representing uploaded data
		self.cv = SimpleUploadedFile('my_cv.pdf', b'Impresive CV')
		self.resume = SimpleUploadedFile('my_resume.pdf', b'Impresive Resume')

	def tearDown(self):
		"""
		Close open files.
		"""
		self.cv.close()
		self.resume.close()

	def test_cv_created(self):
		"""
		Test whether a cv is saved correctly.
		"""

		# Pass a cv file object to CVResume to save to db/disk
		CVResume.objects.create(
			user_profile=self.user_profile,
			cv=self.cv
		)
		self.cv.open() # Reopen the cv object - set seek to 0
		cv_resume = CVResume.objects.get(pk=1)
		self.assertEqual(
			self.cv.read(), cv_resume.cv.read(), # Compare file like objects
			'Created cv does not match the provided one.'
		)

	def test_resume_created(self):
		"""
		Test whether a resume is saved correctly.
		"""

		# Pass a resume file object to CVResume to save to db/disk
		CVResume.objects.create(
			user_profile=self.user_profile,
			resume=self.resume
		)
		self.resume.open() # Reopen the resume object - set seek to 0
		cv_resume = CVResume.objects.get(pk=1)
		self.assertEqual(
			self.resume.read(), cv_resume.resume.read(), # Compare file like objects
			'Created reusme does not match the provided one.'
		)

	def test_cv_and_resume_created(self):
		"""
		Test whether both cv and resume are saved correctly.
		"""
		CVResume.objects.create(
			user_profile=self.user_profile,
			cv=self.cv,
			resume=self.resume
		)
		# Set file positions to the begining
		self.cv.open()
		self.resume.open()

		# Retrieve the saved object
		cv_resume = CVResume.objects.get(pk=1)

		# Check if cv match
		self.assertEqual(
			self.cv.read(), cv_resume.cv.read(), # Compare file like objects
			'Created cv does not match the provided one.'
		)

		# Check if resume match
		self.assertEqual(
			self.resume.read(), cv_resume.resume.read(), # Compare file like objects
			'Created reusme does not match the provided one.'
		)


class EducationTests(APITestCase):
	"""
	Test the Education model.
	"""
	def setUp(self):
		"""
		Create underlying user and user profiles.
		"""
		self.user = User.objects.create_user(
			username='user',
			password='pass'
		)
		self.user_profile = UserProfile.objects.create(
			user=self.user
		)

	def test_education_instance_created(self):
		"""
		Tests if a provided education instance in saved
		to db correctly.
		"""
		school_name = 'My Recent School'
		course_name = 'My Course Name'
		start_date = timezone.now()
		end_date = timezone.now() + timedelta(days=365)
		grade_obtained = 'My Grade'

		Education.objects.create(
			user_profile=self.user_profile,
			school_name=school_name,
			course_name=course_name,
			start_date=start_date,
			end_date=end_date,
			grade_obtained=grade_obtained
		)

		education = Education.objects.get(pk=1)
		self.assertEqual(
			self.user_profile,
			education.user_profile,
			"User profiles don't match.")
		self.assertEqual(
			school_name,
			education.school_name,
			"School names don't match."
		)
		self.assertEqual(
			course_name,
			education.course_name,
			"Course names don't match."
		)
		self.assertEqual(
			start_date,
			education.start_date,
			"Start dates don't match"
		)
		self.assertEqual(
			end_date,
			education.end_date,
			"End dates don't match"
		)
		self.assertEqual(
			grade_obtained,
			education.grade_obtained,
			"Grade obtained don't match"
		)

	def test_education_instance_created_without_required_arguments(self):
		"""
		Tests if a provided education instance (without the required
		arguments) in saved to db correctly.
		"""
		school_name = 'My Recent School'
		course_name = 'My Course Name'
		start_date = timezone.now()

		Education.objects.create(
			user_profile=self.user_profile,
			school_name=school_name,
			course_name=course_name,
			start_date=start_date,
		)

		education = Education.objects.get(pk=1)
		self.assertEqual(
			self.user_profile,
			education.user_profile,
			"User profiles don't match.")
		self.assertEqual(
			school_name,
			education.school_name,
			"School names don't match."
		)
		self.assertEqual(
			course_name,
			education.course_name,
			"Course names don't match."
		)
		self.assertEqual(
			start_date,
			education.start_date,
			"Start dates don't match"
		)