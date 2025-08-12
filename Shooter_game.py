#Создай собственный Шутер!

from time import time as timer
from pygame import *
from random import *


class Game_sprite(sprite.Sprite):
    def __init__(self, sprite_image, x, y, width, height, speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Game_sprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x >= 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x <= 630:
            self.rect.x += self.speed

class Enemy(Game_sprite):
    def update(self):
        if self.rect.y >= 510:
            self.rect.x = randint(5, 630)
            self.rect.y = 0
            global passed
            passed += 1
        else:
            self.rect.y += self.speed

class Bullet(Game_sprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -10:
            self.remove(bullets)

class Asteroid(Game_sprite):
    def update(self):
        if self.rect.y >= 510:
            self.rect.x = randint(5, 630)
            self.rect.y = 0
            global passed
        else:
            self.rect.y += self.speed

space_pressed = False
cur_time = None
last_CD_time = None
shoot_num = 0
def shoot_check():
    global space_pressed
    global last_CD_time
    global shoot_num
    global cd_label
    keys = key.get_pressed()
    if shoot_num < 5:
        if keys[K_SPACE] and not space_pressed:
            fire.play()
            bullets.add(Bullet('bullet.png', ship.rect.x + 27, 400, 25, 25, 10))
            space_pressed = True
            shoot_num += 1
            if shoot_num == 5:
                cd_label = font1.render('Перезарядка', True, (250, 0, 0))
                last_CD_time = timer()
        else:
            if not keys[K_SPACE]:
                space_pressed = False
    else:
        if timer() - last_CD_time > 1:
            cd_label = font1.render('', True, (250, 0, 0))
            shoot_num = 0


game = True
difficty = randint(1, 3)
if difficty == 1:
    enemies_num = 5
    asteroids_num = 2
elif difficty == 2:
    enemies_num = 7
    asteroids_num = 3
elif difficty == 3:
    enemies_num = 9
    asteroids_num = 5

window = display.set_mode((700, 500))
display.set_caption('Shooter')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
ship = Player('rocket.png', 5, 400, 80, 100, 5)
enemy_y = 0
enemies = sprite.Group()
for i in range(enemies_num):
    enemies.add(Enemy('ufo.png', randint(5, 630), enemy_y, 80, 50, 1))
    enemy_y += 25
enemy_y = 0
asteroids = sprite.Group()
for i in range(asteroids_num):
    asteroids.add(Asteroid('asteroid.png', randint(5, 630), enemy_y, 80, 80, 1))
    enemy_y += 25
bullets = sprite.Group()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')

font.init()
font1 = font.Font(None, 35)
label1 = font1.render('Счёт:', True, (250, 250, 250))
label2 = font1.render('Пропущено:', True, (250, 250, 250))
killed_count_lb = font1.render('0', True, (250, 250, 250))
passed_count_lb = font1.render('0', True, (250, 250, 250))
font2 = font.Font(None, 70)
win_text = font2.render('ПОБЕДА!', True, (0, 255, 0))
lose_text = font2.render('ПОРАЖЕНИЕ!', True, (255, 0, 0))
difficty_text = font1.render('Сложность: уровень ' + str(difficty), True, (250, 250, 250))
killed = 0
passed = 0
cd_label = font1.render('', True, (250, 0, 0))


clock = time.Clock()
win = False
lose = False
game_started = False
lives = 3
lives_color = (0, 250, 0)
while game:
    if not win and not lose:
        window.blit(background, (0, 0))
        ship.update()
        ship.reset()
        enemies.draw(window)
        enemies.update()
        asteroids.draw(window)
        asteroids.update()
        window.blit(label1, (0, 0))
        window.blit(label2, (0, 25))
        window.blit(difficty_text, (0, 50))
        passed_count_lb = font1.render(str(passed), True, (250, 250, 250))
        killed_count_lb = font1.render(str(killed), True, (250, 250, 250))
        lives_lb = font2.render(str(lives), True, lives_color)
        window.blit(killed_count_lb, (65, 0))
        window.blit(passed_count_lb, (152, 25))
        window.blit(lives_lb, (675, 0))
        window.blit(cd_label, (270, 475))
        shoot_check()
        bullets.draw(window)
        bullets.update()
        if killed >= 10:
            win = True
        if passed >= 3:
            lose = True
        sprites_list1 = sprite.spritecollide(ship, enemies, True)
        sprites_list2 = sprite.spritecollide(ship, asteroids, True)
        if lives == 0:
            lose = True
        if len(sprites_list1) != 0 or len(sprites_list2) != 0:
            lives -= 1
            if lives == 2:
                lives_color = (252, 248, 3)
            if lives == 1:
                lives_color = (250, 0, 0)
            if lives == 0:
                lives_color = (50, 50, 50)
        sprites_list3 = sprite.groupcollide(enemies, bullets, True, True)
        killed += len(sprites_list3)
        for i in range(len(sprites_list3)):
            enemies.add(Enemy('ufo.png', randint(5, 630), 0, 80, 50, 1))
        sprite.groupcollide(bullets, asteroids, True, False)
        sprites_list4 = sprite.groupcollide(enemies, asteroids, True, False)
        for i in range(len(sprites_list4)):
            enemies.add(Enemy('ufo.png', randint(5, 630), 0, 80, 50, 1))

    if win:
        window.blit(win_text, (225, 225))
        mixer.music.stop()

    if lose:
        window.blit(lose_text, (175, 225))
        mixer.music.stop()

    for e in event.get():
        if e.type == QUIT:
            game = False

    display.update()
    clock.tick(60)