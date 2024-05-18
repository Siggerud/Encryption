from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from base64 import urlsafe_b64encode
from os import listdir, rename, getenv, path
from dotenv import load_dotenv
from datetime import date 
from getpass import getpass
import subprocess
   
"""
Encrypts the filename with given key
"""
def encrypt(filename, key):
    # Given a filename (str) and key (bytes), it encrypts the file and write it
    
    f = Fernet(key)
    
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
        
    encrypted_data = f.encrypt(file_data)
    
    # write the encrypted file
    with open(filename, "wb") as file:
        file.write(encrypted_data)
        
"""
Decrypts the filename with given key
"""  
def decrypt(filename, key):
    # Given a filename (str) and key(bytes), it decrypts the file and write it
    
    f = Fernet(key)
    
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
        
    # decrypt data, return False if wrong key is given
    try:
        decrypted_data = f.decrypt(encrypted_data)
    except InvalidToken:
        return False
    
    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)
        
    # return True if no errors have happened
    return True
    
"""
Gets either the encrypted or decrypted files 
"""
def get_files(flag):
    load_dotenv()
    folderPath = getenv("FOLDERPATH")
    print(folderPath)
    wantedFiles = []
    allFiles = listdir(folderPath)
    
    for file in allFiles:
        if flag == "encrypted":
            if "_Encrypted.txt" in file:
                wantedFiles.append(file)
        elif flag == "decrypted":
            if "_Encrypted.txt" not in file:
                wantedFiles.append(file)
                
    return wantedFiles

"""
Renames files to mark them as either encrypted or not
"""  
def rename_file(oldPath, action):
    if action == "encrypt":
        oldEnding = ".txt"
        newEnding = "_Encrypted.txt"
    elif action == "decrypt":
        oldEnding = "_Encrypted.txt"
        newEnding = ".txt"
        
    index = oldPath.find(oldEnding)
    newPath = oldPath[:index] + newEnding
    
    rename(oldPath, newPath)
    
"""
Generate key from user password
"""
def get_key(password):
    load_dotenv()

    salt = bytes(getenv("SALT"), 'utf-8')
    
    kdf = PBKDF2HMAC (
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
)
    key = urlsafe_b64encode(kdf.derive(password)).decode()
    
    return key

"""
Gets a password for either encrypting or decrypting
"""    
def get_password_from_user(action): 
    if action == "encrypt":
        prompt = "Set the password for encryption: "
    elif action == "decrypt":
        prompt = "Enter the password for decryption: "
    userPassword = getpass(prompt)
    
    return userPassword.encode()
    
def open_file(filePath):
    load_dotenv()
    
    notepadPath = getenv("NOTEPADFILEPATH")
    subprocess.run([notepadPath, filePath])
    
def get_file_path():
    load_dotenv()
    today = date.today()
    
    dateFormatted = today.strftime("%d.%m.%y")
    
    filename = dateFormatted + ".txt"
    folderPath = getenv("FOLDERPATH")
    filePath = folderPath + "/" + filename
    
    return filePath
    
"""
Creates a file with todays date in filename
"""   
def create_file(filePath):
    if check_if_file_exists(filePath):
        print("File already exists")
        print("Do you want to overwrite file?")
        print("y/n")
        
        answer = input()
        if answer != "y":
            return False
          
    file = open(filePath, "w")
    file.close()
    
    print(f"File created")
    
    return True
    
"""
Checks if the file exists
"""
def check_if_file_exists(filepath):
    if path.exists(filepath):
        return True
    return False
        
                
if __name__ == '__main__':
    print("What do you want to do?")
    print("1. Encrypt files")
    print("2. Decrypt files")
    print("3. Create file")
    
    answer = input()
    
    if answer == "3":
        filePath = get_file_path()
        if create_file(filePath):
            open_file(filePath)
        exit(1)
    
    if answer == "1":
        files = get_files("decrypted")
        action = "encrypt"
    elif answer == "2":
        files = get_files("encrypted")
        action = "decrypt"
    else:
        print(f"{answer} not valid option")
        exit(1)
        
    for file in files:
        print(file)
        
    print(f"Do you really want to {action} all these {len(files)} files?")
    print("y/n")
    
    answer = input()
    
    if answer == "y":
        password = get_password_from_user(action)
        key = get_key(password)
        
        folderPath = getenv("FOLDERPATH")
        for file in files:
            filePath = folderPath + "/" + file
            if action == "encrypt":
                encrypt(filePath, key)
            elif action == "decrypt":
                success = decrypt(filePath, key)
                if success == False:
                    print("Wrong decryption key entered")
                    exit(1)
                
            rename_file(filePath, action)
            print(f"{action}ing {file}...")
            
        print(f"{len(files)} files {action}ed")
        

    
    