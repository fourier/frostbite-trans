import logging
import hashlib
import sqlite3

# Local imports
import evnt


class TranslationService(object):
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
        return "Перевод: " + text
