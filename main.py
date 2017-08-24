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

def newDart(direction, x, y):
	dart_guns.append({
		"direction": direction,
		"x": x,
		"y": y,
		"timer": 0,
		"timerMax": 5
	})

def updateDartTimers():
	for dart_gun in dart_guns:
		if dart_gun['timer'] > dart_gun['timerMax']:
			dart_gun['timer'] += 1/TARGET_FPS
		else:
			dart_gun['timer'] = 0

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


	if player[0] < -tile_size:
		player[0] = DIMENSIONS[0]
	if player[0] > DIMENSIONS[0]:
		player[0] = 0
	if player[1] < -tile_size:
		player[1] = DIMENSIONS[1]
	if player[1] > DIMENSIONS[1]:
		player[1] = 0

	SCREEN.fill((255,255,255))

	# Draw here
	pygame.draw.rect(SCREEN, (255,0,0), (player[0], player[1], \
		tile_size, tile_size))
	pygame.draw.rect(SCREEN, (200,200,0), (food[0], food[1], \
		tile_size, tile_size))

	SCREEN.blit(scoretext, (0, 0))

	pygame.display.update()

	movement()

	CLOCK.tick(TARGET_FPS)

pygame.quit()