# models/enemy.py
import pygame
from core.settings import TILE_SIZE, ENEMY_COLOR

class Enemy:
    def __init__(self, x, y):
        # إحداثيات العدو في الـ Grid
        self.x = x
        self.y = y
        # قائمة الخطوات اللي المفروض يمششي فيها (الـ Path اللي هيجيله من الخوارزمية)
        self.path = []
        # الـ Speed Control عشان العدو ميجريش بسرعة طلقة (يتحرك كل كذا فريم)
        self.move_delay = 20  # عدد الفريمات بين كل خطوة وخطوة
        self.move_counter = 0

    def update_path(self, new_path):
        # ميثود عشان الخوارزمية تباصي للعدو الطريق الجديد للاعب
        self.path = new_path

    def move(self):
        # التحكم في سرعة حركة العدو
        self.move_counter += 1
        if self.move_counter < self.move_delay:
            return

        self.move_counter = 0 # تصفير العداد

        # لو فيه خطوات في المسار، خليه ياخد الخطوة الجاية
        if self.path and len(self.path) > 1:
            # الخوارزمية بترجع المسار كامل [مكان_العدو, الخطوة_الجاية, ..., مكان_اللاعب]
            # إحنا محتاجين الخطوة الجاية علطول اللي هي رقم 1 في الـ list
            next_step = self.path[1]
            self.x = next_step[0]
            self.y = next_step[1]
            
            # احذفي الخطوة اللي مشاها عشان ياخد اللي بعدها المرة الجاية
            self.path.pop(0)

    def draw(self, screen):
        # تحويل إحداثيات الـ Grid لبكسل للرسم
        pixel_x = self.x * TILE_SIZE
        pixel_y = self.y * TILE_SIZE
        
        rect = pygame.Rect(pixel_x, pixel_y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, ENEMY_COLOR, rect)