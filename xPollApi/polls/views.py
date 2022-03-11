from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer, UserSerializer
from .models import Poll, Choice
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User
import os


class ChoiceList(generics.ListCreateAPIView):

    def get_queryset(self):
        queryset = Choice.objects.filter(poll__id=self.kwargs['pk'])
        return queryset
    serializer_class = ChoiceSerializer

    def post(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs["pk"])
        if not request.user == poll.created_by:
            raise PermissionDenied("You can not create choice for this poll.")
        return super().post(request, *args, **kwargs)


class CreateVote(APIView):

    def post(self, request, pk, choice_pk):
        voted_by = request.data.get("voted_by")
        data = {'choice': choice_pk, 'poll': pk, 'voted_by': voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PollViewset(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs["pk"])
        if not request.user == poll.created_by:
            raise PermissionDenied("You can not delete this poll.")
        return super().destroy(request, *args, **kwargs)


try:
    val = os.environ['LIST_USERS']
    OBJ = generics.CreateAPIView
    if val:
        OBJ = generics.ListCreateAPIView
except KeyError:
    OBJ = generics.CreateAPIView


class UserCreate(OBJ):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer
    queryset = User.objects.all()


class LoginView(APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
