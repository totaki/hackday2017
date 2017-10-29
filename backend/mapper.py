from processing.named_entities import NamedEntitiesExtractor
from processing.speller import Speller
from processing.processors import *

mapper = {
    'speller': Speller(),
    "named_entities": NamedEntitiesExtractor(),
    "word_tokenizer": WordTokenizer,
    "sentence_tokenizer": SentenceTokenizer,
    "lemmatizer": Lemmatizer,
    "pos_tagger": POSTagger,
    "punctuation_cleaner": PunctuationCleaner,
    "emoji_cleaner": EmojiCleaner,
    "stopwords_cleaner": StopwordsCleaner,
    "links_cleaner": LinksCleaner,
    "indents_cleaner": IndentsCleaner,
    "alphabet_cleaner": AlphabetCleaner,
    "stemming": StemmingProcessor,
    "chars_replace": CharsReplaceProcessor,
    "lowercase": LowerCaseProcessor,
    "syntax_tagger": SyntaxTagger(),
}