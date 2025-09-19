from django.test import TestCase
from .forms import TaskForm
from .models import Category

class TaskFormTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Work")

    def test_task_form_valid(self):
        data = {
            'title': 'Valid Task',
            'due_date': '2025-09-30',
            'category': self.category.id
        }
        form = TaskForm(data)
        self.assertTrue(form.is_valid())

    def test_task_form_invalid(self):
        data = {
            'title': '',  # Title required
            'due_date': '',
            'category': ''
        }
        form = TaskForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('due_date', form.errors)
        self.assertIn('category', form.errors)

    def test_task_form_incomplete(self):
        data = {
            'title': 'Incomplete Task',
            # Missing due_date and category
        }
        form = TaskForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('due_date', form.errors)
        self.assertIn('category', form.errors)

    def test_task_form_title_too_long(self):
        data = {
            'title': 'A' * 201,  # Exceeds max_length=200
            'due_date': '2025-09-30',
            'category': self.category.id
        }
        form = TaskForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)