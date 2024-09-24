import sys
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
current_model = 'gpt-4-turbo'
available_models = ['gpt-4-turbo', 'gpt-3.5-turbo', 'gpt-4']

os.makedirs(log_directory, exist_ok=True)

logging.basicConfig(
    filename=errlog_file,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    force=True
)

def on_exit():
    if sys.exc_info() == (None, None, None):
        logging.info('Program exited successfully.')
    else:
        print('ChatGPT: PyGPT has stopped unexpectedly.')
        logging.error('The program was terminated unexpectedly', exc_info=True)

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

print('🤖 PyGPT V1.2')
while usingai:
    user_input = input("You: ")
    if user_input.lower() in ['help', '?']:
        help_text = """
        Commands:
        - 'exit' or 'quit': Quit the program
        - 'reset' or 'new': Reset the conversation
        - 'help' or '?': Display this help message
        - 'model [model_name]': Switch ChatGPT model
        - 'models': Display available ChatGPT models
        - 'currentmodel': Display the currently selected model
        """
        print(help_text)
        continue

    if user_input.lower().startswith('model '):
        new_model = user_input.split(' ', 1)[1]
        if new_model in available_models:
            current_model = new_model
            print(f'ChatGPT: Model switched to {current_model}.')
            logging.info(f'GPT model successfully switched to {current_model}')
        else:
            print('ChatGPT: Invalid model name.')
        continue

    if user_input.lower() == 'models':
        print(f'ChatGPT: Available models are: {available_models}')
        continue

    if user_input.lower() == 'currentmodel':
        print(f'ChatGPT: The currently selected model is {current_model}.')
        continue

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
            model=current_model,
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