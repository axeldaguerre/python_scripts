# Vimm roms downloader webdriver

# TODOS

- Add more web driver if
# Needed 

1. Python 3
2. Pyinstaller (if you want modify `.exe`)
3. One web driver:
    - https://chromedriver.chromium.org/downloads (check the compatibility of your chrome version)
    - https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
    - https://github.com/mozilla/geckodriver/releases
    - https://webkit.org/blog/6900/webdriver-support-in-safari-10/

# How to use

1. Use the `dist\main.exe` and add params `Game platform` and optional `Page Index to start from`
2. If you want to print option just do `main.exe` command
4. A good command is at least: `main.exe genesis` and means "download all games from genesis pages (from 1 to last)"
3. Build the `exe` file `pyinstaller --onefile main.py`


Download several ROMS from Rom Hustler without click and without account.

I used Python because I didn't want to do anything fancy for it, and it's my first python script. So it's really awfull

