
from django.shortcuts import render
from .models import Task

# Create your views here.
def home(request):
	"""A view to display the home page with tasks."""

	uncompleted_tasks = Task.objects.filter(completed=False).order_by('due_date')
	completed_tasks = Task.objects.filter(completed=True).order_by('due_date')
	context = {
		'uncompleted_tasks': uncompleted_tasks,
		'completed_tasks': completed_tasks,
	}
	return render(request, 'tasks/index.html', context)
