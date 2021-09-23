from django.urls import path
from . import views
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

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

    # path('', views.api_overview, name="api-overview"),  # Api overview
    path('categories/', views.category_list.as_view(), name="category_list"),
    path('categories/<str:name>/', views.category_update.as_view(), name="category_update"),
    path('questions/', views.question_list.as_view(), name="question_list"),
    path('questions/<str:pk>/', views.question_update.as_view(), name="question_update"),
    path('quiz/<str:name>/', views.quiz_list, name="quiz_list"),
]
