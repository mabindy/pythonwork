import atexit
import logging
import json
import os
from g4f.client import Client

client = Client()
usingai = True
convo_logs = []
log_directory = os.path.join(os.path.expanduser('~'), "Documents", "PyGPT")
log_file = os.path.join(log_directory, "pygptlogs.json")
errlog_file = os.path.join(log_directory, "errors.log")

os.makedirs(log_directory, exist_ok=True)

logging.basicConfig(
    filename=errlog_file,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    force=True
)

def on_exit():
    print('ChatGPT: PyGPT has stopped unexpectedly.')
    logging.warning('The program was terminated unexpectedly.')

atexit.register(on_exit)

# Loads the logs from the last conversation before quitting, or returns no chatlogs if there was no previous conversation.
def load_convo_logs():
    try:
        with open(log_file, 'r') as file:
            logs = json.load(file) 
            return logs
    except FileNotFoundError:
        logging.warning('No previous conversation logs found')
        return []
    except json.JSONDecodeError:
        logging.error('An issue occured while attempting to read the conversation logs, logs have been reset.')
        return []

# Saves the conversation logs to a .json file
def save_convo_logs():
    try:
        with open(log_file, 'w') as file:
            json.dump(convo_logs, file, indent=4)
    except Exception as e:
        logging.error(f'Failed to save conversation logs: {e}')

convo_logs = load_convo_logs()

print('PyGPT V1.1')
while usingai:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        usingai = False
        break
    if user_input.lower() in ['reset', 'new']:
        convo_logs = []
        save_convo_logs()
        logging.info('Conversation was reset by the user.')
        print("ChatGPT: The conversation has been reset.")
        continue

    convo_logs.append({"role": "user", "content": user_input})
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=convo_logs,
        )
        ai_response = response.choices[0].message.content
        if ai_response == "One message exceeds the 1000chars per message limit. Join our discord for more: [https://discord.com/invite/q55gsH8z5F](https://discord.com/invite/q55gsH8z5F)":
            print("ChatGPT: Character limit error occurred. Ask the same question again.")
            continue
        convo_logs.append({"role": "assistant", "content": ai_response})
        print(f'ChatGPT: {ai_response}')
    except Exception as e:
        logging.error(f'An unexpected error occured while trying to contact the ChatGPT api: {e}')
        print('ChatGPT: An error has occured, please try again.')

    save_convo_logs()