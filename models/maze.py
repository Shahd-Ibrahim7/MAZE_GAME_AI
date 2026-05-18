# models/maze.py
import pygame
import random
from core.settings import TILE_SIZE, WALL_COLOR

class Maze:
    def __init__(self):
        # تحديد الأبعاد الثابتة للمتاهة مباشرة هنا لتجنب أخطاء الـ Import
        self.width = 15     # العدد الكلي للمربعات عرضاً
        self.height = 11    # العدد الكلي للمربعات طولاً
        self.grid = []
        self.generate_random_maze()

    def generate_random_maze(self):
        # 1. نبدأ بملء المتاهة كلها حوائط (1 يعني حيطة، و0 يعني ممر)
        self.grid = [[1 for _ in range(self.width)] for _ in range(self.height)]
        
        # 2. تحديد نقاط البداية والنهاية ومكان العدو كممرات مفتوحة حتماً
        self.grid[1][1] = 0   # مكان اللاعب الأساسي
        self.grid[7][13] = 0  # مكان العدو الأساسي
        self.grid[1][13] = 0  # مكان الكنز/الهدف الأساسي (13, 1)

        # 3. خوارزمية DFS لتهديم الحوائط وصنع ممرات عشوائية منظمّة
        stack = [(1, 1)]
        visited = set([(1, 1)])

        while stack:
            cx, cy = stack[-1]
            neighbors = []

            # التحقق من الجيران على بعد خطوتين
            directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 0 < nx < self.width - 1 and 0 < ny < self.height - 1:
                    if (nx, ny) not in visited:
                        neighbors.append((nx, ny, dx, dy))

            if neighbors:
                # اختيار اتجاه عشوائي لفتح الممر الجديد
                nx, ny, dx, dy = random.choice(neighbors)
                
                # هدم الحيطة اللي في النص
                self.grid[cy + dy//2][cx + dx//2] = 0
                self.grid[ny][nx] = 0
                
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

        # نفتح شوية حوائط عشوائية زيادة عشان المتاهة متبقاش ممر واحد ضيق جداً واللاعب يعرف يهرب
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.grid[y][x] == 1 and random.random() < 0.18:
                    self.grid[y][x] = 0

    def draw(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 1:
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, WALL_COLOR, rect, border_radius=4)