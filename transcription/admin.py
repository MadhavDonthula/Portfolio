from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Assignment, QuestionAnswer, ClassCode, FlashcardSet, Flashcard, CustomUser

# Register existing models
admin.site.register(Assignment)
admin.site.register(QuestionAnswer)
admin.site.register(ClassCode)

class FlashcardInline(admin.TabularInline):
    model = Flashcard
    extra = 1

@admin.register(FlashcardSet)
class FlashcardSetAdmin(admin.ModelAdmin):
    inlines = [FlashcardInline]
    fields = ('name', 'bulk_flashcards')

@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('french_word', 'english_translation', 'flashcard_set')

# Register CustomUser model with Django admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'class_code', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email', 'class_code')
    ordering = ('username',)

    # Use the default UserAdmin form
    fieldsets = UserAdmin.fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'class_code'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
