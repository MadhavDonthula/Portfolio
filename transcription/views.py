import base64
import whisper
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Transcription, ReferenceText


def record_audio(request):
    return render(request, 'transcription/record_audio.html')


def set_reference_text(request):
    if request.method == 'POST':
        text = request.POST['reference_text']
        ReferenceText.objects.create(text=text)
        return redirect('index')
    return render(request, 'transcription/set_reference_text.html')


def save_audio(request):
    if request.method == 'POST':
        audio_data = request.POST.get('audio_data', '')

        # Debugging: Print the audio_data
        print("Received audio_data:", audio_data[:100])  # Print the first 100 characters to avoid too much output

        try:
            # Check if audio_data contains the expected base64 format
            if "," in audio_data:
                audio_data = audio_data.split(",")[1]
                audio_bytes = base64.b64decode(audio_data)

                # Save the audio file temporarily
                with open("temp_audio.webm", "wb") as f:
                    f.write(audio_bytes)

                # Use whisper to transcribe the audio
                model = whisper.load_model("base")
                result = model.transcribe("temp_audio.webm")
                transcribed_text = result["text"]
                print("Transcribed text:", transcribed_text)

                # Retrieve the reference text
                reference_text_instance = ReferenceText.objects.first()
                if reference_text_instance:
                    reference_text = reference_text_instance.text
                else:
                    reference_text = "No reference text set."

                # Compare transcribed text with reference text (implement comparison logic)
                # ...

                return HttpResponse(f"Transcribed Text: {transcribed_text}\nReference Text: {reference_text}")
            else:
                return HttpResponse("Error: Invalid audio data format")
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")
    return HttpResponse("No audio data received")
