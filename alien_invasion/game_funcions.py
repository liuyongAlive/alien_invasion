import sys
from time import sleep

import pygame
from alien import Alien

from bullet import Bullet

def check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets):
  if event.key == pygame.K_RIGHT:
    ship.moving_right = True
  elif event.key == pygame.K_LEFT:
    ship.moving_left = True
  # elif event.key == pygame.K_UP:
  #   ship.moving_up = True
  # elif event.key == pygame.K_DOWN:
  #   ship.moving_down = True
  elif event.key == pygame.K_SPACE:
    fire_bullet(ai_settings, screen, ship, bullets)
  elif event.key == pygame.K_q:
    sys.exit()
  elif event.key == pygame.K_p and not stats.game_active:
    start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_keyup_events(event, ship):
  if event.key == pygame.K_RIGHT:
    ship.moving_right = False
  elif event.key == pygame.K_LEFT:
    ship.moving_left = False
  elif event.key == pygame.K_UP:
    ship.moving_up = False
  elif event.key == pygame.K_DOWN:
    ship.moving_down = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
  """ 响应键鼠 """
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    elif event.type == pygame.KEYDOWN:
      check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets)
    elif event.type == pygame.KEYUP:
      check_keyup_events(event, ship)
    elif event.type == pygame.MOUSEBUTTONDOWN:
      mouse_x, mouse_y = pygame.mouse.get_pos()
      check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
  # 重置游戏设置
    ai_settings.initialize_dynamic_settings()

    # 隐藏光标
    pygame.mouse.set_visible(False)

    # 重置游戏统计信息
    stats.reset_stats()
    stats.game_active = True
    
    # 重置记分
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    # 清空子弹和外星人列表
    aliens.empty()
    bullets.empty()

    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
  button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

  if button_clicked and not stats.game_active:
    start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
  """更新屏幕图像"""
  screen.fill(ai_settings.bg_color)
  for bullet in bullets.sprites():
    bullet.draw_bullet()

  ship.blitme()
  aliens.draw(screen)
  # 显示得分
  sb.show_score()

  # 非激活情况下，显示开始按钮
  if not stats.game_active:
    play_button.draw_button()

  # 最新的屏幕
  pygame.display.flip()

def fire_bullet(ai_settings, screen, ship, bullets):
  if len(bullets) < ai_settings.bullets_allowed:
      new_bullet = Bullet(ai_settings, screen, ship)
      ai_settings.sound_biu.play()
      bullets.add(new_bullet)

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
  for bullet in bullets.copy():
    if bullet.rect.bottom <= 0:
      bullets.remove(bullet)

  check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
  """响应碰撞（击中）"""
  # 检查是否有子弹击中外星人
  collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
  if collisions:
    ai_settings.sound_boom.play()
    for aliens in collisions.values():
      stats.score += ai_settings.alien_points * len(aliens)
      sb.prep_score()
    check_high_score(stats, sb)

  # 删除子弹和重新生成外星人
  if len(aliens) == 0:
    bullets.empty()
    ai_settings.increase_speed()

    # 提高等级
    stats.level += 1
    sb.prep_level()

    create_fleet(ai_settings, screen, ship, aliens)

def get_number_aliens_x(ai_settings, alien_width):
  avaliable_space_x = ai_settings.screen_width - 2 * alien_width
  return int(avaliable_space_x / (2 * alien_width))


def get_number_rows(ai_settings, ship_height, alien_height):
  available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
  return int (available_space_y / (2 * alien_height))
  
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
  alien = Alien(ai_settings, screen)
  alien_width = alien.rect.width
  alien.x = alien_width + 2 * alien_width * alien_number
  alien.rect.x = alien.x
  alien.rect.y = alien.rect.height + alien.rect.height * row_number
  aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
  """创建目标"""
  alien = Alien(ai_settings, screen)
  number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
  number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
  for row_number in range(number_rows):
    for alien_number in range(number_aliens_x):
      create_alien(ai_settings, screen, aliens, alien_number, row_number)
  
def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
  check_fleet_direction(ai_settings, aliens)
  aliens.update()
  if pygame.sprite.spritecollideany(ship, aliens):
    ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
  check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)

def check_fleet_direction(ai_settings, aliens):
  for alien in aliens.sprites():
    if alien.check_edges():
      change_fleet_direction(ai_settings, aliens)
      break

def change_fleet_direction(ai_settings, aliens):
  for alien in aliens.sprites():
    alien.rect.y += ai_settings.fleet_drop_speed
  ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
  if stats.ships_left > 0:
    stats.ships_left -= 1

    # 更新记分
    sb.prep_ships()

    aliens.empty()
    bullets.empty()

    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    sleep(3)
  else:
    stats.game_active = False
    pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
  screen_rect = screen.get_rect()
  for alien in aliens.sprites():
    if alien.rect.bottom >= screen_rect.bottom:
      ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
      break

def check_high_score(stats, sb):
  """更新最高得分"""
  if stats.score > stats.high_score:
    stats.high_score = stats.score
    sb.prep_high_score()