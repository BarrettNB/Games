'''
This is an old game, Bulls and Cows, that I created years ago and have tweaked
in the years since. I called it 'Lingo Math' because it is similar to the game
show Lingo, but instead of guessing words, the player guesses a number. The
game provides clues as to whether any of the digits guessed are correct, and
whether they are in the right order. However, unlike Lingo, the game does not
identify which specific digit is right or wrong; only general clues are given.

The key difference between my version and most other ones is that in mine, the
difficulty starts at just two or three digits but scales all the way up to ten
digits. This creates quite a challenge that mandates note-taking for everyone
but those who have exceptional memories. My version is not the most efficient
way to write this game, but I have thoroughly documented each part, and it is a
computationally simple game even when the number to guess contains ten digits.

v. 1.0: 1/15/08, Barrett Brister.  Created program.

v. 1.1: 2/13/08, Barrett Brister.  Updated rules; improved difficulty options.

v. 1.2: 5/27/08, Barrett Brister.  Made difficulty selection method more robust.
Introduced six-digit numbers.

v. 1.3: 6/25/08, Barrett Brister.  Relegated the minimum size of the random
number to a constant.  Increased this minimum size to 3.

v. 1.3.1: 7/09/08, Barrett Brister.  Added ASCII art to the game introduction.
Modified rules formatting.

v. 1.3.2: 11/17/08, Barrett Brister.  Made some revisions to comments.  Made
minor display changes.

v. 1.3.3: 12/29/08, Barrett Brister.  Made major revisions to comment styles.

v. 1.4: 4/13/09, Barrett Brister.  Made the program automatically start.

v. 1.4.1 9/12/12, Barrett Brister.  Made various minor revisions to the code.

v. 1.5 12/30/17, Barrett Brister. Max difficulty level starts at 3 and scales up
after each win.

v. 1.5.1 7/14/19, Barrett Brister. Min difficulty reduced to 2. Removed
unused high-score method.

v. 1.5.2 7/23/19, Barrett Brister. Option given to start the game at level
2 or 3.

v. 1.5.3 5/06/20, Barrett Brister. Cleaned up the rules() method. Made various
cleanups to make the code more Pythonic.
'''

import random

STRIKE = 'Strike!'
FOUL = 'Foul'
HIT = 'Hit'

PROMPT = '>> ' #input prompt
GUESS_COUNT = 10

MIN_DIFFICULTY = 2 #Smallest size of the random number.
MAX_DIFFICULTY = 10 #Largest size of the random number. Do not set above 10.

'''TextArt that prints when the game first loads.'''
def entryString():
    leftString = []
    rightString = []
    print()   
    leftString = ('   ......................................',
                  '   ..._..................................',
                  '   ..| |...._............................',
                  '   ..| |...[_].._.._....__.._...___......',
                  '   ..| |...._..| |/ \../  \| |./   \.....',
                  '   ..| |...| |.| /.\ \.| O   |.| O |.....',
                  '   ..|___|.|_|.|_|.|_|.\__/| |.\___/.....',
                  '   ....................._..| |...........',
                  '   ....................| |_| |...........',
                  '   ....v. 1.5.3........\_____/...........')
  
    rightString = ('....................................',
                   '._......_.................. _.......',
                   '| \..../ |............_....| |......',
                   '|  \../  |..__.._..._| |_..| |__....',
                   '|   \/   |./  \| |.|_   _|.|    \...',
                   '| |\  /| |.| O   |...| |...| /.\ \..',
                   '|_|.\/.|_|.\__/|_|...\__|..|_|.|_|..',
                   '....................................',
                   '....................................',
                   '...............by Barrett Brister...')
        
    for left, right in zip(leftString, rightString):
        print(left + right)
    print('\nWelcome to Lingo Math!')

