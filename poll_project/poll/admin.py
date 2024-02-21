from django.contrib import admin
from .models import PollRoom, PollOption

admin.site.register(PollRoom)
admin.site.register(PollOption)