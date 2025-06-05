from flask import Flask, render_template, request, session
from flask_session import Session  # Add Flask-Session
from dotenv import load_dotenv
import os
import openai
import json
from datetime import timedelta

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

# Session configuration
app.secret_key = 'dev'  # Change this to a real secret key in production
app.config['DEBUG'] = True
app.config['SESSION_PERMANENT'] = True
app.permanent_session_lifetime = timedelta(days=30)

# Configure Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = 'flask_session'  # Directory to store session files
Session(app)

load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
openai_api_key = os.environ.get("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai_api_key)

def translate_input_phrases(input_text):
    english_phrases = input_text.splitlines()
    languages = ['spanish', 'german', 'french', 'japanese']
    translations_table = []

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
            row_of_translations.append(translation)
        print(row_of_translations)
        # (4) Add the row of translations to the translations_table
        translations_table.append(row_of_translations)


    # Make the first column the english phrases
    for i in range(len(translations_table)):
        translations_table[i].insert(0, english_phrases[i])
    # Add english as the header of the first column
    languages.insert(0, 'english')
        
    return translations_table, languages
"""
Multiple calls seems to take a long time.
But how can the global cache be done with a single call? By using the metadata schema maybe..?
Though the idea might be that a nice table will be built after a while :)
This is good for now.
"""

@app.route('/')
def input():
    # Get saved input from session, or empty string if none exists
    saved_input = session.get('input_text', '')
    return render_template('input.html', saved_input=saved_input)

@app.route('/table', methods=['GET', 'POST'])
def table():
    if request.method == 'POST':
        # If POST, process the new translation
        input_text = request.form.get('input_text', '')
        translations, languages = translate_input_phrases(input_text)
        # Update session with new data
        session['translations'] = translations
        session['languages'] = languages
        session['input_text'] = input_text
    else:
        # If GET, load from session
        translations = session.get('translations', [])
        languages = session.get('languages', ['english'])
    
    return render_template('table.html', languages=languages, rows=translations)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
