import itertools
import time


def count_anagrams(text: str, word: str):
    if not text or not word:
        return 0
    word_len = len(word)

    anagrams = set(''.join(p) for p in itertools.permutations(word))
    text_permutations = [text[i:i + word_len] for i in range(len(text))]

    count = 0
    for anagram in anagrams:
        count += text_permutations.count(anagram)
    return count
