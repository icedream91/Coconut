# Run "python manage.py shell" and import this module 
# to initialize blog's settings.

from blog.models import Setting

settings=Setting.objects.create(
    blog_name='Your blog name',
)

