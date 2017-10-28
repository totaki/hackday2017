import nltk
from nltk.tokenize import PunktSentenceTokenizer
import pymorphy2
import string
import re

from processing.utils import load_stopwords


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
        tokens = nltk.word_tokenize(text)
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
        if not isinstance(tokens, (list, tuple)):
            raise ValueError
        result = []
        morph = pymorphy2.MorphAnalyzer()
        for token in tokens:
            parsed = morph.parse(token)[0]
            if hasattr(parsed, 'normal_form'):
                result.append(parsed.normal_form)
        return result


class POSTagger(BaseProcessor):

    @staticmethod
    def process(tokens):
        if not isinstance(tokens, (list, tuple)):
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


class PunctuationCleaner(BaseProcessor):
    @staticmethod
    def process(text):
        punctuation_table = str.maketrans("", "", string.punctuation)
        text = text.translate(punctuation_table).lower()
        return text


class EmojiCleaner(BaseProcessor):
    @staticmethod
    def process(text):
        try:
            # UCS-4
            patt = re.compile('[U00010000-U0010ffff]', re.UNICODE)
        except re.error:
            # UCS-2
            patt = re.compile('[uD800-uDBFF][uDC00-uDFFF]', re.UNICODE)
        return patt.sub('', text)


class StopwordsCleaner(BaseProcessor):

    @staticmethod
    def process(text):
        stop_words = load_stopwords()
        words = []
        for word in re.split(r'[,:;!?*()+ ]', text):
            if word:
                cleaned_word = AlphabetCleaner.process(word).strip()
                if cleaned_word and (cleaned_word not in stop_words):
                    words.append(cleaned_word)
        return ' '.join(words)


class LinksCleaner(BaseProcessor):

    @staticmethod
    def process(text):
        return re.sub('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', '', text)


class IndentsCleaner(BaseProcessor):

    @staticmethod
    def process(text):
        result = re.sub(r'[\n\t\r]', ' ', text)
        return result


class AlphabetCleaner(BaseProcessor):

    @staticmethod
    def process(text):
        letters = u'а-яА-ЯёЁa-zA-Z'
        text = re.sub('[^{}]'.format(letters), ' ', text)
        return text


class StemmingProcessor:

    @staticmethod
    def process(text):
        stemmer = nltk.SnowballStemmer('russian')
        return ' '.join([stemmer.stem(w) for w in text.split() if len(w) > 1])


class CharsReplaceProcessor(BaseProcessor):

    @staticmethod
    def process(text):
        text = re.sub('ё', 'е', text)
        return re.sub('Ё', 'Е', text)


class LowerCaseProcessor(BaseProcessor):

    @staticmethod
    def process(text):
        return text.lower()


if __name__ == '__main__':
    text = "qqq Ёё  Тестовое   предложение номер" \
           " один. Я проверяю          процессинг! Тут смайл 🏀. И ссылка http://kk.com"
    print(AlphabetCleaner.process(text))
    print(StemmingProcessor.process(text))
    print(CharsReplaceProcessor.process(text))
    print(IndentsCleaner.process(text))
    print(EmojiCleaner.process(text))
    print(LinksCleaner.process(text))
    print(LowerCaseProcessor.process(text))
    tokens = WordTokenizer.process(text)
    print(tokens)
    print(Lemmatizer.process(tokens))
    print(POSTagger.process(tokens))
