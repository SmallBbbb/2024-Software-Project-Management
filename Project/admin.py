from django.contrib import admin
from .models import Project, Standard, TestStaff, Regulation, Comparison, Equipment, Tutorials

admin.site.register(Project)
admin.site.register(Standard)
admin.site.register(TestStaff)
admin.site.register(Regulation)
admin.site.register(Comparison)
admin.site.register(Equipment)
admin.site.register(Tutorials)