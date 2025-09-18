
from django.db import models

class Category(models.Model):
	name = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return self.name

class Task(models.Model):
	title = models.CharField(max_length=200)
	due_date = models.DateField()
	completed = models.BooleanField(default=False)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tasks')

	def __str__(self):
		return self.title
