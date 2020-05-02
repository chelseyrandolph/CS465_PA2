import sys
import os

#global variables
#checks to see if a user is logged in
userLoginFlag = 0
#keeps track of the lines of instructions
lineOfInstruction = 0
#list of groups with their members
listOfGroups = list()
#list of group names only
groupNames = list()

files = list()
#keeps track of the current user logged in
currentUser = ''
#counts the lines in the instructions file
lineCount = 0
#the files that users are not allowed to access
specialFiles = ["groups.txt", "files.txt", "accounts.txt", "audit.txt"]

#_______________________________________________________________________________________________________________________
def main():
    global lineOfInstruction, lineCount, specialFiles
    #Created necessary files for program
    for path in specialFiles:
        try:
            file_test = open(path)
            file_test.close()
        except FileNotFoundError:
            createFile = open(path, "w+")
            createFile.close()
    #increases the line of instruction everytime main is called
    #used to make sure the first line of instruction is adding a root user
    lineOfInstruction = lineOfInstruction + 1
    #getting the arguments from the terminal line
    arguments = getUserInput()
    #opens the instruction file
    file = open(arguments[1], "r")
    lines = file.readlines()
    file.close()
    #goes through each line in the instruction file to execute that instruction
    for x in range(lineCount, len(lines)):
        command = lines[x].split()
        lineCount = lineCount + 1
        #only used to get the text from the write instruction
        text = ''
        getCommand(command, text)
#_______________________________________________________________________________________________________________________
#This function gets the command from the instruction text file
#It finds the command in this if/elif/else statement and execute that command
def getCommand(command, text):
    if command[0] == 'useradd':
        if len(command) == 3:
            useradd(command[1], command[2])
        else:
            print("ERROR: Invalid number of arguments.")
            writeToLog("ERROR: number of arguments.\n")
            main()

    elif command[0] == 'login':
        if len(command) == 3:
            login(command[1], command[2])
        else:
            print("ERROR: Invalid number of arguments.")
            writeToLog("ERROR: number of arguments.\n")
            main()

    elif command[0] == 'logout':
        if len(command) == 1:
            logout()
        else:
            print("ERROR: Invalid number of arguments.")
            writeToLog("ERROR: number of arguments.\n")
            main()

    elif command[0] == 'groupadd':
        if len(command) == 2:
            groupadd(command[1])
        else:
            print("ERROR: Invalid number of arguments.")
            writeToLog("ERROR: number of arguments.\n")
            main()

    elif command[0] == 'usergrp':
        if len(command) == 3:
            usergrp(command[1], command[2])
        else:
            print("ERROR: Invalid number of arguments.")
            writeToLog("ERROR: number of arguments.\n")
            main()

    elif command[0] == 'mkfile':
        if len(command) == 2:
            mkfile(command[1])
        else:
            print("ERROR: Invalid number of arguments.")
            writeToLog("ERROR: number of arguments.\n")
            main()

    elif command[0] == 'chmod':
        if len(command) == 5:
            chmod(command[1], command[2], command[3], command[4])
        else:
            print("ERROR: Invalid number of arguments.")
            writeToLog("ERROR: number of arguments.\n")
            main()

    elif command[0] == 'chown':
        if len(command) == 3:
            chown(command[1], command[2])
        else:
            print("ERROR: Invalid number of arguments.")
            writeToLog("ERROR: number of arguments.\n")
            main()

    elif command[0] == 'chgrp':
        if len(command) == 3:
            chgrp(command[1], command[2])
        else:
            print("ERROR: Invalid number of arguments.")
            writeToLog("ERROR: number of arguments.\n")
            main()

    elif command[0] == 'read':
        if len(command) == 2:
            read(command[1])
        else:
            print("ERROR: Invalid number of arguments.")
            writeToLog("ERROR: number of arguments.\n")
            main()

    elif command[0] == 'write':
        if len(command) > 2:
            for x in range(2, len(command)):
                text = text + command[x] + " "
            write(command[1], text)
        else:
            print("ERROR: Invalid number of arguments.")
            writeToLog("ERROR: number of arguments.\n")
            main()

    elif command[0] == 'execute':
        if len(command) == 2:
            execute(command[1])
        else:
            print("ERROR: Invalid number of arguments.")
            writeToLog("ERROR: number of arguments.\n")
            main()

    elif command[0] == 'ls':
        if len(command) == 2:
            ls(command[1])
        else:
            print("ERROR: Invalid number of arguments.")
            writeToLog("ERROR: number of arguments.\n")
            main()

    elif command[0] == 'end':
        if len(command) == 1:
            end()
        else:
            print("ERROR: Invalid number of arguments.")
            writeToLog("ERROR: number of arguments.\n")
            main()

    else:
        print("ERROR: Invalid command.")
        writeToLog("ERROR: Invalid command.\n")
        main()
