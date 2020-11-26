from hashlib import md5
from collections import Counter
from itertools import permutations, combinations

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
    print(f"Permutation of length {perm_lenght}")
    for perm in combinations(words, perm_lenght):
        if len("".join(perm)) == req_length:
            yield perm


if __name__ == "__main__":
    valid_chars = sorted("poultry outwits ants".replace(" ", ""))
    valid_words_list = sorted(set(get_valid_words(valid_chars, "wordlist")), key=len)
    found = False
    max_length = 4

    done = [False, False, False]
    for i in range(max_length + 1):
        for comb in find_permutation(valid_words_list, i, 18, "poultry outwits ants"):
            if is_character_count_fine("".join(comb), "poultryoutwitsants"):
                for perm in permutations(comb):
                    secret = " ".join(perm)
                    if test_easy_secret(secret):
                        print(f"Easy secret found --> {secret}")
                        done[0] == True
                    if test_medium_secret(secret):
                        print(f"Medium secret found --> {secret}")
                        done[1] = True
                    if test_hard_secret(secret):
                        print(f"Hard secret found --> {secret}")
                        done[2] = True
            
            if done[0] and done[1] and done[2]:
                break
        if done[0] and done[1] and done[2]:
            break

    print("Finished")
