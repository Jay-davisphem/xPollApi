from rest_framework.authtoken import views
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CreateVote, LoginView, ChoiceList, UserCreate, PollViewset
from rest_framework.schemas import get_schema_view

app_name = 'polls'

urlpatterns = [
    path("polls/<int:pk>/choices/", ChoiceList.as_view(), name="choice_list"),
    path("polls/<int:pk>/choices/<int:choice_pk>/vote/",
         CreateVote.as_view(), name="create_vote"),
    path("users/", UserCreate.as_view(), name="user_create"),
    path("login/", LoginView.as_view(), name="login"),
    path('docs/', get_schema_view(title='Polls API',
         description='An api for polls applications for developers'), name='docs-schemas'),
]

router = DefaultRouter()

router.register('polls', PollViewset, basename='polls')

urlpatterns += router.urls
