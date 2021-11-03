from django.views.generic import TemplateView
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.schemas import get_schema_view
from rest_framework.routers import DefaultRouter
from . import views
import accounts.views
import pprint

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename="categories")
router.register(r'questions', views.QuestionViewSet, basename="questions")
router.register(r'users', accounts.views.UserViewSet, basename="users")
# pprint.pprint(router.get_urls())  # Prints created urls by router


urlpatterns = [
    #  Openapi
    path('openapi', get_schema_view(
        title="Quiz Project",
        description="API for Quiz app",
        version="1.0.0"
    ), name='openapi-schema'),

    #  Swagger
    path('', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),

    #  Redoc
    path('redoc/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='redoc'),

    path('', include(router.urls)),
    path('quiz/<str:name>/', views.get_quiz, name="get_quiz"),

    #  User suggestions for new questions
    path('suggestion/', views.NewQuestionSuggestion.as_view({'post': 'create'}), name='new_question_suggestion'),
    path('suggestion/list/', views.QuestionDraftList.as_view({'get': 'list'}), name="question_draft_list"),
    path('suggestion/list/<pk>/', views.SingleQuestionDraft.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy', 'patch': 'partial_update'}), name="single_question_draft"),

    #  User accounts
    path('accounts/api-token-auth', obtain_auth_token, name='api_token_auth'),
    path('accounts/register/', accounts.views.registration, name="register"),
    path('accounts/login/', accounts.views.login_user, name='login_user'),
    path('accounts/logout/', accounts.views.logout_user, name="logout_user"),
    path('api-auth/', include('rest_framework.urls')),
]
