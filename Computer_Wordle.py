import random
import pandas as pd
from termcolor import colored


# Creating a global dataframe to contain all the words and their probabilistic weights
# for each position of the letter. Making it a global variable for easy access across 
# all functions to edit the dataframe after each guess.
DF_GUESS = pd.DataFrame()



# Loads the words dataset and filters all the words whose lenght is not 5.
def load_words(filename):
    with open(filename, 'r') as f:
        words = f.read().splitlines()
        words = [w for w in words if len(w) == 5]
    return words



# Calculates the frequency of each letter in each position and sums it up for each word in the dataframe.
def calculate_weights():
    # To access the global variable DF_GUESS
    global DF_GUESS

    # Calculating the frequency of each letter in each position.
    for i in range(1,6):
       DF_GUESS['letter_'+ str(i) +'_freq'] = DF_GUESS['letter_'+ str(i)].map(DF_GUESS['letter_'+ str(i)].value_counts())
    
    # Adding all the frequencies of each letter for every word and storing it in the CumiWeight column of the dataframe.
    DF_GUESS['CumiWeight'] = DF_GUESS['letter_1_freq']+DF_GUESS['letter_2_freq'] +DF_GUESS['letter_3_freq'] +DF_GUESS['letter_4_freq'] +DF_GUESS['letter_5_freq']
    
    # Sorting the dataframe with the highest total frequency at the top.
    # This is so that the word which has the highest total frequncy for each letter in each position is our first guess.
    DF_GUESS = DF_GUESS.sort_values('CumiWeight', ignore_index=True,  ascending=False)



# Initialises the dataframe on the first run with the words of the dataset, their frequncies and cumulative weights.
def initialize_dataframe(wordle_list):
    global DF_GUESS

    DF_GUESS = pd.DataFrame(wordle_list, columns =['words'], dtype = str)
    DF_GUESS['letters'] = DF_GUESS['words'].apply(list)

    # Creating new columns for each position of the letter, this is required to calculate the frequency
    # of each letter and the cumulilative weight of the entire word.
    for index, row in DF_GUESS.iterrows():
        word = row['words']
        letters = list(word)
        for i, letter in enumerate(letters):
            DF_GUESS.at[index, 'letter_' + str(i+1)] = letter
    
    # Calculating the weights for the initial set of words.
    calculate_weights()


# Updates the DF_GUESS dataframe with the feedback recieved from previous guesses.
def guess_word(feedback, previousGuess, gs_ys):

    global DF_GUESS

    # count is the current position as we iterate through the feedback.
    count = 0

    for i in feedback:

        # We are iterating through the feedback received for each letter of the previous guess,
        # focus_letter denotes that letter.
        focus_letter = previousGuess[count]

        # If the focus_letter color is green, the dataframe is updated with all the words having the focus_letter
        # in the current position of the iteration.
        if i == 'G':
            DF_GUESS = DF_GUESS.loc[DF_GUESS['letter_' + str(count+1)] == focus_letter]

        # If the focus_letter color is yellow, the dataframe is updated with all the words containing the focus_letter,
        # and all the words containing the focus letter in the current position are removed from the dataframe.
        if i == 'Y':
            yList = [x for x in DF_GUESS.index if focus_letter in DF_GUESS["words"][x]]
            DF_GUESS = DF_GUESS.loc[yList]
            DF_GUESS = DF_GUESS.loc[DF_GUESS['letter_' + str(count+1)] != focus_letter]

        # If the focus_letter color is red and the letter is also marked green or yellow, all the words containing the
        # focus_letter only in the current position are deleted. Otherwise, if focus_letter is red and is not marked 
        # green or yellow, all the words containing the focus_letter are deleted.
        if (i == 'R') and (focus_letter in gs_ys):
            DF_GUESS = DF_GUESS.loc[DF_GUESS['letter_' + str(count+1)] != focus_letter]
        elif i == 'R':
            dropList = [x for x in DF_GUESS.index if focus_letter in DF_GUESS["words"][x]]
            DF_GUESS = DF_GUESS.drop(dropList, axis=0)
        
        count += 1

    # Weights are again calculated for the newly updated dataframe which is based on the previous guess.
    calculate_weights()
    

def main():
    
    global DF_GUESS
    words = load_words("words_alpha.txt")

    initialize_dataframe(words)

    wordle_word_to_guess = random.choice(words)

    print("\nwordle word to guess: " + wordle_word_to_guess)

    for attempt in range(6):

        print("\nGuess: " + str(attempt+1))

        # Our first guess is the word with the highest cumulative weight, which is the first word of the
        # sorted dataframe.
        guess_input = DF_GUESS["words"][0]

        guess_input_letters = list(guess_input)
        wordle_word_to_guess_letters = list(wordle_word_to_guess)

        # Creating a copy of the word to be guessed to make sure we mark the correct color to the correct letter.
        pop_list = wordle_word_to_guess_letters.copy()

        # A list to contain the feedback of the word
        feedback_list = []

        # A list to append the colored version of the output on the terminal.
        result = []

        # gs is a list for all the letters to be marked green.
        gs = []

        # gs_ys is a list of all the letters which are marked green and yellow.
        gs_ys = []

        # We are iterating through the guessed letter and marking 
        # - G for green indicating the letter is in the right position
        # - Y for yelllow indicating the letter is in the word but in the wrong position.
        # - R for red indicating the letter is not in the word.
        for i in range(len(guess_input_letters)):
            if guess_input_letters[i] == wordle_word_to_guess_letters[i]:
                feedback_list.append("G")
                gs.append(i)
                gs_ys.append(guess_input_letters[i])
                result.append(colored(guess_input_letters[i].upper(), 'green'))
            elif guess_input_letters[i] in pop_list:
                feedback_list.append("Y")
                gs_ys.append(guess_input_letters[i])
                result.append(colored(guess_input_letters[i].upper(), 'yellow'))
            else:
                feedback_list.append("R")
                result.append(colored(guess_input_letters[i].upper(), 'red'))

        # Removing all the letters which are marked green from the pop_list.
        pop_list = [l for i, l in enumerate(pop_list) if i not in gs]
        
        # Iterating through the feedback_list and checking for all values of Y if they are in pop_list or not.
        # If they are in the pop_list, we are removing them from the list, else the specific letter is marked red.
        # This is so that no two same letters are marked Y if only one of them exists in the word to be guessed.
        for indx, lettr in enumerate(feedback_list):
            if (lettr == "Y") and (guess_input_letters[indx] in pop_list):
                pop_list.remove(guess_input_letters[indx])
            elif lettr == "Y":
                feedback_list[indx] = "R"
                result[indx] = colored(guess_input_letters[indx].upper(), 'red')
        
        
        for letter in result:
            print("  " + letter, end="")
                
        guess_word(feedback_list, guess_input_letters, gs_ys)
        
        if guess_input_letters == wordle_word_to_guess_letters:
            print("\n\nCongrats! You got the correct word")
            break
        elif attempt == 5:
            print("\n\nEnd of Game! Boo!")
            break


if __name__ == "__main__":
    main()
