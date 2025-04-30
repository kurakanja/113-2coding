import pygame
import os
import random

pygame.init()
study_point = 0
energy_point = 70
health_point = 70
screen_height = 600
screen_width = 1100
screen = pygame.display.set_mode((screen_width, screen_height))
desired_size=(80,80)
theme_size=(538,632)
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
SLEEP_ = pygame.transform.scale(pygame.image.load(os.path.join("images/obj", "睡覺.png")), desired_size)
DRINK_ = pygame.transform.scale(pygame.image.load(os.path.join("images/obj", "喝酒.png")), desired_size)
FOOD_ = pygame.transform.scale(pygame.image.load(os.path.join("images/obj", "食物.png")), desired_size)
TEACHER_ = pygame.transform.scale(pygame.image.load(os.path.join("images/obj", "教授.png")), desired_size)
TTHEME_GIRL=[
    pygame.transform.scale(pygame.image.load(os.path.join("images/teachertheme", "ttheme_girl_normal.png")), theme_size),
    pygame.transform.scale(pygame.image.load(os.path.join("images/teachertheme", "ttheme_girl_dunno.png")), theme_size),
    pygame.transform.scale(pygame.image.load(os.path.join("images/teachertheme", "ttheme_girl_wow.png")), theme_size)
]
TTHEME_TEACHER=pygame.transform.scale(pygame.image.load(os.path.join("images/teachertheme", "ttheme_teacher.png")), theme_size)

class Dinosaur:
    X_pos = 80
    Y_pos = 310
    set_jump_vel = 8.5

    def __init__(self):

        self.run_img = RUNNING
        self.run_index = 0 #動畫用
        self.jump_img = JUMPING

        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.set_jump_vel
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_pos
        self.dino_rect.y = self.Y_pos

        self.start_y = self.Y_pos  # 記住起跳的初始高度
        self.max_jump_height = 170  # 最多可以跳到「高170像素」那麼高

    def update(self, userInput):
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump(userInput)  # jump 要傳 userInput！

        if self.step_index >= 20:
            self.step_index = 0

        if userInput[pygame.K_SPACE] and not self.dino_jump:
            self.dino_run = False
            self.dino_jump = True
            self.start_y = self.dino_rect.y  # 起跳時記錄起點

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

    def jump(self, userInput):
        self.image = self.jump_img
        if self.dino_jump:
            height_jumped = self.start_y - self.dino_rect.y

            if userInput[pygame.K_SPACE] and self.jump_vel > 0 and height_jumped < self.max_jump_height:
                self.jump_vel -= 0.2
            else:
                self.jump_vel -= 0.85

            self.dino_rect.y -= self.jump_vel * 2

            print(f"y pos: {self.dino_rect.y}, jump vel: {self.jump_vel:.2f}, height jumped: {height_jumped}")

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
        self.type = type
        if isinstance(image, list):
            self.image = image[self.type]
        else:
            self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        
    def update(self):
        self.rect.x -= game_speed
        
    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)

class study(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 1)
        super().__init__(image, self.type)
        self.rect.y = random.randint(70, 310)

class food(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.randint(70, 310)

class drink(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.randint(70, 310)

class teacher(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.randint(70, 310)

class sleep(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.randint(70, 310)
 

def main():
    global game_speed, x_pos_bg, y_pos_bg, obstacles, points, study_point,energy_point, health_point
    run = True
    clock = pygame.time.Clock()
    cloud = Cloud()
    player = Dinosaur()
    game_speed = 10
    x_pos_bg = 0
    y_pos_bg = 380
    obstacles = []
    death_count = 0
    study_point = 0
    energy_point = 70
    health_point = 70
    sleep_count = 0
    drink_count = 0
    teacher_count = 0
    font = pygame.font.Font(os.path.join("images/font", "ARCADECLASSIC.TTF"), 30)
    font_ch = pygame.font.Font(os.path.join("images/font", "NotoSansTC-Black.otf"), 20)
   


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
        text_color = (94, 94, 94)

        # 分數
        study_text = font_ch.render(f"讀書進度：{study_point}", True, text_color)

        # 類別統計（中文顯示）
        energy_text = font_ch.render(f"精力值：{energy_point}", True, text_color)
        health_text = font_ch.render(f"健康度：{health_point}", True, text_color)

        screen.blit(study_text, (800, 30))
        screen.blit(energy_text, (800, 60))
        screen.blit(health_text, (800, 90))

    def trigger_teacher_event():
        global  study_point,energy_point
        run_event = True
        stage = 0
        girl_img = TTHEME_GIRL[0]
        teacher_img = TTHEME_TEACHER

        font_ch = pygame.font.Font(os.path.join("images/font", "NotoSansTC-Black.otf"), 24)

        dialogues = [
            ["太好了同學，剛好你來幫我整理這些文件吧", "被迫幫忙教授", 1, -10, 0],
            ["同學有哪裡不懂嗎", "和教授討論中", 2, 0, 10]
        ]
        chosen_dialogue = random.choice(dialogues)

        while run_event:
            screen.fill((255, 255, 255))

            screen.blit(girl_img, (-100, 50))
            screen.blit(teacher_img, (650, 20))

            dialogue_text = font_ch.render(chosen_dialogue[stage], True, (0, 0, 0))
            screen.blit(dialogue_text, (screen_width // 2 - dialogue_text.get_width() // 2, 150))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if stage == 0:
                        girl_img = TTHEME_GIRL[chosen_dialogue[2]]
                        energy_point += chosen_dialogue[3]
                        study_point += chosen_dialogue[4]
                        stage = 1
                        
                    else:
                        run_event = False

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

        # 隨機生成障礙物（增加出現頻率，可同時出現多個）機率
        if random.random() < 0.05:
            r = random.random()
            if r < 0.04:
                obstacles.append(teacher(TEACHER_))
            else:
                obstacle_type = random.choice(["studying", "sleeping", "drinking", "eating"])
                if obstacle_type == "studying":
                    obstacles.append(study(STUDY_))
                elif obstacle_type == "sleeping":
                    obstacles.append(sleep(SLEEP_))
                elif obstacle_type == "drinking":
                    obstacles.append(drink(DRINK_))
                elif obstacle_type == "eating":
                    obstacles.append(food(FOOD_))


        # 更新障礙物與碰撞處理（碰到會加分且消失）
        for obstacle in obstacles[:]:  # 副本避免邊迴圈邊移除問題
            obstacle.draw(screen)
            obstacle.update()
            # 縮小碰撞框，避免偵測過敏
            dino_hitbox = player.dino_rect.inflate(-70, -70)
            obstacle_hitbox = obstacle.rect.inflate(-50, -50)
            #確認hitbox用
            pygame.draw.rect(screen, (255, 0, 0), dino_hitbox, 2)
            pygame.draw.rect(screen, (0, 0, 255), obstacle_hitbox, 2)
            #改分數
            
            if player.dino_rect.colliderect(obstacle_hitbox):
                if isinstance(obstacle, study):
                    study_point += 10
                    energy_point -= 5
                    obstacles.remove(obstacle)
                elif isinstance(obstacle, sleep):
                    health_point += 10
                    energy_point += 10
                    sleep_count += 1
                    obstacles.remove(obstacle)
                elif isinstance(obstacle, drink):
                    health_point -= 15
                    energy_point += 10
                    drink_count += 1
                    obstacles.remove(obstacle)
                elif isinstance(obstacle, food):
                    health_point += 5
                    energy_point += 5
                    obstacles.remove(obstacle)
                elif isinstance(obstacle, teacher):
                    teacher_count += 1
                    obstacles.remove(obstacle)
                    trigger_teacher_event()

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
