from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework.routers import DefaultRouter
import pprint

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'questions', views.QuestionViewSet)

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
]
