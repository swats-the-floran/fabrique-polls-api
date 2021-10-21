from datetime import datetime

from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    TextField,
)


ANSWER_LENGTH = 1024


class Poll(Model):

    title = CharField(max_length=256)
    description = TextField()
    begin_date = DateTimeField()
    finish_date = DateTimeField()

    def __str__(self):
        return f"{self.id}: {self.title}"

    def get_active_polls():
        a_polls = Poll.objects.filter(finish_date__gt=datetime.now())
        return a_polls

    class Meta:
        ordering = ['begin_date']


class PollQuestion(Model):

    TEXT_ANSWER = 'TX'
    RADIO_ANSWER = 'RD'
    CHECK_ANSWER = 'CH'

    TYPE_CHOICES = [
        (TEXT_ANSWER, 'text answer'),
        (RADIO_ANSWER, 'single choice'),
        (CHECK_ANSWER, 'multiple choices'),
    ]

    poll = ForeignKey(Poll, on_delete=CASCADE)
    text = TextField()
    answer_type = CharField(
        max_length=2,
        choices=TYPE_CHOICES,
    )

    def __str__(self):
        return f"{self.id}: {self.text[:30] if self.text else ''}"

    class Meta:
        ordering = ['poll', 'id']


class QuestionOption(Model):

    poll = ForeignKey(Poll, on_delete=CASCADE)
    question = ForeignKey(PollQuestion, on_delete=CASCADE)
    text = CharField(max_length=ANSWER_LENGTH, null=True)

    def __str__(self):
        return f"{self.id}:  {self.text[:30] if self.text else ''}"

    class Meta:
        ordering = ['poll', 'question', 'id']


class QuestionAnswer(Model):

    user_id = CharField(max_length=10)
    poll = ForeignKey(Poll, on_delete=CASCADE)
    question = ForeignKey(PollQuestion, on_delete=CASCADE)
    text = CharField(max_length=ANSWER_LENGTH)