'''Prints the rules of the game.'''
def rules():
    ruleString1 = ' '.join((
        '\nThe objective of Lingo Math is to guess a randomly-generated',
        'number within a limited number of guesses. You may choose the',
        'number of digits that the number has, within a predefined range.',
        'Larger numbers are harder to guess, so you will have more chances',
        'to guess them. There are two important properties to remember',
        'about the number you are trying to guess:\n\n',
        
        '\t1. None of the digits are the same, so it can\'t be 211, 33,',
        '4020, etc.\n',
        '\t2. The number must be a legitimate whole number, so it can\'t',
        'be 059, 06, 132.4, -25, etc.\n\n',
        '\b(NOTE: Your guess must match both conditions.)\n\n',        
    
        '\bTo help you guess the number, you will receive a combination of',
        'three clues after each guess.  They are:\n\n',

        '\t' + STRIKE + ': None of the digits are right.\n',
        '\t' + FOUL + ': A correct digit is in the WRONG place.\n',
        '\t' + HIT + ': A correct digit is in the RIGHT place.'))

    rulestring2 = ' '.join((        
        '\nFor ' + FOUL + 's and ' + HIT + 's, you get one applicable clue',
        'per matching digit. This means that you could get more than one',
        HIT + ' and/or ' + FOUL + ' per guess. For example, if the actual',
        'number is 6135 and your guess is 6013, then you would receive the',
        'following feedback:\n\n',
        
        '\t' + HIT + ' ' + FOUL + ' ' + FOUL + '\n\n',
        '\bThe 6 is present and in the right place, thus producing the',
        HIT + '. Likewise, the 1 and 3 are present, but because they are',
        'in the wrong places, they produce the two ' + FOUL + 's. Use',
        'these clues to help you correctly guess the number. If you do so',
        'before you run out of guesses, you win! Good luck!'))
    
    print(ruleString1)
    input('(Press Enter to continue.)')
    print(rulestring2)

