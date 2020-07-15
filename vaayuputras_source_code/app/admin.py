from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import custom_field

class custome_field_Inline(admin.StackedInline):
    model = custom_field
    can_delete = False
    verbose_name_plural = 'custom_field'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (custome_field_Inline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)