#_______________________________________________________________________________________________________________________
#This function gets the users input from the terminal line
def getUserInput():
    input = sys.argv
    return input
#_______________________________________________________________________________________________________________________
#This functions writes to the audit.txt file
def writeToLog(text):
    auditLog = open("audit.txt", "a+")
    auditLog.write(text)
    auditLog.close()
#_______________________________________________________________________________________________________________________
# login { username password }
def login(username, password):
    global lineOfInstruction, currentUser,userLoginFlag
    #The first line of instruction must be creating a super user
    if lineOfInstruction == 1:
        print("ERROR: The first command must be creating a super user.")
        writeToLog("ERROR: The first command must be creating a super user.\n")
        exit()
    #Checks to see if a user is already logged in
    if userLoginFlag == 1:
        print("Login failed: simultaneous login not permitted")
        writeToLog("Login failed: simultaneous login not permitted\n")
        main()
    loginFlag = 0
    with open("accounts.txt", "r") as accounts:
        #Getting a user from the accounts.txt file
        for line in accounts:
            user = line.split(",")
            userPassword = user[1]
            #if the username and password match it logs them in
            if username == user[0] and password == userPassword[:-1]:
                if username == 'root':
                    writeToLog("User root logged in\n")
                    print("User root logged in")
                    currentUser = username
                    userLoginFlag = 1
                    main()
                print("User " + username + " logged in")
                writeToLog("User " + username + " logged in\n")
                loginFlag = 1
                userLoginFlag = 1
                currentUser = username
                main()
    #if the username or password doesn't match a user in the accounts.txt file, it prints an error
    if loginFlag == 0:
        print("Login failed: invalid username or password ")
        writeToLog("Login failed: invalid username or password\n")
        main()
#_______________________________________________________________________________________________________________________
# logout
def logout():
    global userLoginFlag, currentUser, lineOfInstruction
    if lineOfInstruction == 1:
        print("ERROR: The first command must be creating a super user.")
        writeToLog("ERROR: The first command must be creating a super user.\n")
        exit()
    #If the program receives the logout command without a user being logged in, it throws an error
    if userLoginFlag == 0:
        print("Invalid action: A user must be logged in to logout.")
        writeToLog("Invalid action: A user must be logged in to logout.\n")
        main()
    #if a user is logged in, it resets the userLoginFlag
    else:
        userLoginFlag = 0
        print('User ' + currentUser + ' logged out')
        writeToLog('User ' + currentUser + ' logged out\n')
        main()
#_______________________________________________________________________________________________________________________
# useradd { username password }
def useradd(username, password):
    global currentUser, lineOfInstruction, userLoginFlag
    if lineOfInstruction == 1 and username != 'root':
        print("ERROR: root must be the first user created")
        writeToLog("ERROR: root must be the first user created\n")
    #if there aren't any users in the system, it sets the current user to the username it's trying to add
    if currentUser == '' and username == 'root':
        currentUser = username
    accounts = open("accounts.txt", "r")
    accountsContent = accounts.read()
    #Checking to make sure root is logged in
    if currentUser == 'root':
        # if the current user is root and is already in the system, it throws an error because there can't be more than one root
        if username == 'root' and username in accountsContent:
            print("Invalid action: the user '" + username + "' already exists.\nPlease log in.")
            writeToLog("Invalid action: the user " + username + " already exists.\nPlease log in.\n")
            main()
        # if the username is not in the accounts.txt file, it checks to see if the username and password are valid entries
        elif username not in accountsContent:
            illegalUsernameCharacters = ['/', ':', '/f', '/t', '/n', '/v', ' ']
            illegalPasswordCharacters = ['/f', '/t', '/n', '/v', ' ']

            validUsernameFlag = 0
            validPasswordFlag = 0
            # checking to see if any invalid characters are in the username or the username is greater than 30 ASCII characters
            for char in illegalUsernameCharacters:
                if char in username or len(username) > 30:
                    print("Invalid character: " + char + " within username.\nPlease only use up to 30 ASCII characters excluding /, :, or whitespace characters.")
                    writeToLog("Invalid username.\n")
                    validUsernameFlag = 1
                    main()
            # checking to see if any invalid characters are in the password or the password is greater than 30 ASCII characters
            for char in illegalPasswordCharacters:
                if char in password or len(password) > 30:
                    print("Invalid character: " + char + " within password.\nPlease only use up to 30 ASCII characters excluding whitespace characters.")
                    writeToLog("Invalid password.\n")
                    validPasswordFlag = 1
                    main()
            # If neither throw an error, it attempts to add a user
            if validUsernameFlag == 0 and validPasswordFlag == 0:
                # if the user is not in the system, it adds them
                if username not in accountsContent:
                    accountsAppend = open("accounts.txt", "a+")
                    accountsAppend.write(username + "," + password + "\n")
                    accountsAppend.close()
                    if username == 'root':
                        print("User root created")
                        writeToLog("User root created\n")
                        main()
                    writeToLog("User " + username + " created\n")
                    print("User " + username + " created")
                else:
                    print("User is already in the system.")
                    writeToLog("User is already in the system.\n")
            main()
        # if the username is already in the system, it throws an error
        elif username in accountsContent:
            print("ERROR: user " + username + " already exists")
            writeToLog("ERROR: user " + username + " already exists\n")
            main()
    # only the root user is allowed to add users
    else:
        print("The root user must be logged in to complete this action.")
        writeToLog("The root user must be logged in to add a user.\n")
        main()
