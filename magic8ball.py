import random
import time
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
        print("You pick up the Magic 8 Ball and ask it '" + question + "'.")
        print("You start to shake the 8 ball.")
        time.sleep(1)
        print("*shake*")
        time.sleep(1)
        print("*shake*")
        time.sleep(1)
        print("*shake*")
        time.sleep(1)
        print(f"As you stop shaking the 8 ball, blurry letters start to appear, spelling out the words: '{responseChosen}'")