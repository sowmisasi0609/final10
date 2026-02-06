from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Course, Enrollment, Module, Review

def home(request):
    courses = Course.objects.all()
    return render(request, 'home.html', {'courses': courses})

def course_detail(request, id):
    course = get_object_or_404(Course, id=id)

    enrolled = False
    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(
            user=request.user, course=course
        ).exists()

    reviews = Review.objects.filter(course=course)

    return render(request, 'course_detail.html', {
        'course': course,
        'enrolled': enrolled,
        'reviews': reviews
    })

@login_required
def dashboard(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'enrollments': enrollments})

def login_user(request):
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password']
        )
        return redirect('login')
    return render(request, 'register.html')

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def buy_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # If already enrolled, just go to dashboard
    if Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.info(request, "You are already enrolled in this course.")
        return redirect('dashboard')

    # Fake payment success → enroll user
    Enrollment.objects.create(
        user=request.user,
        course=course,
        progress=0
    )

    # ✅ THIS LINE GOES HERE (after enrollment)
    messages.success(request, "Payment successful! Course added to your dashboard.")

    return redirect('dashboard')


    return redirect('dashboard')

@login_required
def course_modules(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Allow only enrolled users
    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.error(request, "You are not enrolled in this course.")
        return redirect('dashboard')

    modules = Module.objects.filter(course=course)

    return render(request, 'modules.html', {
        'course': course,
        'modules': modules
    })

@login_required
def watch_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    course = module.course

    enrollment = get_object_or_404(
        Enrollment,
        user=request.user,
        course=course
    )

    total_modules = Module.objects.filter(course=course).count()

    if total_modules > 0:
        enrollment.progress = min(
            100,
            int((1 / total_modules) * 100)
            + enrollment.progress
        )
        enrollment.save()

    return redirect(module.video_url)

@login_required
def add_review(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Only enrolled users can review
    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.error(request, "You must enroll to give a review.")
        return redirect('course', id=course.id)

    if request.method == "POST":
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        Review.objects.create(
            user=request.user,
            course=course,
            rating=rating,
            comment=comment
        )

        messages.success(request, "Thank you for your feedback!")
        return redirect('course', id=course.id)