#_______________________________________________________________________________________________________________________
# groupadd { groupname }
def groupadd(groupname):
    global lineOfInstruction, currentUser, listOfGroups, userLoginFlag
    #The first line of instruction must be creating a root user
    if lineOfInstruction == 1:
        print("ERROR: The first command must be creating a super user.")
        writeToLog("ERROR: The first command must be creating a super user.\n")
        exit()
    if currentUser == 'root' and userLoginFlag == 1:
        if groupname == 'nil':
            # 'nil' is reserved for files that don't have group names
            print("Invalid action: Group name cannot be named 'nil'.")
            writeToLog("Invalid action: Group name cannot be named 'nil'.\n")
            main()
        # if the group name doesn't exist, add it
        if groupname not in listOfGroups:
            writeToLog("Group " + groupname + " created\n")
            print("Group " + groupname + " created")
            listOfGroups.append(groupname)
            groupNames.append(groupname)
            groupFile = open("groups.txt", "a+")
            groupFile.write(groupname + "\n")
            groupFile.close()
            main()
        # the group already exists and an error is thrown
        else:
            print("Error: group " + groupname + " already exists")
            writeToLog("Error: group " + groupname + " already exists\n")
            main()
        # only the root user can create groups
    else:
        print("The root user must be logged in to complete this action.")
        writeToLog("The root user must be logged in to add a group.\n")
        main()
#_______________________________________________________________________________________________________________________
# usergrp { username groupname }
def usergrp(username, groupname):
    global lineOfInstruction, currentUser,userLoginFlag
    newGroupUsers = ''
    # The first line of instruction must be creating a root user
    if lineOfInstruction == 1:
        print("ERROR: The first command must be creating a super user.")
        writeToLog("ERROR: The first command must be creating a super user.\n")
        exit()
    if currentUser == 'root' and userLoginFlag == 1:
        users = open("accounts.txt", "r")
        accountInfo = users.read()
        #checking to see if the group name exists
        if groupname not in groupNames:
            print("ERROR: Group name not found.")
            writeToLog("ERROR: Group name not found.\n")
            main()
        #checking to make sure the user exists
        elif username not in accountInfo:
            print("ERROR: Username not found.")
            writeToLog("ERROR: Username not found.\n")
            main()
        #adding user to a group
        else:
            for group in groupNames:
                if groupname in group:
                    index = groupNames.index(group)
                    newGroupUsers = listOfGroups[index] + " " + username
                    listOfGroups[index] = newGroupUsers
            print("User " + username + " added to group " + groupname)
            writeToLog("User " + username + " added to group " + groupname+ "\n")
            file = open("groups.txt", "r")
            lines = file.readlines()
            file.close()
            #a user can only be added to a group if the group file isn't empty
            if lines == []:
                print("ERROR: groups.txt is empty.")
                writeToLog("ERROR: groups.txt is empty.\n")
                main()
            fileTxt = open("groups.txt", "w")
            fileTxt.write('')
            fileTxt.close()
            filesText = open("groups.txt", "a+")
            for line in lines:
                if groupname not in line:
                    filesText.write(line[:-1] + "\n")
                else:
                    filesText.write(newGroupUsers + "\n")
            filesText.close()
        main()
    #only the root user is allowed to add users to group
    else:
        print("The root user must be logged in to complete this action.")
        writeToLog("The root user must be logged in to add a group.\n")
        main()
