import random
import time
playerStreak = 0
#Winning combinations function
def determine_winner(player_choice, bot_choice):
    global playerStreak
    winningCombinations = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper",
    }

    if player_choice == bot_choice:
        print(f"You threw down {player_choice}, and the opponent threw down {bot_choice}! You tied.")
    elif winningCombinations[player_choice] == bot_choice:
        print(f"You threw down {player_choice}, and the opponent threw down {bot_choice}! You win!")
        playerStreak = playerStreak + 1
        print(f"You now have a {playerStreak}🔥  win streak!")
    else:
        print(f"You threw down {player_choice}, and the opponent threw down {bot_choice}! You lose!")
        playerStreak = 0

userChoice = ""
print("Welcome to rock paper scissors! Your commands are 'play', 'streak', and 'quit'")
botRNG = ["rock", "paper", "scissors"]
while userChoice.lower() != "quit":
    userChoice = input("What would you like to do?")
    if userChoice.lower() == "play":
        playing = True
        while playing:
            print(f"You challenge somebody to a game of rock paper scissors! (Current streak: {playerStreak}🔥 )")
            playAsk = input("What will you play?").lower()
            if playAsk in ["rock", "paper", "scissors"]:
                print(f"You get ready to play, and have {playAsk} set as your choice in your mind.")
                botChoice = botRNG[random.randint(0,2)]
                time.sleep(1)
                print("Rock,")
                time.sleep(1)
                print("Paper,")
                time.sleep(1)
                print("Scissors,")
                time.sleep(1)
                print("SHOOT!")
                time.sleep(0.5)
                result = determine_winner(playAsk, botChoice)
                askPlayAgain = True
                while askPlayAgain:

                    playAgain = input("Would you like to play again? (yes/no)").lower()
                    if playAgain == "no":
                        askPlayAgain = False
                        playing = False
                    elif playAgain == "yes":
                        askPlayAgain = False
                    else:
                        print("That is not a yes/no answer.")
            elif playAsk == "quit":
                playing = False
            else:
                print("Thats not a valid choice! Say rock, paper, scissors, or quit.")
    elif userChoice.lower() == "streak":
        print(f"You currently have a {playerStreak}️‍🔥  win streak!")
    elif userChoice.lower() == "quit":
        print("Thanks for playing!")
    else:
        print("That is not a valid command! Say 'play' or 'quit'.")

