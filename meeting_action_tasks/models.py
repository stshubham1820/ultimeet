from django.db import models
from user_authentication.models import User, Session
from recording_transcription.models import Meeting, Transcript

# Create your models here.
class ActionItem(models.Model):
    action_item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    reporter = models.CharField(max_length=255)
    priority = models.CharField(max_length=255)
    due_on = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    actions = models.TextField()
    dependencies = models.CharField(max_length=255, blank=True, null=True)  # New column
    comments = models.TextField(blank=True, null=True)  # New column
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    class Meta:
        db_table = 'action_item'
    