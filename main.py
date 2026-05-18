# main.py
import pygame
import sys
import time
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, FPS
from models.maze import Maze
from models.player import Player
from models.enemy import Enemy
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.astar import astar
from algorithms.greedy import greedy
from ui.buttons import Button

def draw_cheese(screen, x, y, size):
    cx, cy = x * size + size // 2, y * size + size // 2
    points = [(cx - size//3, cy + size//3), (cx + size//3, cy + size//3), (cx + size//4, cy - size//3)]
    pygame.draw.polygon(screen, (241, 196, 15), points)
    pygame.draw.circle(screen, (212, 163, 13), (cx - 2, cy + 4), 2)
    pygame.draw.circle(screen, (212, 163, 13), (cx + 4, cy), 3)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cat & Mouse - 404 Society")
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
    steps_count, start_time, elapsed_time = 0, time.time(), 0

    # --- إعداد الأزرار المودرن بالألوان المميزة ---
    bx, bw, bh = 680, 240, 50
    base_btn_bg = (40, 50, 65)

    # ألوان الأكسنت (Neon Style)
    color_bfs = (52, 152, 219)    # Blue
    color_dfs = (155, 89, 182)    # Purple
    color_astar = (46, 204, 113)  # Green
    color_greedy = (241, 196, 15) # Gold

    btn_bfs = Button(bx, 240, bw, bh, "BFS Algorithm", base_btn_bg, color_bfs)
    btn_dfs = Button(bx, 305, bw, bh, "DFS Algorithm", base_btn_bg, color_dfs)
    btn_astar = Button(bx, 370, bw, bh, "A* Algorithm", base_btn_bg, color_astar)
    btn_greedy = Button(bx, 435, bw, bh, "Greedy BF", base_btn_bg, color_greedy)

    while True:
        if game_state == "PLAYING":
            elapsed_time = int(time.time() - start_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if game_state == "PLAYING":
                if btn_bfs.is_clicked(event): current_algorithm = "BFS"
                elif btn_dfs.is_clicked(event): current_algorithm = "DFS"
                elif btn_astar.is_clicked(event): current_algorithm = "ASTAR"
                elif btn_greedy.is_clicked(event): current_algorithm = "GREEDY"

            if event.type == pygame.KEYDOWN:
                if game_state == "PLAYING":
                    old_x, old_y = player.x, player.y
                    if event.key == pygame.K_LEFT: player.move(-1, 0, maze.grid)
                    elif event.key == pygame.K_RIGHT: player.move(1, 0, maze.grid)
                    elif event.key == pygame.K_UP: player.move(0, -1, maze.grid)
                    elif event.key == pygame.K_DOWN: player.move(0, 1, maze.grid)
                    if player.x != old_x or player.y != old_y: steps_count += 1
                elif game_state in ["GAME_OVER", "WIN"]:
                    if event.key == pygame.K_r:
                        maze.generate_random_maze()
                        player, enemy = Player(1, 1), Enemy(13, 7)
                        steps_count, start_time, elapsed_time, game_state = 0, time.time(), 0, "PLAYING"

        if game_state == "PLAYING":
            if current_algorithm == "BFS": path = bfs(maze.grid, (enemy.x, enemy.y), (player.x, player.y))
            elif current_algorithm == "DFS": path = dfs(maze.grid, (enemy.x, enemy.y), (player.x, player.y))
            elif current_algorithm == "ASTAR": path = astar(maze.grid, (enemy.x, enemy.y), (player.x, player.y))
            elif current_algorithm == "GREEDY": path = greedy(maze.grid, (enemy.x, enemy.y), (player.x, player.y))
            enemy.update_path(path)
            enemy.move()
            if player.x == enemy.x and player.y == enemy.y: game_state = "GAME_OVER"
            if player.x == goal_x and player.y == goal_y: game_state = "WIN"

        # Rendering
        screen.fill(BG_COLOR)
        maze.draw(screen)
        from core.settings import TILE_SIZE
        draw_cheese(screen, goal_x, goal_y, TILE_SIZE)
        player.draw(screen)
        enemy.draw(screen)

        # UI Panel
        text_algo_title = font_ui.render("Control Panel", True, (149, 165, 166))
        screen.blit(text_algo_title, (bx, 50))
        
        # معلومات الـ Stats في كارت شيك
        pygame.draw.rect(screen, (35, 45, 55), (bx, 100, bw, 90), border_radius=15)
        text_score = font_ui.render(f"Steps: {steps_count}", True, (236, 240, 241))
        text_time = font_ui.render(f"Time: {elapsed_time}s", True, (236, 240, 241))
        screen.blit(text_score, (bx + 20, 115))
        screen.blit(text_time, (bx + 20, 145))

        # رسم الأزرار مع تمرير حالة "النشاط"
        btn_bfs.draw(screen, current_algorithm == "BFS")
        btn_dfs.draw(screen, current_algorithm == "DFS")
        btn_astar.draw(screen, current_algorithm == "ASTAR")
        btn_greedy.draw(screen, current_algorithm == "GREEDY")

        if game_state in ["GAME_OVER", "WIN"]:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((20, 24, 30, 220))
            screen.blit(overlay, (0, 0))
            if game_state == "GAME_OVER": end_text = font_large.render("GAME OVER", True, (231, 76, 60))
            else: end_text = font_large.render("MISSION ACCOMPLISHED!", True, (241, 196, 15))
            restart_text = font_small.render("Press 'R' to Restart", True, (255, 255, 255))
            screen.blit(end_text, (SCREEN_WIDTH // 2 - end_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()