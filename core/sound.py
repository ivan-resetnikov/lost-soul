from pygame import mixer
mixer.init()



def loadSound (path, vol=0.25) :
	sound = mixer.Sound(f'assets/sounds/{path}.wav')
	sound.set_volume(vol)
	return sound


Sounds = {
	'player' : {
		'walk' : loadSound('walk', 0.1),
		'jump' : loadSound('jump'),
		'land' : loadSound('land')
	}
}