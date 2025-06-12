from flask import Flask, render_template, request, session, send_file, jsonify
from flask_session import Session  # Add Flask-Session
from dotenv import load_dotenv
import os
import json
from datetime import timedelta
import logic 

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


@app.route('/')
def input():
    """
    Returns the input view
    """
    # Get saved input from session, or empty string if none exists
    saved_input = session.get('input_text', '')
    return render_template('input.html', saved_input=saved_input)

@app.route('/table', methods=['GET', 'POST'])
def table():
    """
    Returns the table view
    Basically just calls logic.create_translation_table with the input text (the phrases to translate)
    """
    if request.method == 'POST':
        # If POST, process the new translation
        input_text = request.form.get('input_text', '')
        table = logic.create_translation_table(input_text)
        # Update session with new data
        session['translations'] = table.rows
        session['languages'] = table.languages
        session['input_text'] = input_text
    else:
        # If GET, load from session
        translations = session.get('translations', [])
        languages = session.get('languages', ['english'])
    
    return render_template('table.html', languages=table.languages, rows=table.rows)

@app.route('/api/audio', methods=['GET'])
def audio():
    """
    Returns a zip of all the audio files where the filename is the <phrase>.mp3
    """
    return send_file(logic.create_audio_zip(), mimetype='application/zip')

"""
@app.route('/text_to_speech', methods=['POST'])
def tts():
    text = 'hello'
    language = 'english'
    file_path, file_name = logic.text_to_speech(text, language)
    print(f'file_path: {file_path}, file_name: {file_name}')
    return send_file(file_path, mimetype='audio/mpeg', as_attachment=True, download_name=file_name)
"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
