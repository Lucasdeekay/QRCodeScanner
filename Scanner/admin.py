from django.contrib import admin


# Register your models here.
from Scanner.models import Person


class PersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'phone_no')


admin.site.register(Person, PersonAdmin)