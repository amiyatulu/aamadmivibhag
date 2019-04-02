from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from profiles_api import models

admin.site.register(models.Department, MPTTModelAdmin)