from datetime import timedelta

from django.utils import timezone

from core.models import (
	User,
	UserProfile,
	Organisation,
	JobCategory,
	Job,
)


def create_user(username=None):
	"""
	Helper to create a user instance.
	"""
	user = UserProfile.objects.create_user(
		username=username if username else 'user',
		password='pass'
	)

	return user

def create_job():
	"""
	Helper to create a job.
	"""
	created_by = create_user()
	organisation = Organisation.objects.create(
		user=created_by,
		name='Big Company',
		description='We are everywhere!'
	)
	category = JobCategory.objects.create(
		category='Engineering'
	)
	title = 'Software Engineering Lead'
	description = 'We are excited to ...'
	allow_comments = True
	start_accepting_applications_at = timezone.now()
	stop_accepting_applications_at = timezone.now() + timedelta(days=30)
	employment_term = 'Full Term'
	seniority_level = 'Mid Level'
	location = 'Nairobi'

	return Job.objects.create(
		created_by=created_by,
		organisation=organisation,
		category=category,
		title=title,
		description=description,
		allow_comments=allow_comments,
		start_accepting_applications_at=start_accepting_applications_at,
		stop_accepting_applications_at=stop_accepting_applications_at,
		employment_term=employment_term,
		seniority_level=seniority_level,
		location=location
	)