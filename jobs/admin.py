from django.contrib import admin
from .models import User, Job, Shift ,Review ,Profile 

admin.site.register(User)
admin.site.register(Job)
admin.site.register(Shift)
admin.site.register(Review)
admin.site.register(Profile)