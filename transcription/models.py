from django.db import models

class Transcription(models.Model):
    audio_file = models.FileField(upload_to="audio/")
    transcribed_text = models.TextField()

class Assignment(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class QuestionAnswer(models.Model):
    assignment = models.ForeignKey(Assignment, related_name="questions", on_delete=models.CASCADE)
    question = models.TextField(max_length=500)
    answer = models.TextField(max_length=500)

    def __str__(self):
        return f"Question: {self.question[:30]}"

class ClassCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    assignment = models.ForeignKey(Assignment, related_name="class_codes", on_delete=models.CASCADE)

    def __str__(self):
        return self.code
