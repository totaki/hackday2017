import nltk
from nltk.tokenize import PunktSentenceTokenizer
import pymorphy2
import string


class BaseProcessor:
    @staticmethod
    def process(text):
        raise NotImplementedError


class WordTokenizer(BaseProcessor):
    """
    Returns list of words tokens
    """
    @staticmethod
    def process(text):
        tokens = nltk.word_tokenize(quote)
        return tokens


class SentenceTokenizer(BaseProcessor):
    """
    Returns list of sentences tokens
    """
    @staticmethod
    def process(text):
        sent_tokenizer = PunktSentenceTokenizer()
        tokens = sent_tokenizer.sentences_from_text(text)
        return tokens


class Lemmatizer(BaseProcessor):

    @staticmethod
    def process(tokens):
        if isinstance(tokens, (list, tuple)):
            raise ValueError
        result = []
        morph = pymorphy2.MorphAnalyzer()
        for token in tokens:
            parsed = morph.parse(token)[0]
            data = {
                'word': token,
                'lemma': parsed.tag.normal_form
            }
            result.append(data)
        return result


class POSTagger(BaseProcessor):

    @staticmethod
    def process(tokens):
        if isinstance(tokens, (list, tuple)):
            raise ValueError
        result = []
        morph = pymorphy2.MorphAnalyzer()
        for token in tokens:
            parsed = morph.parse(token)[0]
            data = {
                'word': token,
                'POS': parsed.tag.POS
            }
            result.append(data)
        return result


class ClearPunctuationProcessor(BaseProcessor):
    @staticmethod
    def process(text):
        punctuation_table = str.maketrans("", "", string.punctuation)
        text = text.translate(punctuation_table).lower()
        return text
