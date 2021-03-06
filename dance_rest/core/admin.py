# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from core import models


class UserDetailsAdminStacked(admin.StackedInline):
    model = models.UserDetails


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email']
    inlines = [UserDetailsAdminStacked]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        # (_('Personal Info'), {'fields': ('name',)}),
        (_('Permissions'),
          {
            'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser'
             )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )

    add_fieldsets = (
        (None, {
                "classes": ('wide',),
                "fields": ('email', 'password1', 'password2')
        }),
    )


class UserDetailsAdmin(admin.ModelAdmin):

    ordering = ['name', 'surname']
    list_display = ['name', 'surname', 'get_email', 'tel']
    def get_email(self, obj):
        return obj.user.email


class EventAdmin(admin.ModelAdmin):
    ordering = ['date']
    list_display = ['name', 'date', 'location']


class PackAdmin(admin.ModelAdmin):
    # ordering = ['date']
    list_display = ['name', 'price', 'starting_date']
    # def starting_date(self, obj):
    #     return max([event.date for event in obj.events.all()])


# @admin.register(models.User, models.UserDetails)
# class UserDetailsAdmin(admin.ModelAdmin):
#     pass

admin.site.register(models.User, UserAdmin)
admin.site.register(models.UserDetails, UserDetailsAdmin)
admin.site.register(models.Artist)
admin.site.register(models.Location)
admin.site.register(models.Event, EventAdmin)
admin.site.register(models.Pack, PackAdmin)
