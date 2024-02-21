from django.db import models
from django.contrib.auth.models import User,AnonymousUser

class PollRoom(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title

class PollOption(models.Model):
    poll_room = models.ForeignKey(PollRoom, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=100)
    vote_count = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.option_text[:20]
