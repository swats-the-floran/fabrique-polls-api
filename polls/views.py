from rest_framework.decorators import action
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import (
    Poll,
    PollQuestion,
    QuestionOption,
    QuestionAnswer,
)
from .serializers import (
    PollSerializer,
    PollQuestionSerializer,
    QuestionOptionSerializer,
    QuestionAnswerSerializer,
)


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class PollMVS(ModelViewSet):
    
    serializer_class = PollSerializer
    permission_classes = [IsAdminUser]
    queryset = Poll.objects.all()

    # getting active polls' list (finish_date is greater than datetime of the request) 
    @action(detail=False, methods=['get'])
    def active_polls(self, request):
        a_polls = Poll.get_active_polls()
        serializer = self.get_serializer(a_polls, many=True)
        return Response(serializer.data)

    # getting polls with answers by user_id
    @action(detail=False, methods=['get'])
    def user_polls(self, request):
        user_id = request.GET.get('user_id')
        u_answers = QuestionAnswer.objects.filter(user_id=user_id)
        serializer = QuestionAnswerSerializer(u_answers, many=True, context={'user_id': user_id})
        return Response(serializer.data)


class PollQuestionMVS(ModelViewSet):

    serializer_class = PollQuestionSerializer
    permission_classes = [IsAdminUser]
    queryset = PollQuestion.objects.all()


class QuestionOptionMVS(ModelViewSet):

    serializer_class = QuestionOptionSerializer
    permission_classes = [IsAdminUser]
    queryset = QuestionOption.objects.all()


class QuestionAnswerMVS(ModelViewSet):

    serializer_class = QuestionAnswerSerializer
    queryset = QuestionAnswer.objects.all()
