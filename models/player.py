# models/player.py
import pygame
from core.settings import TILE_SIZE, PLAYER_COLOR

class Player:
    def __init__(self, x, y):
        # الإحداثيات هنا بالـ Grid (مثلاً الصف 1، العمود 1)
        self.x = x
        self.y = y

    def move(self, dx, dy, maze_grid):
        # حساب المكان الجديد المتوقع للاعب
        new_x = self.x + dx
        # الـ dx والـ dy هما اتجاه الحركة (مثلاً يمين يبقى dx=1, dy=0)
        new_y = self.y + dy

        # الـ Collision Detection (منع اختراق الحوائط):
        # نتأكد إن المربع الجديد مش حيطة (يعني قيمته في الـ grid مش بتساوي 1)
        if maze_grid[new_y][new_x] != 1:
            self.x = new_x
            self.y = new_y

    def draw(self, screen):
        # تحويل إحداثيات الـ Grid لبكسل عشان نرسم على الشاشة
        pixel_x = self.x * TILE_SIZE
        pixel_y = self.y * TILE_SIZE
        
        # رسم اللاعب كمربع ملون (قدام نقدر نغيره بصورة)
        rect = pygame.Rect(pixel_x, pixel_y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, PLAYER_COLOR, rect)