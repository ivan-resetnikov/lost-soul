from pygame import mixer
mixer.init()



def loadSound (path, vol=0.25) :
	sound = mixer.Sound(f'assets/sounds/{path}.wav')
	sound.set_volume(vol)
	return sound


Sounds = {
	'player' : {
		'walk' : loadSound('walk', 0.025),
		'jump' : loadSound('jump', 0.2),
		'land' : loadSound('land', 0.07)
	}
}