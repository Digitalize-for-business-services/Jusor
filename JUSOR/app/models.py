"""
Definition of models.
"""

from django.db import models
from django.utils.text import slugify
import os
from django.urls import reverse
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField('Content')  # Adjust config_name as needed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
def custom_upload_to(instance, filename):
    name, ext = os.path.splitext(filename)
    # Slugify the name (optional) to remove spaces and special characters
    name = slugify(name)
    # Return the new path
    return f'icons/{name}{ext}'
class Icon(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=100, blank=True, null=True)  # Optional for FontAwesome or similar libraries
    image = models.ImageField(upload_to=custom_upload_to, blank=True, null=True)
    link = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def get_link(self):
        """Return the absolute URL for the stored link."""
        # If the link is relative (e.g., "/"), it should stay as is.
        if self.link:
            if self.link.startswith('/'):
                return self.link
            try:
                return reverse(self.link)
            except:
                return self.link
        return "/"

    def display_icon(self):
        """Return HTML code for displaying the icon depending on which field is filled."""
        if self.icon_class:
            return f'<i class="{self.icon_class}"></i>'
        elif self.image:
            return f'<img src="{self.image.url}" alt="{self.name}" />'
        return ""

    display_icon.short_description = "Icon Preview"
    display_icon.allow_tags = True

class TopBar(models.Model):
    name = models.CharField(max_length=100)
    link = models.URLField()
    icon = models.ForeignKey(Icon, on_delete=models.CASCADE, related_name="topbar_icons")

    def __str__(self):
        return self.name

class Header(models.Model):
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name
    def get_link(self):
        """Return the absolute URL for the stored link."""
        # If the link is relative (e.g., "/"), it should stay as is.
        if self.link:
            if self.link.startswith('/'):
                return self.link
            try:
                return reverse(self.link)
            except:
                return self.link
        return "/"

class Slider(models.Model):
    image = models.ImageField(upload_to='sliders/')
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title
    @staticmethod
    def get_all_sliders():
        return Slider.objects.all()

class Service(models.Model):
    icon = models.ForeignKey(Icon, on_delete=models.CASCADE, related_name="service_icons")
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

class Client(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

class ClientImage(models.Model):
    client = models.ForeignKey(Client, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='clients/')

    def __str__(self):
        return f"Image for {self.client.title}"

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    def __str__(self):
        return self.title
    
class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projects/')
    description = models.TextField()

    def __str__(self):
        return f"Project: {self.description[:50]}"

class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='blogs/')

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class ExpertTeamMember(models.Model):
    name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    icons = models.ManyToManyField(Icon, related_name='team_icons')  # Multiple social links

    def __str__(self):
        return self.name

class AboutUs(models.Model):
    image = models.ImageField(upload_to='about_us/')
    title = models.CharField(max_length=200)
    slang = models.CharField(max_length=1000, blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.title