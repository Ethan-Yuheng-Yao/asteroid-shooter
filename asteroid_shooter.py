import pygame
import sys
import random
from pygame.locals import *

pygame.init()

screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Spaceship Game')
score = 0
spawn_rate = 60 
spawn_counter = spawn_rate

WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("graphics/player.png").convert_alpha()
        self.rect = self.image.get_rect(center=(screen_width / 2, screen_height / 2))
        self.speed = 4 
        self.laser_cooldown = 0

    def update(self):
        global running
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_d]:
            self.rect.x += self.speed
        if keys[K_w]:
            self.rect.y -= self.speed
        if keys[K_s]:
            self.rect.y += self.speed

        self.rect.clamp_ip(screen.get_rect())

        if pygame.sprite.spritecollide(self, meteors_group, True):
            running = False
        if self.laser_cooldown > 0:
            self.laser_cooldown -= 1

class Laser(pygame.sprite.Sprite):
    COOLDOWN = 8 

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("graphics/laser.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.y -= 6
        if self.rect.y < -100:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()

        if size == 3 or 4:
            self.image = pygame.transform.scale(pygame.image.load("graphics/meteor.png").convert_alpha(), (120, 90))
            self.speed = 2
            self.health = 6
        elif size == 5:
            self.image = pygame.transform.scale(pygame.image.load("graphics/meteor.png").convert_alpha(), (240, 180))
            self.speed = 1
            self.health = 10
        else:  
            self.image = pygame.image.load("graphics/meteor.png").convert_alpha()
            self.speed = 3
            self.health = 3

        self.rect = self.image.get_rect(center=pos)

    def update(self):
        global score
        self.rect.y += self.speed
        if pygame.sprite.spritecollide(self, lasers_group, True):
            self.health -= 1
            if self.health <= 0:
                self.kill()
                score += size

class CloseButton:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.text = self.font.render('Close', True, WHITE)
        self.rect = self.text.get_rect(topright=(screen_width - 10, 10))
        self.color = RED

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text, self.rect.topleft)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

font = pygame.font.SysFont(None, int(screen_width * 0.06))
player = Player()
player_group = pygame.sprite.GroupSingle()
player_group.add(player)
lasers_group = pygame.sprite.Group()
meteors_group = pygame.sprite.Group()

clock = pygame.time.Clock()
close_button = CloseButton()

star = pygame.image.load("graphics/star.png").convert_alpha()
stars = [(random.randint(0, screen_width), random.randint(0, screen_height)) for _ in range(20)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if close_button.is_clicked(event.pos):
                pygame.quit()
                sys.exit()
        if running:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player.laser_cooldown == 0:
                        laser = Laser(player.rect.center)
                        lasers_group.add(laser)
                        player.laser_cooldown = Laser.COOLDOWN

    if running:
        score_text = font.render(f"Score: {score}", True, "Black")
        score_text_rect = score_text.get_rect(center=(screen_width / 2, 100))

        spawn_counter -= 1
        if spawn_counter <= 0:
            for _ in range(3):
                size = random.randint(1, 5)

                meteor = Meteor((random.randint(20, screen_width - 20), -100), size)

                spawn_counter = random.randint(spawn_rate - 30, spawn_rate + 30)
                if spawn_counter < 5:
                    spawn_counter = 5

            meteors_group.add(meteor)

        player_group.update()
        lasers_group.update()
        meteors_group.update()

        screen.fill('gray')
        for star_pos in stars:
            screen.blit(star, star_pos)

        meteors_group.draw(screen)
        lasers_group.draw(screen)
        player_group.draw(screen)
        close_button.draw(screen)
        screen.blit(score_text, score_text_rect)

    else:
        score_text = font.render(f"Final Score: {score}", True, "Red")
        score_text_rect = score_text.get_rect(center=(screen_width / 2, (screen_height / 2) - 100))
        end_text = font.render('Game Over!', True, 'Red')
        end_text_rect = end_text.get_rect(center=(screen_width / 2, screen_height / 2))

        screen.fill((0, 0, 0))
        close_button.draw(screen)
        screen.blit(score_text, score_text_rect)
        screen.blit(end_text, end_text_rect)

    pygame.display.flip()
    clock.tick(50)

pygame.quit()
sys.exit()
