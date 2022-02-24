from typing import List

import ginza
import spacy

from japanese2phoneme.exceptions import ChunkingError
from japanese2phoneme.exceptions import EmptyStrError
from japanese2phoneme.exceptions import NonKatakanaError
from japanese2phoneme.exceptions import UnidentifiedJapaneseText
from japanese2phoneme.kana import hiragana_to_katakana
from japanese2phoneme.kana import katakana_to_romaji_dict


nlp = spacy.load('ja_ginza')


def read_japanese_sentence(target_sent: str):
    japanese_tokens_list = []
    ret_word_list = []

    katakana_list = list(katakana_to_romaji_dict.keys())
    valid_katakana_list = [u"ャ", u"ュ", u"ョ", u"ッ", u"ァ", u"ィ",
                           u"ゥ", u"ェ", u"ォ", u"ー", ] + katakana_list

    doc = nlp(target_sent)
    for chunk in doc.sents:
        tokens = []
        word_list = []
        for tok in chunk:
            tag = tok.tag_.split('-')[0]
            if u"記号" in tag:
                continue

            # Don't process empty words (can happen a lot,
            # depending on the annotation scheme)
            word = tok.text.strip()
            if word == "":
                continue

            kana = ginza.reading_form(tok, use_orth_if_none=True)

            if kana != '*':
                tokens.append(kana)
            else:
                # Map all hiragana to katakana (in what situations would a
                # hiragana word not appear in our dictionary?
                word = hiragana_to_katakana(word)

                # If the text is all katakana, keep it,
                # otherwise, assume an error
                if (all([char in valid_katakana_list for char in word])):
                    tokens.append(word)
                else:
                    raise UnidentifiedJapaneseText(target_sent, word)
            word_list.append(word)
        japanese_tokens_list.append(tokens)
        ret_word_list.append(word_list)

    return japanese_tokens_list, ret_word_list


def merge_tailing_vowel(xlst: List[str]) -> List[str]:
    """Merge tailing vowel.

    Special case - sometimes 'ー' ends up in its own word or at the start
    of a word, but really it just makes the last vowel longer.  If its
    by itself, attach it to the previous word
    """
    ret_list = []
    for word in xlst:
        if word[0] == u"ー":
            ret_list[-1] += word
        else:
            ret_list.append(word)
    return ret_list


def chunk_katakana(katakana_string: str) -> List[str]:
    """Chunks katakana for use in the katakana chart

    Examples
    --------
    >>> chunk_katakana('テスト')
    ['テ', 'ス', 'ト']
    """
    katakana_list = list(katakana_string)
    katakana_keys = list(katakana_to_romaji_dict.keys())
    chunked_katakana = []
    i = 0
    while i < len(katakana_string):
        kana = katakana_list[i]
        # Some palatalized consonants are in our chart
        # (notably 'jy' and 'shy' are missing)
        kana_flag = kana in [u"ャ", u"ュ", u"ョ"]
        if kana_flag \
                and chunked_katakana[-1] + kana in katakana_keys:
            chunked_katakana[-1] += kana
        elif kana == u'ッ':  # Geminate consonant
            pass
        else:  # Normal case
            chunked_katakana.append(kana)
        i += 1
    return chunked_katakana


def get_chunked_kana(string: str):
    if string == "":
        raise EmptyStrError()

    kana_list, word_list = read_japanese_sentence(string)
    kana_list = ["".join(subList) for subList in kana_list if len(subList) > 0]
    word_list = ["".join(subList) for subList in word_list if len(subList) > 0]

    kana_list = merge_tailing_vowel(kana_list)
    word_list = merge_tailing_vowel(word_list)

    vowel_list = [u"ア", u"イ", u"ウ", u"エ", u"オ"]
    vowel_modifier_dict = {u"ァ": u"a", u"ィ": u"i", u"ゥ": u'u',
                           u"ェ": u"e", u"ォ": u'o'}
    y_modifier_dict = {u"ャ": u"ya", u"ュ": u"yu", u"ョ": u"yo"}

    romanjied_text_list = []
    for word in kana_list:
        # Sanitize kana
        try:
            kana_input_list = chunk_katakana(word)
        except IndexError:
            raise ChunkingError(word)

        # Convert kana to romanji
        romanji_list = []
        for kana in kana_input_list:
            # Over-write the previous vowel (foreign words)
            if kana in vowel_modifier_dict.keys():
                romanji_list[-1] = (romanji_list[-1][:-1] +
                                    vowel_modifier_dict[kana])

            # Last vowel is a long vowel
            elif kana == u'ー':  # Long vowel
                # e.g. 'ホーー' becomes "ho::" or 'ふうんー' becomes "hu:n:"
                #  -- both bad
                if romanji_list[-1][-1] != ":" and romanji_list[-1][-1] != "N":
                    romanji_list[-1] += ":"

                # Should get recognized as a single vowel by the forced aligner

            # Normal case
            else:
                # Single-phone characters
                if kana == u"ン" or kana in vowel_list:
                    romanji_list.append(katakana_to_romaji_dict[kana])
                else:
                    if kana in y_modifier_dict.keys():  # e.g. 'ィ' in 'ティム'
                        romanji_list.pop(-1)
                        syllable = y_modifier_dict[kana]
                    else:
                        try:
                            # Normal case for two-phone characters
                            syllable = katakana_to_romaji_dict[kana]
                        except KeyError:
                            raise NonKatakanaError(kana, string)

                    # The consonant (e.g. 's' or 'sh')
                    romanji_list.append(syllable[:-1])
                    # The vowel
                    romanji_list.append(syllable[-1])

        romanjied_text_list.append(" ".join(romanji_list))

    return word_list, kana_list, romanjied_text_list
