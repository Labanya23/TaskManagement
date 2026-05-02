from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date, timedelta
from django.shortcuts import redirect
from .models import Task
from django.shortcuts import get_object_or_404

def task_list(request):
    return HttpResponse("Task List Working")
def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'tasks/register.html', {'form': form})
@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user)

    
    search = request.GET.get('search')
    if search:
        tasks = tasks.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )


    status = request.GET.get('status')
    if status:
        tasks = tasks.filter(status=status)

    priority = request.GET.get('priority')
    if priority:
        tasks = tasks.filter(priority=priority)

    
    due = request.GET.get('due')

    if due == 'today':
        tasks = tasks.filter(due_date=date.today())
    elif due == 'week':
        tasks = tasks.filter(
            due_date__lte=date.today() + timedelta(days=7)
        )

    elif due == 'overdue':
        tasks = tasks.filter(due_date__lt=date.today())

    # Sorting
    sort = request.GET.get('sort')
    if sort == 'newest':
        tasks = tasks.order_by('-created_at')
    elif sort == 'oldest':
        tasks = tasks.order_by('created_at')

    return render(request, 'tasks/task_list.html', {'tasks': tasks})
@login_required
def create_task(request):
    if request.method == 'POST':
        Task.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            status=request.POST['status'],
            priority=request.POST['priority'],
            due_date=request.POST['due_date'],
            owner=request.user
        )
        return redirect('task_list')

    return render(request, 'tasks/create_task.html')
@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)

    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST['description']
        task.status = request.POST['status']
        task.priority = request.POST['priority']
        task.due_date = request.POST['due_date']
        task.save()
        return redirect('task_list')

    return render(request, 'tasks/update_task.html', {'task': task})
@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    return render(request, 'tasks/delete_confirm.html', {'task': task})
@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})