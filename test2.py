import os
import sys
import cv2
import torch
import torch.nn as nn
import torch.optim as optim
import pygame
import random
from PIL import Image, ImageSequence
import csv

intro_video_path = 'videos/openingtheme1.mp4'  # 启动动画视频
intro_cap = cv2.VideoCapture(intro_video_path)
loopstart_video_path = 'videos/think1.mp4'
loop_path = 'videos/think2.mp4'
loop1_cap = cv2.VideoCapture(loopstart_video_path)
select_text = "Choose Your Character"
loop2_cap = cv2.VideoCapture(loop_path)
pygame.mixer.init()
pygame.mixer.music.load('videos/openingtheme1.mp3')
# Initialize Pygame
pygame.init()
width, height = 800, 600
# Set up the display loading
current_dir = os.path.dirname(__file__)
gif_path = os.path.join(current_dir, "venv", "image", "edgeworth.gif")
raw_path = os.path.join(current_dir, "venv", "image", "Phoenix_Objection.webp")
background_path = 'fonts/Screenshot-court.jpg'
logo_path = 'fonts/PWAA_logo.png'
frame_index = 0
frame_index1 = 0
clock = pygame.time.Clock()
frame_rate = 30
cap = intro_cap
##about gif
current_loop = 1
gif_frames = []
gif_frames1 = []
# 使用Pillow拆解GIF为帧
white = (255, 255, 255)
black = (0, 0, 0)
gif = Image.open(gif_path)

for frame in ImageSequence.Iterator(gif):
    frame = frame.convert('RGBA')  # 转换为RGBA格式以处理透明度
    pygame_image = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
    gif_frames.append(pygame_image)

gif_image = pygame.image.load(gif_path)

gif_s = Image.open(raw_path)

for frame in ImageSequence.Iterator(gif_s):
    frame = frame.convert('RGBA')  # 转换为RGBA格式以处理透明度
    pygame_image = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
    gif_frames1.append(pygame_image)

##gifstuff
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Attorney")
bg_pic = pygame.image.load(background_path)
bg_pic_resized = pygame.transform.scale(bg_pic, (width, height))

logo_pic = pygame.image.load(logo_path)
logo_pic_resized = pygame.transform.scale(logo_pic, (width / 3, height / 3))
three_options = ['Evidence', 'Cross-examination', 'Bluff']
initial_option = 0
WIN_LIST_RPS = [('Evidence', 'Cross-examination'),  # who can be defeated by ROCK
                ('Cross-examination', 'Bluff'),  # who can be defeated by SCISSORS
                ('Bluff', 'Evidence')]  # who can be defeated by PAPER
# Colors 石头 (Rock) - 举证 (Evidence): 剪刀 (Scissors) - 质询 (Cross-examination):布 (Paper) - 虚张声势 (Bluff):
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
attorney_blue = (51, 141, 191)  # 浅蓝色
attorney_yellow = (254, 195, 29)
player_character = 0
computer_character = 0
# Game variables
player_health = 100
computer_health = 100
player_score = 0
computer_score = 0
ties = 0
rounds = 0
options = ["Start Game", "Options", "Quit"]
selected_option = 0
font_path = 'fonts/Faktos.ttf'
font = pygame.font.Font(font_path, 36)
game_initialted = False
loop_start = False
loopflag = False
play_audio = False


class Character:
    def __init__(self, name, rock_star, paper_star, scissors_star):
        self.name = name
        self.rock_star = rock_star
        self.paper_star = paper_star
        self.scissors_star = scissors_star


# 生成随机角色
# def generate_characters(num_characters):
#     characters = []
#     for i in range(num_characters):
#         name = f"角色{i+1}"
#         rock_star = random.randint(1, 5)
#         paper_star = random.randint(1, 5)
#         scissors_star = random.randint(1, 5)
#         character = Character(name, rock_star, paper_star, scissors_star)
#         characters.append(character)
#     return characters
#
# # 生成7个随机角色
# characters = generate_characters(7)

