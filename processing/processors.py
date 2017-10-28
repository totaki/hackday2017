import nltk
from nltk.tokenize import PunktSentenceTokenizer
import pymorphy2
import string
import re

from processing.utils import load_stopwords, get_text


class BaseProcessor:
    @staticmethod
    def process(text_object):
        raise NotImplementedError


class WordTokenizer(BaseProcessor):
    """
    Returns list of words tokens
    """
    @staticmethod
    def process(text_object):
        text = get_text(text_object)
        tokens = nltk.word_tokenize(text)
        text_object.update({'word_tokens': tokens})
        return text_object


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
    def process(text_object):
        if not text_object.get('word_tokens'):
            tokens = WordTokenizer.process(text_object)['word_tokens']
        result = []
        morph = pymorphy2.MorphAnalyzer()
        for token in tokens:
            parsed = morph.parse(token)[0]
            if hasattr(parsed, 'normal_form'):
                result.append(parsed.normal_form)
        text_object.update({'lemm_text': ' '.join(result)})
        return text_object


class POSTagger(BaseProcessor):

    @staticmethod
    def process(text_object):
        if not text_object.get('word_tokens'):
            tokens = WordTokenizer.process(text_object)['word_tokens']
        result = []
        morph = pymorphy2.MorphAnalyzer()
        for token in tokens:
            parsed = morph.parse(token)[0]
            data = {
                'word': token,
                'POS': parsed.tag.POS
            }
            result.append(data)
        text_object.update({'pos': result})
        return text_object


class PunctuationCleaner(BaseProcessor):
    @staticmethod
    def process(text_object):
        text = get_text(text_object)
        punctuation_table = str.maketrans("", "", string.punctuation)
        text = text.translate(punctuation_table).lower()
        text_object.update({'prep_text': text})
        return text_object


class EmojiCleaner(BaseProcessor):
    @staticmethod
    def process(text_object):
        text = get_text(text_object)
        try:
            patt = re.compile('[U00010000-U0010ffff]', re.UNICODE)
        except re.error:
            patt = re.compile('[uD800-uDBFF][uDC00-uDFFF]', re.UNICODE)
        text_object.update({'prep_text': patt.sub('', text)})
        return text_object


class StopwordsCleaner(BaseProcessor):
    @staticmethod
    def process(text_object):
        text = get_text(text_object)
        stop_words = load_stopwords()
        words = []
        for word in re.split(r'[,:;!?*()+ ]', text):
            if word:
                cleaned_word = AlphabetCleaner.process(word).strip()
                if cleaned_word and (cleaned_word not in stop_words):
                    words.append(cleaned_word)
        text_object.update({'prep_text': text})
        return text_object


class LinksCleaner(BaseProcessor):

    @staticmethod
    def process(text_object):
        text = get_text(text_object)
        text_object.update(
            {'prep_text': re.sub('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', '', text)}
        )
        return text_object


class IndentsCleaner(BaseProcessor):
    @staticmethod
    def process(text_object):
        text = get_text(text_object)
        text_object.update({'prep_text':  re.sub(r'[\n\t\r]', ' ', text)})
        return text_object


class AlphabetCleaner(BaseProcessor):
    @staticmethod
    def process(text_object):
        text = get_text(text_object)
        letters = u'а-яА-ЯёЁa-zA-Z'
        text = re.sub('[^{}]'.format(letters), ' ', text)
        text_object.update({'prep_text': text})
        return text_object


class StemmingProcessor:
    @staticmethod
    def process(text_object):
        stemmer = nltk.SnowballStemmer('russian')
        text = get_text(text_object)
        text_object.update(
            {'prep_text': ' '.join([stemmer.stem(w) for w in text.split() if len(w) > 1])}
        )
        return text_object


class CharsReplaceProcessor(BaseProcessor):
    @staticmethod
    def process(text_object):
        text = get_text(text_object)
        text = re.sub('ё', 'е', text)
        text_object.update({'prep_text': re.sub('Ё', 'Е', text)})
        return text_object


class LowerCaseProcessor(BaseProcessor):
    @staticmethod
    def process(text_object):
        text = get_text(text_object)
        text_object.update({'prep_text': text.lower()})
        return text_object


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
