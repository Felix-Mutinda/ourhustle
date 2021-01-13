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
	JobCategory,
	Job,
	JobComment,
	AppliedJob,
)

from .helpers import (
	create_user,
	create_job,
)


User = get_user_model()


class UserTests(APITestCase):
	"""
	Tests User model.
	"""
	def setUp(self):
		self.user = create_user()

	def test_user_profile_created(self):
		"""
		Test if a user profile is created successfully.
		"""
		self.assertTrue(
			hasattr(self.user, 'profile'),
			"User profile does not exist."
		)

		self.assertTrue(
			isinstance(self.user.profile, UserProfile),
			"User profile is of type {}, expected to be of type {}".format(
				type(self.user.profile), type(UserProfile)
			)
		)

class CVResumeTests(APITestCase):
	"""
	Tests CVResume model.
	"""

	def setUp(self):
		self.user = create_user()

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
			user=self.user,
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
			user=self.user,
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
			user=self.user,
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
		self.user = create_user()

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
			user=self.user,
			school_name=self.school_name,
			course_name=self.course_name,
			start_date=self.start_date,
			end_date=self.end_date,
			grade_obtained=self.grade_obtained
		)

		education = Education.objects.get(pk=1)
		self.assertEqual(
			self.user,
			education.user,
			"Users don't match.")
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
			user=self.user,
			school_name=self.school_name,
			course_name=self.course_name,
			start_date=self.start_date,
		)

		education = Education.objects.get(pk=1)
		self.assertEqual(
			self.user,
			education.user,
			"Users don't match.")

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

	def test_can_create_multiple_education_instances_for_one_user(self):
		"""
		Test if the Foreignkey (usser) works as expected.
		"""
		Education.objects.create(
			user=self.user,
			school_name=self.school_name,
			course_name=self.course_name,
			start_date=self.start_date,
			end_date=self.end_date,
			grade_obtained=self.grade_obtained
		)
		Education.objects.create(
			user=self.user,
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
			education_instances.first().user,
			self.user,
			'Users don\'t match'
		)
		self.assertEqual(
			education_instances.last().user,
			self.user,
			'Users don\'t match'
		)

	def test_can_not_create_education_instance_without_user(self):
		"""
		Tests if non nullable field user throws an error
		if not provided.
		"""
		with self.assertRaises(
			IntegrityError,
			msg = 'Should raise IntegrityError if user not provided.'
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
				user=self.user,
				school_name=self.school_name,
				course_name=self.course_name,
			)


