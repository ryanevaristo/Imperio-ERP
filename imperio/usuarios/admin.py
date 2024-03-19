from django.contrib import admin
from .models import Users
from django.contrib.auth import admin as auth_admin
from .forms import UserChangeForm, UserCreationForm


@admin.register(Users)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = Users
    fieldsets = auth_admin.UserAdmin.fieldsets + (
        (None, {'fields': ('cargo',)}),
    )



# Register your models here.
