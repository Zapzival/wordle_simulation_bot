from string import ascii_lowercase
from collections import Counter
import collections
from tqdm import tqdm
import os

def clear(): 
    os.system('cls') #on Windows System

my_file = open("allowed-answers.txt", "r")
worddata = open("worddata.txt", "a")

all_words = my_file.readlines() # Huge word list to read in from text file
current_possible_words = set(all_words)

occurances = {}
topletters = []
results = {}
guesses = {}

wordtoGuess = "crane"


def main():
    global current_possible_words
    global realword
    global wordtoGuess

    total = 0
    progress = 0
    current_possible_words = set(all_words)
    
    for xyz in tqdm(sorted(current_possible_words), desc="Loading..."):
        progress = progress + 1
        realword = xyz.rstrip()
        current_possible_words = set(all_words)
        count = 0
        doescontain = []

        worddata.write(f"=========================================================================================\nTrying to Guess: {xyz.rstrip()}")
        print("")
        print(f"[[[{total}]] [{total / progress}]")
        
        while count < 8:
            if count == 6:
                worddata.write(f"\n----FAILED: {xyz}")
            if len(current_possible_words) == 1:
                guessing = []
                guessing = list(current_possible_words)
                wordtoGuess = guessing[0].rstrip()
                word = wordtoGuess
            else:
                word = wordtoGuess.rstrip()
            pattern = playGame(word).upper().rstrip()
            if pattern == "stop":
                break
            if pattern == "GGGGG":
                results[realword] = count + 1
                total += count + 1
                
                worddata.write(f'\n\nGuessing: "{wordtoGuess.rstrip()}" | {pattern}\n')
                worddata.write(f'\nGuessed: "{xyz.rstrip()}" [{count + 1}]\n -- Total: [[{total}]] [{total / progress}]\n\n')
                wordtoGuess = "crane"

                clear()
                break
            for y in range(0, len(word.rstrip())):
                if pattern[y] == "G":
                    current_possible_words = exact_letter_match(current_possible_words, word[y], y)
                    doescontain.append(word[y])
                if pattern[y] == "Y":
                    current_possible_words = contains_only_elsewhere(current_possible_words, word[y], y)
                    doescontain.append(word[y])
                if pattern[y] == "X":
                    if word[y] not in doescontain:
                        current_possible_words = must_not_contain(current_possible_words, word[y])
                    if word[y] in doescontain:
                        worddata.write("||")
            
            worddata.write(f"\n")
            worddata.write(f'\nGuessing: "{wordtoGuess.rstrip()}" | {pattern} | Words Left [{len(current_possible_words)}] |')
            worddata.write(f"\n    > ")

            for f in sorted(current_possible_words):
                worddata.write(f"{f.rstrip()}, ")

            makeguess()
            count += 1
            
    print(f"[[[{total}]] [{total / len(all_words)}]")

#Find the words that only match the criteria
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

#Make guess based on letter popularity of remaming words. Negate duplicates.
def makeguess():
    global wordtoGuess

    topletters.clear()
    occurances.clear()

    highest = 0
    letter = ''
    maxscore = 0
    maxword = ""

    for c in ascii_lowercase:
        amount = 0
        for x in sorted(current_possible_words):
            amount = amount + x.count(c)
            if amount > highest:
                letter = c
                highest = amount
        occurances[c] = amount

    k = Counter(occurances)
    high = k.most_common(15)

    for i in high:
        topletters.append(i[0])
    
    for z in sorted(current_possible_words):
        score = 0
        for y in range(0, 14):
            if str(topletters[y]) in z:
                score = score + (30/(y+1))
        d = collections.defaultdict(int)
        for c in z:
            d[c] += 1
            if d[c] > 1:
                score = score
        if score > maxscore:
            maxword = z
            maxscore = score
    
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
    return sequence

#Start the program
main()
