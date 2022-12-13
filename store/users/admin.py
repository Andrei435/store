from django.contrib import admin

from .models import User, EmailVerificatiom

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username']

@admin.register(EmailVerificatiom)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['code', 'user', 'expiration']
    fields = ['code', 'user', 'expiration', 'created']
    readonly_fields = ['created']
