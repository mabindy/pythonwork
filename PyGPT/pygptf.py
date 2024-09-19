from g4f.client import Client

client = Client()
usingai = True
convo_logs = []
log_file = r"C:\Users\mberr954\Desktop\vscode projects\flippybot\pygptlogs.txt"

def load_convo_logs():
    try:
        with open(log_file, 'r') as file:
            logs = []
            for line in file:
                role, content = line.strip().split(': ', 1)  # Split line into role and content
                logs.append({"role": role, "content": content})  # Create a dictionary for each log
            return logs
    except FileNotFoundError:
        return []
    except ValueError:
        print("ChatGPT: There was an issue reading the logs file, so it has been reset. Logs saving is still in a buggy state right now.")
        return []
def save_convo_logs():
    with open(log_file, 'w') as file:
        for log in convo_logs:
            file.write(f"{log['role']}: {log['content']}\n")

convo_logs = load_convo_logs()

while usingai:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        usingai = False
        break
    if user_input.lower() in ['reset','new']:
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