# 显示生成的角色信息
# print("生成的随机角色:")
# for character in characters:
#     print(f"角色名称: {character.name}, 拳头星级: {character.rock_star}, 布星级: {character.paper_star}, 剪刀星级: {character.scissors_star}")
# Main game loop


characters = [
    Character("Ryuji", 3, 4, 2),
    Character("Shinada", 5, 3, 4),
    Character("Frantze", 7, 5, 5),  ## fake evidence
    Character("Franziska", 4, 2, 5),
    Character("Godot", 4, 5, 4),
    Character("Edgeworth", 5, 5, 4),
    Character("Phoenix", 5, 4, 5)
]


def write_data_to_csv(data, filename='game_data.csv'):
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())

        # 如果文件是新创建的，就写入表头
        if not file_exists:
            writer.writeheader()

        # 写入数据
        writer.writerow(data)


if __name__ == "__main__":
    print("手动定义的角色:")
    for character in characters:
        print(
            f"角色名称: {character.name}, 拳头星级: {character.rock_star}, 布星级: {character.paper_star}, 剪刀星级: {character.scissors_star}")
    if play_audio:
        pygame.mixer.music.play(0)
        print('a')

    # 玩家选择角色


def calculate_damage(self, player_selection, computer_selection):
    if (player_selection, computer_selection) in WIN_LIST_RPS:
        ##self = player_character
        if player_selection == 'Evidence' and computer_selection == 'Cross-examination':
            return 10 + 3 * self.rock_star
        elif player_selection == 'Cross-examination' and computer_selection == 'Bluff':
            return 10 + 3 * self.paper_star
        elif player_selection == 'Bluff' and computer_selection == 'Evidence':
            return 10 + 3 * self.scissors_star
    elif (computer_selection, player_selection) in WIN_LIST_RPS:
        ##self = computer_character
        if player_selection == 'Cross-examination' and computer_selection == 'Evidence':
            return 10 + 3 * self.rock_star
        elif player_selection == 'Bluff' and computer_selection == 'Cross-examination':
            return 10 + 3 * self.paper_star
        elif player_selection == 'Evidence' and computer_selection == 'Bluff':
            return 10 + 3 * self.scissors_star


def record_game_data(player_choice, computer_choice, result, round_number, player_health, computer_health):
    # 这里假设有一个函数用于记录游戏数据
    game_data = {
        'player_choice': player_choice,
        'computer_choice': computer_choice,
        'result': result,
        'round_number': round_number,
        'player_health': player_health,
        'computer_health': computer_health,
    }

    # 将game_data写入CSV文件或数据库
    write_data_to_csv(game_data)  # 你需要实现这个函数\


def choose_strategy():
    # 获取玩家每个选项的星级
    # player_option_star_levels = get_player_option_star_levels()  # 假设这个函数返回如 {'Evidence': 4, 'Cross-examination': 5, 'Bluff': 3}

    # 根据星级选择玩家最强的策略
    strongest_player_option = \
        max(enumerate([player_character.rock_star, player_character.paper_star, player_character.scissors_star]),
            key=lambda x: x[1])[0]

    # 如果电脑健康值低，尝试反击玩家最强的策略
    if computer_health < 50:
        if strongest_player_option == "Evidence":
            return "Cross-examination"
        elif strongest_player_option == "Cross-examination":
            return "Bluff"
        elif strongest_player_option == "Bluff":
            return "Evidence"
    else:
        # 健康值较高时，考虑玩家最常用的策略
        most_common_player_selection = max(set(strongest_player_option), key=strongest_player_option.count)
        if most_common_player_selection == "Evidence":
            return "Cross-examination"
        elif most_common_player_selection == "Cross-examination":
            return "Bluff"
        else:
            return "Evidence"


def draw_options():
    option_height = 34
    option_width = 300
    option_spacing = 20
    start_x = width // 2 - option_width // 2
    start_y = 300
    selected_color = (254, 195, 29)  # 淡黄色

    ##selected_color.hsla = (30, 238, 133, 100)
    for i, option in enumerate(options):
        option_rect = pygame.Rect(start_x, start_y + i * (option_height + option_spacing), option_width,
                                  option_height)

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


