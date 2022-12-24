from setuptools import setup
APP=["game.py"] # game.py - Is the main python file
DATA_FILES = [('', ['assets'])] # assets - Folder containing sprites/images/sounds etc
OPTIONS = {
    "argv_emulation": False,
    "includes": ["pygame"],
    "iconfile": "icon.ico",
}

setup(
    app=APP,
    name="Flappy Bird",
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=["py2app"],
)
