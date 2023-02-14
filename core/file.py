from json import load, dump




def readFromJSON (path) :
	with open(path, 'r', encoding='utf-8') as file :
		return load(file)


def writeToJSON (path, data) :
	with open(path, 'w', encoding='utf-8') as file :
		return dump(data, file)