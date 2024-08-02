import base64
import io
import whisper
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Assignment

def index(request):
    assignments = Assignment.objects.all()
    return render(request, 'transcription/index.html', {'assignments': assignments})

def record_audio(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    return render(request, 'transcription/record_audio.html', {'assignment': assignment})

def save_audio(request):
    if request.method == 'POST':
        audio_data = request.POST.get('audio_data', '')
        assignment_id = request.POST.get('assignment_id', '')

        try:
            if audio_data:
                # Decode the base64 encoded data
                audio_bytes = base64.b64decode(audio_data)
                
                # Save the audio file temporarily
                with open("temp_audio.wav", "wb") as f:
                    f.write(audio_bytes)

                # Use whisper to transcribe the audio
                model = whisper.load_model("base")
                result = model.transcribe("temp_audio.wav")
                transcribed_text = result["text"]

                # Retrieve the reference text
                assignment = get_object_or_404(Assignment, id=assignment_id)
                reference_text = assignment.reference_text

                # Compare transcribed text with reference text
                missing_words = compare_texts(transcribed_text, reference_text)
                
                return HttpResponse(f"Transcribed Text: {transcribed_text}\nReference Text: {reference_text}\nMissing Words: {missing_words}")
            else:
                return HttpResponse("Error: Invalid audio data format")
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")
    return HttpResponse("No audio data received")

def compare_texts(transcribed_text, reference_text):
    transcribed_words = set(transcribed_text.lower().split())
    reference_words = set(reference_text.lower().split())
    missing_words = reference_words - transcribed_words
    return ", ".join(missing_words)
