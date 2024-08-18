from django.shortcuts import render, redirect, get_object_or_404
import base64
import whisper
import string
from django.http import HttpResponse
from .models import Assignment, QuestionAnswer, ClassCode, FlashcardSet, Flashcard

def blank(request):
    return render(request, "transcription/blank.html")

def home(request):
    if request.method == "POST":
        code = request.POST.get("class_code").upper()  # Convert code to uppercase
        try:
            class_code = ClassCode.objects.get(code=code)
            assignments = [class_code.assignment] 
            return render(request, 'transcription/index.html', {'assignments': assignments})
        except ClassCode.DoesNotExist:
            return render(request, 'transcription/home.html', {'error': 'Invalid class code'})
    return render(request, 'transcription/home.html')

def index(request, assignment_id=None):
    if assignment_id:
        assignment = get_object_or_404(Assignment, id=assignment_id)
        assignments = [assignment]
    else:
        assignments = Assignment.objects.all()
    return render(request, 'transcription/index.html', {'assignments': assignments})

def record_audio(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    questions = assignment.questions.all()
    return render(request, "transcription/record_audio.html", {"assignment": assignment, "questions": questions})

def save_audio(request):
    if request.method == "POST":
        audio_data = request.POST.get("audio_data", "")
        assignment_id = request.POST.get("assignment_id", "")
        question_id = request.POST.get("question_id", "")

        if not assignment_id.isdigit() or not question_id.isdigit():
            return HttpResponse("Error: Invalid ID format")
        
        assignment_id = int(assignment_id)
        question_id = int(question_id)

        try:
            if audio_data:
                # Decode audio data and save it as a WAV file
                audio_bytes = base64.b64decode(audio_data)
                with open("temp_audio.wav", "wb") as f:
                    f.write(audio_bytes)

                # Load the Whisper model
                model = whisper.load_model("medium")

                # Transcribe the audio with language set to French
                result = model.transcribe("temp_audio.wav", language="fr")
                transcribed_text = result["text"]

                # Retrieve the assignment and reference text
                assignment = get_object_or_404(Assignment, id=assignment_id)
                selected_question = get_object_or_404(QuestionAnswer, id=question_id, assignment=assignment)
                selected_answer = selected_question.answer

                Answer = selected_answer if selected_answer else ""
                # Compare the transcribed text with the reference text
                missing_words, score = compare_texts(transcribed_text, Answer)

                # Pass the transcribed text, answer, and score to the result page
                return render(request, 'transcription/result.html', {
                    'transcribed_text': transcribed_text,
                    'answer': Answer,
                    'score': score,
                    'assignment': assignment,
                    'question': selected_question,  # Ensure the question object is passed
                })
            else:
                return HttpResponse("Error: Invalid audio data format")
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")
    return HttpResponse("No audio data received")

def compare_texts(transcribed_text, answer):
    def normalize_text(text):
        text = text.lower()
        text = text.translate(str.maketrans("", "", string.punctuation))
        return text

    transcribed_text = normalize_text(transcribed_text)
    answer = normalize_text(answer)
    
    transcribed_words = set(transcribed_text.split())
    answer_words = set(answer.split())
    
    missing_words = answer_words - transcribed_words
    correct_words = answer_words & transcribed_words
    score = len(correct_words) / len(answer_words) * 100
    return ", ".join(missing_words), round(score, 2)

def recording(request, assignment_id, question_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    question = get_object_or_404(QuestionAnswer, id=question_id)
    
    return render(request, "transcription/recording.html", {"assignment": assignment, "question": question})

def flashcard_sets(request):
    flashcard_sets = FlashcardSet.objects.all()
    return render(request, 'transcription/flashcard_sets.html', {'flashcard_sets': flashcard_sets})

def flashcards(request, set_id):
    flashcard_set = get_object_or_404(FlashcardSet, id=set_id)
    flashcards = flashcard_set.flashcards.all()
    current_flashcard = flashcards.first() if flashcards else None
    return render(request, 'transcription/flashcards.html', {
        'flashcard_set': flashcard_set,
        'flashcards': flashcards,
        'flashcard': current_flashcard,
    })

def check_pronunciation(request):
    if request.method == "POST":
        audio_data = request.POST.get("audio_data", "")
        flashcard_id = request.POST.get("flashcard_id", "")

        if not flashcard_id.isdigit():
            return HttpResponse("Error: Invalid ID format")
        
        flashcard_id = int(flashcard_id)

        try:
            if audio_data:
                # Decode audio data and save it as a WAV file
                audio_bytes = base64.b64decode(audio_data)
                with open("temp_audio.wav", "wb") as f:
                    f.write(audio_bytes)

                # Load the Whisper model
                model = whisper.load_model("medium")

                # Transcribe the audio with language set to French
                result = model.transcribe("temp_audio.wav", language="fr")
                transcribed_text = result["text"]

                # Retrieve the flashcard and reference text
                flashcard = get_object_or_404(Flashcard, id=flashcard_id)
                correct_text = flashcard.french_word

                # Compare the transcribed text with the reference text
                missing_words, score = compare_texts(transcribed_text, correct_text)

                # Pass the transcribed text, answer, and score to the result page
                return render(request, 'transcription/result.html', {
                    'transcribed_text': transcribed_text,
                    'answer': correct_text,
                    'score': score,
                    'flashcard': flashcard,
                })
            else:
                return HttpResponse("Error: Invalid audio data format")
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")
    return HttpResponse("No audio data received")