#_______________________________________________________________________________________________________________________
# mkfile { filename }
def mkfile(filename):
    global files, currentUser, specialFiles
    if userLoginFlag == 1:
        # The first line of instruction must be creating a root user
        if lineOfInstruction == 1:
            print("ERROR: The first command must be creating a super user.")
            writeToLog("ERROR: The first command must be creating a super user.\n")
            exit()
        #users are not allowed to access any of the special files
        if filename in specialFiles:
            print("ERROR: References forbidden file.")
            writeToLog("ERROR: References forbidden file.\n")
            main()
        # making sure the file does not exists
        if not os.path.exists(filename):
            createFile = open(filename, "w+")
            createFile.close()
            files.append(filename)
            print("File " + filename + " with owner " + currentUser + " and default permissions created")
            writeToLog("File " + filename + " with owner " + currentUser + " and default permissions created\n")
            filesText = open("files.txt", "a+")
            filesText.write(filename + ": " + currentUser + " nil rw- --- ---\n")
            filesText.close()
            main()
        #the file already exists
        else:
            print("ERROR: " + filename + " already exists.")
            writeToLog("ERROR: " + filename + " already exists.\n")
            main()
    # a user must be logged in to create a file
    else:
        print("ERROR: A user must be logged in to complete to action.")
        writeToLog("ERROR: A user must be logged in to complete to action. \n")
#_______________________________________________________________________________________________________________________
# chmod { filename rwx rwx rwx }
def chmod(filename, owner, group, others):
    global currentUser, userLoginFlag, specialFiles
    lineToChange = ''
    linesToSave = []
    # The first line of instruction must be creating a root user
    if lineOfInstruction == 1:
        print("ERROR: The first command must be creating a super user.")
        writeToLog("ERROR: The first command must be creating a super user.\n")
        exit()
    # users are not allowed to access any of the special files
    if filename in specialFiles:
        print("ERROR: References forbidden file.")
        writeToLog("ERROR: References forbidden file.\n")
        main()
    # Checking to make sure that a user is logged in before attempting to complete the action.
    if userLoginFlag == 1:
        file = open("files.txt", "r")
        lines = file.readlines()
        file.close()
        try:
            # making sure the file exists
            file = open(filename)
            file.close()
            if lines == []:
                print("ERROR: " + filename + " does not exist.")
                writeToLog("ERROR: " + filename + " does not exist.\n")
                main()
            for line in lines:
                # filename owner group permissions (owner group others)
                info = line.split()
                #only the owner or root user can change permissions of a file
                if info[1] != currentUser and info[1] != 'root':
                    print("ERROR in chmod: Owner of file or root user must be logged it to complete this action.")
                    writeToLog("ERROR in chmod: Owner of file or root user must be logged in to change file permissions.\n")
                    main()
                else:
                    if filename not in line:
                        linesToSave.append(line)
                    else:
                        lineToChange = info
            txtFile = open("files.txt", "w")
            for l in linesToSave:
                txtFile.write(l)
            txtFile.close()
            # changing the permissions of the file
            filesText = open("files.txt", "a+")
            filesText.write(
                filename + ": " + lineToChange[1] + " nil " + owner + " " + group + " " + others + "\n")
            filesText.close()
            print("Permissions for " + filename + " set to " + owner + " " + group + " " + others + " by " +
                  lineToChange[1])
            writeToLog(
                "Permissions for " + filename + " set to " + owner + " " + group + " " + others + " by " +
                lineToChange[1] + "\n")
            main()
        #throw an error if the file doesn't exist
        except FileNotFoundError:
            print("ERROR with chmod: File " + filename + " does not exist.")
            writeToLog("ERROR with chmod: File " + filename + " does not exist.\n")
            main()
    #a user must be logged in to change permissions on a file
    else:
        print("ERROR: A user must be logged in to complete to action.")
        writeToLog("ERROR: A user must be logged in to complete to action. \n")
