# main.py
import pygame
import sys
import time  # استدعاء مكتبة الوقت لحساب الثواني
from core.settings import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, FPS, ENEMY_COLOR
from models.maze import Maze
from models.player import Player
from models.enemy import Enemy
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.astar import astar
from algorithms.greedy import greedy
from ui.buttons import Button

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Game - project by [shahd]")
    clock = pygame.time.Clock()

    pygame.font.init()
    font_large = pygame.font.SysFont("Arial", 60, bold=True)
    font_small = pygame.font.SysFont("Arial", 30)
    font_ui = pygame.font.SysFont("Arial", 22, bold=True)

    maze = Maze()
    player = Player(1, 1)
    enemy = Enemy(13, 7)

    # --- إعدادات الـ Win Condition (نقطة النهاية / الكنز) ---
    # الهدف موجود في المربع (13, 1) - ممر في أعلى اليمين
    goal_x, goal_y = 13, 1
    GOAL_COLOR = (241, 196, 15)  # لون أصفر ذهبي

    # --- إعدادات الـ Score والـ Game States ---
    game_state = "PLAYING"
    current_algorithm = "ASTAR"  
    
    steps_count = 0      # عداد الخطوات
    start_time = time.time()  # تسجيل وقت البداية
    elapsed_time = 0     # الوقت المستغرق

    # --- إنشاء الأزرار الجانبية ---
    button_x = 680
    button_width = 240
    button_height = 45
    btn_color = (52, 73, 94)
    btn_hover = (41, 128, 185)

    btn_bfs = Button(button_x, 240, button_width, button_height, "Use BFS Algorithm", btn_color, btn_hover)
    btn_dfs = Button(button_x, 295, button_width, button_height, "Use DFS Algorithm", btn_color, btn_hover)
    btn_astar = Button(button_x, 350, button_width, button_height, "Use A* Algorithm", btn_color, btn_hover)
    btn_greedy = Button(button_x, 405, button_width, button_height, "Use Greedy BF", btn_color, btn_hover)

    # الـ Game Loop الرئيسي
    while True:
        # حساب الوقت لو اللعبة لسه شغالة
        if game_state == "PLAYING":
            elapsed_time = int(time.time() - start_time)

        # 1. Handling Events (إدارة الأحداث)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if game_state == "PLAYING":
                # تفقد ضغطات أزرار تغيير الخوارزميات بالماوس
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
                    # تسجيل الإحداثيات قبل الحركة للتأكد هل اللاعب تحرك فعلاً أم خبط في حيطة
                    old_x, old_y = player.x, player.y
                    
                    if event.key == pygame.K_LEFT:
                        player.move(-1, 0, maze.grid)
                    elif event.key == pygame.K_RIGHT:
                        player.move(1, 0, maze.grid)
                    elif event.key == pygame.K_UP:
                        player.move(0, -1, maze.grid)
                    elif event.key == pygame.K_DOWN:
                        player.move(0, 1, maze.grid)
                    
                    # لو إحداثيات اللاعب تغيرت فعلياً، زود عداد الخطوات 1
                    if player.x != old_x or player.y != old_y:
                        steps_count += 1
                
                # إعادة تشغيل اللعبة وتوليد متاهة جديدة تماماً عند الضغط على R
                elif game_state in ["GAME_OVER", "WIN"]:
                    if event.key == pygame.K_r:
                        # استدعاء دالة التوليد العشوائي للمتاهة الجديدة
                        maze.generate_random_maze()
                        
                        # تصفير الشخصيات والعدادات للوضع الافتراضي
                        player = Player(1, 1)
                        enemy = Enemy(13, 7)
                        steps_count = 0
                        start_time = time.time()
                        elapsed_time = 0
                        game_state = "PLAYING"

        # 2. Update AI Logic (تحديث ذكاء العدو)
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

            # فحص الخسارة (لو العدو مسك اللاعب)
            if player.x == enemy.x and player.y == enemy.y:
                game_state = "GAME_OVER"

            # fحص الفوز (لو اللاعب وصل للكنز الأصفر)
            if player.x == goal_x and player.y == goal_y:
                game_state = "WIN"

        # 3. Rendering (الرسم والتلوين)
        screen.fill(BG_COLOR)
        
        # رسم المتاهة والشخصيات
        maze.draw(screen)
        
        # رسم مربع الفوز (الكنز الأصفر)
        from core.settings import TILE_SIZE
        goal_rect = pygame.Rect(goal_x * TILE_SIZE, goal_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, GOAL_COLOR, goal_rect, border_radius=4)
        
        player.draw(screen)
        enemy.draw(screen)

        # --- رسم لوحة التحكم والـ Scoreboard الجانبية ---
        # عرض اسم الخوارزمية الشغالة حالياً
        text_algo_title = font_ui.render("Active Algorithm:", True, (255, 255, 255))
        text_algo_name = font_ui.render(f">> {current_algorithm} <<", True, (46, 204, 113))
        screen.blit(text_algo_title, (button_x, 50))
        screen.blit(text_algo_name, (button_x, 80))

        # عرض الـ Score (الخطوات) والوقت
        text_score = font_ui.render(f"Steps Taken: {steps_count}", True, (236, 240, 241))
        text_time = font_ui.render(f"Time: {elapsed_time} Seconds", True, (236, 240, 241))
        screen.blit(text_score, (button_x, 130))
        screen.blit(text_time, (button_x, 160))

        # رسم أزرار التحكم الأربعة
        btn_bfs.draw(screen)
        btn_dfs.draw(screen)
        btn_astar.draw(screen)
        btn_greedy.draw(screen)

        # --- شاشات النهاية فوق اللعبة (Overlay) ---
        if game_state in ["GAME_OVER", "WIN"]:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 190))  # تعتيم الشاشة بنسبة شفافة شيك
            screen.blit(overlay, (0, 0))

            if game_state == "GAME_OVER":
                end_text = font_large.render("GAME OVER", True, ENEMY_COLOR)
            else:
                end_text = font_large.render("YOU WIN!", True, GOAL_COLOR)

            restart_text = font_small.render("Press 'R' to Restart the Game", True, (255, 255, 255))
            stats_text = font_small.render(f"Result - Steps: {steps_count} | Time: {elapsed_time}s", True, (200, 200, 200))
            
            # توسيط النصوص على الشاشة
            screen.blit(end_text, (SCREEN_WIDTH // 2 - end_text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
            screen.blit(stats_text, (SCREEN_WIDTH // 2 - stats_text.get_width() // 2, SCREEN_HEIGHT // 2 + 0))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()