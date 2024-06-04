import cv2
import pygame
import sys
import os
import random
import Prisoner
import inferredgame
import test2
import prisonersDilemma
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import threading
import matplotlib.pyplot as plt
# Initialising Pygame and Video Playback
pygame.init()
intro_video_path = 'videos/opening.mp4'  # Startup animated video
loop_video_path = 'videos/looping.mp4'  # Looped video
intro1_video_path = 'videos/startreverse2.mp4'
background_video_path = 'videos/clean1.mp4'
font_path = 'fonts/Alderamind-Italic.otf'
intro_cap = cv2.VideoCapture(intro_video_path)
intro1_cap = cv2.VideoCapture(intro1_video_path)
loop_cap = cv2.VideoCapture(loop_video_path)
clean_cap = cv2.VideoCapture(background_video_path)
loop_start_time = None  # 初始化为 None
intro_start_time = 0
record_x = 0
record_y = 0
# Set flags to know when to play the startup animation and when to play the looping video
intro_playing = True
game_selected = False

##设置画册变量
artbook_images = [pygame.image.load(os.path.join('artbook folder', img)) for img in os.listdir('artbook folder') if
                  img.endswith(('.png', '.jpg'))]
current_image_index = 0
image_scale = 1.0
# 设置 Pygame 窗口大小和标题
screen = pygame.display.set_mode((960, 600), pygame.RESIZABLE)
pygame.display.set_caption('Bang Bang Simulation')
pygame.font.init()

# 设置字体和大小
font = pygame.font.Font(font_path, 36)
font1 = pygame.font.Font(font_path, 24)

# 定义菜单项和当前选中的项
menu_items = ['Select Games', 'Options', 'Artbook', 'Music', 'Quit', 'Dedication','Instructions']
current_item = 0

# 全局变量定义区域
start_x, start_y = 510, 200  # 初始值基于窗口的默认大小

MENU_MAIN = 0
MENU_MUSIC = 1
MENU_GAMES = 2
MENU_ARTBOOK = 3
MENU_Dedication = 4
menu_options = 5
menu_hawk = 6
meNu_prisoners = 7
MENU_instructions = 8
# 定义游戏选择菜单项
games_menu_items = ['Hawk and Dove', 'Prisoners\' Dilemma', 'Attorney Wright', 'Return to Main Menu']
dedication_menu_items = ['Thank you for watching', 'Rollback']
option_menu_items = ['Quiet Please', 'Louder!', 'Thank you for watching', 'Rollback']
instruction_menu_items = ['Thank you for watching', 'Rollback']
# 当前菜单状态
current_menu = MENU_MAIN

# 在游戏的初始化部分添加
input_active = False
input_text = ""
input_temt = 0
starting_hawk = 100  # 假设这是你想要设置的变量
starting_dove = 300
rounds = 20
min_food = 20
starting_energy = 100
signa_flag = 0

# 主菜单和音乐菜单项
pygame.mixer.init()
select_sound = pygame.mixer.Sound('videos/Persona 5 - Select Sound Effect.mp3')
confirm_sound = pygame.mixer.Sound('videos/click.mp3')
main_menu_items = ['Select Games', 'Options', 'Artbook', 'Music', 'Quit', 'Dedication','Instructions']
music_menu_items = ['Changing Seasons -Reload-', 'Full Moon, Full Life', 'heartbeat, heartbreak', 'Mass Destruction',
                    'Burn My Dread', 'Your Memory', 'Color Your Night',
                    'When The Moon’s Reaching Out Stars', 'When The Moon’s Reaching Out Stars-lofi',
                    'Return to Main Menu', 'Stop Playback']
