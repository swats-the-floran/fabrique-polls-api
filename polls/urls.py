from rest_framework.routers import DefaultRouter

from .views import (
    PollMVS,
    PollQuestionMVS,
    QuestionOptionMVS,
    QuestionAnswerMVS,
)

router = DefaultRouter()
router.register('polls', PollMVS, basename='poll')
router.register('questions', PollQuestionMVS, basename='question')
router.register('options', QuestionOptionMVS, basename='option')
router.register('answers', QuestionAnswerMVS, basename='answer')
urlpatterns = router.urls
