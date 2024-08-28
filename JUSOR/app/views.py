"""
Definition of views.
"""

from datetime import datetime
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import AboutUs, Icon, Header, Service, TopBar, Slider, ClientImage, Client, Project, ProjectImage, Article

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
    logo = Icon.objects.filter(name="Jusor logo").first()
    headers = Header.objects.all()
    icons = Icon.objects.all()
    social_media_icons = TopBar.objects.all()
    sliders = Slider.get_all_sliders()
    about_us = AboutUs.objects.first()  # Fetching the first AboutUs entry
    services = Service.objects.all()  # Fetching all services
    client = Client.objects.first()  # Fetching the first Client entry
    client_images = ClientImage.objects.filter(client=client)
    project = Project.objects.first()  # Assuming there's only one Project instance
    project_images = ProjectImage.objects.filter(project=project)
    articles = Article.objects.all()  # Fetching all images related to the client

    context = {
        'logo': logo,
        'headers': headers,
        'icons': icons,
        'social_media_icons': social_media_icons,
        'sliders': sliders,
        'about_us': about_us,  # Adding about_us to the context
        'services': services,  # Adding services to the context
        'client': client,  # Adding client to the context
        'client_images': client_images,
        'project': project,
        'project_images': project_images,
        'articles': articles,
    }
    return render(request, 'app/index.html', context)

def blog(request):
    logo_icon = Icon.objects.filter(name='Jusor logo').first()
    return render(request, 'app/blog.html', {'logo_icon': logo_icon})

def senior_translation_specialist(request):
    return render(request, 'app/senior_translation_specialist.html')

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

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

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'app/article_detail.html', {'article': article})
