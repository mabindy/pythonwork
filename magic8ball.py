import random
playing = True
responses = ["Yes, definitely.", "No, not at all.", "It is unclear", "It is likely", "It does not look likely",]

while playing:
    # Asks the user what they would like to ask
    question = input("What question would you like to ask the Magic 8 Ball🎱? Say 'quit' to quit.")

    if question == "quit":
        playing = False
    else:
        randomGenerator = random.randint(0,4)
        responseChosen = responses[randomGenerator]
        print(f"The Magic 8 Ball reads: '{responseChosen}'")
        
