from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint


class Poll(models.Model):
    question = models.CharField(max_length=100)
    # Many Polls ---> 1 User(ManyToOne)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(
        Poll, related_name='choices', on_delete=models.CASCADE)  # Many choices ---> 1 Poll(ManyToOne)
    choice_text = models.CharField(max_length=100)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    choice = models.ForeignKey(
        Choice, related_name='votes', on_delete=models.CASCADE)  # Many votes ---> 1 choice(ManyToOne)
    # Many votes ---> 1 poll(ManyToOne)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    # Many votes ---> 1 user(ManyToOne)
    voted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["poll", "voted_by"], name='unique poll votes')]
