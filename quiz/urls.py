from django.urls import path
from . import views
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
    path('openapi', get_schema_view(
        title="Your Project",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),

    path('', views.category_list.as_view(), name="category_list"),
    path('overview/', views.apiOverview, name="api-overview"),  # Api overview
    # path('<slug:slug>/', views.category_detail.as_view(), name="category_detail"),
    path('<slug:slug>/', views.quiz_list, name="quiz_list"),
    path('<slug:slug>/result/', views.quiz_result, name="quiz_result"),
]
