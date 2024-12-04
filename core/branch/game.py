import pygame
import sys
import os
from pygame.locals import *
import serial
import serial.tools.list_ports
from threading import Thread
from time import sleep


'''
ADDED:
разворот в полный экран
инициализация COM порта
события COM Игрока

TODO:
НА первом экране нужно сделать:
1) ввод имени игроков (добавить в глобальные переменные)
2) изменение таймера (контролами + - с шагом 10 сек, по умолчанию 20 сек


В игровом поле:
увеличить размеры лошадей на 50% (сделать больше на 50%)
Вместо Игрок 1 и Игрок 2 вывести имена игроков (с первого экрана)
'''


USER_COM_EVENT = USEREVENT +1


# Инициализация Pygame

pygame.init()



def get_ports():
    ports = serial.tools.list_ports.comports()
    if ports:
        #print("from get ports",str(ports[0]).split(' ')[0])
        return str(ports[0]).split(' ')[0]
    else:
        return 'NO CONTROLLER'


def com_worker():
    
    global COM_USER_EVENT
    com_on = False
    #print("we are in worker")

    #ser = serial.Serial(port,115200)

    dt = ""    
    while True:
        if not(com_on):
            try:
                com_on = True
                ser = serial.Serial(get_ports(),115200)
            except:
                com_on = False        
        else:
            try:
                dt = str(ser.readline())
            except:
                com_on=False
                dt = "NO"

        if "P1" in dt:
            player_event = pygame.event.Event(USER_COM_EVENT, message = "P1")
            pygame.event.post(player_event)
            #print("P1 event publish")
        if "P2" in dt:
            player_event = pygame.event.Event(USER_COM_EVENT, message = "P2")
            pygame.event.post(player_event)
            #print("P2 event publish")





# Параметры окна
#WIDTH, HEIGHT = 900, 600 #1920 1020

video_infos = pygame.display.Info()
WIDTH, HEIGHT = video_infos.current_w, video_infos.current_h






screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption("Pillow Fun")
clock = pygame.time.Clock()

# Иконка приложения

current_dir = os.path.dirname(__file__)
icon_path = current_dir+"./images/ico.png"
app_icon = pygame.image.load(icon_path)
pygame.display.set_icon(app_icon)

# Загрузка фона игры
background = pygame.image.load(current_dir+"./images/bg1.png")

# Загрузка анимаций игроков
player1_frames = [
    pygame.image.load(os.path.join(current_dir, ".\images\c1_f1.png")),
    pygame.image.load(os.path.join(current_dir, ".\images\c1_f2.png")),
    pygame.image.load(os.path.join(current_dir, ".\images\c1_f3.png")),
    pygame.image.load(os.path.join(current_dir, ".\images\c1_f4.png")),
    pygame.image.load(os.path.join(current_dir, ".\images\c2_f1.png")),
    pygame.image.load(os.path.join(current_dir, ".\images\c2_f2.png")),
    pygame.image.load(os.path.join(current_dir, ".\images\c2_f3.png")),

]
player2_frames = player1_frames.copy()

# Шрифт для текста
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    surface.blit(text_obj, (x, y))

def resize_background(surface):
    return pygame.transform.scale(background, surface.get_size())


