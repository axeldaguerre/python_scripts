import requests 
import os
import re
   
def GetHTMLTableContent(text):
    index_s = text.index('tbody')
    index_e = text.index('tbody', index_s + 1)
    result = text[index_s : index_e]
    return result

def ReplaceASCIIReference(match):
    if match.group(1) is not None:
        return chr(int(match.group(1)))
    elif match.group(2) is not None:
        return match.group(2)

def save_links(text, filePath, platform):
    result = []
    index_s = 0

    while True:
        index_end = text.find('</a>', index_s)
        index_start = text.rfind('>', index_s, index_end)
        # because "< ", bad I know
        GameName = text[index_start+2:index_end]
        
        if '&' in GameName:
            pattern = r'&amp;|&#(\d+);|&([^;]+);'
            GameName = re.sub(pattern, ReplaceASCIIReference, GameName)
                
        index_s = text.find('href=', index_s)
        if index_s == -1: break
        index_e = text.find('"', index_s+6)
        urlGameDownload = text[index_s+6:index_e]
        
        result.append(f'{GameName};{urlGameDownload};{platform}')
        index_s = index_e

    with open(filePath, 'a') as file:
            for gameData in result:
                file.write(f'{gameData}')
                file.write('\n')
    file.close()

    return result

def Error(label):
    print(f"Error: {label}\n")
    
def GetHTMLPageContent(pageIndex, url, session):
    #TODO(Axel): checks if pageIndex is greater than the last page Index on RomHustler.org
    print(f"HTTP: Getting content from page {pageIndex}\n")
    # 0  does not exists and 1 is null because the page index is not used for page 1
    if pageIndex == 0 or pageIndex == 1:
        
        if session:
            result = session.get(url)    
        else:
            result = requests.get(url)    
        if result.status_code == 200:
            print("GET request successful")
            # Process the content of the response, e.g., response.text
        else:
            print("GET request failed")
    else:
        result = requests.get(f"{url}/{pageIndex}")
    if result.status_code != 200:
        Error(f"getPageHTMLContent() -> {result.status.code}")
    return result

def GetLastPageIndex(text):

    index_start = text.index('<ul class="pagination">')
    index_start_ul = index_start 
    index_stop = text.index('ul>', index_start)
    index_start = text.index('page-item active', index_start)
    index_start = text.index('li>', index_start)

    text = text[index_start_ul:index_stop]
    index_start = text.rfind('</a')
    index_start = text[:index_start].rfind('</a')
    result = text[index_start-2:index_start]
    # last page is the `next` page link
    return int(result)

def PrepareEnvironment(urlsFilePath, GamefolderPath):
    print(f"Creating folders\n")
    if os.path.exists(urlsFilePath):
        os.remove(urlsFilePath)
        
    if not os.path.exists(GamefolderPath):
            os.makedirs(GamefolderPath)

def print_platforms(Platforms):
    print("Platforms: [", end="")

    for i, platformGame in enumerate(Platforms):
        print(f" {platformGame}, ", end="")

    print("]\n")


def DownloadFromURL(UrlDownload):
    
    return requests.get(UrlDownload)
    
    