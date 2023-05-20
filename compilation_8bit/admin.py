from django.contrib import admin
from .models import File, Directory

# Register your models here.
#
# admin.site.register(File)
# admin.site.register(Directory)


class FileAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(File, FileAdmin)

class DirAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Directory, DirAdmin)
