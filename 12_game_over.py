from pickle import FALSE
import pygame, os, math

class Claw(pygame.sprite.Sprite): # 집게 클래스
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.original_image = image
        self.rect = image.get_rect(center=position)

        self.offset = pygame.math.Vector2(default_offset_x_claw, 0)
        self.position = position

        self.direction = LEFT # 집게의 이동 방향
        self.angle_speed = 2.5 # 집게의 각도 변경 폭(이동 속도)
        self.angle = 10 # 최초 각도 정의 (오른쪽 끝) 범위 : 10~170

    def upadate(self, to_x):
        if self.direction == LEFT:
            self.angle += self.angle_speed
        elif self.direction == RIGHT:
            self.angle -= self.angle_speed
        
        if self.angle > 170:
            self.angle = 170
            self.set_direction(RIGHT)
        elif  self.angle < 10:
            self.angle = 10
            self.set_direction(LEFT)

        self.offset.x += to_x # offset의 x좌표 증가
        self.rotate() # 회전 처리

        # rect_center = self.position + self.offset
        # self.rect = self.image.get_rect(center=rect_center)

    def rotate(self):
        self.image = pygame.transform.rotozoom(self.original_image, -self.angle, 1) # 회전 대상 이미지, 각도, 이미지 크기(1이면 그대로)
        
        offset_rotated = self.offset.rotate(self.angle)

        self.rect = self.image.get_rect(center=self.position + offset_rotated) # x, y 좌표

    def set_direction(self, direction):
        self.direction = direction

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.circle(screen, RED, self.position, 3) # 중심점
        pygame.draw.line(screen, BLACK, self.position, self.rect.center, 5) # 직선

    def set_init_state(self):
        self.offset.x = default_offset_x_claw
        self.angle = 10
        self.direction = LEFT

class Gemstone(pygame.sprite.Sprite): # 보석 클래스
    def __init__(self, image, position, speed, price):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position) #반드시 2가지는 초기화 해야함
        self.speed = speed
        self.price = price

    def set_position(self, position, angle):
        r = self.rect.size[0] // 2 # 반지름
        rad_angle = math.radians(angle)
        to_x = r * math.cos(rad_angle) # 삼각형의 밑변
        to_y = r * math.sin(rad_angle) # 삼각형의 높이
        self.rect.center = (position[0] + to_x, position[1] + to_y)
        
def setup_gemstone():
    small_gold_price, small_gold_speed = 100, 5
    big_gold_price, big_gold_speed = 300, 2
    stone_price, stone_speed = 10, 2
    diamond_price, diamond_speed = 600, 7

    gemstone_group.add(Gemstone(gemstone_images[0], (200, 380), small_gold_speed, small_gold_price))
    gemstone_group.add(Gemstone(gemstone_images[0], (480, 520), small_gold_speed, small_gold_price))
    gemstone_group.add(Gemstone(gemstone_images[0], (1050, 400), small_gold_speed, small_gold_price))
    
    gemstone_group.add(Gemstone(gemstone_images[1], (300, 500), big_gold_speed, big_gold_price))
    gemstone_group.add(Gemstone(gemstone_images[1], (840, 450), big_gold_speed, big_gold_price))
    gemstone_group.add(Gemstone(gemstone_images[1], (510, 340), big_gold_speed, big_gold_price))

    gemstone_group.add(Gemstone(gemstone_images[2], (300, 380), stone_speed, stone_price))
    gemstone_group.add(Gemstone(gemstone_images[2], (654, 570), stone_speed, stone_price))
    gemstone_group.add(Gemstone(gemstone_images[2], (710, 440), stone_speed, stone_price))

    gemstone_group.add(Gemstone(gemstone_images[3], (1300, 420), diamond_speed, diamond_price))
    gemstone_group.add(Gemstone(gemstone_images[3], (780, 690), diamond_speed, diamond_price))
    gemstone_group.add(Gemstone(gemstone_images[3], (1000, 640), diamond_speed, diamond_price))

