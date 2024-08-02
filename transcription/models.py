from django.db import models

class Transcription(models.Model):
    text = models.TextField()

class ReferenceText(models.Model):
    text = models.TextField()
