from django.contrib import admin
from .models import Course, Module, Enrollment, Review

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Enrollment)
admin.site.register(Review)

