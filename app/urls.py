from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from .authentication.auth_view import AuthView, AuthLogoutView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/criterias/', include('app.criterias.urls')),
    path('api/v1/websites/', include('app.websites.urls')),
    path('api/v1/pages/', include('app.pages.urls')),
    path('api/v1/scrape/', include('app.scrape.urls')),
    path('api/v1/login/', AuthView.as_view(), name='login'),
    path('api/v1/logout/', AuthLogoutView.as_view(), name='logout'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
