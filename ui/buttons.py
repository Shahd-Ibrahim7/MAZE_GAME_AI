# ui/buttons.py
import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        # تجهيز الفونت الخاص بالزرار
        self.font = pygame.font.SysFont("Arial", 20, bold=True)

    def draw(self, screen):
        # معرفة مكان الماوس الحالي
        mouse_pos = pygame.mouse.get_pos()
        
        # لو الماوس فوق الزرار، غير لونه للون الـ Hover (التفاعل)
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect, border_radius=8)
        else:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=8)

        # رسم النص في منتصف الزرار بالظبط
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        # التحقق إذا كان الحدث هو ضغطة ماوس شمال وفوق الزرار بالظبط
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False