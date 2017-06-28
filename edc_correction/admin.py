from django.contrib import admin

from .models import SubjectConsent


@admin.register(SubjectConsent)
class HouseholdMemberAdmin(admin.ModelAdmin):
    pass
