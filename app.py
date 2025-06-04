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

@app.route('/')
def input():
    # Get saved input from session, or empty string if none exists
    saved_input = session.get('input_text', '')
    return render_template('input.html', saved_input=saved_input)

@app.route('/translate', methods=['POST'])
def translate():
    if request.method == 'POST':
        input_text = request.form.get('input_text', '')
        # Save to session
        session['input_text'] = input_text
        
        english_phrases = input_text.splitlines()
        languages = ['spanish', 'german', 'french', 'japanese']
        user_message = {
            'phrases': english_phrases,
            'languages': languages
        }
        print("Lines to translate:", english_phrases, flush=True)  # Print to console

        output = client.chat.completions.create(
            model="gpt-4o-2024-11-20",
            messages=[
                {"role": "system", "content": open(os.path.join(os.path.dirname(__file__), 'system_prompts/translate.txt'), 'r').read()},
                {"role": "user", "content": json.dumps(user_message)},
            ],
        )
        translations = json.loads(output.choices[0].message.content)
        print("Output:", translations, flush=True)  # Print to console

        # Make the first column the english phrases
        for i in range(len(translations)):
            translations[i].insert(0, english_phrases[i])
        # Add english as the header of the first column
        languages.insert(0, 'english')

        return render_template('table.html', languages=languages, rows=translations)

@app.route('/table', methods=['GET', 'POST'])
def table():
    if request.method == 'POST':
        input_text = request.form.get('input_text', '')
        rows = input_text.splitlines()
    else:
        rows = ['Row 1', 'Row 2', 'Row 3']
    return render_template('table.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
