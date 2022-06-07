from django.contrib import admin
from website.models import *

admin.site.site_header = 'Administração - ' + clubmodel.objects.first().name
admin.site.site_title = clubmodel.objects.first().name
admin.site.index_title = 'Administração'

class listclub(admin.ModelAdmin):
    list_display = ('name', 'description')

admin.site.register(clubmodel, listclub)
admin.site.register(profile)
admin.site.register(echelonmodel)
admin.site.register(teammodel)
admin.site.register(trainingmodel)
admin.site.register(gamemodel)