from django.contrib import admin

from .models import Assignment, QuestionAnswer, ClassCode, FlashcardSet, Flashcard

admin.site.register(Assignment)
admin.site.register(QuestionAnswer)
admin.site.register(ClassCode)
admin.site.register(FlashcardSet)
admin.site.register(Flashcard)