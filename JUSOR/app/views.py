"""
Definition of views.
"""
from .forms import JobApplicationForm
from datetime import datetime
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import AboutUs, Icon, Header, Service, TopBar, Slider, ClientImage, Client, Project, ProjectImage, Testimonial, ExpertTeamMember, Career, JobApplication, Blog
from django.core.paginator import Paginator


@csrf_exempt
def add_slider(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        slider = Slider.objects.create(title=title, description=description, image=image)
        return JsonResponse({'success': True, 'id': slider.id, 'title': slider.title, 'description': slider.description})
    return JsonResponse({'success': False})

@csrf_exempt
def edit_slider(request, id):
    if request.method == 'POST':
        slider = get_object_or_404(Slider, id=id)
        slider.title = request.POST.get('title')
        slider.description = request.POST.get('description')
        if 'image' in request.FILES:
            slider.image = request.FILES.get('image')
        slider.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@csrf_exempt
def delete_slider(request, id):
    if request.method == 'POST':
        try:
            slider = get_object_or_404(Slider, id=id)
            slider.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})


def homepage(request):
    icons = Icon.objects.all()
    sliders = Slider.get_all_sliders()
    about_us = AboutUs.objects.first()  # Fetching the first AboutUs entry
    services = Service.objects.all()  # Fetching all services
    client = Client.objects.first()  # Fetching the first Client entry
    client_images = ClientImage.objects.filter(client=client)
    project = Project.objects.first()  # Assuming there's only one Project instance
    project_images = ProjectImage.objects.filter(project=project)
    testimonials = Testimonial.objects.all()
    team_members = ExpertTeamMember.objects.all()
    careers = Career.objects.all()
    recent_blogs = Blog.objects.order_by('-published_date')[:3]
    context = {
        'icons': icons,
        'sliders': sliders,
        'about_us': about_us,  # Adding about_us to the context
        'services': services,  # Adding services to the context
        'client': client,  # Adding client to the context
        'client_images': client_images,
        'project': project,
        'project_images': project_images,
        'testimonials': testimonials,
        'team_members': team_members,
        'careers': careers,
        'recent_blogs': recent_blogs,
    }
    return render(request, 'app/index.html', context)

def blog(request):
    blogs_list = Blog.objects.all().order_by('-published_date')
    paginator = Paginator(blogs_list, 6)  # Show 6 blogs per page
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)
    return render(request, 'app/blog.html', {'blogs': blogs})

@login_required
def career_dashboard(request):
    job_applications = JobApplication.objects.select_related('career').all()
    context = {
        'job_applications': job_applications,
    }
    return render(request, 'applied/html/careerdashboard.html', context)

def senior_translation_specialist(request):
    return render(request, 'app/senior_translation_specialist.html')

def contact(request):
    """Renders the contact page and handles form submissions."""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Construct the email content
        email_subject = f"Contact Form Submission: {subject}"
        email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        # Send the email
        send_mail(
            email_subject,
            email_message,
            settings.DEFAULT_FROM_EMAIL,
            ['specific-email@example.com'],  # Replace with the email address you want to send to
        )

        return render(request, 'app/contact.html', {
            'title': 'Contact',
            'message': 'Your message has been sent. Thank you!',
            'year': datetime.now().year,
        })

    return render(request, 'app/contact.html', {
        'title': 'Contact',
        'message': 'Your contact page.',
        'year': datetime.now().year,
    })

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

@csrf_exempt
def add_menu_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        link = data.get('link')
        header = Header.objects.create(name=name, link=link)
        return JsonResponse({'success': True, 'name': header.name, 'link': header.get_link()})
    return JsonResponse({'success': False})

def about_view(request):
    about_us = AboutUs.objects.first()  # Fetching the first AboutUs entry (you can customize this query as needed)
    return render(request, 'app/about.html', {'about_us': about_us})

@csrf_exempt
def upload_icon(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        icon_class = request.POST.get('icon_class')
        image = request.FILES.get('image')
        icon = Icon.objects.create(name=name, icon_class=icon_class, image=image)
        return JsonResponse({'success': True, 'id': icon.id, 'name': icon.name})
    return JsonResponse({'success': False})

@csrf_exempt
def edit_menu_item(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        link = data.get('link')
        header = get_object_or_404(Header, id=id)
        header.name = name
        header.link = link
        header.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@csrf_exempt
def add_social_icon(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            icon = Icon.objects.create(
                name=data.get('name'),
                icon_class=data.get('icon_class')
            )
            TopBar.objects.create(
                name=data.get('name'),
                link=data.get('link'),
                icon=icon
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})

@csrf_exempt
def edit_social_icon(request, icon_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            topbar_icon = TopBar.objects.get(id=icon_id)
            icon = topbar_icon.icon
            topbar_icon.name = data.get('name')
            topbar_icon.link = data.get('link')
            icon.icon_class = data.get('icon_class')
            topbar_icon.save()
            icon.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})

@csrf_exempt
def delete_social_icon(request, icon_id):
    if request.method == 'POST':
        try:
            topbar_icon = TopBar.objects.get(id=icon_id)
            topbar_icon.icon.delete()
            topbar_icon.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})

@csrf_exempt
def delete_menu_item(request, id):
    if request.method == 'POST':
        try:
            header = get_object_or_404(Header, id=id)
            header.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})


@csrf_exempt
def apply_for_career(request, career_id):
    if request.method == 'POST':
        career = Career.objects.get(id=career_id)
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.career = career
            application.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def career_details(request, career_id):
    career = get_object_or_404(Career, id=career_id)
    return render(request, 'app/career_details.html', {'career': career})

@csrf_exempt
@login_required
def update_application_status(request, application_id):
    if request.method == 'POST':
        application = get_object_or_404(JobApplication, id=application_id)
        status = request.POST.get('status')
        if status in dict(JobApplication.STATUS_CHOICES):
            application.status = status
            application.save()

            # Send email if status is interview or rejected
            if status == 'interview':
                send_mail(
                    'Interview Invitation',
                    'Dear {},\n\nYou have been shortlisted for an interview. Please contact us to schedule your interview.\n\nBest regards,\nYour Company'.format(application.name),
                    settings.DEFAULT_FROM_EMAIL,
                    [application.email],
                )
            elif status == 'rejected':
                send_mail(
                    'Application Status',
                    'Dear {},\n\nWe regret to inform you that your application has been rejected. Thank you for your interest.\n\nBest regards,\nYour Company'.format(application.name),
                    settings.DEFAULT_FROM_EMAIL,
                    [application.email],
                )

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid status'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})



def blog_post(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'app/blog_post.html', {'blog': blog})


