import pygame
from copy import deepcopy
from random import choice, randrange

W, H  = 10, 16

Tile = 40
game_size = W*Tile,H*Tile
RES = 400, 740
FPS = 60

pygame.init()
sc = pygame.display.set_mode(RES)
screen = pygame.Surface(game_size)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * Tile, y * Tile, Tile, Tile) for x in range(W) for y in range(H)]

figures_position = [
    [(-1,0),(-2,0),(0,0),(1,0)],
    [(0,-1),(-1,-1),(-1,0),(0,0)],
    [(-1,0),(-1,1),(0,0),(0,-1)],
    [(0,0),(-1,0),(0,1),(-1,-1)],
    [(0,0),(0,-1),(0,1),(-1,-1)],
    [(0,0),(0,-1),(0,1),(-1,-1)],
    [(0,0),(0,-1),(0,1),(-1,0)]
]

figures = [[pygame.Rect(x + W // 2, y+1, 1, 1)for x,y in figur_pos] for figur_pos in figures_position]
figure_rect = pygame.Rect(0,0,Tile-2,Tile-2)
field = [[0 for i in range(W)] for i in range(H)]


anim_count, anim_speed, anim_limit = 0, 60, 2000
figure = deepcopy(choice(figures))

get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30,256))
color = get_color()


font = pygame.font.SysFont('arial', 36)
score_font = pygame.font.SysFont('arial', 40)
score_title = score_font.render('Score:', True, pygame.Color('pink'))
record_title = score_font.render('Record:', True, pygame.Color('purple'))

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 200, 3: 700, 4: 1500}
    
def check_borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True

def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record') as f:
            f.write('0')

def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


while True:
    record = get_record()
    dx = 0
    rotate = False

    sc.fill(pygame.Color('dark blue'))
    sc.blit(screen, (0,100))
    screen.fill(pygame.Color("black"))

    for i in range(lines):
        pygame.time.wait(200)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 120
            elif event.key == pygame.K_UP:
                rotate = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                anim_limit = 2000


    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break
    

    anim_count  += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                color = get_color()
                figure = deepcopy(choice(figures))
                anim_limit = 2000
                break


    line, lines = H-1, 0
    for row in range(H-1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1
        else:
            anim_speed += 3
            lines += 1
    
    score += scores[lines]
            
    center = figure[0]        
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break
    
    
    [pygame.draw.rect(screen, (40, 40, 40), i_rect, 1) for i_rect in grid]

    
    for i in range(4):
        figure_rect.x = figure[i].x * Tile
        figure_rect.y = figure[i].y * Tile
        pygame.draw.rect(screen, color, figure_rect)
    
    for y,row in enumerate(field):
        for x,col in enumerate(row):
            if col:
                figure_rect.x, figure_rect.y = x*Tile, y*Tile
                pygame.draw.rect(screen, col, figure_rect)
    
    sc.blit(score_title, (20, 25))
    sc.blit(font.render(str(score), True, pygame.Color('white')), (130, 30))
    sc.blit(record_title, (200, 25))
    sc.blit(font.render(record, True, pygame.Color('white')), (330, 30))


    for i in range(W):
        if field[0][i]:
            set_record(record, score)
            field = [[0 for i in range(W)] for i in range(H)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            for i_rect in grid:
                pygame.draw.rect(screen, get_color(), i_rect)
                sc.blit(screen, (0, 100))
                pygame.display.flip()
                clock.tick(200)

    pygame.display.flip()
    clock.tick(FPS)