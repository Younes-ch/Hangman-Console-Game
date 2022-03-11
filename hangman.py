#! /usr/bin/env python3

import random
import subprocess
import os
from colorama import Fore
import time

def show_alphabet(alphabet_matrix, character_to_remove = None, character_is_correct = None):
   for i in range(6):
      alphabet_line = [x.upper() for x in alphabet_matrix[i]]
      if character_to_remove is not None:
         alphabet_line = ["❌" if x == character_to_remove.upper() else x for x in alphabet_line]
         print("  ".join(alphabet_line))
         alphabet_matrix[i] = alphabet_line
      elif character_is_correct is not None:
         alphabet_line = ["✅" if x == character_is_correct.upper() else x for x in alphabet_line]
         print("  ".join(alphabet_line))
         alphabet_matrix[i] = alphabet_line
      else:
         print("  ".join(alphabet_line))

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
   if x == " ":
      empty_chosen_word += "  "
   else:
      empty_chosen_word += " _"
empty_chosen_word = empty_chosen_word.strip()

def main_game(possible_words_dict, chosen_word, empty_chosen_word, number_of_tries):
   chosen_word_copy = "_".join(chosen_word)
   lives_available = Fore.RED + "❤️ "*number_of_tries
   print(possible_words_dict[chosen_word], end="     ({} Tries)  {}\n".format(number_of_tries, lives_available.strip()))
   print(Fore.WHITE)
   print(empty_chosen_word)
   print()
   show_alphabet(alphabet_matrix)
   while number_of_tries > 0 and chosen_word != "".join("".join(empty_chosen_word).split()):
      answer = input("Enter a character:\n")
      while len(answer) != 1 or not answer.isalpha():
         answer = input("Enter a character:\n")
      if answer.lower() in chosen_word:
         empty_chosen_word = list(empty_chosen_word)
         for i in range(len(chosen_word_copy)):
            if chosen_word_copy[i] == answer:
               empty_chosen_word[i] = chosen_word_copy[i]
         if os.name == 'nt':
            os.system('cls')
         else:
            subprocess.run(["clear"])
         print(possible_words_dict[chosen_word], end="     ({} Tries)  {}\n".format(number_of_tries, lives_available.strip()))
         print(Fore.WHITE)
         print("".join(empty_chosen_word))
         print()
         show_alphabet(alphabet_matrix, character_is_correct = answer)
      else:
         if os.name == 'nt':
            os.system('cls')
         else:
            subprocess.run(["clear"])
         number_of_tries -= 1
         lives_available = Fore.RED + "❤️ "*number_of_tries
         print(possible_words_dict[chosen_word], end="     ({} Tries)  {}\n".format(number_of_tries, lives_available.strip()))
         print(Fore.WHITE + "".join(empty_chosen_word))
         print()
         show_alphabet(alphabet_matrix, character_to_remove = answer)
      
   if number_of_tries == 0:
      if os.name == 'nt':
         os.system('cls')
      else:
         subprocess.run(["clear"])
      print("="*40)
      print("|{:^38}|".format("Game Over 🙄"))
      print("="*40)
   else:
      if os.name == 'nt':
         os.system('cls')
      else:
         subprocess.run(["clear"])
      print("="*40)
      print("|{:^38}|".format("Congratulations! You figured it out! ✅"))
      print("="*40)

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
      if x == " ":
         empty_chosen_word += "  "
      else:
         empty_chosen_word += " _"
   empty_chosen_word = empty_chosen_word.strip()
   main_game(possible_words_dict, chosen_word, empty_chosen_word, 7)
   time.sleep(2)
   if os.name == 'nt':
      os.system('cls')
   else:
      subprocess.run(["clear"])
   play_again = input("Play Again? (Y / N):\n")      
   while play_again.lower() != "y" and play_again.lower() != "n":
      play_again = input("Play Again? (Y / N):\n")
   if play_again.lower() == "n":
      break