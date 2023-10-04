# ROM Hustler automatic download

It's time consuming to download manually all the roms from the website, maybe you could with a paid account though. But I don't, so I have made this script allowing to do it and create according folders. It will create a structure like following:
    `path_where_exe_is_exec/games/Sega Genesis/batman-1.7z`

# TODOs

1. Not all platforms are implemented yet. I would like to automate it, you give the script a file, it will extract the platforms's name list. That way it's not hard coded and you could use it for more that the actual, Launchbox. I think all rom managers use the same names for them, but I need to check that
2. Data structure are not smart, I didn't use any of them actually, maybe performance is better but as I don't know how to debug in assembly Python, I don't know
3. To me, Python is not a readable programming language, indentation, no bracket use makes it harder for me to read, maybe use a parser that will allow me to add them.
4. Source code is convulated, not readable and not smart, I should make it better 
5. Handle errors better, more checks
6. **The `.exe` does not have the dependecies somewhat, fix it**
7. Add a limit of data size download
8. Add the possibility to ask every time for download


# Needed 

1. Python 3
2. Pyinstaller (if you want modify `.exe`)

# How to use

1. Use the `dist\main.exe` and add params `Game platform` and optional `Page Index to start from`
2. If you want to print option just do `main.exe` command
4. A good command is at least: `main.exe genesis` and means "download all games from genesis pages (from 1 to last)"
3. Build the `exe` file `pyinstaller --onefile main.py`


Download several ROMS from Rom Hustler without click and without account.

I used Python because I didn't want to do anything fancy for it, and it's my first python script. So it's really awfull
