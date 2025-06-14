from google.cloud import texttospeech
import os
import openai
from dotenv import load_dotenv
import json
from utils import utils
import zipfile
from io import BytesIO
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
openai_api_key = os.environ.get("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai_api_key)

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

def create_table_data(input_text):
    english_phrases = input_text.splitlines()
    languages = ['spanish', 'french', 'japanese']
    translations_table = []

    # Create translation
    # (0) For each english phrase
    for english_phrase in english_phrases:
        # (1) Create a new row of translations
        row_of_translations = []
        for language in languages:
            user_message = {
                'phrase': english_phrase,
                'language': language
            }

            # (2) For each language, get the translation
            output = client.chat.completions.create(
                model="gpt-4o-2024-11-20",
                messages=[
                    {"role": "system", "content": open(os.path.join(os.path.dirname(__file__), 'system_prompts/translate_one.txt'), 'r').read()},
                    {"role": "user", "content": json.dumps(user_message)},
                ],
            )
            translation = output.choices[0].message.content
            print(translation)
            # (3) Add the translation to the row of translations
            #row_of_translations.append(translation)
            row_of_translations.append({
                'language': language,
                'phrase': translation,
                'audio_path': f'path/to/audio/.mp3',
                'video_path': f'path/to/audio/.mp4',
            })
        #print(row_of_translations)
        # (4) Add the row of translations to the translations_table
        translations_table.append(row_of_translations)

    # Make the first column the english phrases
    for i in range(len(translations_table)):
        translations_table[i].insert(0, { # Insert phrase in first position of translation row
            'language': 'english',
            'phrase': english_phrases[i] 
        })

    # Create audio
    for row in translations_table:
        for cell in row:
            cell['audio_key'] = text_to_speech(cell['phrase'], cell['language'])

    # Add english as the header of the first column
    languages.insert(0, 'english')
        
    print(f'languages: {languages}')
    return translations_table, languages
