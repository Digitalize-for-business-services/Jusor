from django.contrib import admin
from .models import Icon, TopBar, Header, Slider, Service, Client, Project, ProjectImage, Blog, Testimonial, ExpertTeamMember, AboutUs, ClientImage, Article

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

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')  # The main fields to display
    list_display_links = ('title',)  # Link to edit the article by clicking the title
    search_fields = ('title', 'content')