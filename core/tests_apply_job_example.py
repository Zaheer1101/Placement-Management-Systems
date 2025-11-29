from django.test import TestCase, Client
from django.urls import reverse
from core.models import User, StudentProfile, CompanyProfile, JobPosting, Application
from django.utils import timezone

class ApplyJobExampleTest(TestCase):
    def setUp(self):
        # Create a student user
        self.student_user = User.objects.create_user(username='teststudent', email='stud@example.com', password='pass1234', role='student')
        self.student_profile = StudentProfile.objects.create(user=self.student_user, branch='CSE', cgpa=8.5, backlogs=0)

        # Create a company and job
        self.company_user = User.objects.create_user(username='testcompany', email='comp@example.com', password='pass1234', role='company')
        self.company_profile = CompanyProfile.objects.create(user=self.company_user, name='TestCo')
        self.job = JobPosting.objects.create(
            company=self.company_profile,
            title='Test Job',
            description='Test',
            allowed_branches='CSE, ECE',
            min_cgpa=7.0,
            max_backlogs=1,
            is_approved=True,
            application_deadline=timezone.now().date() + timezone.timedelta(days=10)
        )

        self.client = Client()
        self.client.login(username='teststudent', password='pass1234')

    def test_apply_creates_application(self):
        url = reverse('core:apply_for_job', args=[self.job.id])
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Application.objects.filter(job=self.job, student=self.student_profile).exists())
