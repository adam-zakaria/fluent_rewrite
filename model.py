class TranslationCell:
    def __init__(self, language, phrase, audio_path='', video_path='', audio_key=None):
        self.language = language
        self.phrase = phrase
        self.audio_path = audio_path
        self.video_path = video_path
        self.audio_key = audio_key

    def __str__(self):
        return self.phrase

class TranslationRow:
    def __init__(self, cells):
        self.cells = cells

    def __str__(self):
        return '[' + ', '.join(str(cell) for cell in self.cells) + ']'

    def to_dict(self):
        return {
            'language': self.language,
            'phrase': self.phrase,
            'audio_path': self.audio_path,
            'video_path': self.video_path,
            'audio_key': self.audio_key
        }

class TranslationTable:
    def __init__(self):
        self.rows = []
        self.languages = []
    
    def add_language(self, language):
        if language not in self.languages:
            self.languages.append(language)

    def __str__(self):
        return '\n'.join(str(row) for row in self.rows)

    def get_table(self):
        return [row.to_dict() for row in self.rows]

    def get_translation_row(self, index):
        if 0 <= index < len(self.rows):
            return self.rows[index].to_dict()
        return None

    def add_translation_row(self, row):
        self.rows.append(row)

    def prepend_cell(self, cell):
        self.rows.insert(0, cell)

    def clear_table(self):
        self.rows = []

    #@property
    def rows(self):
        return self.rows