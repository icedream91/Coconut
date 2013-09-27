from blog import models
from django.contrib import admin

admin.site.register(models.Setting)
admin.site.register(models.Article)
admin.site.register(models.Tag)
admin.site.register(models.Category)
admin.site.register(models.Page)