class ExperienceTests(APITestCase):
	"""
	Test Experience model.
	"""
	def setUp(self):
		self.user = create_user()
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
			user=self.user,
			job_title=self.job_title,
			organisation_name=self.organisation_name,
			start_date=self.start_date,
			end_date=self.end_date,
			job_description=self.job_description
		)
		experience_instance = Experience.objects.get(pk=1)
		self.assertEqual(
			self.user,
			experience_instance.user,
			'users don\'t match'
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
		self.user = create_user()
		self.logo = SimpleUploadedFile('logo.jpg', b'JPG IMAGE')
		self.organisation_name = 'Organisation Name'
		self.organisation_description = 'Organisation Description'
		self.organisation = Organisation(
			user=self.user,
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
			organisation_instance.user,
			self.organisation.user,
			'Users don\'t match.'
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
		self.user = create_user()
		self.tag = 'Public Speaking'
		self.skill = Skill(
			user=self.user,
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
			skill_instance.user,
			self.skill.user,
			'User don\'t match.'
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
			Skill.objects.first().user,
			Skill.objects.last().user,
			'Skill instances don\'t belong to the same user.'
		)


class JobCategoryTests(APITestCase):
	"""
	Test JobCategory model.
	"""
	def setUp(self):
		self.category = 'Engineering'
		self.job_category = JobCategory(
			category=self.category,
		)

	def test_can_create_job_category(self):
		"""
		Test if a job category can be created.
		"""
		self.job_category.save()
		job_category_instance = JobCategory.objects.get(pk=1)
		self.assertEqual(
			self.category,
			job_category_instance.category,
			"Job categories don't match."
		)

class JobTests(APITestCase):
	"""
	Test Job model.
	"""
	def setUp(self):
		"""
		Initialize variables.
		"""
		self.created_by = create_user()
		self.organisation = Organisation.objects.create(
			user=self.created_by,
			name='Big Company',
			description='We are everywhere!'
		)
		self.category = JobCategory.objects.create(
			category='Engineering'
		)
		self.title = 'Software Engineering Lead'
		self.description = 'We are excited to ...'
		self.allow_comments = True
		self.start_accepting_applications_at = timezone.now()
		self.stop_accepting_applications_at = timezone.now() + timedelta(days=30)
		self.employment_term = 'Full Term'
		self.seniority_level = 'Mid Level'
		self.location = 'Nairobi'
		self.job = Job(
			created_by=self.created_by,
			organisation=self.organisation,
			category=self.category,
			title=self.title,
			description=self.description,
			allow_comments=self.allow_comments,
			start_accepting_applications_at=self.start_accepting_applications_at,
			stop_accepting_applications_at=self.stop_accepting_applications_at,
			employment_term=self.employment_term,
			seniority_level=self.seniority_level,
			location=self.location
		)

	def test_can_create_job(self):
		"""
		Test if a job instance is created successfully,
		with all fields provided.
		"""
		self.job.save()
		job_instance = Job.objects.get(pk=1)
		self.assertEqual(
			job_instance.created_by,
			self.created_by,
			"created_by fields don't match."
		)
		self.assertEqual(
			job_instance.organisation,
			self.organisation,
			"organisation fields don't match."
		)
		self.assertEqual(
			job_instance.category,
			self.category,
			"category fields don't match."
		)
		self.assertEqual(
			job_instance.title,
			self.title,
			"title fields don't match."
		)
		self.assertEqual(
			job_instance.description,
			self.description,
			"description fields don't match."
		)
		self.assertEqual(
			job_instance.allow_comments,
			self.allow_comments,
			"allow_comments fields don't match."
		)
		self.assertEqual(
			job_instance.start_accepting_applications_at,
			self.start_accepting_applications_at,
			"start_accepting_applications_at fields don't match."
		)
		self.assertEqual(
			job_instance.stop_accepting_applications_at,
			self.stop_accepting_applications_at,
			"stop_accepting_applications_at fields don't match."
		)
		self.assertEqual(
			job_instance.employment_term,
			self.employment_term,
			"employment_term fields don't match."
		)
		self.assertEqual(
			job_instance.seniority_level,
			self.seniority_level,
			"seniority_level fields don't match."
		)
		self.assertEqual(
			job_instance.location,
			self.location,
			"location fields don't match."
		)


class JobCommentTests(APITestCase):
	"""
	Test JobComment model.
	"""
	def setUp(self):
		"""
		Initialize variables.
		"""

		# Create a user for the comment.
		self.created_by = create_user(username='user2')
		self.job = create_job()
		self.text = 'Comment'
		self.heart = True
		self.job_comment = JobComment(
			created_by=self.created_by,
			job=self.job,
			text=self.text,
			heart=self.heart
		)

	def test_can_create_job_comment(self):
		"""
		Test can create a job comment with all fields given.
		"""
		self.job_comment.save()
		job_comment_instance = JobComment.objects.get(pk=1)
		self.assertEqual(
			job_comment_instance.created_by,
			self.created_by,
			"created_by fields don't match."
		)
		self.assertEqual(
			job_comment_instance.job,
			self.job,
			"job fields don't match."
		)
		self.assertEqual(
			job_comment_instance.text,
			self.text,
			"text fields don't match."
		)
		self.assertEqual(
			job_comment_instance.heart,
			self.heart,
			"heart fields don't match."
		)


class AppliedJobTests(APITestCase):
	"""
	Test AppliedJob model.
	"""

	def setUp(self):
		"""
		Initialize variables.
		"""

		# Create a user
		self.applied_by = create_user(username='user2')
		self.job = create_job()
		self.status = 'Applied'
		self.applied_job = AppliedJob(
			applied_by=self.applied_by,
			job=self.job,
			status=self.status
		)

	def test_can_create_applied_job(self):
		"""
		Test if you can create AppliedJob instance, using
		the necesary fields.
		"""
		self.applied_job.save()
		applied_job_instance = AppliedJob.objects.get(pk=1)
		self.assertEqual(
			applied_job_instance.applied_by,
			self.applied_by,
			"applied_by fields don't match."
		)
		self.assertEqual(
			applied_job_instance.job,
			self.job,
			"job fields don't match."
		)
		self.assertEqual(
			applied_job_instance.status,
			self.status,
			"status fields don't match."
		)