import sys, os, json

# Operating Systems
PLATFORMS = {
    "Windows":"win32",
    "MacOS":"darwin",
    "Linux":"linux"
}

user_datas = {
    "files":['data.txt', 'archived.txt', 'recycled.txt', 'user_settings.json'],
    "folders":['documents']
}

def WindowsUserDataInitialize(email):
    data, archived, recycled = user_datas["files"][0], user_datas["files"][1], user_datas["files"][2]
    initialization_command = f"""
    cd users/{email} && python -c "file = open('{data}', 'a').close()" && python -c "file = open('{archived}', 'a').close()" && python -c "file = open('{recycled}', 'a').close()" && python -c "file = open('user_settings.json', 'a').close()" """
    return initialization_command

def UnixKernelUserDataInitialize(email):
    data, archived, recycled = user_datas["files"][0], user_datas["files"][1], user_datas["files"][2]
    initialization_command = f"""
    cd users/{email} && python3 -c "file = open('{data}', 'a').close()" && python3 -c "file = open('{archived}', 'a').close()" && python3 -c "file = open('{recycled}', 'a').close() && python3 -c "file = open('user_settings.json', 'a').close()" """
    return initialization_command


def executePlatformCompatibleAuthCMD(email):
    '''
    This function will switch the command that is to be 
    performed by 'os.system' whenever a user has registered 
    an account to our firebase authentication database. It will
    create the required assets for each user, keeping everyone's 
    data private and secure from each other.
    '''
    if sys.platform.startswith(PLATFORMS["Windows"]): # If we are in Windows
        os.system(WindowsUserDataInitialize(email))
    elif sys.platform.startswith(PLATFORMS["MacOS"]) or sys.platform.startswith(PLATFORMS["linux"]): # Otherwise, if we are in MacOS or Linux
        # Linux & MacOS come with a pre-installed version of Python2 instead of Python3, so we will have to specify that here.
        os.system(UnixKernelUserDataInitialize(email))