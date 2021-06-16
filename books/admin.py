from django.contrib import admin
from . import models
from publishers import models
from books import models

# Register your models here.
admin.site.register(models.Books)
