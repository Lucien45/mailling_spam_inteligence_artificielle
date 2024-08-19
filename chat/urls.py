from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GmailCompteViewSet, GmailMessageViewSet, RecevoirMessageViewSet, EnvoyerMessageViewSet, CreateAccount, Login, Inbox, SendEmail, Logout, RetrainModel, UserInfo, FetchCategories

router = DefaultRouter()
router.register(r'accounts', GmailCompteViewSet)
router.register(r'messages', GmailMessageViewSet)
router.register(r'received', RecevoirMessageViewSet)
router.register(r'sent', EnvoyerMessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create-account/', CreateAccount.as_view(), name='create_account'),
    path('login/', Login.as_view(), name='login'),
    path('inbox/', Inbox.as_view(), name='inbox'),
    path('send-email/', SendEmail.as_view(), name='send_email'),
    path('logout/', Logout.as_view(), name='logout'),
    path('retrain-model/', RetrainModel.as_view(), name='retrain_model'),
    path('user-info/', UserInfo.as_view(), name='user_info'),
    path('categories/', FetchCategories.as_view(), name='fetch_categories'),
]
