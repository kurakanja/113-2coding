import pygame
import os
import random

pygame.init()

screen_height = 600
screen_width = 1100
screen = pygame.display.set_mode((screen_width, screen_height))
desired_size=(80,80)
RUNNING = [
    pygame.transform.scale(pygame.image.load(os.path.join("images/Dino", "charactor1.png")), desired_size),
    pygame.transform.scale(pygame.image.load(os.path.join("images/Dino", "charactor2.png")), desired_size),
    pygame.transform.scale(pygame.image.load(os.path.join("images/Dino", "charactor3.png")), desired_size)
]
JUMPING = pygame.transform.scale(pygame.image.load(os.path.join("images/Dino", "charactor jump.png")), desired_size)

CLOUD = pygame.image.load(os.path.join("images/Other", "Chrome Dinosaur Cloud.png"))
BG = pygame.image.load(os.path.join("images/Other", "Chrome Dinosaur Track.png"))
STUDY_ = [
    pygame.transform.scale(pygame.image.load(os.path.join("images/obj", "讀書.png")), desired_size),
    pygame.transform.scale(pygame.image.load(os.path.join("images/obj", "寫報告.png")), desired_size)
]
LARGE_CACTUS = [
    pygame.image.load(
        os.path.join("images/Cactus", "Chrome Dinosaur Large Cactus.png")),
    pygame.image.load(
        os.path.join("images/Cactus", "Chrome Dinosaur Large Cactus (1).png")),
    pygame.image.load(
        os.path.join("images/Cactus", "Chrome Dinosaur Large Cactus (2).png")),
]
BIRD = [
    pygame.image.load(
        os.path.join("images/Bird", "Chrome Dinosaur Bird1.png")),
    pygame.image.load(
        os.path.join("images/Bird", "Chrome Dinosaur Bird2.png")),
]

class Dinosaur:
    X_pos = 80
    Y_pos = 310
    set_jump_vel = 8.5

    def __init__(self):

        self.run_img = RUNNING
        self.run_index = 0  # 加一個動畫 index
        self.jump_img = JUMPING

        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.set_jump_vel
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_pos
        self.dino_rect.y = self.Y_pos

    def update(self, userInput):
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 20:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_run = False
            self.dino_jump = True

        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_run = True
            self.dino_jump = False
    


    def run(self):
        self.image = self.run_img[self.run_index // 3]  # 每 5 frame 換一張
        self.run_index += 1
        if self.run_index >= 9:  # 有 3 張圖，每張重複 5 次 = 15
            self.run_index = 0
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_pos
        self.dino_rect.y = self.Y_pos
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 5
            self.jump_vel -= 0.85
            print(f"y pos: {self.dino_rect.y}, jump vel: {self.jump_vel: .2f}")
        if self.jump_vel < -self.set_jump_vel:
            self.dino_jump = False
            self.jump_vel = self.set_jump_vel
            print("jump stop", self.jump_vel)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = screen_width + random.randint(500, 2000)
        self.y = random.randint(50, 200)
        self.image = CLOUD
        self.width = self.image.get_width()
    
    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = screen_width + random.randint(500, 1500)
            self.y = random.randint(50, 200)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = screen_width
        
    def update(self):
        self.rect.x -= game_speed
        
    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class study(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 1)
        super().__init__(image, self.type)
        self.rect.y = random.choice([300, 325, 340])

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = random.choice([270, 300, 330])

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice([220, 250, 280, 310]) 
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 10:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

def main():
    global game_speed, x_pos_bg, y_pos_bg, obstacles, points
    run = True
    clock = pygame.time.Clock()
    cloud = Cloud()
    player = Dinosaur()
    game_speed = 14
    x_pos_bg = 0
    y_pos_bg = 380
    obstacles = []
    death_count = 0
    points = 0
    font = pygame.font.Font(os.path.join("images/font", "ARCADECLASSIC.TTF"), 30)


    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        bg_rect = BG.get_rect()
        screen.blit(BG, (x_pos_bg, y_pos_bg))
        screen.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            screen.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed
        bg_rect.x = x_pos_bg
    
    def score():
        global points, game_speed
        points += 1

        text = font.render(str(points), True, (94, 94, 94))
        textRect = text.get_rect()
        textRect.center = (1000, 60)
        screen.blit(text, textRect)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
             run = False

        screen.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        cloud.draw(screen)
        cloud.update()

        background()

        score()

        # 隨機生成障礙物（增加出現頻率，可同時出現多個）
        if random.random() < 0.2:
            obstacle_type = random.choice(["small", "large", "bird"])
            if obstacle_type == "small":
                obstacles.append(study(STUDY_))
            elif obstacle_type == "large":
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif obstacle_type == "bird":
                obstacles.append(Bird(BIRD))

        # 更新障礙物與碰撞處理（碰到會加分且消失）
        for obstacle in obstacles[:]:  # 副本避免邊迴圈邊移除問題
            obstacle.draw(screen)
            obstacle.update()
            # 縮小碰撞框，避免偵測過敏
            dino_hitbox = player.dino_rect.inflate(-100, -100)
            obstacle_hitbox = obstacle.rect.inflate(-100, -100)

            if player.dino_rect.colliderect(obstacle.rect):
                points += 10
                obstacles.remove(obstacle)

        player.draw(screen)
        player.update(userInput)        

        clock.tick(30)
        pygame.display.update()
        #移除食物
    for obstacle in obstacles[:]:  # 逐個檢查
        obstacle.update()
        if obstacle.rect.right < 0:
            obstacles.remove(obstacle)


def menu(death_count):
    global points
    run = True
    while run:
        screen.fill((255, 255, 255))
        font = pygame.font.Font(os.path.join("images/font", "ARCADECLASSIC.TTF"), 30)

        if death_count == 0:
            text = font.render("Press any key to start", True, (94, 94, 94))
        elif death_count > 0:
            text = font.render("Press any key to restart", True, (94, 94, 94))
            score = font.render("Your Score  " + str(points), True, (94, 94, 94))
            scoreRect = score.get_rect()
            scoreRect.center = (screen_width // 2, screen_height // 2 + 50)
            screen.blit(score, scoreRect)

        textRect = text.get_rect()
        textRect.center = (screen_width // 2, screen_height // 2)
        screen.blit(text, textRect)
        screen.blit(RUNNING[0], (screen_width // 2 - 20, screen_height // 2 - 140))   
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()

menu(death_count=0)