#_______________________________________________________________________________________________________________________
# chown { filename username }
def chown(filename, username):
    global currentUser, specialFiles, userLoginFlag
    # The first line of instruction must be creating a root user
    if lineOfInstruction == 1:
        print("ERROR: The first command must be creating a super user.")
        writeToLog("ERROR: The first command must be creating a super user.\n")
        exit()
    # users are not allowed to access any of the special files
    if filename in specialFiles:
        print("ERROR: References forbidden file.")
        writeToLog("ERROR: References forbidden file.\n")
        main()
    info = ''
    # Checking to make sure that root is logged in before attempting to complete the action.
    if currentUser == 'root' and userLoginFlag == 1:
        try:
            # making sure the file exists
            file = open(filename)
            file.close()
            users = open("accounts.txt", "r")
            accountInfo = users.read()
            #user not found in system
            if username not in accountInfo:
                print("ERROR: Username not found.")
                writeToLog("ERROR: Username not found.\n")
                main()
            else:
                file = open("files.txt", "r")
                lines = file.readlines()
                file.close()
                #if there are not files, root can't update the owner
                if lines == []:
                    print("ERROR: " + filename + " does not exist.")
                    writeToLog("ERROR: " + filename + " does not exist.\n")
                    main()
                fileTxt = open("files.txt", "w")
                fileTxt.write('')
                fileTxt.close()
                filesText = open("files.txt", "a+")
                for line in lines:
                    if filename not in line:
                        filesText.write(line)
                    else:
                        # filename owner group permissions (owner group others)
                        info = line.split()
                if info != '':
                    #changing the owner of the file
                    filesText.write(info[0] + " " + username + " " + info[2] + " " + info[3] + " " + info[4] + " " + info[5] + "\n")
                    filesText.close()
                    print("Owner of " + filename + " changed to " + username)
                    writeToLog("Owner of " + filename + " changed to " + username + "\n")
                main()
        # throw an error if the file doesn't exist
        except FileNotFoundError:
            print("ERROR with chown: File " + filename + " does not exist.")
            writeToLog("ERROR with chown: File " + filename + " does not exist.\n")
            main()
#_______________________________________________________________________________________________________________________
# chgrp { filename groupname }
def chgrp(filename, groupname):
    groupUsers = list()
    global userLoginFlag, groupNames, specialFiles, currentUser
    # The first line of instruction must be creating a root user
    if lineOfInstruction == 1:
        print("ERROR: The first command must be creating a super user.")
        writeToLog("ERROR: The first command must be creating a super user.\n")
        exit()
    # users are not allowed to access any of the special files
    if filename in specialFiles:
        print("ERROR: References forbidden file.")
        writeToLog("ERROR: References forbidden file.\n")
        main()
    info = ''
    # Checking to make sure that a user is logged in before attempting to complete the action.
    if userLoginFlag == 1:
        try:
            # making sure the file exists
            file = open(filename)
            file.close()
            for l in listOfGroups:
                if groupname in l:
                    groupUsers = l.split()
            #only a user of the group or root can change the group of file
            if currentUser not in groupUsers and currentUser != 'root':
                print("ERROR with chgrp: User " + currentUser + " is not a member of group " + groupname)
                writeToLog("ERROR with chgrp: User " + currentUser + " is not a member of group " + groupname + "\n")
                main()
            else:
                #group name doesn't exist
                if groupname not in groupNames:
                    print("ERROR with chgrp: " + groupname + " not found.")
                    writeToLog("ERROR with chgrp: " + groupname + " not found.\n")
                    main()
                else:
                    file = open("files.txt", "r")
                    lines = file.readlines()
                    file.close()
                    #a file must exist in files.txt to change its group
                    if lines == []:
                        print("ERROR with chgrp: " + filename + " does not exist.")
                        writeToLog("ERROR with chgrp: " + filename + " does not exist.\n")
                        main()
                    fileTxt = open("files.txt", "w")
                    fileTxt.write('')
                    fileTxt.close()
                    filesText = open("files.txt", "a+")
                    for line in lines:
                        if filename not in line:
                            filesText.write(line)
                        else:
                            info = line.split()
                    if info != '':
                        #changing the group of a file
                        filesText.write(info[0] + " " + info[1] + " " + groupname + " " + info[3] + " " + info[4] + " " + info[5] + "\n")
                        filesText.close()
                        print("Group for " + filename + " changed to " + groupname + " by " + currentUser)
                        writeToLog("Group for " + filename + " changed to " + groupname + " by " + currentUser + "\n")
                    main()
        # throw an error if the file doesn't exist
        except FileNotFoundError:
            print("ERROR with chgrp: File " + filename + " does not exist.")
            writeToLog("ERROR with chgrp: File " + filename + " does not exist.\n")
            main()
