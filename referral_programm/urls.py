from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from django.views.generic import TemplateView

from users.views import (create_token, create_user,
                         UserView, UserProfileGetPath)


router = SimpleRouter()
router.register('users', UserView, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/signup/', create_user, name='signup'),
    path('api/auth/token/', create_token, name='token'),
    path('api/profile/', UserProfileGetPath.as_view()),
    path('api/', include(router.urls),),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
