from cryptography.fernet import Fernet
from os import listdir, rename, getenv, path
from dotenv import load_dotenv
from datetime import date


def write_key():
    # Generates a key and saves it into a file
    
    key = Fernet.generate_key()
    
    with open("key.key", "wb") as key_file:
        key_file.write(key)
  
   
def load_key():
    # Loads the key from the current directory named 'key.key'
    
    return open("key.key", "rb").read()
    
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
        
    
def decrypt(filename, key):
    # Given a filename (str) and key(bytes), it decrypts the file and write it
    
    f = Fernet(key)
    
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
        
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)
    
    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)
    
def get_files(flag):
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
    
def check_if_password_correct():
    load_dotenv()
    password = getenv("PASSWORD")

    print("Enter the password to enter:")
    userPassword = input()
    
    if password != userPassword:
        return False
        
    return True
    
def create_file():
    load_dotenv()
    today = date.today()
    
    dateFormatted = today.strftime("%d.%m.%y")
    
    filename = dateFormatted + ".txt"
    folderPath = getenv("FOLDERPATH")
    filePath = folderPath + "/" + filename
    
    if check_if_file_exists(filePath):
        print("File already exists")
    else:
        file = open(filePath, "w")
        file.close()
        
        print(f"File {filename} created")
    
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
        create_file()
        exit(1)
    
    if check_if_password_correct() == False:
        print("Wrong password")
        exit(1)
    
    if answer == "1":
        files = get_files("decrypted")
        action = "encrypt"
    elif answer == "2":
        files = get_files("encrypted")
        action = "decrypt"
        
    for file in files:
        print(file)
        
    print(f"Do you really want to {action} all these {len(files)} files?")
    print("y/n")
    
    answer = input()
    
    if answer == "y":
        if check_if_file_exists("key.key") == False:
            print("hey")
            write_key()
        
        key = load_key()
        
        folderPath = getenv("FOLDERPATH")
        for file in files:
            filePath = folderPath + "/" + file
            if action == "encrypt":
                encrypt(filePath, key)
            elif action == "decrypt":
                decrypt(filePath, key)
                
            rename_file(filePath, action)
            print(f"{action}ing {file}")
            
        print(f"{len(files)} files {action}ed")
        
        # TODO: legg ut paa github
        # lag key fra password - https://www.youtube.com/watch?v=hsRR9-aZZ4Q&ab_channel=PracticalPythonSolutions
    
    