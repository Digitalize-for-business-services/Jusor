from .models import Icon, Header, TopBar


def global_context(request):
       logo = Icon.objects.filter(name="Jusor logo").first()
       headers = Header.objects.all()
       social_media_icons = TopBar.objects.all()
       return {
           'logo': logo,
           'headers': headers,
           'social_media_icons': social_media_icons,
       }