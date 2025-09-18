from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm

# Create your views here.
def home(request):
  """A view to display the home page with tasks."""

  uncompleted_tasks = Task.objects.filter(completed=False).order_by('due_date')
  completed_tasks = Task.objects.filter(completed=True).order_by('due_date')

  if request.method == 'POST':
    form = TaskForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('home')
  else:
    form = TaskForm()

  context = {
    'uncompleted_tasks': uncompleted_tasks,
    'completed_tasks': completed_tasks,
    'form': form,
  }
  return render(request, 'tasks/index.html', context)
