from django.contrib import admin
from .models import User
from django.utils.html import format_html


admin.site.site_header = 'RRP Administration'
admin.site.site_title = 'RRP admin site'


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "creation_date", "is_superuser", "image_tag")
    list_display_links = ("id", "username")
    prepopulated_fields = {"slug": ("username",)}
    readonly_fields = ("creation_date", "image_tag")

    def image_tag(self, obj):
        if obj.photo:
            return format_html('<img src="{0}" style="width: 80px; height:80px;" />'.format(obj.photo.url))
        else:
            return format_html('<img src="/static/images/default_user.jpg" style="width: 80px; height:80px;" />')


admin.site.register(User, UserAdmin)
