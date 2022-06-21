from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from website.views import *
from django.contrib import admin
from django.urls import path, include
from website.models import *

urlpatterns = [
    path('', index, name='index'),
    path('accounts/', include('django.contrib.auth.urls'), kwargs=dict(club=clubmodel.objects.first())),
    path('accounts/register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profiles, name='profile'),
    path('training/', trainings, name='training'),
    path('game/', games, name='game'),
    path('team/', teams, name='team'),
    path('echelon/', echelons, name='echelon'),
    path('club/', club, name='club'),
    path('admin/', admin.site.urls),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
