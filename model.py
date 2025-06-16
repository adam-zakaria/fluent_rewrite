from flask import session
import openai
import os
import json
from dotenv import load_dotenv
from google.cloud import texttospeech
import helpers

class TranslationCell:
    def __init__(self, language, phrase, audio_path='', video_path='', audio_key=None):
        self.language = language
        self.phrase = phrase
        self.audio_path = audio_path
        self.video_path = video_path
        self.audio_key = audio_key

    def __str__(self):
        return self.phrase

class TranslationRow(list):
    def __init__(self):
        super().__init__()


    def __str__(self):
        return '[' + ', '.join(str(cell) for cell in self) + ']'

    def prepend(self, cell):
        self.insert(0, cell)

    def to_dict(self):
        return {
            'language': self.language,
            'phrase': self.phrase,
            'audio_path': self.audio_path,
            'video_path': self.video_path,
            'audio_key': self.audio_key
        }

class TranslationTable:
    def __init__(self, input_text=None):
        self.rows = []
        self.languages = []
        if input_text:
            self.create_translation_table(input_text)
    
    def __str__(self):
        return '\n'.join(str(row) for row in self.rows)

    def create_translation_table(self, input_text):
        english_phrases = input_text.splitlines()
        languages = ['spanish', 'french', 'japanese']
        
        # Add languages
        for language in languages:
            self.add_language(language)
        self.add_language('english')
        
        # Translate phrases
        for english_phrase in english_phrases:
            row = TranslationRow()
            for language in languages:
                translation = helpers.translate_phrase(english_phrase, language)
                row.append(TranslationCell(language, translation))
            
            row.prepend(TranslationCell('english', english_phrase))
            self.add_translation_row(row)

        self._generate_audio_for_all_rows()
        return self

    def add_language(self, language):
        if language not in self.languages:
            self.languages.append(language)

    def get_table(self):
        return [row.to_dict() for row in self.rows]

    def get_translation_row(self, index):
        if 0 <= index < len(self.rows):
            return self.rows[index].to_dict()
        return None

    def update_translation_row(self, row_number, form_data):
        """
        Updates a translation row in both the session and database
        """
        # Update the session with the new data
        self.rows[row_number] = form_data
        # Update the database with the new data
        # TODO: Implement database update when database is added
        return self.rows[row_number]

    def add_translation_row(self, row):
        self.rows.append(row)

    def prepend_cell(self, cell):
        self.rows.insert(0, cell)

    def clear_table(self):
        self.rows = []

    def update_translation_row(self, row_number, phrases):
        """
        Updates a translation row with new data
        """
        self.rows[row_number] = [TranslationCell(language, phrase) for language, phrase in zip(self.languages, phrases)]
        session['rows'] = self.rows
        """
        updated_cells = []
        for i, (language, phrase) in enumerate(zip(self.languages, phrases)):
            cell = self.rows[row_number][i]
            cell.phrase = phrase
            updated_cells.append(cell)
        self.rows[row_number] = updated_cells
        return self.rows[row_number]
        """

    def rows(self):
        return self.rows

    def _generate_audio_for_all_rows(self):
        for row in self.rows:
            for cell in row:
                cell.audio_key = helpers.text_to_speech(cell.phrase, cell.language)

        # Debug print
        for row in self.rows:
            for cell in row:
                print(cell)