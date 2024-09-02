from django.contrib import admin
from .models import ProfileChild, ProfileParent, ProfileTherapist

@admin.register(ProfileChild)
class ProfileChildAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'age', 'date_of_birth', 'autism_level')

@admin.register(ProfileParent)
class ProfileParentAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'document_type', 'date_of_birth', 'document_number', 'front_document_image', 'back_document_image')

@admin.register(ProfileTherapist)
class ProfileTherapistAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'document_type', 'date_of_birth', 'document_number', 'front_document_image', 'back_document_image')
