import io
import os
from os.path import join

from pybsc import invert_dict


jNlp_KATAKANA_CHART_PATH = join(os.path.dirname(__file__),
                                "data", "katakanaChart.txt")
jNlp_HIRAGANA_CHART_PATH = join(os.path.dirname(__file__),
                                "data", "hiraganaChart.txt")


def parse_chart(chart_filepath):
    with io.open(chart_filepath, "r", encoding="utf-8") as fd:
        chart = fd.read()

    lines = chart.split('\n')
    chart_dict = {}
    output = {}
    col_headings = lines.pop(0).split()
    for line in lines:
        cells = line.split()
        for i, c in enumerate(cells[1:]):
            output[c] = cells[0], col_headings[i]

    for k in sorted(output.keys()):
        # @k = katakana
        # @r = first romaji in row
        # @c = concatinating romaji in column
        r, c = output[k]
        if k == 'X':
            continue
        romaji = ''.join([item.replace('X', '') for item in [r, c]])
        chart_dict[k] = romaji
    return chart_dict


def _get_katakana_to_hiragana_dict():
    ret_dict = {u"ャ": u"ゃ", u"ュ": u"ゅ", u"ョ": u"ょ", u"ッ": u"っ",
                u"ァ": u"ぁ", u"ィ": u"ぃ", u"ゥ": u"ぅ", u"ェ": u"ぇ", u"ォ": u"ぉ",
                }
    for kata in katakana_to_romaji_dict.keys():
        kana = romaji_to_hiragana_dict[katakana_to_romaji_dict[kata]]
        ret_dict[kata] = kana
    return ret_dict


katakana_to_romaji_dict = parse_chart(jNlp_KATAKANA_CHART_PATH)
hiragana_to_romaji_dict = parse_chart(jNlp_HIRAGANA_CHART_PATH)
romaji_to_katakana_dict = invert_dict(katakana_to_romaji_dict)
romaji_to_hiragana_dict = invert_dict(hiragana_to_romaji_dict)
katakan_to_hiragana_dict = _get_katakana_to_hiragana_dict()
hiragana_to_katakana_dict = invert_dict(katakan_to_hiragana_dict)


def hiragana_to_katakana(input_str: str) -> str:
    """Input hiragana and return the corresponding string in katakana

    """
    ret_str = u""
    for char in input_str:
        if char in hiragana_to_katakana_dict.keys():
            char = hiragana_to_katakana_dict[char]
        ret_str += char
    return ret_str


def katakana_to_hiragana(input_str: str) -> str:
    """Input hiragana and return the corresponding string in katakana

    """
    ret_str = u""
    for char in input_str:
        if char in katakan_to_hiragana_dict.keys():
            char = katakan_to_hiragana_dict[char]
        ret_str += char
    return ret_str
