from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from task.models import Photo, Task
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def loginUser(request):
    if request.method == "POST":
        pUsername = request.POST.get('username')
        pPassword = request.POST.get('password')
        user = authenticate(username=pUsername, password=pPassword)
        if user is not None:
            login(request, user)
            request.session['first_name'] = user.first_name 
            request.session['last_name'] = user.last_name
            request.session['user_id'] = user.username  
            return redirect('viewTask')
        else:
            return render(request,'login.html',{'login_failed': True})
    return render(request, 'login.html')

def signupUser(request):
    if request.method == "POST":
        pUsername = request.POST.get('username')
        pPassword = request.POST.get('password')
        pEmail = request.POST.get('email')
        pCpassword = request.POST.get('cPassword')
        pFirst_name = request.POST.get('first_name')
        pLast_name = request.POST.get('last_name')

        if pPassword== pCpassword:
            if User.objects.filter(username= pUsername).exists():
                return render(request,'signup.html',{'signup_failed_1': True})
            elif User.objects.filter(email= pEmail):
                return render(request,'signup.html',{'signup_failed_2': True})
            else: 
                user= User.objects.create_user(username=pUsername, password= pPassword, email= pEmail, first_name = pFirst_name, last_name = pLast_name)
                user.save()
                return render(request, 'signup.html', {'signup_succ': True})
        else:
            return render(request,'signup.html',{'signup_failed_3': True})
    return render(request, 'signup.html')

def logoutUser(request):
    logout(request)
    request.session.clear()
    return redirect(loginUser)

@login_required
def addTask(request):
    if request.method == 'POST':
        # Extract data from the POST request
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('dueDate')
        priority = request.POST.get('priority')
        task_user_id = request.session.get('user_id', None)
        # Create a new Task object
        task = Task(
            title=title,
            description=description,
            creation_date=timezone.now(),
            due_date=due_date,
            priority=priority,
            task_user_id = task_user_id
        )
        task.save()

        # Handle photo uploads
        photos = request.FILES.getlist('photos[]')
        for photo in photos:
            # Create a new Photo object and associate it with the task
            photo_obj = Photo(image=photo)
            photo_obj.save()
            task.photos.add(photo_obj)

        # Save the task with associated photos
        task.save()

        # Return a JSON response to indicate success
        return JsonResponse({'status': 'success'})

    return render(request, 'addTask.html')

@login_required
def viewTask(request):
    # Fetch all tasks from the database
    task_user_id = request.session.get('user_id', None)
    all_tasks = Task.objects.filter(task_user_id=task_user_id).order_by('-id')
    return render(request, 'viewTask.html', {'tasks': all_tasks})

@login_required
def complete_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        if task_id:
            try:
                task = Task.objects.get(id=task_id)
                task.is_completed = True
                task.save()
                return JsonResponse({'message': 'Task completed successfully'})
            except Task.DoesNotExist:
                # Handle the case where the task with the given ID doesn't exist
                return JsonResponse({'error': 'Task not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def editTask(request):
    # Fetch all tasks from the database
    task_user_id = request.session.get('user_id', None)
    all_tasks = Task.objects.filter(task_user_id=task_user_id).order_by('-id')
    return render(request, 'editTask.html', {'tasks': all_tasks})

def get_task_details(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        data = {
            'title': task.title,
            'description': task.description,
            'due_date': task.due_date.strftime('%Y-%m-%d'),  # Format date as needed
            'priority': task.priority,
            # Add more task details here
        }
        return JsonResponse(data)
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)

@login_required  
def update_task(request, task_id):
    try:
        # Retrieve the task based on task_id
        task = Task.objects.get(id=task_id)
        
        if request.method == 'POST':
            # Update task details based on form data
            task.title = request.POST.get('editTitle')
            task.description = request.POST.get('editDescription')
            task.due_date = request.POST.get('editDueDate')
            task.priority = request.POST.get('editPriority')
            # Update other task details as needed
            
            # Save the updated task
            task.save()
            
            return JsonResponse({'success': 'Task updated successfully'})
        
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)

@login_required      
def deleteTask(request):
    # Fetch all tasks from the database
    task_user_id = request.session.get('user_id', None)
    all_tasks = Task.objects.filter(task_user_id=task_user_id).order_by('-id')
    return render(request, 'deleteTask.html', {'tasks': all_tasks})


@login_required
# Define the search_tasks view to handle the AJAX search request
def delete_task(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        if task_id:
            try:
                task = Task.objects.get(id=task_id)
                task.delete()
                return JsonResponse({'message': 'Task deleted successfully'})
            except Task.DoesNotExist:
                # Handle the case where the task with the given ID doesn't exist
                return JsonResponse({'error': 'Task not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)
