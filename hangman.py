#! /usr/bin/env python3

import random
import subprocess
import os
import sys
from colorama import Fore
from termcolor import colored, cprint
import time


# ******************************** Déclaration de nos fonctions ***************************************

# affichage et mettre à jour la matrice des alphabets:
def display_alphabet(alphabet_matrix, character_to_remove = None, character_is_correct = None):
   for i in range(6):
      alphabet_line = [x.upper() for x in alphabet_matrix[i]]
      if character_to_remove is not None:
         alphabet_line = ["❌" if x == character_to_remove.upper() else x for x in alphabet_line]
         print("  ".join(alphabet_line)) # affichage de X quand l'utilisateur choisit une lettre n'appartient pas au mot a deviner
         alphabet_matrix[i] = alphabet_line
      elif character_is_correct is not None:
         alphabet_line = ["✅" if x == character_is_correct.upper() else x for x in alphabet_line]
         print("  ".join(alphabet_line)) # affichage de signe vrai quand l'utilisateur choisit une lettre appartient au mot a deviner
         alphabet_matrix[i] = alphabet_line
      else:
         print("  ".join(alphabet_line))


# l'algorithme principale de jeu:
def main_game(possible_words_dict, chosen_word, empty_chosen_word, number_of_tries, already_chosen_characters):
   global word_number
   word_number = Fore.BLUE + "Word: " + str(word_number) + "/" + str(len(possible_words_list))
   lives_available = Fore.RED + "❤️ "*number_of_tries # nombre des vies
   # affichage de l'indice et de la masque de mot a diviner
   print(Fore.YELLOW+"►",possible_words_dict[chosen_word], end="     ({} Tries)  {} {}\n".format(number_of_tries, lives_available, word_number))
   print(Fore.WHITE)
   print(" ".join(empty_chosen_word))
   print()
   # affichage de la matrice avec avoir compte des lettres choisit
   display_alphabet(alphabet_matrix)
   display_hangman(number_of_tries)
   while number_of_tries > 0 and chosen_word != "".join(empty_chosen_word):
      answer = input("Enter a character:\n")
      while len(answer) != 1 or not answer.isalpha():
         answer = input("Enter a character:\n") # control de saisie de caractère a choisir.
      if answer.lower() in chosen_word: # si l'utilisateur donne une bonne réponse.
        for i in range(len(chosen_word)):
           if chosen_word[i] == answer.lower():
              empty_chosen_word[i] = chosen_word[i] # permutation de "_" dans le masque avec la lettre correcte.

        if answer.lower() not in already_chosen_characters:
          already_chosen_characters[answer.lower()] = "✅"
        else:
          print("Character already entered and was " + Fore.GREEN + "CORRECT!")
          time.sleep(1.5)
        display_hangman(number_of_tries)

        clear()
        # nouveau affichage avec le nouveau masque et les changements au niveau de matrice.
        print(Fore.YELLOW+"►",possible_words_dict[chosen_word], end="     ({} Tries)  {} {}\n".format(number_of_tries, lives_available, word_number))
        print(Fore.WHITE)
        print(" ".join(empty_chosen_word))
        print()
        display_alphabet(alphabet_matrix, character_is_correct = answer)
      else: # si le joueur donne une mauvaise reponse.
         if answer.lower() not in already_chosen_characters:
            number_of_tries -= 1 # decrementation de nombre de vies de joueur s'il a choisit un caractère faux pour la première fois.
            already_chosen_characters[answer.lower()] = "❌"
         else:
            print("Character already entered and was " + Fore.RED + "WRONG!")
            time.sleep(1.5)
         clear()
         lives_available = Fore.RED + "❤️ "*number_of_tries
         # nouveau affichage avec le nouveau masque et les changements au niveau de matrice.
         print(Fore.YELLOW+"►",possible_words_dict[chosen_word], end="     ({} Tries)  {} {}\n".format(number_of_tries, lives_available, word_number))
         print(Fore.WHITE + "".join(empty_chosen_word))
         print()
         display_alphabet(alphabet_matrix, character_to_remove = answer)

   global won # on veut acceder a la variable "won" et "wrong_guesses" pour mise a jour sa valeur.
   global wrong_guesses
   word_number = int(word_number[11:word_number.index("/")]) + 1
   if number_of_tries == 0: # si le joueur est mort (0 vies).
      clear()
      cprint("="*45, 'red')
      cprint("||", 'red', end=" ")
      cprint("{:^38}".format("Wrong Guess! 🙄"), 'red', attrs=['blink'], end=" ") # affichage le message de victoire.
      cprint("||",'red')
      cprint("="*45, 'red')
      wrong_guesses += 1
      won = False
   else: # si le joueur a gagné
      clear()
      cprint("="*45, 'green')
      cprint("||", 'green', end=" ")
      cprint("{:^38}".format("Congrats! You figured it out! ✅"), 'green', attrs=['blink'], end=" ") # affichage le message de victoire.
      cprint("||", 'green')
      cprint("="*45, 'green')
      won = True


