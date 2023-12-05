import sys
import pygame
from pygame.sprite import Group
import numpy as np
from matplotlib import colors
from alien import Alien
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship
import game_funcions as gf



def run_game():
  pygame.init()
  ai_settings = Settings()

  screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
  ship = Ship(ai_settings, screen)
  # 创建统计信息
  stats = GameStats(ai_settings)
  # 创建记分牌
  sb = Scoreboard(ai_settings, screen, stats)

  pygame.display.set_caption("外星人大战")

  play_button = Button(ai_settings, screen, "开始")

  bullets = Group()
  aliens = Group()

  ai_settings.bg_color = (46, 78, 126) # 藏青色
  gf.create_fleet(ai_settings, screen, ship, aliens)

  # 开始游戏主循环
  while True:
    gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

    if stats.game_active:
      ship.update()
      bullets.update()
      gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
      gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)
    gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

# 运行游戏
run_game()