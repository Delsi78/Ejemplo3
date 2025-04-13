import os
from pydub import AudioSegment
import speech_recognition as sr

def aac_to_text(audio_path):
    # Convertir archivo .aac a .wav (SpeechRecognition funciona mejor con .wav)
    wav_path = "temp.wav"
    audio = AudioSegment.from_file(audio_path, format="aac")
    audio.export(wav_path, format="wav")

    # Inicializar el reconocedor
    recognizer = sr.Recognizer()

    with sr.AudioFile(wav_path) as source:
        print("Cargando audio...")
        audio_data = recognizer.record(source)

    try:
        # Usar la API de Google para transcripción
        text = recognizer.recognize_google(audio_data, language="es-PE")  # puedes cambiar "es-PE" por tu región
        print("Transcripción:")
        print(text)
        return text
    except sr.UnknownValueError:
        print("No se pudo entender el audio.")
    except sr.RequestError as e:
        print(f"Error al solicitar resultados desde el servicio de Google: {e}")
    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)

# Ejemplo de uso
aac_file = "tu_archivo.aac"  # Reemplaza con el nombre de tu archivo .aac
aac_to_text(aac_file)
