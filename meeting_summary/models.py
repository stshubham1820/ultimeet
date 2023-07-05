from django.db import models
from user_authentication.models import User, Session
from recording_transcription.models import Meeting, Transcript

# Create your models here.
class Summary(models.Model):
    summary_id = models.AutoField(primary_key=True)
    meeting_id = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    transcript_id = models.ForeignKey(Transcript, on_delete=models.CASCADE)
    summary_text = models.TextField()
    summary_audio = models.BinaryField()

    class Meta:
        db_table = 'summaries'  

class Agenda(models.Model):
    agenda_id = models.AutoField(primary_key=True)
    meeting_id = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    transcript_id = models.ForeignKey(Transcript, on_delete=models.CASCADE)
    agenda_text = models.TextField()

    class Meta:
        db_table = 'agendas'  

class KeyPoint(models.Model):
    keypoint_id = models.AutoField(primary_key=True)
    meeting_id = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    transcript_id = models.ForeignKey(Transcript, on_delete=models.CASCADE)
    keypoint_text = models.TextField()

    class Meta:
        db_table = 'keypoints'