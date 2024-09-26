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
config_file = os.path.join(log_directory, "config.json")
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

def load_settings():
    try:
        with open(config_file, 'r') as file:
            settings = json.load(file)
            return settings
    except FileNotFoundError:
        logging.info('Config file not found. Using default settings.')
        return {'current_model': 'gpt-4-turbo', 'autosave': True}
    except json.JSONDecodeError:
        logging.error('Error decoding config file. Using default settings')
        return {'current_model': 'gpt-4-turbo', 'autosave': True}
def save_settings(settings):
    try:
        with open(config_file, 'w') as file:
            json.dump(settings, file, indent=4)
    except Exception as e:
        logging.error(f'Failed to save settings: {e}')

user_settings = load_settings()
current_model = user_settings.get('current_model', 'gpt-4-turbo')
autosave = user_settings.get('autosave', True)


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

print('🤖 PyGPT V1.3')
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
        - 'autosave [on or off]': Toggle autosave config settings, default is on.
        - 'save config': Saves config settings if you have autosave disabled.
        """
        print(help_text)
        continue

    if user_input.lower().startswith('model '):
        new_model = user_input.split(' ', 1)[1]
        if new_model in available_models and new_model != current_model:
            current_model = new_model
            user_settings['current_model'] = current_model
            if autosave:
                save_settings(user_settings)
            print(f'ChatGPT: Model switched to {current_model}.')
            logging.info(f'GPT model successfully switched to {current_model}')
        elif new_model in available_models and new_model == current_model:
            print(f'ChatGPT: {new_model} is already selected!')
        else:
            print('ChatGPT: Invalid model name.')
        continue

    if user_input.lower().startswith('autosave '):
        autosavechoice = user_input.split(' ', 1)[1]
        if autosavechoice in ['on','off']:
            if autosavechoice == 'on' and autosave:
                print('ChatGPT: Autosave is already enabled!')
                continue
            if autosavechoice == 'off' and not autosave:
                print('ChatGPT: Autosave is already disabled!')
                continue
            autosave = True if autosavechoice == 'on' else False
            user_settings['autosave'] = autosave
            save_settings(user_settings)
            print(f"ChatGPT: Autosave is now {'enabled' if autosave else 'disabled'}.")
            logging.info(f'Autosaved {'enabled' if autosave else 'disabled'}')
        else:
            print("ChatGPT: Invalid setting for autosave. Your options are 'on' or 'off'.")
        continue

    if user_input.lower() == 'save config':
        save_settings(user_settings)
        print(f'ChatGPT: Config settings were successfully saved!')
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
        logging.error(f'An unexpected error occurred while trying to contact the ChatGPT API: {e}')
        print('ChatGPT: An error has occurred, please try again.')

    save_convo_logs()