# Fonction pour sortir du programme en cas ou l'utilisateur a complete tous les niveaux.
def end_game(won, wrong_guesses):
   clear()
   if won and wrong_guesses == 0: # Controle si l'utilisateur a deviné tous les mots avec success ou non.
      cprint("="*46, 'cyan')
      cprint("||",'cyan', end=" ")
      cprint("{:^35}".format("You guessed all the words! You wizard 🧙"), 'cyan', attrs=['blink'], end=" ") # affichage le message de victoire.
      cprint("||", 'cyan')
      cprint("="*46, 'cyan')
   else:
      cprint("="*45, 'cyan')
      cprint("||", 'cyan', end= " ")
      cprint("{:^39}".format(f"Hard Luck! you guessed {len(possible_words_list) - wrong_guesses} words out of {len(possible_words_list)}"), "cyan", attrs=["blink"], end=" ")
      cprint("||", 'cyan') # affichage le message de victoire.
      cprint("="*45, 'cyan')
   sys.exit(0)

# Fonction pour effacer le contenu précédent du console:
def clear():
   if os.name == 'nt':# si le systeme d'exploitation est windows.
      os.system('cls')# il execute le commande 'cls' au console sinon il execute 'clear' pour linux qui sert de effacer le contenu du console.
   else:
      subprocess.run(["clear"])

def display_hangman(number_of_tries_left):
    if number_of_tries_left == 6:
        print("+----+")
        print("|")
        print("|")
        print("|")
        print("|")
        print("|")
        print("====")

def main_menu(): # Pour afficher un message de bienvenue animé et inviter l'utilisateur à démarrer le jeu ou à le quitter.
    clear()
    terminal_width = os.get_terminal_size().columns
    cprint('='*terminal_width, 'magenta')
    cprint('{:^{terminal_width}}'.format('Equipe HAYAS: Hangman Game!', terminal_width=terminal_width), 'magenta', attrs=['blink', 'bold'])
    cprint('='*terminal_width, 'magenta')
    welcome_message = colored("{:>82}".format("Hello! Welcome to the console version of the famous Hangman game!\n"), 'green') + \
    colored("{:>50}".format("This game was made by "), 'blue') + colored("HAYAS ", 'cyan', attrs=['bold']) + \
    colored("Team,\n", 'blue') + \
    colored("{:>55}".format("We hope you like it!\n\n"), 'yellow')
    for c in welcome_message:
        sys.stdout.write(c)
        sys.stdout.flush()
        if c == ' ':
            time.sleep(0.01)
        elif c != '\n':
            time.sleep(0.1)
        else:
            time.sleep(0.8)
    choices = colored('{}1) Start Game.\n\n\n{}'.format(' ' * 35, '{}2) Quit Game.'.format(' '*35)), 'red', attrs=['dark', 'bold'])
    for c in choices:
        sys.stdout.write(c)
        sys.stdout.flush()
        if c == ' ':
            time.sleep(0.01)
        else:
            time.sleep(0.1)
    time.sleep(1)
    while True:
        choice = input(colored('\n\n{}Start Game ? '.format(35*' '), 'green', attrs=['dark']))
        if choice == '1':
            break
        elif choice == '2':
            sys.exit(0)
        else:
            clear()
            cprint('='*terminal_width, 'magenta')
            cprint('{:^{terminal_width}}'.format('Equipe HAYAS: Hangman Game!', terminal_width=terminal_width), 'magenta', attrs=['blink', 'bold'])
            cprint('='*terminal_width, 'magenta')
            print(welcome_message)
            print(choices)
