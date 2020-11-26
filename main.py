from hashlib import md5
from collections import Counter
from itertools import permutations, combinations

import threading


def test_easy_secret(phrase):
    hashed_phrase = hash(phrase) 
    return hashed_phrase == "e4820b45d2277f3844eac66c903e84be"


def test_medium_secret(phrase):
    hashed_phrase = hash(phrase) 
    return hashed_phrase == "23170acc097c24edb98fc5488ab033fe"


def test_hard_secret(phrase):
    hashed_phrase = hash(phrase) 
    return hashed_phrase == "665e5bcb0c20062fe8abaaf4628bb154"


def hash(phrase):
    return md5(phrase.encode()).hexdigest()


def read_words(path):
    return (line.rstrip("\n") for line in open(path))


def is_valid_word(valid_chars, word):
    if "'" in word or len(word) < 2:
        return False
    valid_chars = list(valid_chars)
    for char in list(word):
        if char not in valid_chars:
            return False
        valid_chars.remove(char)

    return True


def is_character_count_fine(tested, searched):
    tested_counter = Counter(tested)
    searched_counter = Counter(searched)

    for char, count in searched_counter.items():
        if tested_counter[char] > count:
            return False

    return True


def get_valid_words(valid_chars, words_path):
    return (word for word in read_words(words_path) if is_valid_word(valid_chars, word))


def find_permutation(words, perm_lenght, req_length, anagram):
    for perm in combinations(words, perm_lenght):
        if len("".join(perm)) == req_length:
            yield perm


def find_secret(words, perm_length, secret_len, anagram, secrets):
    print(f"Anagram search of lenght {perm_length} started!")

    for comb in find_permutation(words, perm_length, secret_len, anagram):
        if is_character_count_fine("".join(comb), anagram):
            for perm in permutations(comb):
                secret = " ".join(perm)
                if test_easy_secret(secret):
                    print(f"Easy secret found --> {secret}")
                    secrets["easy"] = secret
                if test_medium_secret(secret):
                    print(f"Medium secret found --> {secret}")
                    secrets["medium"] = secret
                if test_hard_secret(secret):
                    print(f"Hard secret found --> {secret}")
                    secrets["hard"] = secret
            
                if len(secrets) == 1:
                    break
        if len(secrets) == 1:
            break

    print(f"Checking permutation of length {perm_length} completed!")


if __name__ == "__main__":
    max_length = 4
    anagram = "poultry outwits ants".replace(" ", "")
    anagram_length = len(anagram)
    secrets = {}
    threads = []
    
    valid_chars = sorted(anagram)
    valid_words_list = sorted(
        get_valid_words(valid_chars, "wordlist"),
        key=len
    )

    for i in range(1, max_length + 1):
        threads.append(
            threading.Thread(target=find_secret, args=(valid_words_list, i, anagram_length, anagram, secrets))
        )
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    print("Search complete. Following secrets found:")
    for key, value in secrets.items():
        print(f"{key} --> {value}")

