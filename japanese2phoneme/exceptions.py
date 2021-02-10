class UnidentifiedJapaneseText(Exception):

    def __init__(self, sentence, word):
        super(UnidentifiedJapaneseText, self).__init__()
        self.sentence = sentence
        self.word = word

    def __str__(self):
        return (u"No match in dictionary for word '%s' in sentence: \n'%s'" %
                (self.word, self.sentence))


class ChunkingError(Exception):

    """Raised when a katakana string cannot be parsed correctly

    """

    def __init__(self, txt):
        super(ChunkingError, self).__init__()
        self.textStr = txt

    def __str__(self):
        return u"Chunking error for string: \n %s" % self.textStr


class EmptyStrError(Exception):

    def __str__(self):
        return "Empty string passed in"


class NonKatakanaError(Exception):

    def __init__(self, char, utterance):
        super(NonKatakanaError, self).__init__()
        self.char = char
        self.utterance = utterance

    def __str__(self):
        return (u"Wrongly interpreted character '%s' as kana in utterance:\n%s"
                % (self.char, self.utterance))
