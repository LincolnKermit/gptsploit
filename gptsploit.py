# Created by github.com/Genepix
# Last Modification by github.com/LincolnKermit

try:
    from flask import Flask, request, jsonify
    import subprocess, datetime, os, threading, time, sys
    from pyfiglet import Figlet
    from termcolor import colored
except ImportError as e:
    print("Erreur lors de l'importation d'une librairie : ", e)
    exit(1)
    
API_KEY = os.environ.get("API_KEY", "VOTRE_MOT_DE_PASSE")

app = Flask(__name__)

def print_banner(title):
    f = Figlet(font='slant')
    print_with_delay(colored(f.renderText(title), 'green'))

def print_with_delay(message, delay=0.003):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()
    
if len(API_KEY) < 8:
    print_with_delay(colored("API_KEY ou MOT DE PASSE INCORRECT", 'red'))
    exit(1)


def execute_command_in_thread(command, log_file_path):
    try:
        print_with_delay(colored(f"Exécution de la commande : {command}", 'yellow'))
        subprocess.run(command, shell=True, check=True)
        print_with_delay(colored(f"Commande terminée, résultats enregistrés dans {log_file_path}", 'blue'))
    except subprocess.CalledProcessError as e:
        print_with_delay(colored(f"Erreur lors de l'exécution de la commande : {e}", 'red'))

@app.route('/execute', methods=['POST'])

def execute_command():
    api_key = request.headers.get('X-API-KEY')
    if not api_key or api_key != API_KEY:
        return jsonify({"error": "Accès non autorisé"}), 401
        
    data = request.json
    command = data.get("command")

    if not command:
        return jsonify({"error": "No command provided"}), 400

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_path = f"logs/log_{timestamp}.txt"
    command_with_log_path = command.replace("[log_path]", log_file_path)

    thread = threading.Thread(target=execute_command_in_thread, args=(command_with_log_path, log_file_path))
    thread.start()

    time.sleep(4)

    if os.path.exists(log_file_path) and os.path.getsize(log_file_path) > 0:
        with open(log_file_path, 'r') as file:
            content = file.read()
        return jsonify({f"log_content from {log_file_path} (TOUJOURS utiliser le fichier de log d'origine pour consulter le résultat d'un scan ou d'une commande)": content}), 200
    else:
        return jsonify({"message": f"La commande a été executée, les resultats seront disponibles dans {log_file_path}. l'utilisateur peut demander les résultats rapidement"}), 202

if __name__ == '__main__':
	print_banner('GPTSPLOIT')
	print("By Genepix\n\n")
	app.run(debug=True, host='0.0.0.0', port=1337)
