import re


def split_sentences(text):

    sentences = re.split(
        r'[.!?]+',
        text
    )

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    return sentences