#_______________________________________________________________________________________________________________________
# read { filename }
def read(filename):
    global currentUser, userLoginFlag, specialFiles
    # The first line of instruction must be creating a root user
    if lineOfInstruction == 1:
        print("ERROR: The first command must be creating a super user.")
        writeToLog("ERROR: The first command must be creating a super user.\n")
        exit()
    # users are not allowed to access any of the special files
    if filename in specialFiles:
        print("ERROR: References forbidden file.")
        writeToLog("ERROR: References forbidden file.\n")
        main()
    # Checking to make sure that a user is logged in before attempting to complete the action.
    if userLoginFlag == 1:
        try:
            # making sure the file exists
            file = open(filename)
            file.close()
            file = open("files.txt", "r")
            files = file.readlines()
            file.close()
            groups = open("groups.txt", "r")
            groupText = groups.readlines()
            groups.close()
            for line in files:
                if filename in line:
                    # filename owner group permissions (owner group others)
                    info = line.split()
                    for group in groupText:
                        # root can do anything besides login for another user
                        if currentUser == 'root':
                            filetoRead = open(filename, "r")
                            contents = filetoRead.read()
                            filetoRead.close()
                            print("User " + currentUser + " reads " + filename + " as : " + contents + "\n")
                            writeToLog("User " + currentUser + " reads " + filename + " as : " + contents + "\n")
                            main()
                        # the current user is the owner and the owner has read permissions
                        elif currentUser in info[1]:
                            if 'r' in info[3]:
                                filetoRead = open(filename, "r")
                                contents = filetoRead.read()
                                filetoRead.close()
                                print("User " + currentUser + " reads " + filename + " as : " + contents + "\n")
                                writeToLog("User " + currentUser + " reads " + filename + " as : " + contents + "\n")
                                main()
                            # deny access to the file
                            else:
                                print("User " + currentUser + " denied read access to " + filename)
                                writeToLog("User " + currentUser + " denied read access to " + filename + "\n")
                                main()
                        # current user is not the owner, the current line contains the group name, the current user is in that group, the group has read permissions
                        elif currentUser not in info[1] and info[2] in group and currentUser in group:
                            if 'r' in info[4]:
                                filetoRead = open(filename, "r")
                                contents = filetoRead.read()
                                filetoRead.close()
                                print("User " + currentUser + " reads " + filename + " as : " + contents + "\n")
                                writeToLog("User " + currentUser + " reads " + filename + " as : " + contents + "\n")
                                main()
                            # deny access to the file
                            else:
                                print("User " + currentUser + " denied read access to " + filename)
                                writeToLog("User " + currentUser + " denied read access to " + filename + "\n")
                                main()
                        # current user is not the owner, the file has others read permissions
                        elif currentUser not in info[1] and currentUser not in group:
                            if 'r' in info[5]:
                                filetoRead = open(filename, "r")
                                contents = filetoRead.read()
                                filetoRead.close()
                                print("User " + currentUser + " reads " + filename + " as : " + contents + "\n")
                                writeToLog("User " + currentUser + " reads " + filename + " as : " + contents + "\n")
                                main()
                            #deny access to the file
                            else:
                                print("User " + currentUser + " denied read access to " + filename)
                                writeToLog("User " + currentUser + " denied read access to " + filename + "\n")
                                main()
            main()
        # throw an error if the file doesn't exist
        except FileNotFoundError:
            print("ERROR: File " + filename + " does not exist.")
            writeToLog("ERROR: File " + filename + " does not exist.\n")
            main()
    # a user must be logged in to read a file
    else:
        print("ERROR: A user must be logged in to complete to action.")
        writeToLog("ERROR: A user must be logged in to complete to action. \n")
        main()