# game_data = {
#     'player_choice': player_choice,
#     'computer_choice': computer_choice,
#     'result': result,
#     'round_number': round_number,
#     'player_health': player_health,
#     'computer_health': computer_health,
# }
selected_index = 0  # 当前选中的头像索引
selection_color = (51, 141, 191)  # 选中框的颜色，这里使用红色
selection_thickness = 4  # 选中框的厚度
# 显示玩家和电脑选择的角色信息
avatars = []  # 存储头像的pygame.Surface对象
avatar_positions = []  # 存储头像位置
avatar_size = (100, 100)  # 假设每个头像的大小
start_x, start_y = width / 5, height / 6  # 头像显示的起始位置
spacing = 3 * width / 20  # 头像之间的间距
computer_choice = random.randint(0, 6)
computer_character = characters[computer_choice]
print(f"电脑玩家已选择 {computer_character.name}")
# pygame.mixer.music.play(0)

for character in characters:
    avatar_path = os.path.join("avatar", f"{character.name}.png")
    avatar_image = pygame.image.load(avatar_path)
    avatar_image = pygame.transform.scale(avatar_image, avatar_size)
    avatars.append(avatar_image)

# 计算每个头像的位置
for i in range(len(avatars)):
    if i < 4:  # 第一行的头像（前4个）
        x = start_x + (i % 4) * spacing  # 在第一行中，我们只需要i对4取模
        y = start_y  # 第一行的y坐标保持不变
    else:  # 第二行的头像（剩下3个）
        x = start_x + ((i - 4) % 3) * spacing + spacing / 2  # 第二行头像从中间开始排，因此对3取模，并对x坐标稍作调整
        y = start_y + spacing  # 第二行的y坐标比第一行的y坐标高出一个间距

    avatar_positions.append((x, y))


# 动态计算每个头像的位置
def update_avatar_positions(width, height):
    avatar_positions.clear()  # 清空之前的位置信息
    spacing = 3 * width / 20  # 动态计算间距
    start_x = width / 5
    start_y = height / 6

    # 第一行的头像（前4个）
    for i in range(4):
        x = start_x + (i % 4) * spacing
        y = start_y
        avatar_positions.append((x, y))

    # 第二行的头像（剩下3个），确保居中
    # 计算第二行居中的起始x位置
    total_width_second_row = 3 * avatar_size[0] + 2 * spacing  # 第二行头像的总宽度
    start_x_second_row = (width - total_width_second_row) / 2  # 第二行起始x位置，以保证居中

    for i in range(3):
        x = start_x_second_row + i * (avatar_size[0] + spacing)
        y = start_y + spacing + avatar_size[1]  # 第二行的y位置在第一行之下
        avatar_positions.append((x, y))


