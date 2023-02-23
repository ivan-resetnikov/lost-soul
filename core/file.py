from json    import load, dump
from os      import getenv, mkdir
from os.path import exists

APPDATA = getenv('APPDATA')[:-7:]

SavesPath = f'{APPDATA}/Local/LostSoul'



def readFromJSON (path) :
	with open(path, 'r', encoding='utf8') as file :
		return load(file)


def writeToJSON (path, content) :
	with open(path, 'w', encoding='utf8') as file :
		return dump(content, file, ensure_ascii=True, indent=4)


isFileExists = exists
newFolder    = mkdir