'''Plays the game.  Several local methods are contained here.'''
def playGame(currMaxDifficulty):

    # Collects the number from the user.
    def inputNumber():
        #Starting with MIN_DIFFICULTY, this determines not only the description of
        #each number size's difficulty, but the allowable sizes themselves.
        #So if it has four elements, the allowable digit sizes are 2, 3, 4,
        #and 5.
        resetMatch = False
        
        #Legal size of the number, in digits
        DIGIT_SET = range(MIN_DIFFICULTY, currMaxDifficulty+1)
        ASSURANCE = '(This will increase as you win more games ' +\
            'on the highest difficulty available)'
        if len(DIGIT_SET) > 1:
            print('\nSelect your difficulty level by entering the number of digits')
            print('you want the random number to be:', end=' ')
            for i in DIGIT_SET[:-1]:
                print(str(i) + ',', end=' ')
            print(DIGIT_SET[-1])
            
            #The difficulty level depends solely on how many digits are in the
            #random number. Doing it this way like this builds in flexibility
            #to the allowable entry sizes.
            if currMaxDifficulty < MAX_DIFFICULTY:
                print(ASSURANCE)
        
            digits = None
            while not(digits in DIGIT_SET):
                #Keep this going until we get a good entry.
                try:
                    digits = int(input(PROMPT)) #Enter the number of digits.
                except(ValueError):
                    digits = None
                if not(digits in DIGIT_SET):
                    DIGIT_STRINGS = ''
                    for i in range(len(DIGIT_SET) - 1):
                        #all allowable digit sizes except the last (for grammar
                        #purposes)
                        DIGIT_STRINGS += str(DIGIT_SET[i]) + ', '
                    print('Please enter ' + DIGIT_STRINGS + 'or ' +\
                          str(DIGIT_SET[len(DIGIT_SET) - 1]) + '.')
            toReturn = digits
        else:
            toReturn =  DIGIT_SET[0]
            print('Difficulty level:', str(DIGIT_SET[0]), 'digits')
            print(ASSURANCE)
        return [resetMatch, toReturn]

    '''Generates the random number. Because the game has to analyze the
    guesses digit by digit, this is generated as a list, not a number. (A
    method is put in place to convert it back to an int.)'''
    def generateNumber(digits):
        numberSet = []
        for i in range(digits):
            lowLimit = [0,1][i==0]

            #Make sure that trialDigit is not already in numberSet.
            while True:
                trialDigit = random.randrange(lowLimit, 10)
                if not trialDigit in numberSet:
                    break
            numberSet.append(trialDigit)
        return numberSet

    '''Breaks apart an integer into a list. It takes the units digit, puts it
    on the list, divides the number by 10, and repeats until done. This puts
    the list in backwards order, though, so it has to be reversed.'''
    def numberToSet(number):
        newSet = []
        while (number > 0):
            newSet.append(number % 10) #Append the units digit to the list.
            number = number//10 #Discards the number's unit digit.
        newSet.reverse()
        return newSet

    '''Puts a set of single-digit integers back into a single number. It
    assumes that the incoming list uniquely contains single-digit whole
    numbers.'''
    def setToNumber(numSet):
        newNumber = 0
        for i, digit in enumerate(reversed(numSet)):
            newNumber += 10**i * digit
        return newNumber

    '''Analyzing the guess to see how closely it matches, and return the
    appropriate clues. This method assumes that the two set lengths are
    identical; this must be checked prior. Note: The message returned is never
    blank.  At least one clue is always given--remember, if nothing matches,
    it's a strike.'''
    def analyzeGuess(guessSet, answerSet):
        fouls = 0; hits = 0
        strike = True; message = ''
        for i in range(len(guessSet)):
            if guessSet[i] == answerSet[i]: #right number, right location
                hits += 1
                strike = False #because at least one digit has been found
            for j in range(len(guessSet)):
                if guessSet[i] == answerSet[j]: #right number, wrong location
                    fouls += 1
                    strike = False #because at least one digit has been found
        if strike:
            return STRIKE
        fouls = fouls - hits #to take away the extra matches
        message += hits*(HIT + ' ')
        message += fouls*(FOUL + ' ')
        return message

    #playGame() starts here.
    QUIT = 0
    resetMatch, digits = inputNumber() #Receive the number of digits
    guessCount = max(15, GUESS_COUNT*(digits - 1))
    answerSet = generateNumber(digits) #Set the random number
    gameOn = True
    while gameOn and not resetMatch:
        #Convert the entry to an int, if possible
        print('\nGuess the number here (Enter', QUIT, 'to return to '\
              'the main menu).')
        if guessCount > 1:
            suffix = 'es'
        else:
            suffix = ''
        try:
            #collect the guess
            guessNumber = int(input('(' + str(guessCount) +\
                                    ' guess' + suffix + ' left)' + PROMPT))
            guessSet = numberToSet(guessNumber)
        except:
            guessNumber = None
            guessSet = [0] #to trigger the illegal answer line

        #Conditions based on the entry given
        if guessNumber == QUIT: #option to quit
            print()
            gameOn = False
        elif guessSet == answerSet: #successful guess
            print('\nYes! That\'s the number.')
            gameOn = False
            if currMaxDifficulty < 6:
                currMaxDifficulty += max(0, digits - currMaxDifficulty + 2)
            elif currMaxDifficulty < MAX_DIFFICULTY:
                currMaxDifficulty += max(0, digits - currMaxDifficulty + 1)
            if len(answerSet) == MAX_DIFFICULTY:
                print('Congratulations! You have won at the highest difficulty level!')
            print()
        elif len(guessSet) != len(answerSet): #wrong number of digits
            print('\n\tPlease enter a ' + str(digits) + '-digit whole number.')
            #Note: There is no penalty if this occurs.

        else:
            legalNumber = True
            for i in range(0, len(guessSet)):
                for j in range(0, i):
                #don't want to compare digits to themselves!
                    if guessSet[i] == guessSet[j]:
                        legalNumber = False
                        break
                else:
                    continue
                break
            #This forces the player to guess a number that does
            #not duplicate digits, which would make guessing
            #artificially easier. There is no penalty if this occurs.
            if not(legalNumber):
                print('\n\tGuesses must contain unique digits.')
            else: #good entry, but not the answer, so analyze it
                print(analyzeGuess(guessSet, answerSet))
                guessCount -= 1 #because a guess has been used

        #Game-lost scenarios
        if guessCount == 0: #Ran out of guesses
            gameOn = False
            print('\nSorry!')
        if not(gameOn) and guessSet != answerSet:
            print('The number was ' + str(setToNumber(answerSet)) + '.')
    return currMaxDifficulty

'''Main method'''
def main():
    QUIT = 0
    RULES = 1
    PLAY = 2
    # option = None
    currMaxDifficulty = MIN_DIFFICULTY+1
    #Starting value. Can increase as the game goes on.
    
    entryString()
    # while option != QUIT:
    while True:
        print('\nChoose one of the following:')
        print(QUIT, 'to quit;')
        print(RULES, 'to see the rules;')
        print(PLAY, 'to play Lingo Math.')
        try:
            option = int(input(PROMPT))
        except(ValueError):
            option = None #forces the last elif
        
        if option == RULES:
            rules()
        elif option == PLAY:
            currMaxDifficulty = playGame(currMaxDifficulty)
        elif option == QUIT:
            break
        else:
            print(''.join(('Please enter ', str(QUIT), ', ', str(RULES),
                           ', or ', str(PLAY), '.')))
    
    print('\nThank you for playing Lingo Math!')
    print('You can now safely exit Python, or you may enter \'main()\' '\
          'to play again.')

main() #automatically starts the program