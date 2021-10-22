from datetime import datetime
from pytz import utc

from rest_framework.serializers import (
    ModelSerializer,
    ValidationError
)

from polls.models import (
    Poll,
    PollQuestion,
    QuestionOption,
    QuestionAnswer,
)


def get_poll(value):
    poll = value.get('poll')
    if not poll:
        raise ValidationError("this answer doesn't belong to any poll")
    return poll


def get_question(value):
    question = value.get('question')
    if not question:
        raise ValidationError("this option or answer doesn't belong to any question")
    return question


class PollSerializer(ModelSerializer):
    
    def validate_begin_date(self, value):
        if self.instance and self.instance.begin_date != value:
            raise ValidationError("this field can't be changed.")
        return value
    
    class Meta:
        model = Poll
        fields = '__all__'


class PollQuestionSerializer(ModelSerializer):
 
    class Meta:
        model = PollQuestion
        fields = '__all__'


class QuestionOptionSerializer(ModelSerializer):

    def validate(self, value):
        question = get_question(value)

        # text_answer type of questions doesn't have options
        if question.answer_type == PollQuestion.TEXT_ANSWER:
            raise ValidationError("text_answer type of questions doesn't have options")

        return value
        
    class Meta:
        model = QuestionOption
        fields = '__all__'


class QuestionAnswerSerializer(ModelSerializer):

    def validate(self, value):
        poll = get_poll(value)
        if poll.finish_date < utc.localize(datetime.now()):
            raise ValidationError("this poll is finished. you can't add your answer.")
    
        question = get_question(value)
        
        # checking for douplicate answer in text_answer and radio_answer types of question
        if question.answer_type in (PollQuestion.TEXT_ANSWER, PollQuestion.RADIO_ANSWER):
            another_answer = QuestionAnswer.objects.filter(question=question)
            if another_answer and not self.instance:
                raise ValidationError("question with text or radio type of answer can't have multiple answers.")

        # checking if answer is corresponding with question's options
        if question.answer_type in (PollQuestion.RADIO_ANSWER, PollQuestion.CHECK_ANSWER):
            question_options = QuestionOption.objects.filter(question=question)
            if not question_options:
                raise ValidationError("this question doesn't have options you can choose from.")

            question_options = question_options.filter(text=value.get('text'))
            if not question_options:
                raise ValidationError("there is no such option in this question.")
        
        return value

    class Meta:
        model = QuestionAnswer
        fields = '__all__'
