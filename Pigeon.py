import pygame
import sys

# 初始化 Pygame
pygame.init()

# 设置窗口大小
size = width, height = 800, 600
screen = pygame.display.set_mode(size)

# 设置标题
pygame.display.set_caption("Pigeon Game")
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 游戏逻辑
    # ...

    # 绘制
    screen.fill((255, 255, 255))  # 白色背景

    # 绘制游戏元素
    # ...

    pygame.display.flip()