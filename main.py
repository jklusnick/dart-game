import pygame, random

pygame.init()

DIMENSIONS = (600, 480)
SCREEN = pygame.display.set_mode(DIMENSIONS)
CLOCK = pygame.time.Clock()
TARGET_FPS = 60

score = 0

pygame.display.set_caption("dart-game")

is_running = True

KEYS = {
	"d": False,
	"a": False,
	"s": False,
	"w": False
}

directions = [
	'up',
	'down',
	'left',
	'right'
]

def changeKeys(key, value):
	if key == pygame.K_d:
		KEYS['d'] = value
	if key == pygame.K_a:
		KEYS['a'] = value
	if key == pygame.K_s:
		KEYS['s'] = value
	if key == pygame.K_w:
		KEYS['w'] = value

tile_size = 24
player = [DIMENSIONS[0]/2 - tile_size/2, DIMENSIONS[1]/2 - tile_size/2]
speed = 4
bullet_size = 8

def rand_x():
	return random.randint(0, DIMENSIONS[0])

def rand_y():
	return random.randint(0, DIMENSIONS[1])

def movement():
	if KEYS['d']:
		player[0] += speed
	elif KEYS['a']:
		player[0] -= speed
	if KEYS['s']:
		player[1] += speed
	if KEYS['w']:
		player[1] -= speed

food = [random.randint(0, DIMENSIONS[0]-tile_size), \
	random.randint(0, DIMENSIONS[1]-tile_size)]

myfont = pygame.font.SysFont('Comic Sans MS', 30)
scoretext = myfont.render("Score = {0}".format(score), 1, (0, 0, 0))

bullets = []
dart_guns = []
bullet_speed = 8

def newBullet(dart_gun):
	vx, vy = 0, 0
	if dart_gun['shoot_direction'] == 'right':
		vx = bullet_speed
	if dart_gun['shoot_direction'] == 'left':
		vx = -bullet_speed
	if dart_gun['shoot_direction'] == 'up':
		vy = -bullet_speed
	if dart_gun['shoot_direction'] == 'down':
		vy = bullet_speed
	bullets.append({
		'x': dart_gun['x'],
		'y': dart_gun['y'],
		'vx': vx,
		'vy': vy
	})

def updateBullets():
	for bullet in bullets:
		bullet['x'] += bullet['vx']
		bullet['y'] += bullet['vy']

def newDart(direction):
	x = 0
	y = 0
	shoot_direction = ''
	if direction == 'right':
		x=DIMENSIONS[0] - tile_size
		y=rand_y()
		shoot_direction = 'left'
	elif direction == 'left':
		x=0
		y=rand_y()
		shoot_direction = 'right'
	elif direction == 'down':
		x=rand_x()
		y=DIMENSIONS[1] - tile_size
		shoot_direction = 'up'
	elif direction == 'up':
		x=rand_x()
		y=0
		shoot_direction = 'down'
	dart_guns.append({
		"shoot_direction": shoot_direction,
		"x": x,
		"y": y,
		"timer": 0,
		"timerMax": 5
	})

def updateDartTimers():
	for dart_gun in dart_guns:
		if dart_gun['timer'] < dart_gun['timerMax']:
			dart_gun['timer'] += .1
		else: 
			dart_gun['timer'] = 0
			newBullet(dart_gun)

while is_running:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			changeKeys(event.key, True)
			if event.key == pygame.K_ESCAPE:
				is_running = False
		if event.type == pygame.KEYUP:
			changeKeys(event.key, False)
		if event.type == pygame.QUIT:
			is_running = False

	# Other updates
	if food[0] < player[0] + tile_size and \
	food[0] + tile_size > player[0] and \
	food[1] < player[1] + tile_size and \
	food[1] + tile_size > player[1]:
		food[0] = random.randint(0, DIMENSIONS[0]-tile_size)
		food[1] = random.randint(0, DIMENSIONS[1]-tile_size)
		score+=1
		scoretext = myfont.render("Score = {0}".format(score), 1, (0, 0, 0))
		direction = directions[random.randint(0, len(directions)-1)]
		newDart(direction)

	if player[0] < -tile_size:
		player[0] = DIMENSIONS[0]
	if player[0] > DIMENSIONS[0]:
		player[0] = 0
	if player[1] < -tile_size:
		player[1] = DIMENSIONS[1]
	if player[1] > DIMENSIONS[1]:
		player[1] = 0

	for bullet in bullets:
		if bullet['x'] < player[0] + tile_size and \
		bullet['x'] + bullet_size > player[0] and \
		bullet['y'] < player[1] + tile_size and \
		bullet['y'] + bullet_size > player[1]:
			is_running = False
			print score

	updateDartTimers()
	updateBullets()

	SCREEN.fill((255,255,255))

	# Draw here
	pygame.draw.rect(SCREEN, (255,0,0), (player[0], player[1], \
		tile_size, tile_size))
	pygame.draw.rect(SCREEN, (200,200,0), (food[0], food[1], \
		tile_size, tile_size))

	for dart_gun in dart_guns:
		pygame.draw.rect(SCREEN, (100,100,100), (dart_gun['x'], dart_gun['y'], \
			tile_size, tile_size))
	for bullet in bullets:
		pygame.draw.rect(SCREEN, (100,0,0), (bullet['x'], bullet['y'], \
			8, 8))

	SCREEN.blit(scoretext, (0, 0))

	pygame.display.update()

	movement()

	CLOCK.tick(TARGET_FPS)

pygame.quit()