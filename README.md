# SkypeChatBackup
A script written with Python 3.7 to backup Skype chats to text files. Made with the intent of helping me learn Python and basic SQL commands.
Tested on Windows 10 with the Skype for Windows 10 app v.12.1815.209.0. This should work on Mac and Linux and with the Skype desktop app, assuming that Skype uses the same `.db` file across platforms and versions.

# Explnations

### Note
All paths given apply to the Skype for Windows 10 App (installed from the Microsoft Store). For the Skype desktop app (installed from the Skype website), I believe the needed files and folders are also stored somewhere within the dephts of the `AppData` folder, although I'm not positive because I don't use the desktop app. I'm also not sure of the paths on Mac and Linux

### `PATH_TO_DB`
Should be equal to a string of the path to the `skype.db` file. For the Windows 10 app, it is located at `C:\Users\Username\AppData\Local\Packages\Microsoft.SkypeApp_randomtext\LocalState\skypeusername`. Don't forget to escape the backslashes.

### `BACKUP_MEDIA` 
Should be equal to either `True` or `False` depending on whether you want to backup media sent and received through Skype. This is set to `False` by default because I use a very quick and dirty method that may not get _all_ media depending on how often Skype clears its media folder, if at all. It also gets any low-res thumbnails that Skype automatically generates.

### `PATH_TO_MEDIA`
Only apples if `BACKUP_MEDIA` is set to true. This should be equal to a string of the path to the `media_cache_v3` folder. For the Windows 10 App, it is located at `C:\Users\Username\AppData\Local\Packages\Microsoft.SkypeApp_randomtext\LocalState\skypeusername\media_messaging\media_cache_v3\` Don't forget to escape the backslashes. **NOTE:** Be sure to keep the trailing `\` (or `/` on Mac and Linux) at the end of the path as the script operates on the assumption that those are already there.

## `MEDIA_BACKUP_EXTENSIONS`
A tuple of strings consisting of the file extensions that you want to backup. I only include `.jpg` by default but you could also add extensions to backup videos as well.

## `BACKUP_PATH`
The path relative to the python script where all the backups will be placed. **NOTE:** Be sure to keep the trailing `\` (or `/` on Mac and Linux) at the end of the path as the script operates on the assumption that those are already there.
