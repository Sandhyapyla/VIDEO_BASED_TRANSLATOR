import os
from gtts import gTTS
from googletrans import Translator, LANGUAGES
import moviepy.editor as mp
import speech_recognition as sr
from IPython.display import Audio

def extract_audio(video_path, audio_path):
    """Extract audio from the video file."""
    try:
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
        video.close()
        print("Audio extracted successfully.")
    except Exception as e:
        print(f"Error extracting audio: {e}")

def detect_gender(audio_path):
    """Detect the gender of the speaker in the audio file."""
    return 'male'  # Placeholder for actual detection logic

def create_audio(text, lang_code, filename, gender):
    """Generate audio from text using gTTS."""
    try:
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save(filename)
        print(f"Audio created: {filename}")
    except Exception as e:
        print(f"Error creating audio: {e}")

def translate_audio(audio_path, lang_code):
    """Translate the audio file to the requested language."""
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            print(f"Extracted text: {text}")
        
        translator = Translator()
        translated_text = translator.translate(text, dest=lang_code).text
        print(f"Translated text: {translated_text}")
        return translated_text
    except Exception as e:
        print(f"Error translating audio: {e}")
        return None

def lip_sync_effect(video_path, audio_path, output_path):
    """Combine the original video with new audio, adjusting for duration."""
    try:
        video = mp.VideoFileClip(video_path)
        audio = mp.AudioFileClip(audio_path)

        video_duration = audio.duration
        video = video.subclip(0, video_duration)

        final_video = video.set_audio(audio)
        final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')
        print(f"Video with new audio created: {output_path}")
    except Exception as e:
        print(f"Error combining video and audio: {e}")

def main():
    video_path = r"C:\Users\SANDHYA RANI.P\Downloads\When you fall, rise stronger 💪🌟.mp4"
    audio_path = os.path.join(os.getcwd(), "extracted_audio.wav")
    output_audio_path = os.path.join(os.getcwd(), "translated_audio.mp3")
    output_video_path = os.path.join(os.getcwd(), r"C:\Users\SANDHYA RANI.P\Videos\output_video.mp4")

    # Extract audio from the video
    extract_audio(video_path, audio_path)

    if not os.path.exists(audio_path):
        print(f"Audio extraction failed. File {audio_path} not found.")
        return

    gender = detect_gender(audio_path)

    print("Available languages:")
    for code, lang in LANGUAGES.items():
        print(f"{code}: {lang}")

    lang_code = input("Please select a language code from the list above: ").strip()

    if lang_code not in LANGUAGES:
        print("Invalid language code selected.")
        return

    translated_text = translate_audio(audio_path, lang_code)

    if translated_text:
        create_audio(translated_text, lang_code, output_audio_path, gender)

        if not os.path.exists(output_audio_path):
            print(f"Failed to create translated audio. File {output_audio_path} not found.")
            return

        # Show the translated audio in the notebook
        display(Audio(output_audio_path))

        # Combine the original video with the new audio
        lip_sync_effect(video_path, output_audio_path, output_video_path)

if __name__ == "__main__":
    main()