#_______________________________________________________________________________________________________________________
# write { filename }
def write(filename, text):
    global currentUser, userLoginFlag, specialFiles
    # The first line of instruction must be creating a root user
    if lineOfInstruction == 1:
        print("ERROR: The first command must be creating a super user.")
        writeToLog("ERROR: The first command must be creating a super user.\n")
        exit()
    # users are not allowed to access any of the special files
    if filename in specialFiles:
        print("ERROR: References forbidden file.")
        writeToLog("ERROR: References forbidden file.\n")
        main()
    # Checking to make sure that a user is logged in before attempting to complete the action.
    if userLoginFlag == 1:
        try:
            # making sure the file exists
            file = open(filename)
            file.close()
            file = open("files.txt", "r")
            files = file.readlines()
            file.close()
            groups = open("groups.txt", "r")
            groupText = groups.readlines()
            groups.close()
            for line in files:
                if filename in line:
                    # filename owner group permissions (owner group others)
                    info = line.split()
                    for group in groupText:
                        # root can do anything besides login for another user
                        if currentUser == 'root':
                            textToWrite = open(filename, "a+")
                            textToWrite.write("\n" + text)
                            textToWrite.close()
                            print("File " + filename + " wrote to " + currentUser)
                            writeToLog("File " + filename + " wrote to " + currentUser + "\n")
                            main()
                        # the current user is the owner and the owner has write permissions
                        elif currentUser in info[1]:
                            if 'w' in info[3]:
                                textToWrite = open(filename, "a+")
                                textToWrite.write("\n" + text)
                                textToWrite.close()
                                print("User " + currentUser + " wrote to " + filename + ": " + text + "\n")
                                writeToLog("User " + currentUser + " wrote to " + filename + ": " + text + "\n")
                                main()
                            # deny the user access
                            else:
                                print("User " + currentUser + " denied write access to " + filename)
                                writeToLog("User " + currentUser + " denied write access to " + filename + "\n")
                                main()
                        # current user is not the owner, the current line contains the group name, the current user is in that group, the group has write permissions
                        elif currentUser not in info[1] and info[2] in group and currentUser in group:
                            if'w' in info[4]:
                                textToWrite = open(filename, "a+")
                                textToWrite.write("\n" + text)
                                textToWrite.close()
                                print("User " + currentUser + " wrote to " + filename + ": " + text + "\n")
                                writeToLog("User " + currentUser + " wrote to " + filename + ": " + text + "\n")
                                main()
                            # deny the user access
                            else:
                                print("User " + currentUser + " denied write access to " + filename)
                                writeToLog("User " + currentUser + " denied write access to " + filename + "\n")
                                main()
                        # current user is not the owner, the current user is not in the group, the file has others write permissions
                        elif currentUser not in info[1] and currentUser not in group:
                            if'w' in info[5]:
                                textToWrite = open(filename + "", "a+")
                                textToWrite.write("\n" + text)
                                textToWrite.close()
                                print("User " + currentUser + " wrote to " + filename + ": " + text + "\n")
                                writeToLog("User " + currentUser + " wrote to " + filename + ": " + text + "\n")
                                main()
                            #deny the user access
                            else:
                                print("User " + currentUser + " denied write access to " + filename)
                                writeToLog("User " + currentUser + " denied write access to " + filename + "\n")
                                main()
            main()
        # throw an error if the file doesn't exist
        except FileNotFoundError:
            print("ERROR: File " + filename + " does not exist.")
            writeToLog("ERROR: File " + filename + " does not exist.\n")
            main()
    # a user must be logged in to write to a file
    else:
        print("ERROR: A user must be logged in to complete to action.")
        writeToLog("ERROR: A user must be logged in to complete to action. \n")
        main()

