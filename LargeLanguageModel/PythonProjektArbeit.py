#---------------------------------------------
# Dateiname: PythonProjektArbeit.py
# Load a file and call the class to create the extractive summary
# Autor: Alex Stiller
# Letzte Änderung: 14.10.2025
#---------------------------------------------

from ExtractiveSummarizer import ExtractiveSummarizer
    
def loadText(path):
    '''Load a text from a file and return a string'''
    try:
        with open(path) as file:
            return file.read()
    except Exception as e:
        print(f"Failed to load file: {e}")
        return None
   
if __name__ == "__main__":
    language = "english"
    path = "Data/ClimateScienceText.txt"
    originalText = loadText(path)
    
    # create a ExtractiveSummarizer object and print the summariezed text
    converter = ExtractiveSummarizer()
    converter.prepareForTextGeneration(originalText, language)
    print(converter.createExtractivText(0.2))