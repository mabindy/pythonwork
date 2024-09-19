import json
import os
from g4f.client import Client

client = Client()
usingai = True
convo_logs = []
log_directory = os.path.join(os.path.expanduser('~'), "Documents", "PyGPT")
log_file = os.path.join(log_directory, "pygptlogs.json")
os.makedirs(log_directory, exist_ok=True)
# Loads the logs from the last conversation before quitting, or returns no chatlogs if there was no previous conversation.
def load_convo_logs():
    try:
        with open(log_file, 'r') as file:
            logs = json.load(file) 
            return logs
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("ChatGPT: There was an issue reading the logs file, so it has been reset. Logs saving is still in a buggy state right now.")
        return []

# Saves the conversation logs to a .json file
def save_convo_logs():
    with open(log_file, 'w') as file:
        json.dump(convo_logs, file, indent=4) 

convo_logs = load_convo_logs()

while usingai:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        usingai = False
        break
    if user_input.lower() in ['reset', 'new']:
        convo_logs = []
        print("ChatGPT: The conversation has been reset.")
        continue

    convo_logs.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=convo_logs,
    )
    ai_response = response.choices[0].message.content
    convo_logs.append({"role": "assistant", "content": ai_response})
    print(f'ChatGPT: {ai_response}')

    save_convo_logs()