def main_game():
    global screen
    # Параметры игроков
    player1_x, player1_y = 600, HEIGHT // 2 - 100
    player2_x, player2_y = 300, HEIGHT // 2 - 100
    player1_score, player2_score = 0, 0
    player1_frame_index, player2_frame_index = 0, 0 
    player1_animating, player2_animating = False, False
    player1_animation_time, player2_animation_time = 0, 0
    animation_interval = 65 

    # Таймер
    game_time = 20  # Продолжительность игры в секундах
    timer_width = 300
    timer_height = 20
    start_time = pygame.time.get_ticks()

    running = True
    while running:
        # Фон на весь экран
        scaled_background = resize_background(screen)

        # Отображение фона
        screen.blit(scaled_background, (0, 0))
        # Обработка событий

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == USER_COM_EVENT: # Ком-порт игрока 1
                if event.message == "P1":
                    player1_score += 10
                    player1_animating = True
                    player1_animation_time = pygame.time.get_ticks()

                if event.message == "P2": # Ком порт игрока 2
                    player2_score += 10
                    player2_animating = True
                    player2_animation_time = pygame.time.get_ticks()
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:  # Клавиша для игрока 1
                    player1_score += 10
                    player1_animating = True
                    player1_animation_time = pygame.time.get_ticks()
                if event.key == pygame.K_l:  # Клавиша для игрока 2
                    player2_score += 10
                    player2_animating = True
                    player2_animation_time = pygame.time.get_ticks()
            if event.type == pygame.VIDEORESIZE:
                
                # Изменяем размер окна
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                       
        # Анимация игроков
        current_time = pygame.time.get_ticks()

        if player1_animating:
            if current_time - player1_animation_time > animation_interval:
                player1_animation_time = current_time
                player1_frame_index += 1
                if player1_frame_index >= len(player1_frames):
                    player1_frame_index = 0
                    player1_animating = False

        if player2_animating:
            if current_time - player2_animation_time > animation_interval:
                player2_animation_time = current_time
                player2_frame_index += 1
                if player2_frame_index >= len(player2_frames):
                    player2_frame_index = 0
                    player2_animating = False
   

        # Перерасчет позиций игрока
        player2_x = 2.8* screen.get_width() // 4
        player1_x = screen.get_width() // 4
        player1_y = screen.get_height() // 2
        player2_y = screen.get_height() // 2 
        # Отрисовка игроков
        screen.blit(player1_frames[player1_frame_index], (player1_x, player1_y))
        screen.blit(player2_frames[player2_frame_index], (player2_x, player2_y))

        # Обновление таймера
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # В секундах
        remaining_time = max(0, game_time - elapsed_time)
        timer_bar_width = int((remaining_time / game_time) * timer_width)

        timer_bar_x = (screen.get_width() - timer_width) // 2
        timer_bar_y = 20

        pygame.draw.rect(screen, (255, 255, 255), (timer_bar_x, timer_bar_y, timer_width, timer_height))
        pygame.draw.rect(screen, (0, 0, 0), (timer_bar_x, timer_bar_y, timer_bar_width, timer_height))

        # Отображение очков и таймера
        draw_text(f"Игрок 1: {player1_score}", small_font, (0, 0, 0), screen, screen.get_width() // 4, 100)
        draw_text(f"Игрок 2: {player2_score}", small_font, (0, 0, 0), screen, 2.8 * screen.get_width() // 4 , 100)
        draw_text(f"Время: {int(remaining_time)}", small_font, (0, 0, 0), screen, timer_bar_x + timer_width// 2 - 40, 50)

        # Проверка на окончание игры
        if remaining_time <= 0:
            return player1_score, player2_score

        # Обновление экрана
        pygame.display.flip()
        clock.tick(30)

def show_winner(player1_score, player2_score):
    while True:
        scaled_background = resize_background(screen)
        screen.blit(scaled_background, (0, 0))

        if player1_score > player2_score:
            result_text = "Игрок 1 победил!"
        elif player2_score > player1_score:
            result_text = "Игрок 2 победил!"
        else:
            result_text = "Ничья!"

        draw_text(result_text, font, (0, 0, 0), screen, screen.get_width() // 2 - 200, screen.get_height() // 2 - 50)
        draw_text("Нажмите R для перезапуска или Q для выхода", small_font, (0, 0, 0), screen, screen.get_width() // 2 - 250, screen.get_height() // 2 + 50)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Перезапуск
                    return True
                if event.key == pygame.K_q:  # Выход
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(30)


def main_menu():
    
    serial_on = False

#запускаем демона опроса СОМ порта (похуй если порт не доступен - там все обернуто эксептами)
    t = Thread(target=com_worker)
    t.daemon = True
    t.start()

    while True:

# вот тут проверяем доступность порта (не открывая сам порт - в принципе есть или нет)
        if (get_ports()!='NO CONTROLLER'):
            serial_on=True
        else:
            serial_on=False
        
        #sleep(0.2)
 

        
        scaled_background = resize_background(screen)
        screen.blit(scaled_background, (0, 0))
        draw_text("Попрыгунчики", font, (0, 0, 0), screen, screen.get_width() // 2 - 200, screen.get_height() // 2 - 100)
        if (not(serial_on)):
            draw_text("Контроллер не подключен", small_font, (0, 0, 0), screen, screen.get_width() // 2 - 200, screen.get_height() // 2)
        else:
            draw_text("Нажмите Enter, чтобы начать игру", small_font, (0, 0, 0), screen, screen.get_width() // 2 - 200, screen.get_height() // 2)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Начало игры
                    return

        pygame.display.flip()
        clock.tick(30)

# Основной цикл игры
while True:
    main_menu()
    player1_score, player2_score = main_game()
    if not show_winner(player1_score, player2_score):
        break
