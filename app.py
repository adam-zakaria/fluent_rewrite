from flask import Flask, render_template, request, session, send_file, jsonify, redirect, url_for
from flask_session import Session  # Add Flask-Session
from dotenv import load_dotenv
import os
import json
from datetime import timedelta
import model
import helpers

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

@app.before_request
def set_session_defaults():
    #session.setdefault('table', model.TranslationTable())
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
        session['table'] = model.create_translation_table(input_text)
        session['input_text'] = input_text

    # From anywhere else, just render from session
    return render_template('table.html', languages=table.languages, rows=table.rows)

@app.route('/edit_row/<int:row_number>', methods=['GET'])
def edit_row(row_number):
    """
    Returns the edit view for a row
    """
    row = session['rows'][row_number]
    return render_template('edit.html', row=row, row_number=row_number)

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
    print(request.form)

    table = session['table']
    row_updated = table.update_translation_row(row_number, [phrase for phrase in request.form.values()])

    if row_updated:
        session['rows'] = table.rows
        session['languages'] = table.languages
    
    return redirect(url_for('table'))

@app.route('/api/clear_data', methods=['POST'])
def clear_data():
    """
    Clears the data from the session
    """
    session.clear()
    return redirect(url_for('input'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
