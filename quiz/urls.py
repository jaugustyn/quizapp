from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'questions', views.QuestionViewSet)


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


# MANUAL VIEWSET URLS

# category_list = views.CategoryViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# category_detail = views.CategoryViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
#
# question_list = views.QuestionViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# question_detail = views.CategoryViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })

# path('categories/', category_list, name='category_list'),
# path('categories/<str:name>/', category_detail, name='category_detail'),
# path('questions/', question_list, name='question_list'),
# path('questions/<str:pk>/', question_detail, name='question_detail'),