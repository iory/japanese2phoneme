def normalize_japanese_text(line: str) -> str:
    for char in [u"（", u"）", u" ", u"．", u"？", u"「", u"」",
                 u"［", u"］", u"＠Ｗ", u"＠Ｓ", u"＜", u"＞", u" ", u"。"]:
        line = line.replace(char, "")

    for char in [u"・", u"·"]:
        line = line.replace(char, " ")

    line = line.strip()
    return line
