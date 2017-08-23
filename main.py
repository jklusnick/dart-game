import pygame, random

pygame.init()

DIMENSIONS = (600, 480)
SCREEN = pygame.display.set_mode(DIMENSIONS)
CLOCK = pygame.time.Clock()
TARGET_FPS = 60

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

	if player[0] < 0:
		player[0] = DIMENSIONS[0]
	if player[0] > DIMENSIONS[0]:
		player[0] = 0
	if player[1] < 0:
		player[1] = DIMENSIONS[1]
	if player[1] > DIMENSIONS[1]:
		player[1] = 0

	SCREEN.fill((255,255,255))

	# Draw here
	pygame.draw.rect(SCREEN, (255,0,0), (player[0], player[1], \
		tile_size, tile_size))
	pygame.draw.rect(SCREEN, (200,200,0), (food[0], food[1], \
		tile_size, tile_size))

	pygame.display.update()

	movement()

	CLOCK.tick(TARGET_FPS)

pygame.quit()