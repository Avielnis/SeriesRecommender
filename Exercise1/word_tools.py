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


def count_anagrams_performance():
    text = "abcdbacbacbacdbcdabcdbacbacbacdbcdabcdbacbacbacdbcd"
    word = "abcd"
    start = time.time()
    for _ in range(1000):
        count_anagrams(text, word)
    end = time.time()
    time_took_ms = (end - start) * 1000
    print(f"time took is: {time_took_ms}")


count_anagrams_performance()