hawk_menu_items = ['Starting Hawks', 'Starting Doves', 'Rounds', 'MIN_FOOD_PER_ROUND', 'STARTING_ENERGY','Initiate Game','Start Game', 'Rollback']
prisoners_menu_items = ['Results are shown below', 'Rollback']
volume_default = 1
current_track = 0
rollback_flag = 0
# 音乐文件列表
music_files = [
    'music/Changing seasons.mp3',
    'music/Full moon, Full Life.mp3',
    'music/heartbeat.mp3',
    'music/川村ゆみ,Lotus Juice - Mass Destruction.mp3',
    'music/川村ゆみ - Burn My Dread.mp3',
    'music/川村ゆみ - キミの記憶.mp3',
    'music/ATLUS Sound Team,Lotus Juice,高橋あず美 - Color Your Night.mp3',
    'music/ATLUS Sound Team - When The Moon’s Reaching Out Stars -Reload-.mp3',
    'music/夜巡事务所音乐部 - When The Moon’s Reaching Out Stars.mp3',

]
###

Dedication_content = "As time hurtles forward, we stand on the brink of graduation, a testament to the swift passage of four transformative years. Throughout this journey, we've navigated a myriad of challenges, each obstacle a lesson in resilience, teaching us to face the world with grace and composure." \
                     " It's in these moments of trial and triumph that we find the true essence of our college experience—not just in the academic rigor, but in the profound personal growth it fosters." \
                     "In the waning days of this chapter, I encountered Persona 3: Reload, a game that captivated me not just with its gameplay, but with the depth of its protagonist and the complexity of their journey." \
                     " It's a narrative that resonates deeply, reflecting the struggles and revelations we've encountered in our own lives." \
                     "This dedication is a tribute to everything that has colored my nights during these college years." \
                     " To the friends who've stood by me, to the lessons that have shaped me, and to the experiences that have challenged me—thank you. Your influence has been the palette with which I've painted my story, turning the darkest nights into a canvas of stars. Here's to the moments we've shared and the memories we've created, a mosaic of our collective journey."

instruction_content = "Starting Hawks: The number of hawks before round 1 starts(in round 0)."\
 "Starting Doves: The number of doves before round 1 starts(in round 0)."\
 "Rounds: The entire number of rounds to be played(if input is 100, it will take drastically long)"\
 "Min_food_per_round: The minimum food amount generated by system in each round." \
  "Starting Energy: The starting energy amount for two groups to breed and survive."\
  "All parameters in integer format, other formats would be caught and thrown out."\
  "If you do not know how to set these parameters, just click on start game to kickstart with default values."

instruction_content1 = [
    "Starting Hawks: The number of hawks before round 1 starts (in round 0).",
    "Starting Doves: The number of doves before round 1 starts (in round 0).",
    "Rounds: The entire number of rounds to be played (if input is 100, it will take drastically long)",
    "Min_food_per_round: The minimum food amount generated by system in each round.",
    "Starting Energy: The starting energy amount for two groups to breed and survive.",
    "All parameters in integer format, other formats would be caught and thrown out.",
    "If you do not know how to set these parameters, just click on start game to kickstart with default values.",
    "For prisoners' dilemma, C for cooperation, D for defect ",
    "If player1 cooperates, player2 defects. player1 benefit:0 player2 benefit: +5",
    "If both cooperate, player1:+3 player2：+3 if both defect, player1:+0 benefit player2:+0 benefit",
    "Extend the current strategy pool by adding new strategies into the strategy folder",
    "For attorney wright, remember that Evidence = Rock Cross-Exam = Scissors Bluff = Paper",
    "Damage calculation formula: Damage = 10+3* Strategy star level",
    "E.g.,the damage caused by 7-star evidence strat is:10+3*7 =31hp, only cause damage if you win the duel",
    "Each player starts with 100hp, the one lost hp to 0 counts as eliminated"
]

####拨片动画
image1_path = 'fonts/[lab.magiconch.com][福音戰士標題生成器]-1710810726979.jpg'
image2_path = 'fonts/[lab.magiconch.com][福音戰士標題生成器]-1710811149906.jpg'
image1 = pygame.image.load(image1_path)
image2 = pygame.image.load(image2_path)

# 初始化拨片图片显示逻辑的变量
show_splash_screens = True
splash_screen_index = 1  # 从第一张图片开始
splash_screen_start_time = pygame.time.get_ticks()  # 记录开始显示拨片图片的时间
splash_screen_duration = 1000  # 每张图片显示2000毫秒（2秒）
record = 200

