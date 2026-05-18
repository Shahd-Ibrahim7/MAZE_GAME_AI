# models/player.py
import pygame
from core.settings import TILE_SIZE

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy, grid):
        # التحقق من أن الحركة داخل المتاهة وليست في حيطة
        if 0 <= self.x + dx < len(grid[0]) and 0 <= self.y + dy < len(grid):
            if grid[self.y + dy][self.x + dx] == 0:
                self.x += dx
                self.y += dy

    def draw(self, screen):
        # حساب إحداثيات مركز المربع
        cx = self.x * TILE_SIZE + TILE_SIZE // 2
        cy = self.y * TILE_SIZE + TILE_SIZE // 2
        radius = TILE_SIZE // 2 - 4

        # رسم جسم الفار (رمادي فاتح مودرن)
        pygame.draw.circle(screen, (149, 165, 166), (cx, cy), radius)
        
        # رسم الأذان اللطيفة (وردي / رمادي)
        pygame.draw.circle(screen, (127, 140, 141), (cx - 6, cy - 8), 5)
        pygame.draw.circle(screen, (127, 140, 141), (cx + 6, cy - 8), 5)
        pygame.draw.circle(screen, (241, 148, 180), (cx - 6, cy - 8), 2) # داخل الأذن
        pygame.draw.circle(screen, (241, 148, 180), (cx + 6, cy - 8), 2)

        # رسم العينين (نقاط سوداء صغيرة)
        pygame.draw.circle(screen, (44, 62, 80), (cx - 4, cy - 2), 2)
        pygame.draw.circle(screen, (44, 62, 80), (cx + 4, cy - 2), 2)

        # الأنف (نقطة وردي صغيرة في المركز)
        pygame.draw.circle(screen, (231, 76, 60), (cx, cy + 3), 3)