# execute { filename }
def execute(filename):
    global currentUser, userLoginFlag, specialFiles
    # The first line of instruction must be creating a root user
    if lineOfInstruction == 1:
        print("ERROR: The first command must be creating a super user.")
        writeToLog("ERROR: The first command must be creating a super user.\n")
        exit()
    # users are not allowed to access any of the special files
    if filename in specialFiles:
        print("ERROR: References forbidden file.")
        writeToLog("ERROR: References forbidden file.\n")
        main()
    # Checking to make sure that a user is logged in before attempting to complete the action.
    if userLoginFlag == 1:
        try:
            # making sure the file exists
            file = open(filename)
            file.close()
            file = open("files.txt", "r")
            files = file.readlines()
            file.close()
            groups = open("groups.txt", "r")
            groupText = groups.readlines()
            groups.close()
            for line in files:
                if filename in line:
                    # filename owner group permissions (owner group others)
                    info = line.split()
                    for group in groupText:
                        #root can do anything besides login for another user
                        if currentUser == 'root':
                            print("File " + filename + " executed by " + currentUser)
                            writeToLog("File " + filename + " executed by " + currentUser + "\n")
                            main()
                        # the current user is the owner and the owner has write permissions
                        elif currentUser in info[1]:
                            if 'x' in info[3]:
                                print("File " + filename + " executed by " + currentUser)
                                writeToLog("File " + filename + " executed by " + currentUser + "\n")
                                main()
                            # deny user access
                            else:
                                print("User " + currentUser + " denied execute access to " + filename)
                                writeToLog("User " + currentUser + " denied execute access to " + filename + "\n")
                                main()
                        # current user is not the owner, the current line contains the group name, the current user is in that group, the group has write permissions
                        elif currentUser not in info[1] and info[2] in group and currentUser in group:
                            if 'x' in info[4]:
                                print("File " + filename + " executed by " + currentUser)
                                writeToLog("File " + filename + " executed by " + currentUser + "\n")
                                main()
                            # deny user access
                            else:
                                print("User " + currentUser + " denied execute access to " + filename)
                                writeToLog("User " + currentUser + " denied execute access to " + filename + "\n")
                                main()
                        # current user is not the owner, the current user is not in the group, the file has others write permissions
                        elif currentUser not in info[1] and currentUser not in group:
                            if 'x' in info[5]:
                                print("File " + filename + " executed by " + currentUser)
                                writeToLog("File " + filename + " executed by " + currentUser + "\n")
                                main()
                            # deny user access
                            else:
                                print("User " + currentUser + " denied execute access to " + filename)
                                writeToLog("User " + currentUser + " denied execute access to " + filename + "\n")
                                main()
            main()
        # throw an error if the file doesn't exist
        except FileNotFoundError:
            print("ERROR: File " + filename + " does not exist.")
            writeToLog("ERROR: File " + filename + " does not exist.\n")
            main()
    # a user must be logged in to execute a file
    else:
        print("ERROR: A user must be logged in to complete to action.")
        writeToLog("ERROR: A user must be logged in to complete to action. \n")
        main()
#_______________________________________________________________________________________________________________________
# ls { filename }
def ls(filename):
    global userLoginFlag
    # The first line of instruction must be creating a root user
    if lineOfInstruction == 1:
        print("ERROR: The first command must be creating a super user.")
        writeToLog("ERROR: The first command must be creating a super user.\n")
        exit()
    # users are not allowed to access any of the special files
    if filename in specialFiles:
        print("ERROR: References forbidden file.")
        writeToLog("ERROR: References forbidden file.\n")
        main()
    # Checking to make sure that a user is logged in before attempting to complete the action.
    if userLoginFlag == 1:
        try:
            #making sure the file exists
            file = open(filename)
            file.close()
            file = open("files.txt", "r")
            files = file.readlines()
            file.close()
            for line in files:
                if filename in line:
                    writeToLog(line)
            main()
        # throw an error if the file doesn't exist
        except FileNotFoundError:
            print("ERROR: File " + filename + " does not exist.")
            writeToLog("ERROR: File " + filename + " does not exist.\n")
            main()
    # a user must be logged in
    else:
        print("ERROR: A user must be logged in to complete to action.")
        writeToLog("ERROR: A user must be logged in to complete to action. \n")
        main()
#_______________________________________________________________________________________________________________________
# end
def end():
    global specialFiles
    # The first line of instruction must be creating a root user
    if lineOfInstruction == 1:
        print("ERROR: The first command must be creating a super user.")
        writeToLog("ERROR: The first command must be creating a super user.\n")
        exit()
    file = open("files.txt", "r")
    files = file.readlines()
    file.close()
    for line in files:
        info = line.split()
        filename = info[0]
        try:
            file = open(filename[:-1])
            file.close()
            file = open(filename[:-1], "r")
            fileContents = file.read()
            file.close()
            #removing any files created by users
            os.remove(filename[:-1])
            #printing the contents of a file
            print(filename)
            print("---------------------------")
            print(fileContents)
            print("\n")
        # throw an error if the file doesn't exist
        except FileNotFoundError:
            print("ERROR: File " + filename + " does not exist.")
            writeToLog("ERROR: File " + filename + " does not exist.\n")

    for x in range(0, len(specialFiles)):
        file = open(specialFiles[x], "r")
        files = file.read()
        file.close()
        #printing the contents on the special files
        print(specialFiles[x])
        print("---------------------------")
        print(files)
        print("\n")
    for x in range(0, len(specialFiles)):
        #erasing the contents of all the special files
        file = open(specialFiles[x], "w")
        file.write('')
        file.close()
    exit()
#_______________________________________________________________________________________________________________________
#start execution of main
main()