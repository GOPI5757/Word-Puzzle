import random
from string import ascii_uppercase

orientations = [(-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def generate(row, col, wordlist, word_count=None):
    if word_count == None or word_count > len(wordlist):
        word_count = len(wordlist)
    board = [[None]*col for _ in range(row)]
    coords = [(i, j) for i in range(row) for j in range(col)]
    added_words = {}

    for word in random.sample(wordlist, k=word_count):
        word = word.upper()
        length = len(word)
        ox, oy = random.choice(orientations)
        try:
            x, y = random.choice(
                [(i, j) for i, j in coords if 0 <= i+length*ox < row and 0 <= j+length*oy < col and not any(board[i+d*ox][j+d*oy] for d in range(length))])

            for i in range(length):
                board[x+ox*i][y+oy*i] = word[i]

            added_words[((x, y), (x+ox*i, y+oy*i))] = word
        except:
            continue

    for i, j in coords:
        if board[i][j] is None:
            board[i][j] = random.choice(ascii_uppercase)

    for x, y in coords:
        for word in list(added_words.values()):
            length = len(word)
            for ox, oy in orientations:
                if not (0 <= x+length*ox < row and 0 <= y+length*oy < col):
                    continue
                if all(board[x+d*ox][y+d*oy] == word[d] for d in range(length)):
                    added_words[((x, y), (x+ox*(length-1),
                                 y+oy*(length-1)))] = word
    return board, added_words


if __name__ == "__main__":
    print(*generate(10, 10, ['hello', 'sike'], 2), sep="\n")
