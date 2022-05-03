from django.contrib import admin

# Register your models here.
from .models import Task


@admin.register(Task)
class PortDetailAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'complete')

