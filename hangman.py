#! /usr/bin/env python3

import random
import subprocess
import os
from colorama import Fore
import time

# affichage de la matrice des alphabets 
def show_alphabet(alphabet_matrix, character_to_remove = None, character_is_correct = None):
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
                      "everest",
                      "paris",
                      "kaiessaied",
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
                    
# choisir une mot aléatoire de la liste
chosen_word = random.choice(possible_words_list)

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
empty_chosen_word = ""
for x in chosen_word:
   empty_chosen_word += " _"
empty_chosen_word = empty_chosen_word.strip()

# le code principale de jeu
def main_game(possible_words_dict, chosen_word, empty_chosen_word, number_of_tries):
   chosen_word_copy = "_".join(chosen_word) # le mot a diviner sous forme de la masque
   lives_available = Fore.RED + "❤️ "*number_of_tries # nombre des vies
   # affichage de l'indice et de la masque de mot a diviner
   print(Fore.YELLOW+"►",possible_words_dict[chosen_word], end="     ({} Tries)  {}\n".format(number_of_tries, lives_available.strip()))
   print(Fore.WHITE)
   print(empty_chosen_word)
   print()
   # affichage de la matrice avec avoir compte des lettres choisit 
   show_alphabet(alphabet_matrix)
   while number_of_tries > 0 and chosen_word != "".join("".join(empty_chosen_word).split()):
      answer = input("Enter a character:\n")
      while len(answer) != 1 or not answer.isalpha():
         answer = input("Enter a character:\n") # control de saisie de caractère a choisir.
      if answer.lower() in chosen_word: # si l'utilisateur donne une bonne réponse.
         empty_chosen_word = list(empty_chosen_word)
         for i in range(len(chosen_word_copy)):
            if chosen_word_copy[i] == answer:
               empty_chosen_word[i] = chosen_word_copy[i] # permutation de "_" dans le masque avec la lettre correcte.
         if os.name == 'nt': # si le système d'exploitation est windows.
            os.system('cls') # il execute le commande 'cls' au console sinon il execute 'clear' pour linux qui sert de effacer le contenu du console.
         else:
            subprocess.run(["clear"])
         # nouveau affichage avec le nouveau masque et les changements au niveau de matrice.
         print(Fore.YELLOW+"►",possible_words_dict[chosen_word], end="     ({} Tries)  {}\n".format(number_of_tries, lives_available.strip()))
         print(Fore.WHITE)
         print("".join(empty_chosen_word))
         print()
         show_alphabet(alphabet_matrix, character_is_correct = answer)
      else: # si le joueur donne une mauvaise reponse.
         if os.name == 'nt':# si le systeme d'exploitation est windows.
            os.system('cls')# il execute le commande 'cls' au console sinon il execute 'clear' pour linux qui sert de effacer le contenu du console.
         else:
            subprocess.run(["clear"])
         number_of_tries -= 1 # decrementation de nombre de vie de joueur.
         lives_available = Fore.RED + "❤️ "*number_of_tries
         # nouveau affichage avec le nouveau masque et les changements au niveau de matrice.
         print(Fore.YELLOW+"►",possible_words_dict[chosen_word], end="     ({} Tries)  {}\n".format(number_of_tries, lives_available.strip()))
         print(Fore.WHITE + "".join(empty_chosen_word))
         print()
         show_alphabet(alphabet_matrix, character_to_remove = answer)
      
   if number_of_tries == 0: # si le joueur est mort (0 vies).
      if os.name == 'nt':
         os.system('cls')
      else:
         subprocess.run(["clear"])
      print(Fore.RED+"="*40)
      print(Fore.RED+"||{:^35}||".format("Game Over 🙄")) # affichage le message de la perte.
      print(Fore.RED+"="*40)
   else: # si le joueur a gagné
      if os.name == 'nt':
         os.system('cls')
      else:
         subprocess.run(["clear"])
      print(Fore.GREEN+"="*40)
      print(Fore.GREEN+"||{:^35}||".format("Congrats! You figured it out! ✅")) # affichage le message de victoire.
      print(Fore.GREEN+"="*40)

while True:
   if os.name == 'nt':
      os.system('cls')
   else:
      subprocess.run(["clear"])
   chosen_word = random.choice(possible_words_list)
   alphabet_matrix = [
                        ["a", "b", "c", "d", "e"],
                        ["f", "g", "h", "i", "j"],
                        ["k", "l", "m", "n", "o"],
                        ["p", "q", "r", "s", "t"],
                        ["u", "v", "w", "x", "y"],
                        ["z"]
                     ]

   empty_chosen_word = ""
   for x in chosen_word:
         empty_chosen_word += " _"
   empty_chosen_word = empty_chosen_word.strip() # initialisation de masque.
   main_game(possible_words_dict, chosen_word, empty_chosen_word, 7)
   time.sleep(2.3) # permet d'attendre 2.3 sec aprés passer a l'instruction suivante.
   if os.name == 'nt':
      os.system('cls')
   else:
      subprocess.run(["clear"])
   play_again = input(Fore.BLUE+"► Play Again? (Y / N) ◄:\n")      # choix de jouer une autre fois.
   while play_again.lower() != "y" and play_again.lower() != "n": # control de saisie de play_again
      play_again = input(Fore.BLUE+"► Play Again? (Y / N) ◄:\n")
   if play_again.lower() == "n": # si la reponse est non le program va se fermer sinon il va s'executer à nouveau.
      break                      
