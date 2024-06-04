import pygame
import sys
import os
from PIL import Image, ImageSequence
from pygame.locals import *
import pygame.mixer
import threading
import Prisoner
import inferredgame

import prisonersDilemma
import multiprocessing
from queue import Queue
# 初始化pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('music/heartbeat.mp3')  # 替换 'your_bgm_file.mp3' 为你的背景音乐文件路径

animation_duration = 3000  # 3秒
start_time = pygame.time.get_ticks()
# 定义窗口尺寸
subgameinitialed = 0
subgamesflag = 0
width, height = 800, 600
gameflag = 0
iconload = 0  ##iconloading
# 创建窗口
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Bang Bang Simulation")
# 获取当前脚本所在目录
current_dir = os.path.dirname(__file__)

# 构建图片的相对路径
kamen_path = os.path.join(current_dir, "venv", "image", "kamenrider1.png")
icon_path = os.path.join(current_dir, "venv", "image", "icon.png")
prisoner_path = os.path.join(current_dir, "venv", "image", "prisoner2.png")
gif_path = os.path.join(current_dir, "venv", "image", "edge.gif")
pigeon_path = os.path.join(current_dir, "venv", "image", "pigeon12.png")
title_path = os.path.join(current_dir, "venv", "image", "bangbang.png")
image_path = os.path.join(current_dir, "venv", "image", "senpai.jpeg")
pointer_path = os.path.join(current_dir, "venv", "image", "pointer(1)w.png")
white = (255, 255, 255)
black = (0, 0, 0)

gif_frames = []
# 使用Pillow拆解GIF为帧
gif = Image.open(gif_path)
for frame in ImageSequence.Iterator(gif):
    frame = frame.convert('RGBA')  # 转换为RGBA格式以处理透明度
    pygame_image = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
    gif_frames.append(pygame_image)

