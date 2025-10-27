#---------------------------------------------
# Dateiname: ExtractiveSummarizerTest.py
# Do some Tests
# Autor: Alex Stiller
# Letzte Änderung: 14.10.2025
#---------------------------------------------

from nltk.stem import PorterStemmer
from ExtractiveSummarizer import ExtractiveSummarizer

class ExtractiveStemmingSummarizer(ExtractiveSummarizer):
    def __init__(self):
        ExtractiveSummarizer.__init__(self)
        self.stemmer = PorterStemmer()
        
    def _convertWord(self, word):
        '''Überladene Funktion um alle Worte zusätzlich auf ihren Grundstamm zu setzen'''
        # Jedes Wort wird auf seine Grundversion zurück gesetzt
        return self.stemmer.stem(word.casefold())
    
def loadText(path):
    '''Läd einen Text aus einer File zum bearbeiten'''
    try:
        with open(path) as file:
            return file.read()
    except Exception as e:
        print(f"Fehler beim Laden der Datei: {e}")
   
if __name__ == "__main__":
    language = "english"
    originalText = loadText("Data/ClimateScienceText.txt")
    originalText = None    
    converter = ExtractiveSummarizer()
    converter.prepareForTextGeneration(originalText, language)
    print(converter.createExtractivText(0.2))
    
    example_string = """Muad'Dib learned rapidly because his first training was in how to learn.
    And the first lesson of all was the basic trust that he could learn.
    It's shocking to find how many people do not believe they can learn,
    and how many more believe learning to be difficult."""

