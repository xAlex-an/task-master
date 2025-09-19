from django.test import TestCase
from django.urls import reverse
from .models import Category, Task
from .forms import TaskForm

class HomeViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Work")
        self.task = Task.objects.create(
            title="Test Task",
            due_date="2025-09-30",
            completed=False,
            category=self.category
        )

    def test_home_view_renders_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')

    def test_home_view_context_contains_tasks_and_form(self):
        response = self.client.get(reverse('home'))
        self.assertIn('uncompleted_tasks', response.context)
        self.assertIn('completed_tasks', response.context)
        self.assertIn('form', response.context)
        self.assertIn(self.task, response.context['uncompleted_tasks'])
        self.assertIsInstance(response.context['form'], TaskForm)

    def test_home_view_post_valid_data_creates_task(self):
        data = {
            'title': 'New Task',
            'due_date': '2025-10-01',
            'category': self.category.id
        }
        response = self.client.post(reverse('home'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_home_view_post_invalid_data(self):
        data = {
            'title': '',  # Title required
            'due_date': '',
            'category': ''
        }
        response = self.client.post(reverse('home'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'title', 'This field is required.')

    def test_home_view_no_tasks(self):
        Task.objects.all().delete()
        response = self.client.get(reverse('home'))
        self.assertQuerysetEqual(response.context['uncompleted_tasks'], [])
        self.assertQuerysetEqual(response.context['completed_tasks'], [])