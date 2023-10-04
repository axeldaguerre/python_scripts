import sys
import requests 
import os
from defs import PrepareEnvironment, GetHTMLPageContent, GetLastPageIndex, GetHTMLTableContent, save_links, Error, print_platforms, DownloadFromURL



# Dinamically get all platforms ? Missing some of them here
# TODO(Not exhaustive and broken list, right now only mains are ok)
romHustlerPlatforms = []
romHustlerPlatforms.insert(0, 'genesis') 
romHustlerPlatforms.insert(1, 'sms') 
romHustlerPlatforms.insert(1, 'snes') 

LaunchBoxPlatformNames = []
LaunchBoxPlatformNames.insert(0, 'Sega Genesis') 
LaunchBoxPlatformNames.insert(1, 'Sega Master System') 
LaunchBoxPlatformNames.insert(1, 'Super Nintendo Entertainment System')

IS_PREMIUM = False

RootPath = os.getcwd()

gameDataFilePath = f'{RootPath}\\roms_urls.txt'
root_url = 'https://romhustler.org'

#TODO() Seems useless
GamesFolderPath = F'{RootPath}'

script_name = sys.argv[0]

if len(sys.argv) == 1:
    print(f"{script_name} [ platform ] [start page] [with login] [max data usage]")
    print_platforms(romHustlerPlatforms)
    sys.exit(0)

print(f"========= {script_name} ========= \n")

platformGame = sys.argv[1]
print(f"Platform: {platformGame} ========= \n")

if not sys.argv[2]:
    PageIndex = 1
else:
    PageIndex = int(sys.argv[2])
print(f"Start Page Index: {PageIndex} ========= \n")

if len(sys.argv) >= 4:
    if sys.argv[3] == "true":
        session = requests.Session()
        session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
        login = {
            # "username": input("Login:"),
            # "password": input("Password:")
            
            "login": "axeldaguerre@protonmail.com",
            "password": "RX9MhFFY4QvSNCtVQj69"
        }    
        response = session.post("https://romhustler.org/user/login", data=login)
        cookie_obj = response.cookies.get_dict()
        if(cookie_obj.get("romu_id")):
            IS_PREMIUM = True
            print("Login successful")
        else:
            print("Login failed")
            exit()

PrepareEnvironment(gameDataFilePath, GamesFolderPath)

urlRomList = f"{root_url}/roms/{platformGame}"
response = GetHTMLPageContent(PageIndex, urlRomList, session)

PageCount = GetLastPageIndex(response.text)
PageCount -= PageIndex
if PageCount < 0:
    print("page index to start from is too large")
    sys.exit()

for i in range(PageCount):
    
        HTMLTableContent = GetHTMLTableContent(response.text)
        save_links(HTMLTableContent, gameDataFilePath, platformGame)
        PageIndex += 1
        response = GetHTMLPageContent(PageIndex + 1, urlRomList)
        
        with open(gameDataFilePath, 'r') as file:
            content = file.read()
            gamesData = content.split('\n')

        for gameData in gamesData:   
            GameName = gameData.split(';')[0]  
            url = gameData.split(';')[1]
            fileName = url.split('/')[-1]
            platformGame = gameData.split(';')[2]

            #TODO(Axel): Create a data structure for string chunk
            if not IS_PREMIUM:               
                response = requests.get(url)
                indexDownload = response.text.index('/roms/download/guest')
                indexEnd = response.text.find('"', indexDownload+20)
                URLDownload = f'{root_url}{response.text[indexDownload:indexEnd]}'

                response = requests.get(URLDownload)

                #TODO(Axel) a bug occur when going to https://romhustler.org/roms/download/guest/6568/eyJpdiI6Indud095RC9RRi9xaG9ISWlYOXJLSHc9PSIsInZhbHVlIjoiREdJU015RHhtRmVsa2QyOUswejlyQzZmK0k2Q09XdUZSWlFMYWdLMlp1QT0iLCJtYWMiOiJiZDE4NjVhMDUxMzlhMzYwNTAyOWJhNzAyMzc4ZDdmMWY4ZDFjN2U5ZmYzYzUwOTFjOTJkNDhmMTY0MTIwNDA5IiwidGFnIjoiIn0= (can't find the 'https://dl.romhustler.org/files'), but when debugging it was in the specific url, not in the response from the code though
                try:
                    indexDownload = response.text.index('https://dl.romhustler.org/files')
                except ValueError:
                    Error(f"This game is restricted, only premium can get it!")
                    continue
                indexEnd = response.text.find('"', indexDownload+20)
                URLDownload = response.text[indexDownload:indexEnd]
                    
                try:
                    indexPlatform = romHustlerPlatforms.index(platformGame)
                except ValueError:
                    Error(f"Can't match '{platformGame}' with an actual platform in Launchbox.")
                
                LaunchboxPlatformName = LaunchBoxPlatformNames[indexPlatform]
                GameFolderPlatformPath = f"{GamesFolderPath}"
                # it could be a zip or a folder (unzip)
                folderNamePath = f"{GameFolderPlatformPath}\\{GameName}"
                fileNamePath = f"{GameFolderPlatformPath}\\{fileName}.7z"
                
                #TODO(Axel): Even if exists, it does pass. 
                
                IsGameFolderExist = os.path.exists(folderNamePath.replace('/', '\\'))
                if not IsGameFolderExist:
                    IsGameFolderExist = os.path.exists(folderNamePath.lower())
                    if not IsGameFolderExist:
                        IsGameFolderExist = os.path.exists(folderNamePath.lower().replace(" ", "-"))
                FullFilePath = fileNamePath.replace('/', '\\')
                IsFileArchiveExist = os.path.exists(FullFilePath)            

                if not IsFileArchiveExist and not IsGameFolderExist:
                        print(f"Downloading {GameName}")
                        response = requests.get(URLDownload)
                        with open(FullFilePath, 'wb') as file:
                            file.write(response.content)
                    
                else:
                    print(f"{fileNamePath} already")
                    continue
            # elif IS_PREMIUM:
                # response = session.get(url)
                # SaveLinks(HTMLTableContent, gameDataFilePath, platformGame)
                # PageIndex += 1
                # response = GetHTMLPageContent(PageIndex + 1, urlRomList)
                # with open(gameDataFilePath, 'r') as file:
                #     content = file.read()
                #     gamesData = content.split('\n')