if __name__ == "__main__":
    opening_theme = True
    choosing_character = False
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                # 处理窗口缩放事件
                width1, height1 = event.size
                width, height = event.size
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                update_avatar_positions(width, height)
                # 重新缩放背景图像以匹配新的窗口尺寸
                bg_pic_resized = pygame.transform.scale(bg_pic, (width, height))
            elif opening_theme:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:  # Start Game
                            print("Starting game...")
                            opening_theme = False
                            choosing_character = True

                            # 在这里添加你的游戏逻辑
                        elif selected_option == 1:  # Options
                            print("Opening options...")
                            # 在这里添加选项界面的逻辑
                        elif selected_option == 2:  # Quit
                            print("Quitting...")
                            running = False
                            pygame.quit()
                            sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
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
                                        opening_theme = False
                                        choosing_character = True
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
            elif choosing_character:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # 鼠标点击选择的处理...
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # 检查是否点击了某个头像
                    for i, (x, y) in enumerate(avatar_positions):
                        if x <= mouse_x <= x + avatar_size[0] and y <= mouse_y <= y + avatar_size[1]:
                            player_character = characters[i]
                            print(f"您已选择 {player_character.name}")
                            choosing_character = False
                            game_initialted = True
                            break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # 确认选择
                        player_character = characters[selected_index]
                        print(f"您已选择 {player_character.name}")
                        choosing_character = False
                        game_initialted = True
                    elif event.key in [pygame.K_LEFT, pygame.K_a]:
                        selected_index = (selected_index - 1) % len(characters)  # 向左移动
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        selected_index = (selected_index + 1) % len(characters)  # 向右移动
                    elif event.key in [pygame.K_UP, pygame.K_w] and selected_index >= 4:
                        selected_index -= 4  # 第二行向上移动到第一行
                    elif event.key in [pygame.K_DOWN, pygame.K_s] and selected_index < 4:
                        selected_index = min(selected_index + 4, len(characters) - 1)  # 第一行向下移动到第二行
                    elif event.key == pygame.K_BACKSPACE:
                        opening_theme = True
                        choosing_character = False
        if not game_initialted and not loop_start:
            screen.blit(bg_pic_resized, (0, 0))
        if opening_theme:
            screen.blit(logo_pic_resized, (
                width / 2 - logo_pic_resized.get_width() / 2, height / 8))
            draw_options()
        if choosing_character:
            text = font.render(select_text, True, white)
            option_rect = pygame.Rect(width / 2 - text.get_width() / 2, 50, text.get_width(),
                                      34)
            # 绘制选项文本
            pygame.draw.rect(screen, attorney_yellow, option_rect)
            screen.blit(text, (width / 2 - text.get_width() / 2, 50))
            # 绘制头像和选中框
            for i, avatar in enumerate(avatars):
                x, y = avatar_positions[i]
                screen.blit(avatar, (x, y))
                if i == selected_index:
                    # 绘制选中框
                    pygame.draw.rect(screen, selection_color, (
                        x - selection_thickness, y - selection_thickness, avatar_size[0] + 2 * selection_thickness,
                        avatar_size[1] + 2 * selection_thickness), selection_thickness)
        pygame.display.flip()
        cap1 = loop1_cap
        cap2 = loop2_cap
        # 读取视频的下一帧
        if game_initialted:
            cap = intro_cap
        elif loop_start:
            cap1 = loop1_cap
        elif loopflag:
            cap2 = loop2_cap

        # -1 表示循环播放
        ret, frame = cap.read()
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if game_initialted and play_audio == False:
            play_audio = True
            pygame.mixer.music.play(0)

        if game_initialted:
            if ret:
                # 将图像的颜色空间从 BGR 转换成 RGB（Pygame 使用 RGB）
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # 缩放视频帧以填满窗口
                window_size = screen.get_size()
                frame = cv2.resize(frame, window_size, interpolation=cv2.INTER_LINEAR)

                # 将 OpenCV 的图像转换成 Pygame 的 Surface
                frame = pygame.surfarray.make_surface(frame.transpose(1, 0, 2))

                # 在 Pygame 窗口上渲染视频帧
                screen.blit(frame, (0, 0))
                # intro_cap.release()
                # loop_start_time = pygame.time.get_ticks()  # 记录循环视频开始的时间

                pygame.display.flip()
                pygame.time.Clock().tick(60)
            else:
                game_initialted = False
                loop_start = True
                intro_cap.release()
                pygame.display.flip()
            # 如果 frame 读取成功
        elif loop_start:
            if current_loop == 1:
                ret, frame = loop1_cap.read()
            else:
                ret, frame = loop2_cap.read()

            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                window_size = screen.get_size()
                frame = cv2.resize(frame, window_size, interpolation=cv2.INTER_LINEAR)
                frame = pygame.surfarray.make_surface(frame.transpose(1, 0, 2))
                screen.blit(frame, (0, 0))
                pygame.display.flip()
                pygame.time.Clock().tick(60)
            else:
                # 循环视频重新开始
                if current_loop == 1:
                    current_loop = 2  # 切换到 loop2
                loop1_cap.release()
                loop2_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 重新开始 loop2

    pygame.display.flip()

    # Game over
    if player_health <= 0:
        print("You lost!")
    elif computer_health <= 0:
        print("You won!")
    else:
        print("It's a tie!")

    # Quit Pygame
