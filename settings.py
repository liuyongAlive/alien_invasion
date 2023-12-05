import pygame


class Settings():
  """
  Settings 存储所有的设置类
  """

  def __init__(self, screen_width = 1600, screen_height = 900, bg_color=(230,230,230)) -> None:
    # 屏幕设置
    self.screen_width = screen_width
    self.screen_height = screen_height
    self.bg_color = bg_color
    
    # 字体设置
    self.light_font = 'fonts/Alibaba-PuHuiTi/Alibaba-PuHuiTi-Light.ttf'
    self.bold_font = 'fonts/Alibaba-PuHuiTi/Alibaba-PuHuiTi-Bold.ttf'

    # 飞船设置
    self.ship_speed_factor = 1.5
    self.ship_limit = 3

    # 子弹设置
    self.bullets_speed_factor = 3
    self.bullets_width = 3
    self.bullets_height = 15
    self.bullets_color = 255,0,0
    self.bullets_allowed = 10

    # 外星人设置
    self.alien_speed_factor = 1
    self.fleet_drop_speed = 5

    # 加快节奏
    self.FPS = 120
    self.speedup_scale = 1.1
    self.score_scale = 1.5

    self.initialize_dynamic_settings()

  def initialize_dynamic_settings(self):
    self.ship_speed_factor = 1.5
    self.bullets_speed_factor = 3
    self.alien_speed_factor = 1

    # 1: 左， -1： 右
    self.fleet_direction = 1

    # 记分
    self.alien_points = 50

    # 声音
    self.sound_biu = pygame.mixer.Sound('sounds/biu.mp3')
    self.sound_boom = pygame.mixer.Sound('sounds/boom.mp3')

  def increase_speed(self):
    """提高速度设置和得分设置"""
    self.ship_speed_factor *= self.speedup_scale
    self.bullets_speed_factor *= self.speedup_scale
    self.alien_speed_factor *= self.speedup_scale
    self.alien_points = int(self.alien_points * self.score_scale)

  
