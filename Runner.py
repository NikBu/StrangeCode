#Импортируем pygame и random
import pygame
import random

#Импортируем содержимое модуля Locals для облегчения работы с клавиатурой
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Устанавливаем ширину и высоту окна
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

#Инициализируем Pygame
pygame.init()

#Загружаем и определяем музыку и необходимые звуки
pygame.mixer.music.load("1.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)
LaserSound=pygame.mixer.Sound("Y2meta.com-Laser-Gun-Sound-Effect-_128-kbps_.wav")
LaserSound.set_volume(0.1)
DeathSound=pygame.mixer.Sound("Sound_15115.wav")
DeathSound.set_volume(0.1)
UFOdestroySound=pygame.mixer.Sound( "expl3.wav")
METdestroySound=pygame.mixer.Sound( "expl6.wav")
METdestroySound.set_volume(0.9)
UFOdestroySound.set_volume(0.9)
HealingSound=pygame.mixer.Sound("y2meta.com-Heal-Sound-Effect.wav")
HealingSound.set_volume(0.9)

# Определяем класс игрока
class Player(pygame.sprite.Sprite):

    #Инициализация и установка начальных очков и здоровья
    def __init__(self):
        super(Player, self).__init__()
        self.HitPoint=3
        self.Score=0
        self.surf = pygame.image.load("Ship.png").convert()
        self.surf = pygame.transform.scale(self.surf ,(110,90))
        self.surf.set_colorkey((247, 247, 247), RLEACCEL)
        self.rect = self.surf.get_rect()

    #Настройка движений с помощью клавиатуры
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -7)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 7)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-7, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(7, 0)
         # Удержание в пределах экрана
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

#Создание метеоров
class Meteor(pygame.sprite.Sprite):

    #Инициализация
    def __init__(self):
        super(Meteor, self).__init__()
        self.surf = pygame.image.load("2i.jpg").convert()
        self.surf = pygame.transform.scale(self.surf ,(100,36))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)

        #Настройка случайного появления и скорости
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH+70 , SCREEN_WIDTH+70),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speedX = random.randint(3, 6)
        self.speedY = random.randint(-3,3)

    #Настройка движения и удаления при выходе за экран
    def update(self):
        self.rect.move_ip(-self.speedX, self.speedY)
        if self.rect.right < 0 or self.rect.bottom < 0 or self.rect.top>SCREEN_HEIGHT:
            self.kill()

#Создание класса НЛО
class UFO(pygame.sprite.Sprite):

    #Инициализация
    def __init__(self):
        super(UFO, self).__init__()
        self.surf = pygame.image.load("lgi01a201411190400.jpg").convert()
        self.surf = pygame.transform.scale(self.surf ,(200,100))
        self.surf.set_colorkey((255, 255,255), RLEACCEL)

        #Настройка случайного появления
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    #Настройка движения и удаления
    def update(self):
        self.rect.move_ip(-3, 0)
        if self.rect.right < 0:
            self.kill()

#Создание класса исцеляющих сердец
class Heal(pygame.sprite.Sprite):

    #Инициализация
    def __init__(self):
        super(Heal, self).__init__()
        self.surf = pygame.image.load("BlueHeart.png").convert()
        self.surf = pygame.transform.scale(self.surf ,(50,50))
        self.surf.set_colorkey((255, 255,255), RLEACCEL)

        # Настройка появления
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    #Настройка движения
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

#Создание класса выстрелов
class Laser(pygame.sprite.Sprite):

    #Инициализация
    def __init__(self,x):
        super(Laser, self).__init__()
        self.surf = pygame.image.load("laser-transparent-sprite-8.png").convert()
        self.surf = pygame.transform.scale(self.surf ,(70,10))
        self.surf.set_colorkey((255, 255,255), RLEACCEL)

        #Появление у корабля
        self.rect = self.surf.get_rect(
        center=(x)
        )

    #Настройка движения
    def update(self):
        self.rect.move_ip(10, 0)
        if self.rect.right > SCREEN_WIDTH+100:
            self.kill()

#Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Название игры
pygame.display.set_caption('Cosmic shooter')

#Событие появления метеора и его частота
ADDMeteor = pygame.USEREVENT + 1
pygame.time.set_timer(ADDMeteor, 230)
#Событие появления НЛО и его частота
ADDUFO = pygame.USEREVENT + 2
pygame.time.set_timer(ADDUFO, 2500)
#Событие появления выстрелов и их частота
LASERSHOOT = pygame.USEREVENT + 3
pygame.time.set_timer(LASERSHOOT,900)
#Событие появления исцеления и его частота
ADDHEAL = pygame.USEREVENT + 4
pygame.time.set_timer(ADDHEAL, 21000)

#Первая инициализация игрока и всех групп спрайтов
player = Player()
meteors = pygame.sprite.Group()
UFOs = pygame.sprite.Group()
heals = pygame.sprite.Group()
lasers = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#Активация времени
clock = pygame.time.Clock()

#Установка переменной для определения работы программы
running = True
#Счётчик смертей
DeathCount=0
#Переменная для слежения за активностью меню
MenuON = True

