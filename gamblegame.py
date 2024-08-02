import random
print("Welcome to Gamble Game! Your commands are 'balance' and 'gamble'. If you want to know how to play, say 'help' and if you want to quit, say 'quit'.")
userCommand = ""
balance = 100

while userCommand.lower() != "quit":
    
    userCommand = input("What would you like to do?")
    if userCommand == "balance":
        print(f"You have ${balance} in your balance.")
    
    elif userCommand == "gamble":
        userBid = int(input("How much would you like to bid?"))
        if userBid <= balance:
            playing = True
            failChance = 5
            newBidBalance = userBid
            balance = balance - userBid
            while playing:
            
                
                print(f"You have a {failChance}% chance of losing everything but if your win you will gain 25%")
                askContinue = input("Would you like to continue? (yes/no)")
                if askContinue == "yes":
                    if random.randint(1, 100) <= failChance:
                        print("You failed and lost your bid.")
                        playing = False
                    else:
                        newBidBalance = round(newBidBalance * 1.25)
                        failChance = failChance + 5
                        print(f"You won! You now have ${newBidBalance}.")
                elif askContinue == "no":
                    print(f"Ok, you got you cashed out ${newBidBalance}.")
                    balance = balance + newBidBalance
                    failChance = 5
                    playing = False
        elif userBid > balance:
            print("You don't have that much money!")
    elif userCommand == "help":
        print("This game is very simple. When you gamble, you can decide to take a risk and have a chance at losing the money you bid, but if you win, you make more money than you bid, but the risk goes up. If you lose, you lose all the money that you have in the game.")