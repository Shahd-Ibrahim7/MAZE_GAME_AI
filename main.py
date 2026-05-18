# main.py
import pygame
import sys
import time
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, FPS, ENEMY_COLOR
from models.maze import Maze
from models.player import Player
from models.enemy import Enemy
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.astar import astar
from algorithms.greedy import greedy
from ui.buttons import Button

def draw_cheese(screen, x, y, size):
    # دالة ذكية لرسم قطعة جبن مثلثية مودرن مع فتحات الجبن اللطيفة
    cx = x * size + size // 2
    cy = y * size + size // 2
    
    # نقاط المثلث الخاص بالجبنة
    points = [
        (cx - size//3, cy + size//3), # زاوية يسار تحت
        (cx + size//3, cy + size//3), # زاوية يمين تحت
        (cx + size//4, cy - size//3)  # الرأس فوق
    ]
    pygame.draw.polygon(screen, (241, 196, 15), points)
    
    # رسم ثقوب صغيرة في الجبن لإعطائه شكلاً واقعياً جميلاً
    pygame.draw.circle(screen, (212, 163, 13), (cx - 2, cy + 4), 2)
    pygame.draw.circle(screen, (212, 163, 13), (cx + 4, cy), 3)
    pygame.draw.circle(screen, (212, 163, 13), (cx + 2, cy + 8), 1.5)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Game - 404 Society") # تحديث اسم النافذة لشعاركم
    clock = pygame.time.Clock()

    pygame.font.init()
    font_large = pygame.font.SysFont("Segoe UI", 60, bold=True)
    font_small = pygame.font.SysFont("Segoe UI", 26, bold=True)
    font_ui = pygame.font.SysFont("Segoe UI", 20, bold=True)

    maze = Maze()
    player = Player(1, 1)
    enemy = Enemy(13, 7)

    goal_x, goal_y = 13, 1

    game_state = "PLAYING"
    current_algorithm = "ASTAR"  
    
    steps_count = 0
    start_time = time.time()
    elapsed_time = 0

    # --- أزرار مودرن بألوان متناسقة جداً (ستايل Dark Cyber) ---
    button_x = 680
    button_width = 240
    button_height = 45
    btn_color = (44, 62, 80)       # لون زجاجي داكن شيك
    btn_hover = (52, 152, 219)     # أزرق نيون مضيء عند الهوفر

    btn_bfs = Button(button_x, 240, button_width, button_height, "Use BFS Algorithm", btn_color, btn_hover)
    btn_dfs = Button(button_x, 295, button_width, button_height, "Use DFS Algorithm", btn_color, btn_hover)
    btn_astar = Button(button_x, 350, button_width, button_height, "Use A* Algorithm", btn_color, btn_hover)
    btn_greedy = Button(button_x, 405, button_width, button_height, "Use Greedy BF", btn_color, btn_hover)

    while True:
        if game_state == "PLAYING":
            elapsed_time = int(time.time() - start_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if game_state == "PLAYING":
                if btn_bfs.is_clicked(event):
                    current_algorithm = "BFS"
                elif btn_dfs.is_clicked(event):
                    current_algorithm = "DFS"
                elif btn_astar.is_clicked(event):
                    current_algorithm = "ASTAR"
                elif btn_greedy.is_clicked(event):
                    current_algorithm = "GREEDY"

            if event.type == pygame.KEYDOWN:
                if game_state == "PLAYING":
                    old_x, old_y = player.x, player.y
                    
                    if event.key == pygame.K_LEFT:
                        player.move(-1, 0, maze.grid)
                    elif event.key == pygame.K_RIGHT:
                        player.move(1, 0, maze.grid)
                    elif event.key == pygame.K_UP:
                        player.move(0, -1, maze.grid)
                    elif event.key == pygame.K_DOWN:
                        player.move(0, 1, maze.grid)
                    
                    if player.x != old_x or player.y != old_y:
                        steps_count += 1
                
                elif game_state in ["GAME_OVER", "WIN"]:
                    if event.key == pygame.K_r:
                        maze.generate_random_maze()
                        player = Player(1, 1)
                        enemy = Enemy(13, 7)
                        steps_count = 0
                        start_time = time.time()
                        elapsed_time = 0
                        game_state = "PLAYING"

        if game_state == "PLAYING":
            if current_algorithm == "BFS":
                path = bfs(maze.grid, (enemy.x, enemy.y), (player.x, player.y))
            elif current_algorithm == "DFS":
                path = dfs(maze.grid, (enemy.x, enemy.y), (player.x, player.y))
            elif current_algorithm == "ASTAR":
                path = astar(maze.grid, (enemy.x, enemy.y), (player.x, player.y))
            elif current_algorithm == "GREEDY":
                path = greedy(maze.grid, (enemy.x, enemy.y), (player.x, player.y))
            
            enemy.update_path(path)
            enemy.move()

            if player.x == enemy.x and player.y == enemy.y:
                game_state = "GAME_OVER"

            if player.x == goal_x and player.y == goal_y:
                game_state = "WIN"

        # Rendering
        screen.fill(BG_COLOR)
        maze.draw(screen)
        
        # --- رسم قطعة الجبن بدلاً من المربع الأصفر الثابت ---
        from core.settings import TILE_SIZE
        draw_cheese(screen, goal_x, goal_y, TILE_SIZE)
        
        player.draw(screen)
        enemy.draw(screen)

        # لوحة التحكم والـ Scoreboard الجانبية المحدثة بصرياً
        text_algo_title = font_ui.render("Active Algorithm:", True, (149, 165, 166))
        text_algo_name = font_ui.render(f">> {current_algorithm} <<", True, (46, 204, 113))
        screen.blit(text_algo_title, (button_x, 50))
        screen.blit(text_algo_name, (button_x, 80))

        text_score = font_ui.render(f"Steps Taken: {steps_count}", True, (236, 240, 241))
        text_time = font_ui.render(f"Time: {elapsed_time} Seconds", True, (236, 240, 241))
        screen.blit(text_score, (button_x, 130))
        screen.blit(text_time, (button_x, 160))

        btn_bfs.draw(screen)
        btn_dfs.draw(screen)
        btn_astar.draw(screen)
        btn_greedy.draw(screen)

        # شاشات النهاية الاحترافية والشفافة
        if game_state in ["GAME_OVER", "WIN"]:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((24, 28, 36, 210))  # خلفية داكنة مع تباين ممتاز
            screen.blit(overlay, (0, 0))

            if game_state == "GAME_OVER":
                end_text = font_large.render("GAME OVER", True, (231, 76, 60))
            else:
                end_text = font_large.render("YOU WIN!", True, (241, 196, 15))

            restart_text = font_small.render("Press 'R' to Restart and Generate New Maze", True, (255, 255, 255))
            stats_text = font_small.render(f"Final Score - Steps: {steps_count} | Time: {elapsed_time}s", True, (189, 195, 199))
            
            screen.blit(end_text, (SCREEN_WIDTH // 2 - end_text.get_width() // 2, SCREEN_HEIGHT // 2 - 90))
            screen.blit(stats_text, (SCREEN_WIDTH // 2 - stats_text.get_width() // 2, SCREEN_HEIGHT // 2 + 0))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 70))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()