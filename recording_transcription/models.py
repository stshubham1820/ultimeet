from django.db import models

# Create your models here.
class Meeting(models.Model):
    meeting_id = models.AutoField(primary_key=True)
    meeting_title = models.CharField(max_length=100)
    meeting_organizer = models.CharField(max_length=100)
    meeting_nature = models.CharField(max_length=100,null=True)
    meeting_time = models.DateTimeField(null=True)
    meeting_from = models.DateTimeField(null=True)
    meeting_to = models.DateTimeField(null=True)
    #meeting_organizer_id = models.CharField(max_length=100)
    meeting_organizer_email = models.EmailField(default='')
    meeting_organizer_profile_picture = models.ImageField(upload_to='profile_pictures',null=True)
    meeting_organizer_username = models.CharField(max_length=100,null=True)
    meeting_type = models.CharField(max_length=100,null=True)
    meeting_channel = models.CharField(max_length=100,null=True)
    participants_list = models.ManyToManyField('Participant', related_name='meetings')
    action_item_approved_by_list = models.ManyToManyField('Action_Item_Approved_By', related_name='meetings_approved_by')
    meeting_description = models.CharField(max_length=100,null=True)
    meeting_location = models.CharField(max_length=100,null=True)
    meeting_action_items_count = models.CharField(max_length=100,null=True)
    absents_list = models.ManyToManyField('Absents', related_name='meetings_absents')
    class Meta:
        db_table = 'meetings'

class Participant(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    username = models.CharField(max_length=255)
    profile_picture = models.URLField()

    class Meta:
        db_table = 'Participant'

class Absents(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    profile_picture = models.URLField()

    class Meta:
        db_table = 'Absents'

class Action_Item_Approved_By(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    profile_picture = models.URLField()

    class Meta:
        db_table = 'Action_Item_Approved_By'

class Transcript(models.Model):
    #meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    transcript_id = models.AutoField(primary_key=True)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    raw_transcript = models.TextField()

    class Meta:
        db_table = 'Transcript'