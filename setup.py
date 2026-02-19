#!/usr/bin/env python
"""
Setup script for FixMate AI Django project
Run this after installing requirements.txt
"""
import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fixmate.settings')
django.setup()

from django.contrib.auth.models import User
from marketplace.models import Worker, Job, ClientProfile

def create_sample_data():
    print("Creating sample data...")
    
    # Create admin user
    if not User.objects.filter(email='admin@gmail.com').exists():
        admin = User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')
        admin.first_name = 'Admin'
        admin.last_name = 'User'
        admin.save()
        print("✓ Admin: admin@gmail.com / admin")
    
    # Create sample clients with profiles
    clients_data = [
        {
            'username': 'alex',
            'email': 'client@gmail.com',
            'password': 'client',
            'first_name': 'Alex',
            'last_name': 'Johnson',
            'total_spent': 8500,
            'total_bookings': 12,
            'preferred_location': 'Downtown'
        },
        {
            'username': 'priya',
            'email': 'priya123@gmail.com',
            'password': 'priya',
            'first_name': 'Priya',
            'last_name': 'Sharma',
            'total_spent': 15200,
            'total_bookings': 23,
            'preferred_location': 'South Delhi'
        },
        {
            'username': 'rahul',
            'email': 'rahul456@gmail.com',
            'password': 'rahul',
            'first_name': 'Rahul',
            'last_name': 'Verma',
            'total_spent': 6300,
            'total_bookings': 8,
            'preferred_location': 'Bangalore'
        },
        {
            'username': 'anjali',
            'email': 'anjali789@gmail.com',
            'password': 'anjali',
            'first_name': 'Anjali',
            'last_name': 'Patel',
            'total_spent': 12800,
            'total_bookings': 18,
            'preferred_location': 'Mumbai'
        },
        {
            'username': 'vikram',
            'email': 'vikram321@gmail.com',
            'password': 'vikram',
            'first_name': 'Vikram',
            'last_name': 'Singh',
            'total_spent': 4200,
            'total_bookings': 5,
            'preferred_location': 'Pune'
        }
    ]
    
    for client_data in clients_data:
        if not User.objects.filter(email=client_data['email']).exists():
            user = User.objects.create_user(
                username=client_data['username'],
                email=client_data['email'],
                password=client_data['password']
            )
            user.first_name = client_data['first_name']
            user.last_name = client_data['last_name']
            user.save()
            
            avg_budget = client_data['total_spent'] / client_data['total_bookings'] if client_data['total_bookings'] > 0 else 0
            ClientProfile.objects.create(
                user=user,
                total_spent=client_data['total_spent'],
                total_bookings=client_data['total_bookings'],
                average_budget=avg_budget,
                preferred_location=client_data['preferred_location'],
                loyalty_points=client_data['total_bookings'] * 10
            )
            print(f"✓ Client: {client_data['email']} / {client_data['password']}")
    
    # Create sample workers
    workers_data = [
        {
            'username': 'sarah',
            'email': 'sarah@gmail.com',
            'password': 'sarah',
            'first_name': 'Sarah',
            'last_name': 'Miller',
            'skills': 'Plumbing, Heating, Water Systems',
            'rating': 4.9,
            'technical_rating': 4.8,
            'job_count': 156,
            'completed_jobs': 148,
            'reliability_score': 98,
            'location': 'Delhi',
            'is_new': False,
            'earnings': 14500,
            'response_time': 15,
            'specialization': 'Plumbing Expert'
        },
        {
            'username': 'marcus',
            'email': 'marcus@gmail.com',
            'password': 'marcus',
            'first_name': 'Marcus',
            'last_name': 'Chen',
            'skills': 'Electrical, Smart Home, Wiring',
            'rating': 4.7,
            'technical_rating': 4.9,
            'job_count': 89,
            'completed_jobs': 84,
            'reliability_score': 95,
            'location': 'Bangalore',
            'is_new': False,
            'earnings': 9800,
            'response_time': 20,
            'specialization': 'Electrical Specialist'
        },
        {
            'username': 'elena',
            'email': 'elena@gmail.com',
            'password': 'elena',
            'first_name': 'Elena',
            'last_name': 'Rodriguez',
            'skills': 'Carpentry, Furniture, General Repairs',
            'rating': 5.0,
            'technical_rating': 4.7,
            'job_count': 12,
            'completed_jobs': 12,
            'reliability_score': 100,
            'location': 'Mumbai',
            'is_new': True,
            'earnings': 2800,
            'response_time': 10,
            'specialization': 'Carpentry'
        },
        {
            'username': 'rajesh',
            'email': 'rajesh@gmail.com',
            'password': 'rajesh',
            'first_name': 'Rajesh',
            'last_name': 'Kumar',
            'skills': 'HVAC, AC Repair, Cooling Systems',
            'rating': 4.8,
            'technical_rating': 4.9,
            'job_count': 134,
            'completed_jobs': 128,
            'reliability_score': 96,
            'location': 'Pune',
            'is_new': False,
            'earnings': 12500,
            'response_time': 18,
            'specialization': 'HVAC Expert'
        },
        {
            'username': 'meera',
            'email': 'meera@gmail.com',
            'password': 'meera',
            'first_name': 'Meera',
            'last_name': 'Nair',
            'skills': 'Painting, Interior Design, Wallpaper',
            'rating': 4.6,
            'technical_rating': 4.5,
            'job_count': 67,
            'completed_jobs': 63,
            'reliability_score': 94,
            'location': 'Chennai',
            'is_new': False,
            'earnings': 72000,
            'response_time': 25,
            'specialization': 'Painting Specialist'
        },
        {
            'username': 'amit',
            'email': 'amit@gmail.com',
            'password': 'amit',
            'first_name': 'Amit',
            'last_name': 'Desai',
            'skills': 'Cleaning, Deep Cleaning, Sanitization',
            'rating': 4.9,
            'technical_rating': 4.6,
            'job_count': 203,
            'completed_jobs': 198,
            'reliability_score': 97,
            'location': 'Hyderabad',
            'is_new': False,
            'earnings': 15600,
            'response_time': 12,
            'specialization': 'Professional Cleaning'
        },
        {
            'username': 'kavita',
            'email': 'kavita@gmail.com',
            'password': 'kavita',
            'first_name': 'Kavita',
            'last_name': 'Reddy',
            'skills': 'Appliance Repair, Electronics',
            'rating': 4.7,
            'technical_rating': 4.8,
            'job_count': 45,
            'completed_jobs': 42,
            'reliability_score': 93,
            'location': 'Kolkata',
            'is_new': False,
            'earnings': 54000,
            'response_time': 22,
            'specialization': 'Appliance Expert'
        }
    ]
    
    for worker_data in workers_data:
        if not User.objects.filter(email=worker_data['email']).exists():
            user = User.objects.create_user(
                username=worker_data['username'],
                email=worker_data['email'],
                password=worker_data['password']
            )
            user.first_name = worker_data['first_name']
            user.last_name = worker_data['last_name']
            user.save()
            
            Worker.objects.create(
                user=user,
                skills=worker_data['skills'],
                rating=worker_data['rating'],
                technical_rating=worker_data['technical_rating'],
                job_count=worker_data['job_count'],
                completed_jobs=worker_data['completed_jobs'],
                reliability_score=worker_data['reliability_score'],
                location=worker_data['location'],
                is_new=worker_data['is_new'],
                earnings=worker_data['earnings'],
                response_time=worker_data['response_time'],
                specialization=worker_data['specialization']
            )
            print(f"✓ Worker: {worker_data['email']} / {worker_data['password']}")
    
    # Create sample jobs with specific worker assignments
    print("\n✓ Creating sample jobs with worker tracking...")
    
    clients = User.objects.filter(clientprofile__isnull=False)
    workers_dict = {
        'Plumbing': Worker.objects.filter(specialization='Plumbing Expert').first(),
        'Electrical': Worker.objects.filter(specialization='Electrical Specialist').first(),
        'Carpentry': Worker.objects.filter(specialization='Carpentry').first(),
        'HVAC': Worker.objects.filter(specialization='HVAC Expert').first(),
        'Painting': Worker.objects.filter(specialization='Painting Specialist').first(),
        'Cleaning': Worker.objects.filter(specialization='Professional Cleaning').first(),
    }
    
    jobs_data = [
        # Client 1 (Alex) - Multiple bookings showing progression
        {
            'title': 'Fix Kitchen Sink Leak',
            'description': 'Kitchen sink is leaking from the pipe connection. Water dripping constantly. Need urgent fix.',
            'category': 'Plumbing',
            'location': 'Downtown',
            'urgency': 'high',
            'status': 'completed',
            'client_email': 'client@gmail.com',
            'price': 1250,
        },
        {
            'title': 'Install Ceiling Fan',
            'description': 'Need to install a new ceiling fan in the bedroom with proper wiring and switch connection.',
            'category': 'Electrical',
            'location': 'Downtown',
            'urgency': 'medium',
            'status': 'completed',
            'client_email': 'client@gmail.com',
            'price': 650,
        },
        {
            'title': 'AC Maintenance and Gas Refill',
            'description': 'Annual AC maintenance, cleaning, and gas refill required. AC not cooling properly.',
            'category': 'HVAC',
            'location': 'Downtown',
            'urgency': 'high',
            'status': 'assigned',
            'client_email': 'client@gmail.com',
            'price': 1100,
        },
        {
            'title': 'Bedroom Deep Cleaning',
            'description': 'Need deep cleaning of master bedroom including carpet cleaning and window washing.',
            'category': 'Cleaning',
            'location': 'Downtown',
            'urgency': 'low',
            'status': 'pending',
            'client_email': 'client@gmail.com',
            'price': 450,
        },
        
        # Client 2 (Priya) - High spender with ongoing projects
        {
            'title': 'Complete Home Electrical Rewiring',
            'description': 'Need complete electrical rewiring for 3BHK apartment. Old wiring causing frequent trips.',
            'category': 'Electrical',
            'location': 'South Delhi',
            'urgency': 'high',
            'status': 'completed',
            'client_email': 'priya123@gmail.com',
            'price': 2500,
        },
        {
            'title': 'Bathroom Plumbing Renovation',
            'description': 'Complete bathroom plumbing renovation including new fixtures, pipes, and drainage system.',
            'category': 'Plumbing',
            'location': 'South Delhi',
            'urgency': 'medium',
            'status': 'completed',
            'client_email': 'priya123@gmail.com',
            'price': 1800,
        },
        {
            'title': 'Living Room and Dining Area Painting',
            'description': 'Paint living room and dining area with premium Asian Paints. Need color consultation.',
            'category': 'Painting',
            'location': 'South Delhi',
            'urgency': 'medium',
            'status': 'assigned',
            'client_email': 'priya123@gmail.com',
            'price': 1200,
        },
        {
            'title': 'Custom Wardrobe Installation',
            'description': 'Install custom-made wooden wardrobe in master bedroom with sliding doors.',
            'category': 'Carpentry',
            'location': 'South Delhi',
            'urgency': 'low',
            'status': 'assigned',
            'client_email': 'priya123@gmail.com',
            'price': 950,
        },
        
        # Client 3 (Rahul) - Regular customer
        {
            'title': 'Repair Wooden Cabinet Door',
            'description': 'Kitchen cabinet door is broken and hinges need replacement. Door not closing properly.',
            'category': 'Carpentry',
            'location': 'Bangalore',
            'urgency': 'low',
            'status': 'completed',
            'client_email': 'rahul456@gmail.com',
            'price': 350,
        },
        {
            'title': 'Full House Deep Cleaning',
            'description': 'Full house deep cleaning including kitchen, bathrooms, and all rooms. Pre-festival cleaning.',
            'category': 'Cleaning',
            'location': 'Bangalore',
            'urgency': 'medium',
            'status': 'completed',
            'client_email': 'rahul456@gmail.com',
            'price': 900,
        },
        {
            'title': 'Fix Water Heater Not Heating',
            'description': 'Water heater not heating properly, needs inspection and possible element replacement.',
            'category': 'Plumbing',
            'location': 'Bangalore',
            'urgency': 'high',
            'status': 'assigned',
            'client_email': 'rahul456@gmail.com',
            'price': 1150,
        },
        {
            'title': 'Replace Bathroom Exhaust Fan',
            'description': 'Bathroom exhaust fan making noise and not working efficiently. Need replacement.',
            'category': 'Electrical',
            'location': 'Bangalore',
            'urgency': 'medium',
            'status': 'pending',
            'client_email': 'rahul456@gmail.com',
            'price': 550,
        },
        
        # Client 4 (Anjali) - Premium customer
        {
            'title': 'Split AC Installation 1.5 Ton',
            'description': 'Install new 1.5 ton split AC in bedroom with copper piping and proper drainage.',
            'category': 'HVAC',
            'location': 'Mumbai',
            'urgency': 'high',
            'status': 'completed',
            'client_email': 'anjali789@gmail.com',
            'price': 1400,
        },
        {
            'title': 'Exterior Wall Painting',
            'description': 'Paint exterior walls of the house with weather-resistant paint. 2000 sq ft area.',
            'category': 'Painting',
            'location': 'Mumbai',
            'urgency': 'low',
            'status': 'completed',
            'client_email': 'anjali789@gmail.com',
            'price': 2200,
        },
        {
            'title': 'Fix Electrical Short Circuit',
            'description': 'Frequent power trips in main bedroom. Need to fix short circuit issue urgently.',
            'category': 'Electrical',
            'location': 'Mumbai',
            'urgency': 'high',
            'status': 'assigned',
            'client_email': 'anjali789@gmail.com',
            'price': 1050,
        },
        {
            'title': 'Kitchen Chimney Installation',
            'description': 'Install new kitchen chimney with ducting and proper ventilation setup.',
            'category': 'Electrical',
            'location': 'Mumbai',
            'urgency': 'medium',
            'status': 'assigned',
            'client_email': 'anjali789@gmail.com',
            'price': 800,
        },
        
        # Client 5 (Vikram) - Business customer
        {
            'title': 'Office Deep Cleaning and Sanitization',
            'description': 'Complete office space cleaning and sanitization. 1500 sq ft area with 10 workstations.',
            'category': 'Cleaning',
            'location': 'Pune',
            'urgency': 'medium',
            'status': 'completed',
            'client_email': 'vikram321@gmail.com',
            'price': 1100,
        },
        {
            'title': 'Install Smart Home Switches',
            'description': 'Replace 8 regular switches with WiFi-enabled smart home switches. Need app setup.',
            'category': 'Electrical',
            'location': 'Pune',
            'urgency': 'low',
            'status': 'assigned',
            'client_email': 'vikram321@gmail.com',
            'price': 850,
        },
        {
            'title': 'Conference Room AC Repair',
            'description': 'Conference room AC not cooling. Need urgent repair for client meeting tomorrow.',
            'category': 'HVAC',
            'location': 'Pune',
            'urgency': 'high',
            'status': 'pending',
            'client_email': 'vikram321@gmail.com',
            'price': 1300,
        },
        {
            'title': 'Office Furniture Assembly',
            'description': 'Assemble 5 new office desks and 10 chairs. Need professional assembly.',
            'category': 'Carpentry',
            'location': 'Pune',
            'urgency': 'medium',
            'status': 'pending',
            'client_email': 'vikram321@gmail.com',
            'price': 700,
        },
    ]
    
    for job_data in jobs_data:
        try:
            client = User.objects.get(email=job_data['client_email'])
            category = job_data['category']
            worker = workers_dict.get(category)
            
            # Assign worker only if status is not pending
            assigned_worker = worker if job_data['status'] != 'pending' else None
            
            Job.objects.create(
                title=job_data['title'],
                description=job_data['description'],
                category=category,
                location=job_data['location'],
                urgency=job_data['urgency'],
                status=job_data['status'],
                user=client,
                worker=assigned_worker,
                price=job_data['price'],
                ai_match_score=round(random.uniform(85, 98), 1),
                estimated_duration=random.randint(2, 8)
            )
            print(f"  ✓ Job: {job_data['title']} - {client.first_name} → {worker.user.first_name if assigned_worker else 'Unassigned'}")
        except Exception as e:
            print(f"  ✗ Error creating job: {e}")
    
    print("\n✅ Setup complete!")
    print("\nLogin credentials:")
    print("  Admin:  admin@gmail.com  / admin")
    print("\nClients:")
    print("  client@gmail.com  / client")
    print("  priya123@gmail.com  / priya")
    print("  rahul456@gmail.com  / rahul")
    print("  anjali789@gmail.com  / anjali")
    print("  vikram321@gmail.com  / vikram")
    print("\nWorkers:")
    print("  sarah@gmail.com  / sarah")
    print("  marcus@gmail.com  / marcus")
    print("  elena@gmail.com  / elena")
    print("  rajesh@gmail.com  / rajesh")
    print("  meera@gmail.com  / meera")
    print("  amit@gmail.com  / amit")
    print("  kavita@gmail.com  / kavita")

if __name__ == '__main__':
    create_sample_data()
