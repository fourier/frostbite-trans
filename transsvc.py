import logging
import hashlib
import sqlite3
from google.cloud import translate
# Local imports
import evnt

class TranslationService(object):
    GOOGLE_PROJECT_ID = "clear-shadow-321318"
    GOOGLE_PROJECT_LOCATION = "global"
    
    def __init__(self, input_queue, output_queue):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.db = sqlite3.connect('trans.db')
        self.cursor = self.db.cursor()
        self.cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='translations' ''')
        # if the count is 1, then table exists
        if self.cursor.fetchone()[0] == 1:
            self.logger.debug("Found existing database")
        else:
            self.logger.debug("Create a database")
            self.db.execute('''CREATE TABLE translations (sha1 text, original text, translation text)''')
        self.db.commit()

    def start(self):
        while True:
            ev = self.input_queue.get()
            if type(ev) == evnt.RequestTranslation:
                self.logger.debug("Translation requested")
                translation = self.query_cached_translation(ev.text)
                if not translation:
                    self.logger.debug("Translation not found in database")
                    translation = self.get_translation(ev.text)
                    if not translation:
                        translation = ev.text
                    else:
                        self.store_translation(ev.text, translation)
                self.output_queue.put(evnt.SendTranslation(ev.text, translation ))
            else:
                self.logger.error("Unknown event")

    def query_cached_translation(self, text):
        sha1 = hashlib.sha1(str.encode(text)).hexdigest()
        self.cursor.execute("select translation from translations where sha1=:sha", {"sha": sha1})
        translation = self.cursor.fetchone()
        if translation:
            translation = translation[0]
        return translation

    def store_translation(self, text, translation):
        self.logger.debug("storing translation")
        sha1 = hashlib.sha1(str.encode(text)).hexdigest()
        self.cursor.execute("insert into translations values (?, ?, ?)", (sha1, text, translation))
        self.db.commit()

    def get_translation(self, text):
        """Translating Text. Based on
        https://github.com/googleapis/python-translate/blob/master/samples/snippets/translate_v3_translate_text.py"""
        try:
            project_id = TranslationService.GOOGLE_PROJECT_ID
            client = translate.TranslationServiceClient()
            location = TranslationService.GOOGLE_PROJECT_LOCATION
            parent = f"projects/{project_id}/locations/{location}"
            # Detail on supported types can be found here:
            # https://cloud.google.com/translate/docs/supported-formats
            response = client.translate_text(
                request={
                    "parent": parent,
                    "contents": [text],
                    "mime_type": "text/plain",  # mime types: text/plain, text/html
                    "source_language_code": "en-US",
                    "target_language_code": "ru",
                    }
                    )
            if len(response.translations) == 1:
                return response.translations[0].translated_text
        except:
            self.logger.error("Unable to get translation")
        return None

