from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
import accounts.views
from . import views
from accounts.views import UserViewSet
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'questions', views.QuestionViewSet)
router.register(r'users', UserViewSet)
# pprint.pprint(router.get_urls())  # Prints created urls by router


urlpatterns = [
    path('', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
    path('openapi', get_schema_view(
        title="Quiz Project",
        description="API for Quiz app",
        version="1.0.0"
    ), name='openapi-schema'),

    path('', include(router.urls)),
    path('quiz/<str:name>/', views.quiz_list, name="quiz_list"),
    path('accounts/api-auth/', include('rest_framework.urls')),
    path('accounts/api-token-auth', obtain_auth_token, name='api_token_auth'),
    path('accounts/register/', accounts.views.registration_view, name="register"),
]