# ************************************************************************************************************

# ******************************** Initialisation de nos variables globales **********************************
# liste des mots utilisé dans le jeu
possible_words_list = [
                      "abracadabra",
                      "python",
                      "tomato",
                      "issatso",
                      "ukraine",
                      "table",
                      "ramadan",
                      "heaven",
                      "spongebob",
                      "kaiessaied",
                      "paris",
                      "everest",
                      "tokyo",
                      "asia"
                     ]
# dictionnaire qui contient les mot avec leurs indices
possible_words_dict = {
                       "abracadabra" : "Magic spell.",
                       "python" : "This game is written in ...?",
                       "tomato" : "Is it a fruit or a vegetable?",
                       "issatso" : "a hole.",
                       "ukraine" : "A country is currently at war.",
                       "table" : "Has 4 legs and doesn't move.",
                       "ramadan" : "A month where muslims fast everyday 🌜.",
                       "heaven" : "The opposite of hell.",
                       "spongebob" : "Who lives in a pineapple under the sea 🎵🎶?",
                       "kaiessaied" : "Tunisia's president.",
                       "paris" : "City of lights 💡.",
                       "everest" : "Highest mountain in the world 🗻.",
                       "tokyo" : "Most populated city in the world 🏙️.",
                       "asia" : "Largest continent on earth 🌏."
                    }
already_chosen_words = []
wrong_guesses = 0
word_number = 1

# ************************************************************************************************************


# ************************************** Programme Principale ***************************************************
# main_menu()
while True:
   already_chosen_characters = {}
   clear()
   # choisir une mot aléatoire de la liste et guarantir que le mot a deviner va etre choisit une seule fois.
   while True:
      chosen_word = random.choice(possible_words_list)
      if chosen_word in already_chosen_words:
         chosen_word = random.choice(possible_words_list)
      else:
         already_chosen_words.append(chosen_word)
         break

   # initialisation de la matrice principal avec les alphabets
   alphabet_matrix = [
                        ["a", "b", "c", "d", "e"],
                        ["f", "g", "h", "i", "j"],
                        ["k", "l", "m", "n", "o"],
                        ["p", "q", "r", "s", "t"],
                        ["u", "v", "w", "x", "y"],
                        ["z"]
                     ]

   # creation de la masque de mot a deviner
   empty_chosen_word = []
   for x in chosen_word:
      empty_chosen_word.append("_") # initialisation de masque.

   main_game(possible_words_dict, chosen_word, empty_chosen_word, 6, already_chosen_characters)
   time.sleep(2.3) # permet d'attendre 2.3 sec aprés passer a l'instruction suivante.
   clear()
   if len(already_chosen_words) == len(possible_words_list): # Si l'utilisateur a trouve tout les mots alors on quitte.
      end_game(won, wrong_guesses)
   else:
      play_again = input(Fore.BLUE+"► Next Word? (Y / N) ◄:\n")      # choix de jouer une autre fois.
      while play_again.lower() != "y" and play_again.lower() != "n": # control de saisie de play_again
         play_again = input(Fore.BLUE+"► Next Word? (Y / N) ◄:\n")
      if play_again.lower() == "n": # si la reponse est non le program va se fermer sinon il va s'executer à nouveau.
         break

# ************************************************************************************************************
