import pygame
import random
import os
import sys

# 初始化pygame
pygame.init()

# 设置屏幕大小
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("坦子哥不要再画画了")

# 设置角色大小
player_width = 80

# 分数
score = 0

# 定义颜色
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# 加载emoji图像
emojis = [
    pygame.image.load(resource_path(os.path.join("assets", "man.png"))),
    pygame.image.load(resource_path(os.path.join("assets", "ene.png")))
]

# 缩放emoji图像
for i in range(len(emojis)):
    emojis[i] = pygame.transform.scale(emojis[i], (player_width, player_width))

# 加载子弹图像
bullet_width = 40
bullet_height = 60
bullet_image = pygame.image.load(resource_path(os.path.join("assets", "bullet.png")))
bullet_image = pygame.transform.scale(bullet_image, (bullet_width, bullet_height))  # 调整子弹大小

# 子弹设置
bullet_speed = 10
bullets = []

# 玩家初始位置和速度
player_x = screen_width // 2
player_y = screen_height - 100
player_speed = 5

# 玩家朝向
player_direction = 'left'  # 初始朝向为左

# 敌人列表
enemies = []
enemy_count = 5

# 创建敌人
def create_enemy():
    x = random.randint(0, screen_width - player_width)
    y = random.randint(-5 * player_width, -player_width)
    emoji_index = random.randint(1, len(emojis) - 1)
    return [x, y, emoji_index]

def reset_game():
    global score, enemies, bullets, player_x, player_y, player_direction, enemy_spawn_interval, enemy_spawn_timer
    score = 0
    enemies = [create_enemy() for _ in range(enemy_count)]
    bullets = []
    player_x = screen_width // 2
    player_y = screen_height - 100
    player_direction = 'left'
    enemy_spawn_interval = 500
    enemy_spawn_timer = 0

def show_game_over_screen():
    game_over_font = pygame.font.Font(None, 72)
    score_font = pygame.font.Font(None, 36)
    button_font = pygame.font.Font(None, 48)

    game_over_text = game_over_font.render("Game Over", True, red)
    score_text = score_font.render(f"Score: {score}", True, black)

    restart_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 50, 200, 50)
    quit_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 150, 200, 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if restart_button.collidepoint(mouse_pos):
                    reset_game()
                    return
                elif quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()

        screen.fill(white)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 100))
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 - 30))

        pygame.draw.rect(screen, black, restart_button)
        pygame.draw.rect(screen, black, quit_button)

        restart_text = button_font.render("Restart", True, white)
        quit_text = button_font.render("Quit", True, white)

        screen.blit(restart_text, (restart_button.x + 60 - restart_text.get_width() // 2, restart_button.y + 25 - restart_text.get_height() // 2))
        screen.blit(quit_text, (quit_button.x + 50 - quit_text.get_width() // 2, quit_button.y + 25 - quit_text.get_height() // 2))

        pygame.display.flip()
        clock.tick(60)

# 游戏循环标志
running = True
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# 敌人生成相关变量
enemy_spawn_interval = 500  # 初始生成间隔时间（毫秒）
enemy_spawn_timer = 0  # 计时器

# 初始化敌人列表
reset_game()

# 提示文本
hint_text = font.render("Use LEFT/RIGHT arrows to move, SPACE to shoot.", True, black)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # 发射子弹
                bullet_x = player_x + player_width // 2 - 5  # 子弹从玩家中心发射
                bullet_y = player_y
                bullets.append([bullet_x, bullet_y])

    # 获取按键状态
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
        player_direction = 'left'
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
        player_direction = 'right'

    # 确保玩家不移出屏幕边界
    player_x = max(0, min(player_x, screen_width - player_width))

    # 更新子弹位置
    for bullet in bullets[:]:  # 使用切片复制列表以避免在迭代时修改列表
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)

    # 更新敌人位置
    for enemy in enemies[:]:  # 使用切片复制列表以避免在迭代时修改列表
        enemy[1] += 3
        if enemy[1] > screen_height:
            enemies.remove(enemy)
            enemies.append(create_enemy())

    # 检查子弹与敌人的碰撞
    for bullet in bullets[:]:  # 使用切片复制列表以避免在迭代时修改列表
        bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)
        for enemy in enemies[:]:  # 使用切片复制列表以避免在迭代时修改列表
            enemy_rect = pygame.Rect(enemy[0], enemy[1], player_width, player_width)
            if bullet_rect.colliderect(enemy_rect):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1
                enemies.append(create_enemy())

    # 检查玩家与敌人的碰撞
    player_rect = pygame.Rect(player_x, player_y, player_width, player_width)
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], player_width, player_width)
        if player_rect.colliderect(enemy_rect):
            running = False
            show_game_over_screen()
            running = True  # 重新启动游戏循环

    # 绘制背景
    screen.fill(white)

    # 更新敌人生成计时器
    enemy_spawn_timer += clock.get_rawtime()
    clock.tick()  # 重置时钟
    if enemy_spawn_timer >= enemy_spawn_interval:
        enemies.append(create_enemy())
        enemy_spawn_timer = 0

        # 根据分数调整敌人生成间隔时间
        if score % 10 == 0 and enemy_spawn_interval > 100:  # 每10分减少一次生成间隔时间
            enemy_spawn_interval -= 50

    # 绘制敌人
    for enemy in enemies:
        screen.blit(emojis[enemy[2]], (enemy[0], enemy[1]))

    # 绘制子弹
    for bullet in bullets:
        screen.blit(bullet_image, (bullet[0], bullet[1]))

    # 根据朝向绘制玩家
    if player_direction == 'left':
        screen.blit(emojis[0], (player_x, player_y))
    else:
        screen.blit(pygame.transform.flip(emojis[0], True, False), (player_x, player_y))

    # 显示分数（这里简单地显示敌人的数量）
    score_text = font.render(f"Score: {score}", True, black)
    screen.blit(score_text, (10, 50))

    # 显示提示文本
    screen.blit(hint_text, (10, 10))

    # 更新屏幕
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)

# 退出游戏
pygame.quit()






