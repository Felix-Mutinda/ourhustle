from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.db import IntegrityError

from rest_framework.test import APITestCase

from core.models import (
	CVResume,
	UserProfile,
	Education,
	Experience,
	Organisation,
	Skill,
)

from .helpers import create_user_profile


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


class ExperienceTests(APITestCase):
	"""
	Test Experience model.
	"""
	def setUp(self):
		self.user = User.objects.create_user(
			username='user',
			password='pass'
		)
		self.user_profile = UserProfile.objects.create(
			user=self.user
		)
		self.job_title = 'Job Title'
		self.organisation_name = 'Organisation Name'
		self.start_date = timezone.now() - timedelta(days=365*2)
		self.end_date = timezone.now() - timedelta(days=30)
		self.job_description = 'Job Description'

	def test_experience_created(self):
		"""
		Tests if an experience instance is created when all
		fields are provided.
		"""
		Experience.objects.create(
			user_profile=self.user_profile,
			job_title=self.job_title,
			organisation_name=self.organisation_name,
			start_date=self.start_date,
			end_date=self.end_date,
			job_description=self.job_description
		)
		experience_instance = Experience.objects.get(pk=1)
		self.assertEqual(
			self.user_profile,
			experience_instance.user_profile,
			'user_profiles don\'t match'
		)
		self.assertEqual(
			self.job_title,
			experience_instance.job_title,
			'job_titles don\'t match'
		)
		self.assertEqual(
			self.organisation_name,
			experience_instance.organisation_name,
			'organisation_names don\'t match'
		)
		self.assertEqual(
			self.start_date,
			experience_instance.start_date,
			'start_dates don\'t match'
		)
		self.assertEqual(
			self.end_date,
			experience_instance.end_date,
			'end_dates don\'t match'
		)
		self.assertEqual(
			self.job_description,
			experience_instance.job_description,
			'job_descriptions don\'t match'
		)


class OrganisationTests(APITestCase):
	"""
	Test Organisation model.
	"""
	def setUp(self):
		"""
		Initialize variables.
		"""
		self.user_profile = create_user_profile()
		self.logo = SimpleUploadedFile('logo.jpg', b'JPG IMAGE')
		self.organisation_name = 'Organisation Name'
		self.organisation_description = 'Organisation Description'
		self.organisation = Organisation(
			user_profile=self.user_profile,
			logo=self.logo,
			name=self.organisation_name,
			description=self.organisation_description
		)

	def tearDown(self):
		"""
		Close open files.
		"""
		self.logo.close()

	def test_organisation_created(self):
		"""
		Test an organisation instance is created correctly,
		given all the data.
		"""
		self.organisation.save()
		organisation_instance = Organisation.objects.get(pk=1)
		self.assertEqual( # Compare file like objects(logos)
			organisation_instance.logo.read(),
			self.organisation.logo.read(),
			'Organisation logo\'s don\'t match.'
		)
		self.assertEqual(
			organisation_instance.user_profile,
			self.organisation.user_profile,
			'User profile\'s don\'t match.'
		)
		self.assertEqual(
			organisation_instance.name,
			self.organisation.name,
			'Organisation name\'s don\'t match.'
		)
		self.assertEqual(
			organisation_instance.description,
			self.organisation.description,
			'Organisation description\'s don\'t match.'
		)


class SkillsTest(APITestCase):
	"""
	Test skill model.
	"""
	def setUp(self):
		"""
		Initialize variables.
		"""
		self.user_profile = create_user_profile()
		self.tag = 'Public Speaking'
		self.skill = Skill(
			user_profile=self.user_profile,
			tag=self.tag
		)

	def test_skill_created(self):
		"""
		Test if a skill instance is created, given
		all the needed data.
		"""
		self.skill.save()
		skill_instance = Skill.objects.get(pk=1)
		self.assertEqual(
			skill_instance.user_profile,
			self.skill.user_profile,
			'User profile\'s don\'t match.'
		)
		self.assertEqual(
			skill_instance.tag,
			self.tag,
			'Skill tag\'s don\'t match.'
		)

	def test_can_create_many_skills(self):
		"""
		Test if a user can create many skills.
		"""
		skill2 = self.skill
		skill2.tag = 'Test Driven Development'
		self.skill.save()
		skill2.save()
		self.assertEqual(
			Skill.objects.first().user_profile,
			Skill.objects.last().user_profile,
			'Skill instances don\'t belong to the same user.'
		)
