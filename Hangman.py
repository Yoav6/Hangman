import random

MAX_TRIES = 6
HANGMAN_PHOTOS = {
    0: r'''
    x-------x
    ''',
    1: r'''
    x-------x
    |
    |
    |
    |
    |
    ''',
    2: r'''
    x-------x
    |       |
    |       0
    |
    |
    |
    ''',
    3: r'''
    x-------x
    |       |
    |       0
    |       |
    |
    |
    ''',
    4: r'''
    x-------x
    |       |
    |       0
    |      /|\
    |
    |
    ''',
    5: r'''
    x-------x
    |       |
    |       0
    |      /|\
    |      /
    |
    ''',
    6: r'''
    x-------x
    |       |
    |       0
    |      /|\
    |      / \
    |
    ''',
}
TOPICS = ['scientists', 'philosophers']
num_of_tries = 0
old_letters_guessed = []
secret_word = ''

topic = ''
game_state = ''

def title_screen():
    print(r'''
    Welcome to - 
       _    _                                         
     | |  | |                                        
     | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
     |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
     | |  | | (_| | | | | (_| | | | | | | (_| | | | |
     |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                          __/ |                      
                         |___/
    ''')

def choose_word(topic_index):
    '''
    This function sets both the topic and the secret word. it checks wether the index number for a topic exists,
    if so sets the topic and the file path to it. then it gets the the file, transforms it to a list,
    and chooses a random word from it, which is set to be the secret_word.
    :param topic_index: an index number entered by the user
    :return: none
    '''
    selected = False
    topic = ''
    # sets the topic if the input is valid, otherwise asks for it again
    while not selected:
        if int(topic_index) <= len(TOPICS):
            topic = TOPICS[int(topic_index)-1]
            selected = True
        else:
            topic_index = input('\ninvalid number, please enter a new one: ')

    # prints the chosen topic
    print('\nthe topic is', topic)

    print('you can choose up to {num} letters wrong before you lose, choose wisely!'.format(num=MAX_TRIES))

    # creates the file path for the chosen topic
    path = topic + '.txt'

    # opens the file and creates the secret word
    with open(path, 'r') as file:
        words = file.read().split()
        length = len(words) - 1
        # Generates a random number ranging from 0 to the length of the words list
        global secret_word
        secret_word = words[random.randint(0, length)]

def show_hidden_word(word, old_letters):
    result = ''
    for letter in word:
        if letter in old_letters:
            result = result + letter + ' '
        else:
            result = result + '_ '
    return print(result)


def check_valid_input(letter_guessed, old_letters):
    # checks if the letter was used already
    if letter_guessed in old_letters:
        print('You used this letter already!')
        return 'error'
    # checks if all characters are letters, and whether the length is equal to 1. if true returns valid.
    elif letter_guessed.isalpha() == 1 and len(letter_guessed) == 1:
        '''global old_letters_guessed
        old_letters_guessed.append(letter_guessed)
        print(*old_letters, sep=' -> ')'''
        return 'valid'
    # check if both of the above aren't true.
    elif letter_guessed.isalpha() == 0 and len(letter_guessed) > 1:
        print('the input must be one letter from a-z')
        return 'error'
    # checks if the error was non-letter characters.
    elif letter_guessed.isalpha() == 0:
        print('please enter only a-z letters')
        return 'error'
    # checks if the error was more than 1 letter
    elif len(letter_guessed) > 1:
        print('please enter only one letter')
        return 'error'

def update_letter_guessed(letter_guessed):
    '''

    :param letter_guessed:
    :return:
    '''
    # checks whether the player made a mistake, and updates num_of_tries accordingly
    if letter_guessed not in secret_word:
        print('this letter is not part of the word :(\n')
        global num_of_tries
        num_of_tries += 1
        print('you have {num} more tries'.format(num=(MAX_TRIES - num_of_tries)))
    global old_letters_guessed
    old_letters_guessed.append(letter_guessed)
    print('gussed letters ', *old_letters_guessed, sep=' | ')

def check_win(word, old_letters):
    for letter in word:
        if letter in old_letters:
            continue
        else:
            return
    print('\n  == you won! ==')
    global game_state
    game_state = 'won'

def check_lose():
    if num_of_tries == MAX_TRIES:
        print(HANGMAN_PHOTOS[6])
        print(''':( you lost! the word was''', secret_word)
        global game_state
        game_state = 'lost'

def play_again():
    '''
    this function is called after the player either correctly guessed the word, or lost, and asks them whether
    they want to play again.
    :return: 'false'
    '''
    play_again = input('''\nWould you like to play again (yes/no)? ''')
    if play_again == 'yes':
        global old_letters_guessed, game_state, num_of_tries
        old_letters_guessed = []
        game_state = ''
        num_of_tries = 0
        main()
    else:
        print('Thanks for playing!')
        return 'false'

def main():

    choose_word(input('''Available Topic:
    1. Scientists
    2. Philosophers

    Choose one by entering a number: '''))

    while True:
        print(HANGMAN_PHOTOS[num_of_tries])

        show_hidden_word(secret_word, old_letters_guessed)

        is_valid = ''
        while is_valid != 'valid':
            # takes player input and turns it into lower case
            letter = input('\nGuess a letter: ').lower()

            # calls function to check the validity of the letter
            is_valid = check_valid_input(letter, old_letters_guessed)
            if is_valid == 'valid':
                update_letter_guessed(letter)

        check_win(secret_word, old_letters_guessed)
        check_lose()
        if game_state in ('won', 'lost'):
            replay = play_again()
            if replay == 'false':
                break

title_screen()

if __name__ == '__main__':
    main()





