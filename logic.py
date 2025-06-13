from google.cloud import texttospeech
import os
import openai
from dotenv import load_dotenv
import json
from utils import utils
import zipfile
from io import BytesIO
import model

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
openai_api_key = os.environ.get("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai_api_key)

table = model.TranslationTable()

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

def create_translation_table(input_text):
    english_phrases = input_text.splitlines()
    languages = ['spanish', 'french', 'japanese']
    
    # Clear existing table data
    table.clear_table()
    table.add_language('english')
    # rows = [] # this probably isn't needed because the rows can just be appended in the loop

    # Create a TranslationRow for each english phrase where (len(TranslationRow) == len(languages))
    # Append the row to the table
    for english_phrase in english_phrases:
        row = []
        for language in languages:
            table.add_language(language)
            user_message = {
                'phrase': english_phrase,
                'language': language
            }

            output = client.chat.completions.create(
                model="gpt-4o-2024-11-20",
                messages=[
                    {"role": "system", "content": open(os.path.join(os.path.dirname(__file__), 'system_prompts/translate_one.txt'), 'r').read()},
                    {"role": "user", "content": json.dumps(user_message)},
                ],
            )
            translation = output.choices[0].message.content
            row.append(model.TranslationCell(language, translation))

        # Prepend the english phrase to the row
        row.insert(0, model.TranslationCell('english', english_phrase))
        table.add_translation_row(row)

    # Create audio
    for row in table.rows:
        for cell in row:
            #cell['audio_key'] = text_to_speech(cell['phrase'], cell['language'])
            cell.audio_key = text_to_speech(cell.phrase, cell.language)

    # Debug print
    for row in table.rows:
        for cell in row:
            print(cell)

    return table

def update_translation_row(row_number, form_data):
    """
    Updates a translation row in both the session and database
    """
    # Update the session with the new data
    session['rows'][row_number] = form_data
    # Update the database with the new data
    # TODO: Implement database update when database is added
    return session['rows'][row_number]