# 设置帧速率
frame_rate = 10
clock1 = pygame.time.Clock()
clock2 = pygame.time.Clock()
frame_index = 0
##
ratio = 2
kamen_ride = pygame.image.load(kamen_path)
scaled_kamen_width = kamen_ride.get_width() // ratio
scaled_kamen_height = kamen_ride.get_height() // ratio
finally_kamen_ride_decade = pygame.transform.scale(kamen_ride, (scaled_kamen_width, scaled_kamen_height))
##假面骑士改装装填
icon_image = pygame.image.load(icon_path)
prisoner_image = pygame.image.load(prisoner_path)
prisoner_image1 = pygame.transform.scale(prisoner_image,
                                         (prisoner_image.get_width() // 4, prisoner_image.get_height() // 4))
gif_image = pygame.image.load(gif_path)
background_image = pygame.image.load(image_path)  # 替换为你的图片路径
title_image = pygame.image.load(title_path)
pigeon_image = pygame.image.load(pigeon_path)
pointer_image = pygame.image.load(pointer_path)
# 假设 pointer_image 是你想要缩小的图像
original_width = pointer_image.get_width()
original_height = pointer_image.get_height()

# 定义新的宽度，高度将根据原始比例计算
scaled_width = original_width // 6  # 例如，缩小到原始宽度的一半
# 计算新的高度以保持图像比例不变
scaled_height = int((scaled_width / original_width) * original_height)

# 使用 pygame.transform.scale 缩放图像
scaled_pointer_image = pygame.transform.scale(pointer_image, (scaled_width, scaled_height))
##small_title_image = pygame.transform.scale(title_image, (new_width, new_height))
options = ["Start Game", "Options", "Quit"]
selected_option = 0
font_path = 'fonts/Faktos.ttf'
font = pygame.font.Font(font_path, 36)


##规定线程


##实验定义sprite玩家类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)

    def update(self):
        self.rect.x += 1  # 简单的移动效果


def draw_options():
    option_height = 34
    option_width = 300
    option_spacing = 20
    start_x = width // 2 - option_width // 2
    start_y = 300
    selected_color = (254, 195, 29)  # 淡黄色

    ##selected_color.hsla = (30, 238, 133, 100)
    for i, option in enumerate(options):
        option_rect = pygame.Rect(start_x, start_y + i * (option_height + option_spacing), option_width, option_height)

        # 根据选中状态选择底板颜色
        if i == selected_option:
            option_color = selected_color
        else:
            option_color = (51, 141, 191)  # 浅蓝色

        # 绘制底板
        pygame.draw.rect(screen, option_color, option_rect)

        text = font.render(option, True, white if i == selected_option else white)
        text_rect = text.get_rect(center=option_rect.center)

        # 绘制选项文本
        screen.blit(text, text_rect)


def draw_title():
    screen.blit(title_image, (5, 0))


def draw_pigeon():
    # pygame.draw.rect(screen, (51, 141, 191),
    #                  (width // 4 - pigeon_image.get_width() // 2 - 5, 255, pigeon_image.get_width() + 10,
    #                   pigeon_image.get_height() + 10), 2)
    screen.blit(pigeon_image, (width // 4 - pigeon_image.get_width() // 2, 260))
    # 创建字体对象
    screen.blit(prisoner_image1, (width * 4 / 5 - prisoner_image1.get_width() // 2, 260))
    text = font.render("Select Your Game", True, (255, 255, 255))  # 设置文本和颜色

    kamen_x = width // 2 - finally_kamen_ride_decade.get_width() // 2
    screen.blit(finally_kamen_ride_decade, (kamen_x, 50))
    # 计算文本位置
    text_x = width // 2 - text.get_width() // 2  # 居中文
    screen.blit(text, (text_x, 50))

def animation_scene1():

    frame_index = 0
    screen.blit(gif_frames[frame_index], (2*width // 3 - gif_image.get_width() // 2, 260))

    frame_index += 1
    if frame_index >= len(gif_frames):
        frame_index = 0
    clock1.tick(frame_rate)


pygame.mixer.music.play(-1)
# 主循环
while True:
    # 处理事件

    speed = 30

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            # 处理窗口缩放事件
            width, height = event.size
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

        elif event.type == pygame.KEYDOWN and gameflag == 0 and iconload == 1:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                selected_option = (selected_option + 1) % len(options)
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                selected_option = (selected_option - 1) % len(options)
            elif event.key == pygame.K_RETURN:
                if selected_option == 0:  # Start Game
                    print("Starting game...")
                    gameflag = 1

                    # 在这里添加你的游戏逻辑
                elif selected_option == 1:  # Options
                    print("Opening options...")
                    # 在这里添加选项界面的逻辑
                elif selected_option == 2:  # Quit
                    print("Quitting...")
                    running = False
                    pygame.quit()
                    sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            if gameflag == 1:  # 监听回退键按下事件
                gameflag = 0
        elif event.type == pygame.MOUSEBUTTONDOWN and gameflag == 0 and iconload == 1:
            if event.button == 1:  # 鼠标左键点击
                # 获取鼠标位置
                mouse_x, mouse_y = pygame.mouse.get_pos()
                option_height = 34
                option_width = 300
                option_spacing = 20
                start_x = width // 2 - option_width // 2
                start_y = 300

                for i, _ in enumerate(options):
                    option_rect = pygame.Rect(start_x, start_y + i * (option_height + option_spacing),
                                              option_width,
                                              option_height)
                    if option_rect.collidepoint(mouse_x, mouse_y):
                        if selected_option == i:  # 如果点击的是当前已选中的选项
                            if selected_option == 0:  # Start Game
                                print("Starting game...")
                                gameflag = 1
                            elif selected_option == 1:  # Options
                                print("Opening options...")
                                # 在这里添加选项界面的逻辑
                            elif selected_option == 2:  # Quit
                                print("Quitting...")
                                pygame.mixer.music.stop()
                                pygame.mixer.quit()
                                pygame.quit()
                                sys.exit()
                        else:
                            selected_option = i  # 否则更新选中的选项
                        break
        elif event.type == pygame.KEYDOWN and gameflag == 1:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                subgamesflag = (subgamesflag + 1) % len(options)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                subgamesflag = (subgamesflag - 1) % len(options)
            elif event.key == pygame.K_RETURN:
                if subgamesflag == 0:
                    subgameinitialed = 1
                    Prisoner.STARTING_DOVES = 600

                    process1 = threading.Thread(target=Prisoner.main)

                    process1.start()
                elif subgamesflag == 1:
                    process2 = threading.Thread(target=socalledmeta.welcome)
                elif subgamesflag == 2:
                    process3 = threading.Thread(target=prisonersDilemma.runFullPairingTournament)
                    # socalledmeta.welcome()


                    # 等待所有线程完成



    screen.fill((255, 255, 255))
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time
    fade_duration = 1000
    # 渲染游戏背景
    if iconload == 0:
        alpha = min(255, elapsed_time * 255 // fade_duration)
        icon_image.set_alpha(alpha)

        # 显示入场logo

        # 显示入场logo
        screen.blit(icon_image,
                    (width // 2 - icon_image.get_width() // 2, height // 2 - icon_image.get_height() // 2))
        clock2.tick(60)
        if elapsed_time >= animation_duration:
            iconload = 1

    elif iconload == 1:

        screen.blit(background_image, (width // 2 - icon_image.get_width() // 2, 0))

        if gameflag == 0:
            draw_title()
            draw_options()

        elif gameflag == 1:
            draw_pigeon()
            ##import Prisoner

            # 游戏循环
            screen.blit(gif_frames[frame_index], (width // 2 - gif_image.get_width() // 2, 260))

            frame_index += 1
            if frame_index >= len(gif_frames):
                frame_index = 0
            clock1.tick(frame_rate)
            # icon_x = width // 2 - 150 + (selected_icon_index * (subgame_icons[0].get_width() + 10))
            # icon_y = height // 2 - arrow_icon.get_height() - 10  # 箭头位于图标上方
            gap = width // 2 - gif_image.get_width() // 2 - (width // 4 - pigeon_image.get_width() // 2)
            # target_x = width // 4 - pigeon_image.get_width() // 2 + subgamesflag * gap
            # current_x = width // 4 - pigeon_image.get_width() // 2
            # if current_x < target_x:
            #     current_x += min(speed, target_x - current_x)  # 向右移动，但不超过目标位置
            # elif current_x > target_x:
            #     current_x -= min(speed, current_x - target_x)  # 向左移动，但不超过目标位置
            # screen.blit(scaled_pointer_image, (current_x, 120))
            screen.blit(scaled_pointer_image, (width // 4 - pigeon_image.get_width() // 2 + subgamesflag * gap, 120))


            Prisoner.STARTING_DOVES = 600


            # icon_x = width // 2 - 150  # 起始X位置
            # icon_y = height // 2  # Y位置保持不变
            # for index, icon in enumerate(subgame_icons):
            #     if index == selected_icon_index:
            #         # 为选中的图标画一个边框
            #         pygame.draw.rect(screen, (255, 0, 0),
            #                          (icon_x - 5, icon_y - 5, icon.get_width() + 10, icon.get_height() + 10), 2)
            #     screen.blit(icon, (icon_x, icon_y))
            #     icon_x += icon.get_width() + 10  # 更新X位置以放置下一个图标

            # if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            #     if gameflag == 1:  # 监听回退键按下事件
            #         gameflag = 0
            # 设置回初始界面
    # 在这里添加绘制游戏对象的代码

    # 刷新屏幕
    pygame.display.flip()
