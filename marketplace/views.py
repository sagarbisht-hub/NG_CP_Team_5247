from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db import models
import json
from .models import Worker, Job
import random
import string

def landing_page(request):
    return render(request, 'landing.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        otp_code = request.POST.get('otp_code')
        role = request.POST.get('role')
        
        print(f"Login attempt - Username: {username}, Email: {email}, Role: {role}")
        
        # Verify OTP from session
        session_otp = request.session.get('login_otp_code')
        session_email = request.session.get('login_otp_email')
        
        print(f"Session OTP: {session_otp}, Session Email: {session_email}, Provided OTP: {otp_code}")
        
        if not session_otp or not session_email:
            messages.error(request, 'Please verify your email with OTP first.')
            return render(request, 'login.html')
        
        if session_email != email:
            messages.error(request, 'Email mismatch. Please try again.')
            return render(request, 'login.html')
        
        if session_otp != otp_code:
            messages.error(request, 'Invalid OTP code.')
            return render(request, 'login.html')
        
        # Find user by username and email
        try:
            user_obj = User.objects.get(username=username, email=email)
            print(f"User found: {user_obj.username}, Is Worker: {Worker.objects.filter(user=user_obj).exists()}")
            
            # Verify role matches user type
            if role == 'ADMIN':
                if not user_obj.is_staff:
                    messages.error(request, 'This account is not registered as an Admin.')
                    return render(request, 'login.html')
            elif role == 'WORKER':
                if not Worker.objects.filter(user=user_obj).exists():
                    messages.error(request, 'This account is not registered as a Worker.')
                    return render(request, 'login.html')
            elif role == 'USER':
                # Client should not be admin or worker
                if user_obj.is_staff:
                    messages.error(request, 'This account is registered as an Admin. Please select Admin role.')
                    return render(request, 'login.html')
                if Worker.objects.filter(user=user_obj).exists():
                    messages.error(request, 'This account is registered as a Worker. Please select Worker role.')
                    return render(request, 'login.html')
            
            user = authenticate(request, username=user_obj.username, password=password)
            if user:
                # Clear OTP from session
                del request.session['login_otp_code']
                del request.session['login_otp_email']
                
                login(request, user)
                print(f"Login successful for {user.username}")
                return redirect('dashboard')
            else:
                print(f"Authentication failed for {username}")
                messages.error(request, 'Incorrect password. Please try again.')
        except User.DoesNotExist:
            print(f"User not found: {username} / {email}")
            messages.error(request, 'Username or email not found. Please sign up first.')
    
    return render(request, 'login.html')

@require_http_methods(["POST"])
def send_login_otp(request):
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        role = data.get('role', 'USER')
        
        print(f"OTP Request - Email: {email}, Role: {role}")
        
        # Validate email format (allow numbers in email)
        if not email:
            return JsonResponse({'success': False, 'message': 'Email is required'})
            
        if '@' not in email or '.' not in email.split('@')[1]:
            return JsonResponse({'success': False, 'message': 'Please enter a valid email address'})
        
        # Check if user exists with this email
        try:
            user = User.objects.get(email=email)
            print(f"User found: {user.username}, Email: {user.email}")
        except User.DoesNotExist:
            print(f"User not found with email: {email}")
            return JsonResponse({'success': False, 'message': 'Email not found. Please sign up first.'})
        
        # Check role-specific access (no overlap)
        if role == 'ADMIN':
            if not user.is_staff:
                return JsonResponse({'success': False, 'message': 'This email is not registered as an Admin.'})
        elif role == 'WORKER':
            worker_exists = Worker.objects.filter(user=user).exists()
            print(f"Worker check for {user.username}: {worker_exists}")
            if not worker_exists:
                return JsonResponse({'success': False, 'message': 'This email is not registered as a Worker.'})
        elif role == 'USER':
            # Client should not be admin or worker
            if user.is_staff:
                return JsonResponse({'success': False, 'message': 'This email is registered as Admin. Please select Admin role.'})
            if Worker.objects.filter(user=user).exists():
                return JsonResponse({'success': False, 'message': 'This email is registered as Worker. Please select Worker role.'})
        
        # Generate 6-digit OTP
        otp_code = ''.join(random.choices(string.digits, k=6))
        
        # Store OTP in session with timestamp
        request.session['login_otp_code'] = otp_code
        request.session['login_otp_email'] = email
        request.session['login_otp_role'] = role
        request.session.modified = True
        
        # In production, send email here
        print(f"✓ Login OTP for {email} ({role}): {otp_code}")
        
        return JsonResponse({
            'success': True,
            'message': f'OTP sent to {email}',
            'otp': otp_code  # Remove in production
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data'})
    except Exception as e:
        print(f"Error in send_login_otp: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'message': 'An error occurred. Please try again.'})

@require_http_methods(["POST"])
def verify_login_otp(request):
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        otp_code = data.get('otp_code', '').strip()
        
        print(f"Verify OTP - Email: {email}, OTP: {otp_code}")
        
        if not email or not otp_code:
            return JsonResponse({'success': False, 'message': 'Email and OTP are required'})
        
        session_otp = request.session.get('login_otp_code')
        session_email = request.session.get('login_otp_email')
        
        print(f"Session - OTP: {session_otp}, Email: {session_email}")
        
        if not session_otp or not session_email:
            return JsonResponse({'success': False, 'message': 'OTP expired or not found. Please request a new OTP.'})
        
        if session_email != email:
            return JsonResponse({'success': False, 'message': 'Email mismatch. Please try again.'})
        
        if session_otp != otp_code:
            return JsonResponse({'success': False, 'message': 'Invalid OTP code. Please check and try again.'})
        
        print(f"✓ OTP verified successfully for {email}")
        return JsonResponse({'success': True, 'message': 'Email verified successfully!'})
    
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data'})
    except Exception as e:
        print(f"Error in verify_login_otp: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'success': False, 'message': 'An error occurred. Please try again.'})

def signup_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        # Validate name - only letters and spaces allowed
        if not all(c.isalpha() or c.isspace() for c in name):
            messages.error(request, 'Name should only contain letters and spaces, no numbers or special characters.')
            return render(request, 'signup.html')
        
        # Split name into first and last name
        name_parts = name.strip().split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Create username from first name (letters only)
        username = ''.join(c for c in first_name.lower() if c.isalpha())
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please login.')
            return redirect('login')
        
        # If username exists, add letters from last name or make it unique
        if User.objects.filter(username=username).exists():
            if last_name:
                username = username + ''.join(c for c in last_name.lower() if c.isalpha())[:3]
            if User.objects.filter(username=username).exists():
                # Add suffix with letters only
                import string
                suffix = ''.join(random.choices(string.ascii_lowercase, k=3))
                username = username + suffix
        
        # Create user with name
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        # Create worker if role is worker
        if role == 'WORKER':
            Worker.objects.create(
                user=user,
                skills='General',
                location='Downtown',
                reliability_score=80,
                rating=0.0,
                job_count=0,
                is_new=True,
                earnings=0
            )
        
        login(request, user)
        return redirect('dashboard')
    
    return render(request, 'signup.html')

@login_required
def dashboard(request):
    user = request.user
    
    # check if worker
    try:
        worker = Worker.objects.get(user=user)
        jobs = Job.objects.filter(worker=worker)
        active_jobs_count = jobs.filter(status='assigned').count()
        return render(request, 'worker_dashboard.html', {
            'worker': worker, 
            'jobs': jobs,
            'active_jobs_count': active_jobs_count
        })
    except Worker.DoesNotExist:
        pass
    
    # check if admin
    if user.is_staff:
        from django.db.models import Count, Avg, Sum, Q
        from marketplace.models import ClientProfile
        
        workers = Worker.objects.all().order_by('-rating')
        jobs = Job.objects.all()
        clients = User.objects.filter(clientprofile__isnull=False)
        
        # AI Analysis Data
        total_jobs = jobs.count()
        pending_jobs = jobs.filter(status='pending').count()
        assigned_jobs = jobs.filter(status='assigned').count()
        completed_jobs = jobs.filter(status='completed').count()
        total_revenue = jobs.aggregate(Sum('price'))['price__sum'] or 0
        
        # Client Analysis
        client_profiles = ClientProfile.objects.all()
        total_clients = clients.count()
        avg_client_budget = client_profiles.aggregate(Avg('average_budget'))['average_budget__avg'] or 0
        total_client_spent = client_profiles.aggregate(Sum('total_spent'))['total_spent__sum'] or 0
        
        # Worker Analysis
        total_workers = workers.count()
        avg_worker_rating = workers.aggregate(Avg('rating'))['rating__avg'] or 0
        avg_technical_rating = workers.aggregate(Avg('technical_rating'))['technical_rating__avg'] or 0
        total_worker_earnings = workers.aggregate(Sum('earnings'))['earnings__sum'] or 0
        avg_response_time = workers.aggregate(Avg('response_time'))['response_time__avg'] or 0
        
        # Location Analysis
        location_stats = jobs.values('location').annotate(count=Count('id')).order_by('-count')[:5]
        
        # Category Analysis
        category_stats = jobs.values('category').annotate(count=Count('id')).order_by('-count')
        
        # AI Match Score Analysis
        avg_match_score = jobs.aggregate(Avg('ai_match_score'))['ai_match_score__avg'] or 0
        high_match_jobs = jobs.filter(ai_match_score__gte=90).count()
        
        # Top performers
        top_workers = workers.order_by('-rating', '-completed_jobs')[:5]
        top_clients = client_profiles.order_by('-total_spent')[:5]
        
        # Urgency Analysis
        urgency_stats = {
            'low': jobs.filter(urgency='low').count(),
            'medium': jobs.filter(urgency='medium').count(),
            'high': jobs.filter(urgency='high').count(),
        }
        
        # Status breakdown with percentages
        status_percentages = {
            'pending': (pending_jobs / total_jobs * 100) if total_jobs > 0 else 0,
            'assigned': (assigned_jobs / total_jobs * 100) if total_jobs > 0 else 0,
            'completed': (completed_jobs / total_jobs * 100) if total_jobs > 0 else 0,
        }
        
        # Worker-Client Interaction Stats
        active_interactions = jobs.filter(status='assigned').count()
        completed_interactions = jobs.filter(status='completed').count()
        
        # Average job value by category
        category_avg_price = jobs.values('category').annotate(
            avg_price=Avg('price'),
            total_jobs=Count('id')
        ).order_by('-avg_price')
        
        # Client retention (clients with multiple bookings)
        repeat_clients = client_profiles.filter(total_bookings__gte=2).count()
        client_retention_rate = (repeat_clients / total_clients * 100) if total_clients > 0 else 0
        
        # Worker utilization
        active_workers = workers.filter(job__status='assigned').distinct().count()
        worker_utilization_rate = (active_workers / total_workers * 100) if total_workers > 0 else 0
        
        context = {
            'workers': workers,
            'jobs': jobs,
            'clients': clients,
            'total_jobs': total_jobs,
            'pending_jobs': pending_jobs,
            'assigned_jobs': assigned_jobs,
            'completed_jobs': completed_jobs,
            'total_revenue': total_revenue,
            'total_clients': total_clients,
            'avg_client_budget': avg_client_budget,
            'total_client_spent': total_client_spent,
            'total_workers': total_workers,
            'avg_worker_rating': avg_worker_rating,
            'avg_technical_rating': avg_technical_rating,
            'total_worker_earnings': total_worker_earnings,
            'avg_response_time': avg_response_time,
            'location_stats': location_stats,
            'category_stats': category_stats,
            'avg_match_score': avg_match_score,
            'high_match_jobs': high_match_jobs,
            'top_workers': top_workers,
            'top_clients': top_clients,
            'urgency_stats': urgency_stats,
            'status_percentages': status_percentages,
            'active_interactions': active_interactions,
            'completed_interactions': completed_interactions,
            'category_avg_price': category_avg_price,
            'repeat_clients': repeat_clients,
            'client_retention_rate': client_retention_rate,
            'active_workers': active_workers,
            'worker_utilization_rate': worker_utilization_rate,
        }
        return render(request, 'admin_dashboard.html', context)
    
    # regular user - check if they have any jobs
    jobs = Job.objects.filter(user=user)
    workers = Worker.objects.all()
    
    # Calculate stats for dashboard
    pending_count = jobs.filter(status='pending').count()
    completed_count = jobs.filter(status='completed').count()
    total_spent = sum(job.price for job in jobs if job.price)
    
    # Always show dashboard, even if no jobs
    context = {
        'jobs': jobs,
        'workers': workers,
        'pending_count': pending_count,
        'completed_count': completed_count,
        'total_spent': total_spent,
    }
    return render(request, 'user_dashboard.html', context)

@login_required
def create_job_form(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        urgency = request.POST.get('urgency')
        location = request.POST.get('location', 'Downtown')
        
        # AI matching simulation - find workers by specialization or skills
        workers = Worker.objects.filter(
            models.Q(specialization__icontains=category) | 
            models.Q(skills__icontains=category)
        ).order_by('-reliability_score', '-technical_rating')
        
        recommended_worker = workers.first() if workers.exists() else None
        
        # Price calculation in Indian Rupees (₹)
        base_price = 500  # Base price in INR
        if urgency == 'high':
            base_price = 1200
        elif urgency == 'low':
            base_price = 300
        
        price = base_price + random.randint(-100, 200)
        
        # Calculate AI match score
        ai_match_score = 85 + random.randint(0, 15) if recommended_worker else 0
        
        # Estimate duration based on category and urgency
        duration_map = {
            'Plumbing': 3,
            'Electrical': 4,
            'Carpentry': 6,
            'Cleaning': 2,
            'HVAC': 5,
            'Painting': 8,
            'General': 3
        }
        estimated_duration = duration_map.get(category, 3)
        if urgency == 'high':
            estimated_duration = int(estimated_duration * 0.7)
        
        job = Job.objects.create(
            title=title,
            description=description,
            category=category,
            urgency=urgency,
            location=location,
            user=request.user,
            worker=recommended_worker,
            price=price,
            status='assigned' if recommended_worker else 'pending',
            ai_match_score=ai_match_score,
            estimated_duration=estimated_duration
        )
        
        # Redirect to tracking page
        return redirect('job_tracking', job_id=job.id)
    
    return render(request, 'job_request_form.html')

@login_required
def job_tracking(request, job_id):
    job = Job.objects.get(id=job_id, user=request.user)
    return render(request, 'job_tracking.html', {'job': job})

@login_required
def create_job(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        urgency = request.POST.get('urgency')
        location = request.POST.get('location', 'Downtown')
        
        # AI matching simulation
        workers = Worker.objects.filter(skills__icontains=category).order_by('-reliability_score')
        recommended_worker = workers.first() if workers.exists() else None
        
        # Price calculation in Indian Rupees (₹)
        base_price = 500  # Base price in INR
        if urgency == 'high':
            base_price = 1200
        elif urgency == 'low':
            base_price = 300
        
        price = base_price + random.randint(-100, 200)
        
        job = Job.objects.create(
            title=title,
            description=description,
            category=category,
            urgency=urgency,
            location=location,
            user=request.user,
            worker=recommended_worker,
            price=price,
            status='assigned' if recommended_worker else 'pending'
        )
        
        messages.success(request, f'Job created! Matched with {recommended_worker.user.first_name if recommended_worker else "pending"}')
        return redirect('dashboard')
    
    return redirect('dashboard')

def help_page(request):
    return render(request, 'help.html')

@login_required
def delete_job(request, job_id):
    if request.method == 'POST':
        try:
            job = Job.objects.get(id=job_id, user=request.user)
            job.delete()
            messages.success(request, 'Job deleted successfully!')
        except Job.DoesNotExist:
            messages.error(request, 'Job not found or you do not have permission to delete it.')
    return redirect('dashboard')

def logout_view(request):
    logout(request)
    return redirect('landing')
