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
        ('Informações Adicionais', {'fields': ('cargo', 'empresa', 'telefone')}),
    )
    list_display = ('username', 'email', 'cargo', 'empresa', 'is_staff', 'is_active')
    list_filter = ('cargo', 'empresa', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')



# Register your models here.
