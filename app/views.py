from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from datetime import datetime
import pytz
import time
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

def index(request):
    # Generate current time in local timezone
    current_time = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S %Z")
    
    # Context dictionary
    context = {
        'current_time': current_time,
    }
    
    return render(request, 'app/index.html', context)

def new_user_form(request):
    # Only accept GET requests for the form
    if request.method != 'GET':
        return HttpResponseForbidden("Only GET requests are allowed for this endpoint.")
    
    return render(request, 'app/new.html')

@csrf_exempt
def create_user(request):
    # Only accept POST requests for user creation
    if request.method != 'POST':
        return HttpResponseForbidden("Only POST requests are allowed for this endpoint.")
    
    # Extract data from the POST request
    user_name = request.POST.get('user_name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    is_admin = request.POST.get('is_admin', '0') == '1'
    
    # For API requests
    is_api_request = request.headers.get('Accept') == 'application/json' or request.headers.get('Content-Type') == 'application/json'
    
    # Check if all required fields are provided
    if not user_name or not email or not password:
        if is_api_request:
            return HttpResponseForbidden("All fields are required.")
        else:
            return render(request, 'app/new.html', {'error_message': 'All fields are required.'})
    
    # Check if email is already in use
    if User.objects.filter(email=email).exists():
        if is_api_request:
            return HttpResponseForbidden("Email address is already in use.")
        else:
            return render(request, 'app/new.html', {'error_message': 'Email address is already in use.'})
    
    # Check if username is already in use
    if User.objects.filter(username=user_name).exists():
        if is_api_request:
            return HttpResponseForbidden("Username is already in use.")
        else:
            return render(request, 'app/new.html', {'error_message': 'Username is already in use.'})
    
    # Create new user
    try:
        user = User.objects.create_user(
            username=user_name,
            email=email,
            password=password
        )
        user.is_staff = is_admin  # Set admin status
        user.save()
        
        # Authenticate and log in the user
        login_user = authenticate(request, username=user_name, password=password)
        if login_user is not None:
            login(request, login_user)
            
            # For API calls, return JSON
            if is_api_request:
                return JsonResponse({"message": "User created successfully!"})
            
            # For form submissions, redirect to home
            return redirect('/')
        else:
            if is_api_request:
                return HttpResponseForbidden("Failed to authenticate user after creation.")
            else:
                return render(request, 'app/new.html', {'error_message': 'Failed to authenticate user after creation.'})
    
    except Exception as e:
        if is_api_request:
            return HttpResponseForbidden(f"Error creating user: {str(e)}")
        else:
            return render(request, 'app/new.html', {'error_message': f'Error creating user: {str(e)}'})

@csrf_exempt
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # For API requests
        is_api_request = request.headers.get('Accept') == 'application/json' or request.headers.get('Content-Type') == 'application/json'
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # For API calls, return JSON
            if is_api_request:
                return JsonResponse({"message": "Login successful!"})
            
            # For form submissions, redirect to home
            return redirect('/')
        else:
            # For API calls, return error in JSON
            if is_api_request:
                return HttpResponseForbidden("Invalid credentials.")
            
            # For form submissions, return to login page with error
            return render(request, 'registration/login.html', {'error_message': 'Invalid username or password.'})
    else:
        return render(request, 'registration/login.html') 