# Define menu rendering functions
def draw_menu():
    global current_menu, current_item, current_angle

    # Select the menu item list according to the current menu status
    if current_menu == MENU_MAIN:
        menu_items = main_menu_items
        angle_decrement = 11  # Angle decrement value between each option
        initial_angle = 40
    elif current_menu == MENU_MUSIC:

        menu_items = music_menu_items
        angle_decrement = 5
        initial_angle = 40
    elif current_menu == MENU_GAMES:
        menu_items = games_menu_items
        angle_decrement = 0  # Angle decrement value between each option
        initial_angle = 0
    elif current_menu == MENU_Dedication:
        menu_items = dedication_menu_items
        angle_decrement = 0
        initial_angle = 0
        wrapped_text = wrap_text(Dedication_content, font1, 3 * screen.get_width() / 5)

        y = screen.get_height() / 3  # Initial y-coordinate
        for line in wrapped_text:
            text_surface = font1.render(line, True, (255, 255, 255))  # Assuming the text colour is white
            screen.blit(text_surface, (screen.get_width() / 5 * 2, 9 / 7 * y))
            y += font1.get_linesize()  # Update y-coordinate
    elif current_menu == MENU_instructions:
        menu_items = instruction_menu_items
        angle_decrement = 0
        initial_angle = 0
        wrapped_text = wrap_text(instruction_content, font1, screen.get_width()*0.45)

        y = screen.get_height() / 3  # Update y-coordinate
        for line in instruction_content1:
            text_surface = font1.render(line, True, (255, 255, 255))  # Assuming the text colour is white
            screen.blit(text_surface, (screen.get_width() *0.35, 9 / 7 * y))
            y += font1.get_linesize()  # Update y-coordinate once again
    elif current_menu == MENU_ARTBOOK:
        menu_items = dedication_menu_items
        angle_decrement = 0
        initial_angle = 0
        # current_image = pygame.transform.scale(artbook_images[current_image_index],
        #                                        (int(artbook_images[
        #                                                 current_image_index].get_width() * image_scale),
        #                                         int(artbook_images[
        #                                                 current_image_index].get_height() * image_scale)))
        # #
        # # # 将图片绘制到屏幕中心
        # image_rect = current_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(current_image, image_rect.topleft)
        # for event in pygame.event.get():
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_LEFT:
        #             # 切换到上一张图片
        #             current_image_index = (current_image_index - 1) % len(artbook_images)
        #             image_scale = 1.0  # 重置缩放比例
        #         elif event.key == pygame.K_RIGHT:
        #             # 切换到下一张图片
        #             current_image_index = (current_image_index + 1) % len(artbook_images)
        #             image_scale = 1.0  # 重置缩放比例
        #         elif event.key == pygame.K_UP:
        #             # 放大图片
        #             image_scale *= 1.1
        #         elif event.key == pygame.K_DOWN:
        #             # 缩小图片
        #             image_scale *= 0.9
    elif current_menu == menu_options:
        menu_items = option_menu_items
        angle_decrement = 0
        initial_angle = 0
    elif current_menu == menu_hawk:
        menu_items = hawk_menu_items
        angle_decrement = 0
        initial_angle = 0
    elif current_menu == meNu_prisoners:
        menu_items = prisoners_menu_items
        angle_decrement = 0
        initial_angle = 0
        with open('results.txt', 'r') as file:
            content = file.read()

            # Find what comes after 'total scores:'
        index = content.find('TOTAL SCORES')
        if index != -1:
            display_text = content[index:]
            lines = display_text.split('\n')
            text_color = (255, 255, 255)
            # Create text surface
            y_offset = 3*screen.get_height()/7
            for line in lines:
                text_surface = font1.render(line, True, text_color)
                screen.blit(text_surface, (screen.get_width()/2-text_surface.get_width()/2, y_offset))
                y_offset += 30  # Increase the y-coordinate to show the next line

    item_height = 49
    # initial_angle = 40  # 初始旋转角度

    for index, item in enumerate(menu_items):
        # 计算当前选项的旋转角度
        current_angle = initial_angle - index * angle_decrement

        # 设置文本颜色
        text_color = (255, 255, 255)
        # text_color = (106, 249, 255)  # 默认白色
        if index == current_item:
            text_color = (0, 0, 0)  # 选中项为黑色

        text_surface = font.render(item, True, text_color)

        # Plotting triangles on selected options
        if index == current_item:
            # 创建一个足够大的Surface来容纳旋转后的三角形
            triangle_surface = pygame.Surface((text_surface.get_width() + 60, text_surface.get_height() + 30),
                                              pygame.SRCALPHA)
            triangle_surface1 = pygame.Surface((text_surface.get_width() + 60, text_surface.get_height() + 30),
                                               pygame.SRCALPHA)
            # 绘制三角形
            pygame.draw.polygon(triangle_surface, (225, 225, 225),
                                [(0, triangle_surface.get_height()), (triangle_surface.get_width() / 2, 0),
                                 (triangle_surface.get_width(), triangle_surface.get_height())])
            pygame.draw.polygon(triangle_surface1, (251, 135, 244),
                                [(0, triangle_surface.get_height() + 7), (triangle_surface.get_width() / 2 - 7, -5),
                                 (triangle_surface.get_width() + 7, triangle_surface.get_height() + 7)])
            # 旋转三角形
            rotated_triangle = pygame.transform.rotate(triangle_surface, current_angle)
            rotated_triangle1 = pygame.transform.rotate(triangle_surface1, current_angle)
            triangle_rect = rotated_triangle.get_rect(center=(start_x, start_y + index * item_height))
            screen.blit(rotated_triangle1, triangle_rect.topleft)
            screen.blit(rotated_triangle, triangle_rect.topleft)

        scale_factor = 2  # magnify the scale of text
        scaled_surface = pygame.transform.smoothscale(text_surface, (
            text_surface.get_width() * scale_factor, text_surface.get_height() * scale_factor))

        # rotating text after magnify

        # Rotating text surface
        text_surface = pygame.transform.rotate(text_surface, current_angle)

        # Get position after rotation
        text_rect = text_surface.get_rect(center=(start_x, start_y + index * item_height))
        screen.blit(text_surface, text_rect)


