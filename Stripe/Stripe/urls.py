from django.contrib import admin
from django.urls import path, include


handler404 = 'api.views.error_404'
handler500 = 'api.views.error_500'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
]
