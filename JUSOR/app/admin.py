from django.contrib import admin
from .models import Icon, TopBar, Header, Slider, Service, Client, Project, ProjectImage, Blog, Testimonial, ExpertTeamMember, AboutUs, ClientImage, Career, JobApplication

admin.site.register(Slider)
admin.site.register(Service)
admin.site.register(Client)
admin.site.register(Project)
admin.site.register(ProjectImage)
admin.site.register(Blog)
admin.site.register(Testimonial)
admin.site.register(ExpertTeamMember)
admin.site.register(AboutUs)
admin.site.register(ClientImage)

@admin.register(Icon)
class IconAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_icon', 'link')
    readonly_fields = ('display_icon',)

@admin.register(TopBar)
class TopBarAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'icon')

@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'link')

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('title', 'details_link', 'apply_link')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'career', 'email', 'phone', 'applied_at')
    search_fields = ('name', 'email', 'phone', 'career__title')
    list_filter = ('career', 'applied_at')