def update_score(score):
    global curr_score
    curr_score += score

def display_score():
    txt_curr_score = game_font.render(f"Curr Score : {curr_score:,}", True, BLACK)
    screen.blit(txt_curr_score, (50, 20))

    txt_goal_score = game_font.render(f"Goal Score : {goal_score:,}", True, BLACK)
    screen.blit(txt_goal_score, (50, 80))

def display_time(time):
    txt_timer = game_font.render(f"Time : {time}", True, BLACK)
    screen.blit(txt_timer, (1100, 50))

def display_game_over():
    game_font = pygame.font.SysFont("arialrounded", 60)
    txt_game_over = game_font.render(game_result, True, BLACK)
    rect_game_over = txt_game_over.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
    screen.blit(txt_game_over,rect_game_over)

pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Gold Miner")

clock = pygame.time.Clock()

game_font = pygame.font.SysFont("arialrounded", 30)

goal_score = 1000
curr_score = 0

game_result = None
total_time = 60
start_ticks = pygame.time.get_ticks() # 현재 시간을 받아옴

default_offset_x_claw = 40
to_x = 0 # x좌표 기준으로 집게 이미지를 이동시킬 값 저장
caught_gemstone = None # 잡은 보석의 정보

move_speed = 12 # 발사 속도 (x좌표 기준으로 증가)
return_speed = 20 # 돌아오는 속도

# 집게 방향 변수
LEFT = -1
RIGHT = 1
STOP = 0

RED = (255, 0, 0)
BLACK = (0, 0, 0)

current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, "background.png"))

gemstone_images = [
    pygame.image.load(os.path.join(current_path, "small_gold.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "big_gold.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "stone.png")).convert_alpha(),
    pygame.image.load(os.path.join(current_path, "diamond.png")).convert_alpha()
]

# 보석 그룹
gemstone_group = pygame.sprite.Group()
setup_gemstone()

claw_image = pygame.image.load(os.path.join(current_path, "claw.png")).convert_alpha()
claw = Claw(claw_image, (screen_width // 2, 110))

running = True
while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN: # 마우스 누를 때
           if claw.direction != STOP:
               claw.set_direction(STOP)
               to_x = move_speed

    if claw.rect.left < 0 or claw.rect.right > screen_width or claw.rect.bottom > screen_height:
        to_x = -return_speed
    
    if claw.offset.x < default_offset_x_claw: # 원위치에 오면
        to_x = 0
        claw.set_init_state() # 처음 상태로 되돌림
        if caught_gemstone:
            update_score(caught_gemstone.price)
            gemstone_group.remove(caught_gemstone) # 잡힌 보석 삭제
            caught_gemstone = None 

    if not caught_gemstone:
        for gemstone in gemstone_group:
            # if claw.rect.colliderect(gemstone.rect): #직사각형 기준으로 충돌체크
            if pygame.sprite.collide_mask(claw, gemstone): # 실제 이미지 영역과 충돌체크 (그림에 투명도 설정해줘야함 conver_alpha())
                caught_gemstone = gemstone
                to_x = -gemstone.speed # 잡힌 보석의 속도만큼 -
                break

    if caught_gemstone:
        caught_gemstone.set_position(claw.rect.center, claw.angle)

    screen.blit(background, (0, 0))
    gemstone_group.draw(screen) # 그룹 내 모든 스프라이트 출력
    claw.upadate(to_x)
    claw.draw(screen)

    display_score()

    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ms -> s
    display_time(total_time - int(elapsed_time))

    if total_time - int(elapsed_time) <= 0:
        running = False
        if curr_score >= goal_score:
            game_result = "Mission Complete"
        else: game_result = "Game Over"
        display_game_over()

    
    pygame.display.update()

pygame.time.delay(2000)
pygame.quit()