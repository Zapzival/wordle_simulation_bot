from string import ascii_lowercase
from collections import Counter
import collections
import random

my_file = open("list.txt", "r")

words = my_file.readlines()
realword = random.choice(words)

list = []
removed = []
occurances = {}
topletters = []
wordtoGuess = "crane"

def main():

    print("===================================================================================================================")
    print(f"Trying to guess: {realword}")
    print("-------------------------------------------------------------------------------------------------------------------")
    count = 0
    while count < 8:
        word = wordtoGuess
        print(f"Guessing: {word}")
        pattern = playGame(word).upper()
        print("")
        if pattern == "stop":
            break
        if pattern == "GGGGG":
            print(f"[{realword.rstrip()}] Done ({count + 1})")
            print("===================================================================================================================")
            break
        for y in range(0, len(word.rstrip())):
            pattern = pattern.rstrip()
            if pattern[y] == "G":
                isletter(word[y], y)
            if pattern[y] == "Y":
                contains(word[y], y)
            if pattern[y] == "X":
                nocontains(word[y])

        for x in list:
            print (f"{x.rstrip()}", end=", ")
        print ("")
        global words
        words = list.copy()
        makeguess()
        count += 1
        print("-------------------------------------------------------------------------------------------------------------------")

#Find the words that only match the criteria
def contains(letter, place):
    list.clear()
    for x in words:
        if x not in removed:
            if letter in x:
                if letter == x[place]:
                    removed.append(x)
                else:
                    list.append(x)
            else:
                removed.append(x)
def nocontains(letter):
    list.clear()
    for x in words:
        if x not in removed:
            if letter not in x:
                list.append(x)
            else:
                removed.append(x)
def isletter(letter, place):
    list.clear()
    for x in words:
        if x not in removed:
            if letter == x[place]:
                list.append(x)
            else:
                removed.append(x)

#Make guess based on letter popularity of remaming words. Negate duplicates.
def makeguess():
    highest = 0
    letter = 'e'
    occurances.clear()
    for c in ascii_lowercase:
        amount = 0
        for x in words:
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
    maxword = "hello"
    for z in words:
        score = 0
        if str(topletters[0]) in z:
            score = score + 15
        if str(topletters[1]) in z:
            score = score + 13
        if str(topletters[2]) in z:
            score = score + 12
        if str(topletters[3]) in z:
            score = score + 11
        if str(topletters[4]) in z:
            score = score + 9
        if str(topletters[5]) in z:
            score = score + 8
        if str(topletters[6]) in z:
            score = score + 5
        if str(topletters[7]) in z:
            score = score + 3
        if str(topletters[8]) in z:
            score = score + 2
        if str(topletters[9]) in z:
            score = score + 1
        d = collections.defaultdict(int)
        for c in z:
            d[c] += 1
            if d[c] > 1:
                score = score - 5
        if score > maxscore:
            maxword = z
            maxscore = score
    print("")
    print("")
    print (f"[{len(words)}] {maxword}")
    global wordtoGuess
    wordtoGuess = maxword

#Play the wordle game
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

#Start the program
main()
