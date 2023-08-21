from config import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.urls import reverse



class OpenPollsManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status=Polls.Status.OPEN)


class Polls(models.Model):

    # enum to enable poll open and closure
    class Status(models.TextChoices):
        OPEN = 'opn', 'Open'
        CLOSE = 'cls', 'Close'


    question = models.CharField(max_length=250)
    pc_mail = models.EmailField()
    option1 = models.CharField(max_length=50)
    option2 = models.CharField(max_length=50)
    option3 = models.CharField(max_length=50)
    option1_count = models.IntegerField(default=0)
    option2_count = models.IntegerField(default=0)
    option3_count = models.IntegerField(default=0)
    status = models.CharField(max_length=3, 
                               choices=Status.choices,
                               default=Status.OPEN)
    date = models.DateTimeField(auto_now_add=True)
    

    objects = models.Manager()
    open = OpenPollsManager()

    class Meta:
         ordering = ['-question']
         indexes = models.Index(fields=['-question']),


    # method to close a poll
    def close_poll(self):
      return self.status == Polls.Status.CLOSE

    def __str__(self):
        return self.option1, self.option2, self.option3
    
    def get_absolute_url(self):
        return reverse('poll_detail', args=[self.pk])

    def total_votes(self):
         return self.option1_count + self.option2_count + self.option3_count
         
    
class OneTimeCode(models.Model):
    email = models.CharField(max_length=35)
    code = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Code for {self.email}'
    
