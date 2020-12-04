from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.db import IntegrityError

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
		Create underlying user and user profiles,
		and other variables.
		"""
		self.user = User.objects.create_user(
			username='user',
			password='pass'
		)
		self.user_profile = UserProfile.objects.create(
			user=self.user
		)

		self.school_name = 'My Recent School'
		self.course_name = 'My Course Name'
		self.start_date = timezone.now()
		self.end_date = timezone.now() + timedelta(days=365)
		self.grade_obtained = 'My Grade'


	def test_education_instance_created(self):
		"""
		Tests if a provided education instance in saved
		to db correctly.
		"""

		Education.objects.create(
			user_profile=self.user_profile,
			school_name=self.school_name,
			course_name=self.course_name,
			start_date=self.start_date,
			end_date=self.end_date,
			grade_obtained=self.grade_obtained
		)

		education = Education.objects.get(pk=1)
		self.assertEqual(
			self.user_profile,
			education.user_profile,
			"User profiles don't match.")
		self.assertEqual(
			self.school_name,
			education.school_name,
			"School names don't match."
		)
		self.assertEqual(
			self.course_name,
			education.course_name,
			"Course names don't match."
		)
		self.assertEqual(
			self.start_date,
			education.start_date,
			"Start dates don't match"
		)
		self.assertEqual(
			self.end_date,
			education.end_date,
			"End dates don't match"
		)
		self.assertEqual(
			self.grade_obtained,
			education.grade_obtained,
			"Grade obtained don't match"
		)

	def test_education_instance_created_without_required_arguments(self):
		"""
		Tests if a provided education instance (without the required
		arguments) in saved to db correctly.
		"""

		Education.objects.create(
			user_profile=self.user_profile,
			school_name=self.school_name,
			course_name=self.course_name,
			start_date=self.start_date,
		)

		education = Education.objects.get(pk=1)
		self.assertEqual(
			self.user_profile,
			education.user_profile,
			"User profiles don't match.")
		self.assertEqual(
			self.school_name,
			education.school_name,
			"School names don't match."
		)
		self.assertEqual(
			self.course_name,
			education.course_name,
			"Course names don't match."
		)
		self.assertEqual(
			self.start_date,
			education.start_date,
			"Start dates don't match"
		)

	def test_can_create_multiple_education_instances_for_one_user_profile(self):
		"""
		Test if the Foreignkey (user_profile) works as expected.
		"""
		Education.objects.create(
			user_profile=self.user_profile,
			school_name=self.school_name,
			course_name=self.course_name,
			start_date=self.start_date,
			end_date=self.end_date,
			grade_obtained=self.grade_obtained
		)
		Education.objects.create(
			user_profile=self.user_profile,
			school_name=self.school_name,
			course_name=self.course_name,
			start_date=self.start_date,
			end_date=self.end_date,
			grade_obtained=self.grade_obtained
		)

		education_instances = Education.objects.all()
		self.assertEqual(
			2,
			education_instances.count(),
			'Expected 2 education instances, got {} instead.'.format(education_instances.count())
		)
		self.assertEqual(
			education_instances.first().user_profile,
			self.user_profile,
			'User profiles don\'t match'
		)
		self.assertEqual(
			education_instances.last().user_profile,
			self.user_profile,
			'User profiles don\'t match'
		)

	def test_can_not_create_education_instance_without_user_profile(self):
		"""
		Tests if non nullable field user_profile throws an error
		if not provided.
		"""
		with self.assertRaises(
			IntegrityError,
			msg = 'Should raise IntegrityError if user_profile not provided.'
			):

			Education.objects.create(
				school_name=self.school_name,
				course_name=self.course_name,
				start_date=self.start_date,
			)

	def test_can_not_create_education_instance_without_start_date(self):
		"""
		Tests if non nullable field start_date throws an error
		if not provided.
		"""
		with self.assertRaises(
			IntegrityError,
			msg = 'Should raise IntegrityError if start_date not provided.'
			):

			Education.objects.create(
				user_profile=self.user_profile,
				school_name=self.school_name,
				course_name=self.course_name,
			)