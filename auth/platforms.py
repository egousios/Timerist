import sys, os

# Operating Systems
PLATFORMS = {
    "Windows":"win32",
    "MacOS":"darwin",
    "Linux":"linux"
}

def executePlatformCompatibleAuthCMD(email):
    '''
    This function will switch the command that is to be 
    performed by 'os.system' whenever a user has registered 
    an account to our firebase authentication database. It will
    create the required assets for each user, keeping everyone's 
    data private and secure from each other.
    '''
    if sys.platform.startswith(PLATFORMS["Windows"]): # If we are in Windows
        os.system(f"""cd users/{email} && mkdir database && python -c "file = open('data.txt', 'a').close()" && python -c "file=open('editor_settings.json', 'a').close(); " """)
    elif sys.platform.startswith(PLATFORMS["MacOS"]) or sys.platform.startswith(PLATFORMS["linux"]): # Otherwise, if we are in MacOS or Linux
        # Linux & MacOS come with a pre-installed version of Python2 instead of Python3, so we will have to specify that here.
        os.system(f"""cd users/{email} && mkdir database && python3 -c "file = open('data.txt', 'a').close()" && python3 -c "file=open('editor_settings.json', 'a').close(); " """)