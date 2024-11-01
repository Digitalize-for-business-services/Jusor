"""
Definition of urls for JUSOR.
"""
from datetime import datetime
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.conf import settings
from django.conf.urls.static import static
from app.views import delete_menu_item, career_dashboard, blog_post

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', views.homepage, name='homepage'),
    path('blog/', views.blog, name='blog'),
    path('senior-translation-specialist/', views.senior_translation_specialist, name='senior-translation-specialist'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('add_menu_item/', views.add_menu_item, name='add_menu_item'),
    path('upload_icon/', views.upload_icon, name='upload_icon'),
    path('edit_menu_item/<int:id>/', views.edit_menu_item, name='edit_menu_item'),
    path('add_social_icon/', views.add_social_icon, name='add_social_icon'),
    path('edit_social_icon/<int:icon_id>/', views.edit_social_icon, name='edit_social_icon'),
    path('delete_social_icon/<int:icon_id>/', views.delete_social_icon, name='delete_social_icon'),
    path('add_slider/', views.add_slider, name='add_slider'),
    path('edit_slider/<int:id>/', views.edit_slider, name='edit_slider'),
    path('delete_slider/<int:id>/', views.delete_slider, name='delete_slider'),
    path('about/', views.about_view, name='about'),
    path('apply/', views.apply_for_career, name='apply_for_career'),
    path('career/<int:career_id>/', views.career_details, name='career_details'),
    path('apply/<int:career_id>/', views.apply_for_career, name='apply_for_career'),
    path('update_application_status/<int:application_id>/', views.update_application_status, name='update_application_status'),
    path('career_dashboard/', career_dashboard, name='career_dashboard'),
    path('delete_menu_item/<int:id>/', delete_menu_item, name='delete_menu_item'),
    path('blog/<int:blog_id>/', views.blog_post, name='blog_post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)