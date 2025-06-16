import openai
import os
import json
from dotenv import load_dotenv
from io import BytesIO
import zipfile
from utils import utils
from google.cloud import texttospeech

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
openai_api_key = os.environ.get("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai_api_key)

def translate_phrase(phrase, language):
    print(f'Translating phrase: {phrase} to {language}')
    user_message = {
        'phrase': phrase,
        'language': language
    }

    output = client.chat.completions.create(
        model="gpt-4o-2024-11-20",
        messages=[
            {"role": "system", "content": open(os.path.join(os.path.dirname(__file__), 'system_prompts/translate_one.txt'), 'r').read()},
            {"role": "user", "content": json.dumps(user_message)},
        ],
    )
    return output.choices[0].message.content

def create_audio_zip():
    # Create zip file in memory
    memory_zip = BytesIO()
    with zipfile.ZipFile(memory_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        audio_dir = os.path.join(os.path.dirname(__file__), 'audio')
        for file in utils.ls(audio_dir):
            file_path = os.path.join(audio_dir, file)
            zf.write(file_path, arcname=utils.basename(file))
    
    # Get the content and return a new BytesIO
    memory_zip.seek(0)
    return BytesIO(memory_zip.getvalue())

def text_to_speech(text, language):
    language_map = {
        'english': 'en-US',
        'spanish': 'es-ES',
        'mandarin': 'cmn-CN',
        'japanese': 'ja-JP',
        'russian': 'ru-RU',
        'hindi': 'hi-IN',
        'arabic': 'ar-XA',
        'portuguese (br)': 'pt-BR',
        'french': 'fr-FR',
        'bengali': 'bn-BD',
        'urdu': 'ur-PK',
        'indonesian': 'id-ID',
        'german': 'de-DE',
        'thai': 'th-TH'
    }

    language_code = language_map[language]

    try:
        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = texttospeech.TextToSpeechClient().synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Save the audio content to a file
        # Don't NEED to save locally, but will for now
        # Could just send the audio content
        with open(os.path.join(os.path.dirname(__file__), 'audio', f'{text}.mp3'), 'wb') as out:
            out.write(response.audio_content)

        return text

    except Exception as e:
        print(f'Error: {e}')
        return None
