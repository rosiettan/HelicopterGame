import pygame

pygame.init()
size = (700, 500)
screen_width = size[0]
screen_height = size[1]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Helicopter")
clock = pygame.time.Clock() #frame

heli_right = pygame.image.load("heli_right.png")
heli_right = pygame.transform.scale(heli_right, (screen_width//10, screen_width//10))
heli_left = pygame.image.load("heli_left.png")
heli_left = pygame.transform.scale(heli_left, (screen_width//10, screen_width//10))

background_image = pygame.image.load("plx-5.png")
background_image = pygame.transform.scale(background_image, size)

x = screen_width//2 - screen_width//20
y = screen_height//2 - screen_width//20

dx = 0
dy = 0
flying_up = False
heading_right = True

background_x = 0

level = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 2, 0, 1, 1, 1, 1, 1, 0, 0, 0, 2, 2, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
]

platforms = list()
platforms2 = list()

brick_size = size[1] // 11

for i in range(len(level)):
    for j in range(len(level[i])):
        if level[i][j] == 1:
            platforms.append(pygame.Rect(j*brick_size, i*brick_size, brick_size, brick_size))
        if level[i][j] == 2:
            platforms2.append(pygame.Rect(j*brick_size, i*brick_size, brick_size, brick_size))
        if level[i][j] == 7:
            x, y = j*brick_size, i*brick_size


fire = False
fire_x, fire_y = 50, 50
fire_dx = 10
fire_dy = 0
fire_counter = 0

game_over = False
while not game_over:
    if flying_up:
        dy = dy - 1
    else:
        dy = dy + 0.5
        if dy > 10:
            dy = 10

    x = x + dx
    heli_rect = pygame.Rect(x, y, screen_width//10, screen_width//12)
    for platform in platforms + platforms2:
        if heli_rect.colliderect(platform):
            x = x - dx

    y = y + dy
    heli_rect = pygame.Rect(x, y, screen_width //10, screen_width //12)
    for platform in platforms + platforms2:
        if heli_rect.colliderect(platform):
            y = y - dy
            dy = 0

    if x + background_x > size[0] * 3/4:
        background_x = size[0] * 3/4 - x

    if x + background_x < size[0] * 1/4:
        background_x = size[0] * 1/4 - x

    if fire:
        fire_counter -= 1
        if fire_counter <= 0:
            fire = False
        fire_x += fire_dx
        fire_y += fire_dy
        for platform in platforms:
            if platform.collidepoint(fire_x, fire_y):
                fire = False
        for platform in platforms2:
            if platform.collidepoint(fire_x, fire_y):
                fire = False
                platforms2.remove(platform)
                break

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # if pressed X
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                dx = 7
                heading_right = True
            if event.key == pygame.K_LEFT:
                dx = -7
                heading_right = False
            if event.key == pygame.K_UP:
                flying_up = True
            if event.key == pygame.K_DOWN:
                dy = 7
            if event.key == pygame.K_SPACE:
                if not fire:
                    fire = True
                    fire_x = x + screen_width//20
                    fire_y = y + screen_width//20
                    fire_counter = 40
                    if heading_right:
                        fire_dx = 10
                    else:
                        fire_dx = -10
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                if dx > 0:
                    dx = 0
            if event.key == pygame.K_LEFT:
                if dx < 0:
                    dx = 0
            if event.key == pygame.K_UP:
                flying_up = False
            if event.key == pygame.K_DOWN:
                if dy > 0:
                    dy = 0

    screen.fill((255, 255, 255))
    screen.blit(background_image, (background_x % size[0], 0))
    screen.blit(background_image, (background_x % size[0] - size[0], 0))

    for platform in platforms:
        pygame.draw.rect(screen, (0, 120, 0), (platform.x + background_x,
                                               platform.y,
                                               platform.width,
                                               platform.height))

    for platform in platforms2:
        pygame.draw.rect(screen, (150, 250, 150), (platform.x + background_x,
                                               platform.y,
                                               platform.width,
                                               platform.height))

    #pygame.draw.rect(screen, (0, 0, 200), heli_rect)

    if heading_right:
        screen.blit(heli_right, (x + background_x, y))
    else:
        screen.blit(heli_left, (x + background_x, y))

    if fire:
        pygame.draw.circle(screen, (120, 0, 0), (fire_x + background_x, fire_y), 5)

    pygame.display.flip()
    clock.tick(25) # fps

pygame.quit()