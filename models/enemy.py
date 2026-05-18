# models/enemy.py
import pygame
from core.settings import TILE_SIZE

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.path = []
        self.move_delay = 12  # التحكم في سرعة القطة
        self.delay_counter = 0

    def update_path(self, new_path):
        self.path = new_path

    def move(self):
        if not self.path or len(self.path) <= 1:
            return
            
        self.delay_counter += 1
        if self.delay_counter >= self.move_delay:
            self.delay_counter = 0
            # الانتقال للخطوة التالية في المسار
            next_step = self.path[1]
            self.x = next_step[0]
            self.y = next_step[1]

    def draw(self, screen):
        cx = self.x * TILE_SIZE + TILE_SIZE // 2
        cy = self.y * TILE_SIZE + TILE_SIZE // 2
        radius = TILE_SIZE // 2 - 3

        # رسم رأس القطة (برتقالي شيك غامق / أو نيون رائع)
        cat_color = (230, 126, 34)
        pygame.draw.circle(screen, cat_color, (cx, cy), radius)

        # رسم الأذان المثلثية فوق الرأس
        # الأذن اليسرى
        pygame.draw.polygon(screen, cat_color, [(cx - 10, cy - 4), (cx - 12, cy - 14), (cx - 2, cy - 10)])
        # الأذن اليمنى
        pygame.draw.polygon(screen, cat_color, [(cx + 10, cy - 4), (cx + 12, cy - 14), (cx + 2, cy - 10)])

        # رسم العينين (عشرية خضراء شريرة أو سوداء)
        pygame.draw.circle(screen, (46, 204, 113), (cx - 5, cy - 2), 3)
        pygame.draw.circle(screen, (46, 204, 113), (cx + 5, cy - 2), 3)
        pygame.draw.circle(screen, (44, 62, 80), (cx - 5, cy - 2), 1)
        pygame.draw.circle(screen, (44, 62, 80), (cx + 5, cy - 2), 1)

        # الأنف والفم
        pygame.draw.polygon(screen, (231, 76, 60), [(cx, cy + 2), (cx - 2, cy + 4), (cx + 2, cy + 4)])