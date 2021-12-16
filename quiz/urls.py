from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from . import views
import accounts.views
import pprint

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename="categories")
router.register(r'questions', views.QuestionViewSet, basename="questions")
router.register(r'users', accounts.views.UserViewSet, basename="users")
# pprint.pprint(router.get_urls())  # Prints created urls by router


urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Optional UI - Docs:
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Swagger as main page
    path('', include(router.urls)),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    #  Quiz
    path('quiz/<str:name>/', views.GetQuiz.as_view(), name="get_quiz"),

    #  User suggestions for new questions
    path('suggestion/', views.NewQuestionSuggestion.as_view({'post': 'create'}), name='new_question_suggestion'),
    path('suggestion/list/', views.QuestionDraftList.as_view({'get': 'list'}), name="question_draft_list"),
    path('suggestion/list/<pk>/', views.SingleQuestionDraft.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy', 'patch': 'partial_update'}),
         name="question_suggestion_details"),

    #  User accounts
    path('accounts/api-token-auth', obtain_auth_token, name='api_token_auth'),
    path('accounts/register/', accounts.views.Registration.as_view(), name="register"),
    path('accounts/login/', accounts.views.Login_user.as_view(), name='login_user'),
    path('accounts/logout/', accounts.views.LogoutUser.as_view(), name="logout_user"),

    #  Login to the Browsable API
    path('api-auth/', include('rest_framework.urls')),
]
