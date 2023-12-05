from pygame.sprite import Sprite
import pygame

class Ship(Sprite):
  def __init__(self, ai_settings, screen) -> None:
    super().__init__()
    self.ai_settings = ai_settings
    self.screen = screen

    image = pygame.image.load('images/ship.bmp')
    self.image = pygame.transform.scale(image, (64,64))
    self.rect = self.image.get_rect()
    self.screen_rect = screen.get_rect()

    # 初始化到底部中间
    self.rect.centerx = self.screen_rect.centerx
    self.rect.bottom = self.screen_rect.bottom
    
    # 可存储小数数值
    self.centerx = float(self.rect.centerx)
    self.centery = float(self.rect.centery)

    # 移动标志
    self.moving_right = False
    self.moving_left = False
    self.moving_up = False
    self.moving_down = False

  def blitme(self):
    self.screen.blit(self.image, self.rect)

  def update(self):
    if self.moving_right and self.centerx < self.screen_rect.right:
       self.centerx += self.ai_settings.ship_speed_factor
    elif self.moving_left and self.centerx > self.screen_rect.left:
       self.centerx -= self.ai_settings.ship_speed_factor
    elif self.moving_up and self.centery > self.screen_rect.top:
       self.centery -= self.ai_settings.ship_speed_factor
    elif self.moving_down and self.centery < self.screen_rect.bottom:
       self.centery += self.ai_settings.ship_speed_factor
    
    # 更新 self.center 更新 rect 对象
    self.rect.centerx = self.centerx
    self.rect.centery = self.centery

  def center_ship(self):
     self.centerx = self.screen_rect.centerx
     self.centery = self.screen_rect.bottom - self.rect.height / 2
