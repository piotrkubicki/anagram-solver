from hashlib import md5
from collections import Counter
from itertools import permutations, combinations, combinations_with_replacement

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


def find_combination(words, comb_lenght, req_length, anagram):
    for comb in combinations(words, comb_lenght):
        if len("".join(comb)) == req_length:
            yield comb


def find_secret(words, words_len_comb, comb_length, secret_len, anagram, secrets):

    selected_words = [word for word in words if len(word) in words_len_comb]
    print(f"Anagram search with comb {words_len_comb} started! Words count: {len(selected_words)}")

    for comb in find_combination(selected_words, comb_length, secret_len, anagram):
        if is_character_count_fine("".join(comb), anagram):
            for perm in permutations(comb):
                secret = " ".join(perm)
                if secrets.get("easy", 0) == 0 and test_easy_secret(secret):
                    print(f"Easy secret found --> {secret}")
                    secrets["easy"] = secret
                if secrets.get("medium", 0) == 0 and test_medium_secret(secret):
                    print(f"Medium secret found --> {secret}")
                    secrets["medium"] = secret
                if secrets.get("hard", 0) == 0 and test_hard_secret(secret):
                    print(f"Hard secret found --> {secret}")
                    secrets["hard"] = secret
            
                if len(secrets) == 3:
                    break
        if len(secrets) == 3:
            break

    print(f"Checking permutation for comb {words_len_comb} completed!")


def find_words_lengths(num_words, min_chars, max_chars):
    combs = [c for c in combinations_with_replacement(list(range(min_chars, max_chars - min_chars)), num_words) if sum(c) == 18]
    return combs


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

    for i in range(max_length):

        words_len_comb = find_words_lengths(i+1, 2, anagram_length)

        for comb in words_len_comb:
            threads.append(
                threading.Thread(target=find_secret, args=(valid_words_list, comb, i+1, anagram_length, anagram, secrets))
            )
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    print("Search complete. Following secrets found:")
    for key, value in secrets.items():
        print(f"{key} --> {value}")   

