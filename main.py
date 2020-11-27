from hashlib import md5
from collections import Counter, defaultdict
from itertools import permutations, combinations_with_replacement, product
from typing import List, Dict, Generator
from concurrent.futures import ThreadPoolExecutor


hashed_secrets = {
    "easy": "e4820b45d2277f3844eac66c903e84be",
    "medium": "23170acc097c24edb98fc5488ab033fe",
    "hard": "665e5bcb0c20062fe8abaaf4628bb154",
}


def get_hashed_secret(difficulty: str) -> str:
    return hashed_secrets.get(difficulty, "")


def test_secret(phrase: str, difficulty: str) -> bool:
    hashed_phrase = hash_word(phrase) 
    return hashed_phrase == get_hashed_secret(difficulty)


def hash_word(phrase: str) -> str:
    return md5(phrase.encode()).hexdigest()


def read_words(path: str) -> Generator:
    return (line.rstrip("\n") for line in open(path))


def is_valid_word(valid_chars: List[str], min_word_len: int, word: List[str]) -> bool:
    if len(word) < min_word_len:
        return False
    valid_chars = list(valid_chars)
    for char in list(word):
        if char not in valid_chars:
            return False
        valid_chars.remove(char)

    return True


def is_character_count_fine(tested: str, searched: str) -> bool:
    tested_counter = Counter(tested)
    searched_counter = Counter(searched)

    for char, count in searched_counter.items():
        if tested_counter[char] > count:
            return False

    return True


def get_valid_words(valid_chars: List[str], min_word_len: int, words_path: str) -> Generator:
    return (word for word in read_words(words_path) if is_valid_word(valid_chars, min_word_len, word))


def find_combination(words: List[str], words_len_comb: List[int]) -> List[str]:
    words_by_len = defaultdict(list)
    for word in words:
        words_by_len[len(word)].append(word)

    values = []
    for comb_len in words_len_comb:
        values.append(words_by_len[comb_len])
    for comb in product(*values):
        yield comb         


def find_words_lengths(num_words: int, min_chars: int, max_chars: int, limit: int) -> List[List[int]]:
    combs = [c for c in combinations_with_replacement(list(range(min_chars, max_chars - min_chars)), num_words) if sum(c) == limit]
    return combs


def shout_secret_found(secret: str, difficulty: str) -> None:
    print("-" * 50)
    print(f"{difficulty} secret found --> {secret}!!!")
    print("-" * 50)

def find_secret(words: List[str], words_len_comb: List[int], comb_length: int, secret_len: int, anagram: str, secrets: Dict[str, str], secrets_req: int) -> None:
    if len(secrets) == secrets_req:
        return
        
    selected_words = [word for word in words if len(word) in words_len_comb]
    print(f"Anagram search with comb {words_len_comb} started! Words count: {len(selected_words)}")
    
    for comb in find_combination(selected_words, words_len_comb):
        if is_character_count_fine("".join(comb), anagram):
            for perm in permutations(comb):
                secret = " ".join(perm)
                if secrets.get("easy", "") == "" and test_secret(secret, "easy"):
                    shout_secret_found(secret, "Easy")
                    secrets["easy"] = secret
                if secrets.get("medium", "") == "" and test_secret(secret, "medium"):
                    shout_secret_found(secret, "Medium")
                    secrets["medium"] = secret
                if secrets.get("hard", "") == "" and test_secret(secret, "hard"):
                    shout_secret_found(secret, "Hard")
                    secrets["hard"] = secret
            
                if len(secrets) == secrets_req:
                    break
        if len(secrets) == secrets_req:
            break

    print(f"Checking permutation for comb {words_len_comb} completed!")


if __name__ == "__main__":
    max_length = 4
    min_word_len = 2
    anagram = "poultry outwits ants".replace(" ", "")
    anagram_length = len(anagram)
    secrets = {}
    threads = []
    
    valid_chars = sorted(anagram)
    valid_words_list = sorted(
        get_valid_words(valid_chars, min_word_len, "wordlist"),
        key=len
    )

    with ThreadPoolExecutor(max_workers=5) as executor:
        for i in range(max_length):            

            words_len_comb = find_words_lengths(i+1, 2, anagram_length, anagram_length)

            for comb in words_len_comb:
                threads.append(
                    executor.submit(find_secret, valid_words_list, comb, i+1, anagram_length, anagram, secrets, 3)
                )

    print("-" * 50)
    print("Search complete. Following secrets found:")
    for key, value in secrets.items():
        print(f"{key} --> {value}")   
