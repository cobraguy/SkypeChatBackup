from shutil import copyfile
import html
import os
import sqlite3

#Path to skype.db file
PATH_TO_DB = 'C:\\Path\\To\\skype.db'
#Should this script backup media as well?
BACKUP_MEDIA = False
#Path to media_cache_v3 folder
PATH_TO_MEDIA = 'C:\\Path\\To\\media_cache_v3\\' #IMPORTANT - Keep \\ (or / on Mac and Linux) at the end of the path
#Extensions of media you want to back up
MEDIA_BACKUP_EXTENSIONS = ('.jpg',)
#Where to store backups (relative to this script)
BACKUP_PATH = 'chat_backups\\' #IMPORTANT - Keep \\ (or / on Mac and Linux) at the end of the path
#Where to store backups of media (relative to this script)
MEDIA_BACKUP_PATH = BACKUP_PATH + 'media\\' #IMPORTANT - Keep \\ (or / on Mac and Linux) at the end of the path

def main():  
    #Make sure the path to skype.db exists
    if os.path.exists(PATH_TO_DB):
        #Create a copy of skype.db to work with
        try:
            copyfile(PATH_TO_DB, 'skype.db')
        except Exception as e:
            print(e)
        db = sqlite3.connect('skype.db')
        cursor = db.cursor() #cursor is used to execute SQL commands
    else:
        print('Path to skype.db does not exist')
        return
        
    #Get the list of conversations
    conversations = get_convo_list(cursor)
    
    #Create path to store backup
    if not os.path.exists(BACKUP_PATH):
        os.makedirs(BACKUP_PATH)
    
    #Backup each conversation
    for row in conversations:
        backup_convo(cursor, row)
    
    db.close()
    
    #Backup media folder
    if BACKUP_MEDIA:
        backup_media()
    
def get_convo_list(cursor):
    #Gets the list of conversations
    #cursor - cursor variable to execute SQL commands

    #Get the list of conversations (NOT the actual messages)
    cursor.execute('SELECT dbid, id FROM conversations')
    return cursor.fetchall()

def backup_convo(cursor, row):
    #Backup a conversation
    #cursor - cursor variable to execute SQL commands
    #row - tuple of (dbid, id)

    #dbid is a unique id number given to each conversation
    dbid = row[0] 
    
    #The id is the username of the other person (NOT the display name)
    id = row[1]
    
    #Select all the messages from a conversation
    cursor.execute('SELECT author, content FROM messages WHERE convdbid = ? ORDER BY originalarrivaltime', (dbid,))
    messages = cursor.fetchall()
    
    if not messages:
        pass #No messages in this conversation. Don't attempt a backup
    else:
        #Use the encoding argument because skype escapes some apostrophes with utf-8
        #Also windows would throw a UnicodeEncodeError
        with open(BACKUP_PATH + id + '.txt', 'w', encoding='utf-8') as file:
            for message in messages:
                author = message[0][message[0].index(':')+1:] #Trim the contact type from the author name
                #Skype escapes some apostrophes with &apos;
                message_content = html.unescape(message[1])
                file.write(author + ': ' + message_content + '\n')
        
        print(id, 'backup successful')
        
def backup_media():
    #Backup sent a received media
    #This is a quick and dirty implementation that may get duplicates and low-res thumbnails
    #May not get all media if the folder was recently cleared

    #Create the directories to backup media
    backup_dest = MEDIA_BACKUP_PATH
    if not os.path.exists(backup_dest):
        os.mkdir(backup_dest)
        
    #Make sure the path to skype's media exists
    if os.path.exists(PATH_TO_MEDIA):
        #Iterate through all files in the media folder
        for filename in os.listdir(PATH_TO_MEDIA):
            #If the file ends in a whitelisted extension
            if filename.endswith(MEDIA_BACKUP_EXTENSIONS):
                #Copy the file from the media folder to the backup folder
                copyfile(PATH_TO_MEDIA+filename, backup_dest+filename)
                print(filename, 'backup successful')
    else:
        print('Path to media_cache_v3 does not exist')
    
if __name__ == '__main__':
    main()
    input('Press Enter to continue...')
