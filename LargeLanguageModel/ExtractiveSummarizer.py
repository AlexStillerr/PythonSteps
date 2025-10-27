#---------------------------------------------
# Dateiname: ExtractiveSummarizer.py
# A class for creating extractive summaries using the Natural Language Toolkit(nltk).
# The prepareForTextGeneration method calculates the word count and sentence count based on the given text and language.
# The summariezed text is generated using createExtractivText, taking the percentage value to define how much of the original text to include
# Autor: Alex Stiller
# Letzte Änderung: 14.10.2025
#---------------------------------------------

# import function to create word and sentence tokens with nltk
from nltk.tokenize import sent_tokenize, word_tokenize
# import stopwords to get the predefined wordlist from nltk
from nltk.corpus import stopwords

class ExtractiveSummarizer:
    '''Will create a extractive summary from a given text'''
    
    def __init__(self):
        '''Constructor. Define attributes for WordCount and SentenceCount'''
        self.wordCountNormalized = {}
        self.sentenceCount = {}
       
    def _cleanupWordList(self, wordList, language):
        '''Remove all punctuation character and stopwords.
        Also call a convert method for all words to unify all word (uppercase/lowercase)'''
        # remove signs
        signsToRemove = self._getSignsToRemove()
        wordList = [word for word in wordList if word not in signsToRemove]
        # remove all stop words
        stopwordSet = set(stopwords.words(language))
        return [self._convertWord(word) for word in wordList
                if self._convertWord(word) not in stopwordSet]
    
    def _convertWord(self, word):
        '''Convert a word for caseless comparison'''
        return word.casefold()
    
    def _getSignsToRemove(self):
        '''Return a set of signs for removal'''
        return ("?",".","!",",",";",":","'","-","_")
                
    def _generateCleanedTokens(self, text, language):
        '''Generate a word token list without signs and stopwords'''
        wordTokens = word_tokenize(text)
        return self._cleanupWordList(wordTokens, language)

    def _generateNormalizedWordCount(self, wordList):
        '''Generate a normalized word to wordcount attibute'''
        # count all words
        countedWords = { word: wordList.count(word) for word in set(wordList) }
        maxAmount = max(countedWords.values())
        # normalize all word count values
        self.wordCountNormalized = { key:countedWords[key]/maxAmount for key in countedWords.keys()}

    def _calculateSentenceCount(self, sentence):
        '''Iterate through each word in the sentence and sum up the word's value'''
        wordValues = [ self.wordCountNormalized[self._convertWord(word)] for word in sentence.split()
                       if self._convertWord(word) in self.wordCountNormalized.keys() ]
        return sum(wordValues)
        
    def _generateSenctenceCount(self, text, language):
        '''Iterate through each sentence to get the sentence count and save it in an attibute'''
        sentenceList = sent_tokenize(text, language)
        for sentence in sentenceList:
            self.sentenceCount[sentence] = self._calculateSentenceCount(sentence)
    
    def prepareForTextGeneration(self, text, language):
        '''Prepate the text generation and create the WordCount and SentenceCount with the given language'''
        assert text, "Text is empty"
        
        tokens = self._generateCleanedTokens(text, language)
        self._generateNormalizedWordCount(tokens)
        self._generateSenctenceCount(text, language)
    
    def createExtractivText(self, percentage):
        '''Create the summary with  X (percentage) most valuable sentences.
        The percentage must be between 0.01 and 1'''
        assert percentage <= 1 and percentage >= 0.01, f"The percentage must be between 0.01 and 1. {percentage} is an invalid value"
        assert self.sentenceCount, "Sentence count is not set, please call prepareForTextGeneration()"
        
        # create a list of Tuple(SentenceCount, sentence) and sort them by highest sentenceCount
        valueSentenceList = [(self.sentenceCount[key],key) for key in self.sentenceCount.keys()]
        valueSentenceList.sort(reverse=True)
        
        # get the best matching 20% of the sentences
        sentenceCount = round(len(self.sentenceCount) * percentage)
        topSentences = [word for _,word in valueSentenceList[:sentenceCount]]
        
        # get the sentences in correct order from the original Text
        extractiveList = [key for key in self.sentenceCount.keys() if key in topSentences]
        return " ".join(extractiveList);