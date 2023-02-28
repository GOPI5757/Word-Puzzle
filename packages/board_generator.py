import random
from string import ascii_uppercase

orientations = [(-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def is_palindrome(word):
    for i in range(len(word)//2):
        if word[i] != word[-i-1]:
            return False
    return True


def generate(size, word_count=None):
    wordlist = open(
        r'files\words.txt').read().splitlines()
    if word_count == None or word_count > len(wordlist):
        word_count = len(wordlist)
    board = [[None]*size for _ in range(size)]
    coords = [(i, j) for i in range(size) for j in range(size)]
    added_words = {}

    k = word_count
    random.shuffle(wordlist)
    for word in wordlist:
        if k == 0:
            break
        word = word.upper()
        length = len(word)
        ox, oy = random.choice(orientations)
        try:
            x, y = random.choice(
                [(i, j) for i, j in coords if 0 <= i+length*ox < size and 0 <= j+length*oy < size and not any(board[i+d*ox][j+d*oy] for d in range(length))])

            for i in range(length):
                board[x+ox*i][y+oy*i] = word[i]

            added_words[((x, y), (x+ox*i, y+oy*i))] = word
            k -= 1
        except:
            continue

    for i, j in coords:
        if board[i][j] is None:
            board[i][j] = random.choice(ascii_uppercase)

    for x, y in coords:
        for word in list(added_words.values()):
            length = len(word)
            for ox, oy in orientations:
                if not (0 <= x+length*ox < size and 0 <= y+length*oy < size):
                    continue
                if all(board[x+d*ox][y+d*oy] == word[d] for d in range(length)):
                    added_words[((x, y), (x+ox*(length-1),
                                 y+oy*(length-1)))] = word
                    if is_palindrome(word):
                        added_words[((x+ox*(length-1),
                                     y+oy*(length-1)), (x, y))] = word

    return board, added_words
