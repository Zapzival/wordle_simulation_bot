my_file = open("allowed-guesses.txt", "r")

words = my_file.readlines()

realword = "irate"

while 1 == 1:
    word = input("Guess: ").lower()
    if word == "stop":
        break
    for x in range(0, len(word)):
        if word[x] == realword[x]:
             print("G", end="")
        elif word[x] in realword:
            print("Y", end="")
        else:
            print("X", end="")
    print("")
