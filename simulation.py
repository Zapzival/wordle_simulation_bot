from string import ascii_lowercase
from collections import Counter
import collections
import random
import os


my_file = open("allowed-answers.txt", "r")

realword = input("Guess: ")

all_words = my_file.readlines() # Huge word list to read in from text file
current_possible_words = set(all_words)
occurances = {}
topletters = []
wordtoGuess = "crane"


def main():
    global current_possible_words
    global wordtoGuess
    print("=========================================================================================================")
    print(f"Trying to guess: {realword}")
    count = 0
    while count < 8:
        if len(current_possible_words) == 1:
            guessing = []
            guessing = list(current_possible_words)
            wordtoGuess = guessing[0].rstrip()
            word = wordtoGuess
        else:
            word = wordtoGuess.rstrip()
        pattern = playGame(word).upper().rstrip()
        print(f"Guessing: {word}")
        print("")
        if pattern == "stop":
            break
        if pattern == "GGGGG":
            print(f"[{realword.rstrip()}] Done ({count + 1})")
            break
        for y in range(len(word.rstrip())):
            if pattern[y] == "G":
                current_possible_words = exact_letter_match(current_possible_words, word[y], y)
            if pattern[y] == "Y":
                current_possible_words = contains_only_elsewhere(current_possible_words, word[y], y)
            if pattern[y] == "X":
                current_possible_words = must_not_contain(current_possible_words, word[y])

        for x in current_possible_words:
            print (f"{x.rstrip()}", end=", ")
        print ("")
        makeguess()
        count += 1
        print("---------------------------------------------------------------------------------------------------------")

def contains_only_elsewhere(possible_words, letter, place):
    to_remove = {word for word in possible_words
                 if letter not in word or word[place] == letter}
    return possible_words - to_remove

def must_not_contain(possible_words, letter):
    to_remove = {word for word in possible_words
                 if letter in word}
    return possible_words - to_remove

def exact_letter_match(possible_words, letter, place):
    to_remove = {word for word in possible_words
                 if word[place] != letter}
    return possible_words - to_remove

def makeguess():
    topletters.clear()
    highest = 0
    letter = 'e'
    occurances.clear()
    for c in ascii_lowercase:
        amount = 0
        for x in current_possible_words:
            amount = amount + x.count(c)
            if amount > highest:
                letter = c
                highest = amount
        occurances[c] = amount
    print("")
    k = Counter(occurances)
    high = k.most_common(10)
    for i in high:
        print("(",i[0],":",i[1],") ", end="")
        topletters.append(i[0])
    maxscore = 0
    maxword = ""
    print("")
    for z in current_possible_words:
        score = 0
        for y in range(0, 9):
            if str(topletters[y]) in z:
                score = score + (30/(y+5))
        print(f"({z.rstrip()}, {score})")
        d = collections.defaultdict(int)
        for c in z:
            d[c] += 1
            if d[c] > 1:
                score = score - 30
        if score > maxscore:
            maxword = z
            maxscore = score
    print("")
    print("")
    print (f"[{len(current_possible_words)}] {maxword}")
    global wordtoGuess
    wordtoGuess = maxword

def playGame(guess):
    sequence = ""
    guess = guess.rstrip()
    for x in range(0, len(guess)):
        if guess[x] == realword[x]:
            sequence = sequence + "G"
        elif guess[x] in realword:
            sequence = sequence + "Y"
        else:
            sequence = sequence + "X"
    print("")
    print(sequence)
    return sequence

main()
