from flask import Flask, render_template, request, session, send_file, jsonify, redirect, url_for
from flask_session import Session  # Add Flask-Session
from dotenv import load_dotenv
import os
import json
from datetime import timedelta
import model
import helpers

load_dotenv()
app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')
# Session configuration
#app.secret_key = 'dev'  # Change this to a real secret key in production
#app.config['DEBUG'] = True
app.config['SESSION_PERMANENT'] = True
app.permanent_session_lifetime = timedelta(days=30)
# Configure Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = 'flask_session'  # Directory to store session files
app.config['SERVER_NAME'] = 'fluent.monster'

Session(app)

@app.context_processor
def inject_env():
    """Inject environment variables into all templates"""
    return dict(api_host=os.getenv('API_HOST'),
                debug=os.getenv('DEBUG'),
                port=os.getenv('PORT'),
                host=os.getenv('HOST'))

@app.before_request
def set_session_defaults():
    session.setdefault('table', None)
    session.setdefault('input_text', '')

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
        # From /input - Translate and update session, then render
        input_text = request.form.get('input_text', '')
        # If table doesn't exist, create it, otherwise update it
        if session['table'] is None:
            session['table'] = model.TranslationTable(input_text)
        else:
            session['table'].update_table(input_text)
        session['input_text'] = input_text

    # From anywhere else, just render from session
    return render_template('table.html', languages=session['table'].languages, rows=session['table'].rows)

@app.route('/edit_row/<int:row_number>', methods=['GET'])
def edit_row(row_number):
    """
    Returns the edit view for a row
    """
    row = session['table'].rows[row_number]
    return render_template('edit.html', row=row, row_number=row_number)

@app.route('/login', methods=['GET'])
def login():
    """
    Returns the login view
    """
    return render_template('login.html')

@app.route('/register', methods=['GET'])
def register():
    """
    Returns the register view
    """
    return render_template('register.html')

@app.route('/api/audio', methods=['GET'])
def audio():
    """
    Returns a zip of all the audio files where the filename is the <phrase>.mp3
    """
    return send_file(helpers.create_audio_zip(), mimetype='application/zip')

@app.route('/api/edit_row/<int:row_number>', methods=['POST'])
def edit_row_db(row_number):
    """
    Updates a translation row and returns the updated table view
    """
    table = session['table']
    row_updated = table.update_translation_row(row_number, [phrase for phrase in request.form.values()])

    return redirect(url_for('table', _external=True))

@app.route('/api/clear_data', methods=['POST'])
def clear_data():
    """
    Clears the data from the session
    """
    session.clear()
    return redirect(url_for('input', _external=True))

if __name__ == '__main__':
    app.run(debug=True, host=os.getenv('HOST'), port=os.getenv('PORT'))