def get_menu_item_under_mouse(mouse_pos):
    item_height = 45
    for index, item in enumerate(menu_items):
        # Assume that each menu item has a width of 200px and a height of item_height
        item_rect = pygame.Rect(start_x - 100, start_y + index * item_height, 247, item_height)

        if item_rect.collidepoint(mouse_pos):
            return index
    return None


def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    return lines



# 游戏主循环
running = True
while running:
    current_image = pygame.transform.scale(artbook_images[current_image_index],
                                           (int(artbook_images[
                                                    current_image_index].get_width() * image_scale),
                                            int(artbook_images[
                                                    current_image_index].get_height() * image_scale)))
    image_rect = current_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    # 检查事件
    # current_time = pygame.time.get_ticks()
    # if show_splash_screens:
    #     if splash_screen_index == 1:
    #         screen.blit(image1, (0, 0))  # 显示第一张图片
    #     elif splash_screen_index == 2:
    #         screen.blit(image2, (0, 0))  # 显示第二张图片
    #
    #     # 检查是否应该切换到下一张图片或结束显示拨片图片
    #     if current_time - splash_screen_start_time > splash_screen_duration:
    #         splash_screen_index += 1
    #         splash_screen_start_time = current_time  # 重置计时器
    #         if splash_screen_index > 2:
    #             show_splash_screens = False  # 结束显示拨片图片
    #             intro_start_time = pygame.time.get_ticks()  # 重置介绍视频的开始时间，如果你在之后需要它

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # 用户改变了窗口大小
            window_size = event.size  # 新的窗口大小
            screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
            # 更新菜单的起始位置，这里以居中为例
            start_x = window_size[0] * 17 / 32  # 水平居中
            record_x = window_size[0] * 17 / 32
            start_y = window_size[1] / 3  # 垂直位置根据需要调整
            record_y = window_size[1] / 3
        elif event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_RETURN:
                    # 用户按下回车键，输入结束
                    try:
                        if signa_flag == 0:
                            starting_hawk = int(input_text)  # 尝试将文本转换为整数
                        elif signa_flag == 1:
                            starting_dove = int(input_text)  # 尝试将文本转换为整数
                        elif signa_flag == 2:
                            rounds = int(input_text)
                        elif signa_flag == 3:
                            min_food = int(input_text)
                        elif signa_flag == 4:
                            starting_energy = int(input_text)

                    except ValueError:
                        print("Only type in integers please")
                        # 如果转换失败，可能需要提示用户重新输入
                        pass
                    input_active = False  # 关闭输入状态
                    input_text = ""  # 清空输入文本
                    # 可以在这里添加代码来处理输入完成后的逻辑，比如返回游戏菜单
                elif event.key == pygame.K_BACKSPACE:
                    # 处理退格键，删除最后一个字符
                    input_text = input_text[:-1]
                    if input_text == "":
                        input_active = False
                else:
                    # 添加新的字符到输入文本
                    input_text += event.unicode

            if current_menu != MENU_ARTBOOK:
                if event.key == pygame.K_UP:
                    select_sound.play()
                    current_item = (current_item - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    select_sound.play()
                    current_item = (current_item + 1) % len(menu_items)
            else:
                if event.key == pygame.K_LEFT:
                    # 切换到上一张图片
                    current_image_index = (current_image_index - 1) % len(artbook_images)
                    image_scale = 0.7  # 重置缩放比例
                elif event.key == pygame.K_RIGHT:
                    print("test")
                    print(current_image_index)
                    # 切换到下一张图片
                    current_image_index = (current_image_index + 1) % len(artbook_images)
                    image_scale = 0.7  # 重置缩放比例
                elif event.key == pygame.K_UP:
                    # 放大图片
                    image_scale *= 1.1
                elif event.key == pygame.K_DOWN:
                    # 缩小图片
                    image_scale *= 0.9

        elif event.type == pygame.MOUSEMOTION:
            # get position of mouse
            mouse_pos = event.pos
            # check if it is on menu item
            hovered_item = get_menu_item_under_mouse(mouse_pos)
            if hovered_item is not None:
                if hovered_item != current_item:
                    select_sound.play()
                current_item = hovered_item

        elif event.type == pygame.MOUSEBUTTONDOWN:

            # Dealing with the operating logic of mouse movement after clicking
            # for instance，if clicked on left （button 1）, conduct corresponding results/switches
            if event.button == 1:  # left click

                # Check if clicked on item
                clicked_item = get_menu_item_under_mouse(event.pos)
                if clicked_item is not None:
                    confirm_sound.play()
                    current_item = clicked_item
                    # Adding logic of menues
                    print(f"Clicked on menu item: {menu_items[current_item]}")
                    if current_menu == MENU_MAIN and menu_items[current_item] == "Music":
                        record = start_y
                        start_y = 90
                        current_menu = MENU_MUSIC

                        menu_items = music_menu_items
                        current_item = 0  # reset the item number to the first item

                        # choosing music from options
                    elif current_menu == MENU_MUSIC:
                        if current_item < len(music_files):
                            # Playing selected song
                            pygame.mixer.music.load(music_files[current_item])
                            pygame.mixer.music.play(-1)
                        elif menu_items[current_item] == 'Return to Main Menu':
                            # returning back to main menu
                            current_menu = 0
                            menu_items = main_menu_items
                            start_y = record
                            current_item = 0
                        elif menu_items[current_item] == "Stop Playback":
                            pygame.mixer.music.stop()  # Stop Playing Music
                    elif current_menu == MENU_MAIN and main_menu_items[current_item] == "Select Games":
                        # intro_cap = intro1_cap

                        loop_cap = clean_cap
                        # intro_playing = True  # Set to True to start playing intro2
                        game_selected = True  # flag is set to True
                        current_menu = MENU_GAMES
                        menu_items = games_menu_items
                        current_item = 0  # 重置到游戏菜单的第一个选项
                    elif current_menu == MENU_GAMES and menu_items[current_item] == "Hawk and Dove":
                        current_menu = menu_hawk
                        menu_items = hawk_menu_items
                    elif current_menu == MENU_GAMES and menu_items[current_item] == "Prisoners' Dilemma":
                        current_menu = meNu_prisoners
                        menu_items = prisoners_menu_items
                        process2 = threading.Thread(target=prisonersDilemma.run_tournament())

                        process2.start()
                    elif current_menu == MENU_GAMES and menu_items[current_item] == "Attorney Wright":
                        # inferredgame.main()
                        process3 = threading.Thread(
                            target=inferredgame.main)

                        process3.start()
                    elif current_menu == meNu_prisoners and menu_items[current_item] == "Rollback":
                        current_menu = MENU_GAMES
                        menu_items = games_menu_items
                        current_item = 0

                    elif current_menu == menu_hawk and menu_items[current_item] == "Starting Hawks":
                        input_active = True  # 激活输入状态
                        input_text = ""  # 清空之前的输入（如果有）
                        print(f"starting_hawk number: {starting_hawk}")
                    elif current_menu == menu_hawk and menu_items[current_item] == "Starting Doves":
                        input_active = True  # 激活输入状态
                        input_text = ""
                        signa_flag = 1
                        print(starting_dove)
                    elif current_menu == menu_hawk and menu_items[current_item] == "Rounds":
                        input_active = True  # 激活输入状态
                        input_text = ""
                        signa_flag = 2
                        print(rounds)
                    elif current_menu == menu_hawk and menu_items[current_item] == "MIN_FOOD_PER_ROUND":
                        input_active = True  # 激活输入状态
                        input_text = ""
                        signa_flag = 3
                        print(min_food)
                    elif current_menu == menu_hawk and menu_items[current_item] == "STARTING_ENERGY":
                        input_active = True  # 激活输入状态
                        input_text = ""
                        signa_flag = 4
                        print(starting_energy)
                    elif current_menu == menu_hawk and menu_items[current_item] == "Initiate Game":
                        Prisoner.STARTING_HAWKS = starting_hawk
                        Prisoner.STARTING_DOVES = starting_dove
                        Prisoner.ROUNDS = rounds
                        Prisoner.MIN_FOOD_PER_ROUND = min_food
                        Prisoner.STARTING_ENERGY = starting_energy
                        process1 = threading.Thread(target=Prisoner.main)

                        process1.start()
                    elif current_menu == menu_hawk and menu_items[current_item] == "Start Game":
                        process1 = threading.Thread(target=Prisoner.main)

                        process1.start()
                    elif current_menu == menu_hawk and menu_items[current_item] == "Rollback":
                        current_menu = MENU_GAMES
                        menu_items = games_menu_items
                        current_item = 0
                    elif current_menu == MENU_MAIN and main_menu_items[current_item] == "Dedication":
                        current_menu = MENU_Dedication
                        menu_items = dedication_menu_items
                        # wrapped_text = wrap_text(Dedication_content, font, screen.get_width())
                        #
                        # y = 400  # 初始y坐标
                        # for line in wrapped_text:
                        #     text_surface = font.render(line, True, (255, 255, 255))  # 假设文本颜色为白色
                        #     screen.blit(text_surface, (500, y))
                        #     y += font.get_linesize()  # 更新y坐标 重复故注解掉了
                        current_item = 0  # 重置到游戏菜单的第一个选项
                    elif current_menu == MENU_Dedication and menu_items[current_item] == 'Rollback':

                        current_menu = 0
                        menu_items = main_menu_items
                        current_item = 0
                    elif current_menu == MENU_MAIN and main_menu_items[current_item] == "Instructions":
                        current_menu = MENU_instructions
                        menu_items = instruction_menu_items

                        current_item = 0  # 重置到游戏菜单的第一个选项
                    elif current_menu == MENU_instructions and menu_items[current_item] == 'Rollback':

                        current_menu = 0
                        menu_items = main_menu_items
                        current_item = 0
                    elif current_menu == MENU_MAIN and menu_items[current_item] == "Artbook":
                        menu_items = dedication_menu_items
                        current_menu = MENU_ARTBOOK
                        current_image_index = 0  # 显示第一张图片
                        image_scale = 0.7  # 重置缩放比例
                    elif current_menu == MENU_ARTBOOK:

                        # 获取当前图片并应用缩放
                        current_image = pygame.transform.scale(artbook_images[current_image_index],
                                                               (int(artbook_images[
                                                                        current_image_index].get_width() * image_scale),
                                                                int(artbook_images[
                                                                        current_image_index].get_height() * image_scale)))

                        # 将图片绘制到屏幕中心
                        image_rect = current_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
                        # screen.blit(current_image, image_rect.topleft)
                        if menu_items[current_item] == 'Rollback':
                            current_menu = 0
                            menu_items = main_menu_items
                            current_item = 0

                        # 处理键盘事件进行图片切换和缩放
                    elif current_menu == MENU_MAIN and main_menu_items[current_item] == "Options":
                        current_menu = menu_options
                        menu_items = option_menu_items
                        current_item = 0
                    elif current_menu == menu_options:
                        if menu_items[current_item] == 'Quiet Please':
                            print('test')
                            volume_default = volume_default - 0.1
                            pygame.mixer.music.set_volume(volume_default)
                        if menu_items[current_item] == 'Louder!':
                            print('test1')
                            volume_default = volume_default + 0.1
                            pygame.mixer.music.set_volume(volume_default)
                        if menu_items[current_item] == 'Rollback':
                            current_menu = 0
                            menu_items = main_menu_items
                            current_item = 0

                    elif current_menu == MENU_GAMES:
                        if current_item < len(games_menu_items) - 1:
                            # 播放选中的歌曲
                            print(current_item)
                        elif menu_items[current_item] == 'Return to Main Menu':
                            # 返回主菜单
                            loop_cap = cv2.VideoCapture(loop_video_path)
                            current_menu = MENU_MAIN
                            menu_items = main_menu_items
                            start_y = 200
                            current_item = 0

                    elif current_menu == MENU_MAIN and menu_items[current_item] == "Quit":
                        pygame.quit()

    # Select the correct cap object according to the currently playing video
    if intro_playing:
        cap = intro_cap
    elif game_selected:  # Replace this with your actual condition check
        cap = intro1_cap
        pygame.display.flip()
        pygame.time.Clock().tick(120)
    else:
        cap = loop_cap

    # Read the next frame of the video
    ret, frame = cap.read()

    # If the frame is read successfully
    if ret:
        # Converts an image's colour space from BGR to RGB (Pygame uses RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Scaling video frames to fill the window
        window_size = screen.get_size()
        frame = cv2.resize(frame, window_size, interpolation=cv2.INTER_LINEAR)

        # Converting an OpenCV image to Pygame's Surface
        frame = pygame.surfarray.make_surface(frame.transpose(1, 0, 2))

        # Rendering video frames on the Pygame window
        screen.blit(frame, (0, 0))

        if pygame.time.get_ticks() - intro_start_time > 2800:
            draw_menu()

    else:

        # 如果启动动画播放完毕，切换到循环视频
        if intro_playing:
            intro_playing = False  # 停止播放启动动画
            intro_cap.release()  # 释放启动动画的 cap 对象
            loop_start_time = pygame.time.get_ticks()  # 记录循环视频开始的时间
        elif game_selected:
            game_selected = False
            intro1_cap.release()  # 释放启动动画的 cap 对象
            loop_start_time = pygame.time.get_ticks()
        else:
            # 如果循环视频播放完毕，重置视频（重新开始）

            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    if input_active:
        # 假设你有一个专门的函数来处理文本渲染，这里只是一个示例
        input_surface = font.render(input_text, True, pygame.Color('white'))
        screen.blit(input_surface, (200, start_y+signa_flag*49))
    # 更新屏幕
    pygame.display.flip()

    # 控制游戏帧率
    pygame.time.Clock().tick(60)

# 释放 VideoCapture 对象
# if intro_playing:
#     intro_cap.release()
# else:
#     loop_cap.release()

# 退出 Pygame
pygame.quit()
sys.exit()