#Загрузка и форматирование изображений
StartButton = pygame.image.load("STARTVER1.jpg").convert()
StartButton = pygame.transform.scale(StartButton ,(300,150))
Dead = pygame.image.load("Death2.jpg").convert()
Dead = pygame.transform.scale(Dead ,(350,350))
BackGround = pygame.image.load("uKmISB.jpg").convert()
BackGround = pygame.transform.scale(BackGround ,(SCREEN_WIDTH, SCREEN_HEIGHT))
Hearts = pygame.image.load("heart.png").convert()
Hearts = pygame.transform.scale(Hearts  ,(50,50))
Hearts.set_colorkey((255, 255, 255), RLEACCEL)

#Загрузка шрифта
f1 = pygame.font.Font(None, 36)

#Главный цикл
while running:

    #Проверка событий в очереди
    for event in pygame.event.get():

        # Проверка действий, приводящих к выходу из программы
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

        #Проверка необходимости добавлеия метеора
        elif event.type == ADDMeteor:
            # Создание нового метеора
            new_Meteor = Meteor()
            meteors.add(new_Meteor)
            all_sprites.add(new_Meteor)

        #Проверка необходимости добавлеия НЛО
        elif event.type == ADDUFO:
            # Создание нового НЛО
            new_UFO = UFO()
            UFOs.add(new_UFO)
            all_sprites.add(new_UFO)

        #Проверка необходимости добавлеия исцеления
        elif event.type == ADDHEAL:
            # Cоздание нового исцеления
            new_heal = Heal()
            heals.add(new_heal)
            all_sprites.add(new_heal)

        #Проверка необходимости добавлеия выстрела
        elif event.type == LASERSHOOT:
            # Создание выстрела
            new_laser = Laser(player.rect.center)
            lasers.add(new_laser)
            all_sprites.add(new_laser)
            LaserSound.play()

        #Нажатие на кнопку "Старт" и запуск игры
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if MenuON == True:
                    StartButtonArea = pygame.Rect(SCREEN_WIDTH/2-150,SCREEN_HEIGHT/2+85,300,170)
                    if  StartButtonArea.collidepoint(event.pos):
                        #Выход из меню
                        MenuON = False

                        #Повторная инициализация для новой игры
                        player = Player()
                        meteors = pygame.sprite.Group()
                        UFOs = pygame.sprite.Group()
                        heals = pygame.sprite.Group()
                        lasers = pygame.sprite.Group()
                        all_sprites = pygame.sprite.Group()
                        all_sprites.add(player)

    #Получение списка нажатых клавиш
    pressed_keys = pygame.key.get_pressed()

    #Установка фона
    screen.blit ( BackGround, (0,0))

    #Действия во время игры
    if MenuON == False:
        #Обновление всех объектов
        player.update(pressed_keys)
        meteors.update()
        UFOs.update()
        heals.update()
        lasers.update()
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        #Проверка столкновения игрока с метеорами или НЛО
        if pygame.sprite.spritecollide(player, meteors, True) or pygame.sprite.spritecollide(player, UFOs, True):
            #Отнимание здоровья
            player.HitPoint -=1

            #Действия при смерти
            if player.HitPoint==0:
                player.kill()
                DeathSound.play()
                #Активация меню
                MenuON=True
                DeathCount+=1

        #Проверка столкновения игрока и исцеления
        if pygame.sprite.spritecollide(player, heals, True):
            HealingSound.play()
            player.HitPoint +=1
        #Проверка столкновения лазера и НЛО
        if pygame.sprite.groupcollide(UFOs, lasers, True, True):
            player.Score+=2
            UFOdestroySound.play()
        #Проверка столкновения лазера и МЕтеорита
        if pygame.sprite.groupcollide(meteors, lasers, True, True):
            player.Score+=1
            METdestroySound.play()
        #Небольшое усложнение на случай крайне долгой игры
        if player.Score>1500 :
            pygame.time.set_timer(ADDMeteor, 200)
        #Ускорение атаки при накоплении более 5 сердец
        if player.HitPoint>5 :
            pygame.time.set_timer(LASERSHOOT,900+player.HitPoint*10)

        #Отрисовка игрока на экран
        screen.blit(player.surf, player.rect)

    #Действия при активном меню
    if MenuON == True:
        #Экран поражения
        if DeathCount>0:
            screen.blit ( Dead, (425,0))
        #Вывод количества смертей
        DeathCountT = f1.render(('Количество смертей: '+str(DeathCount)), True,(255, 255, 0))
        screen.blit (DeathCountT, (0,0) )
        #Кнопка старта
        screen.blit ( StartButton, (SCREEN_WIDTH/2-150,SCREEN_HEIGHT/2+85))
    #Вывод счёта
    ScoreT = f1.render(('Счёт: '+str(player.Score)), True,(255, 255, 0))
    screen.blit (ScoreT , (50,50) )
    #Отрисовка здоровья
    for i in range(player.HitPoint):
        screen.blit ( Hearts, (SCREEN_WIDTH-60-(50*i),10))

    #"Переворот" экрана
    pygame.display.flip()
    #Ограничение в 30 кадров
    clock.tick(30)

#Остановка музыки и выход
pygame.mixer.music.stop()
pygame.quit()
