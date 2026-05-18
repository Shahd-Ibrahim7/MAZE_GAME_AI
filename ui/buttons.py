# ui/buttons.py
import pygame

class Button:
    def __init__(self, x, y, width, height, text, base_color, accent_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.base_color = base_color      # اللون الداكن للزرار
        self.accent_color = accent_color  # اللون المضيء الخاص بالخوارزمية
        self.font = pygame.font.SysFont("Segoe UI", 19, bold=True)

    def draw(self, screen, is_active):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)

        # 1. رسم ظل خفيف خلف الزرار لإعطاء عمق (Shadow)
        shadow_rect = self.rect.copy()
        shadow_rect.y += 3
        pygame.draw.rect(screen, (20, 24, 30), shadow_rect, border_radius=12)

        # 2. تحديد لون الخلفية بناءً على الحالة
        if is_active:
            bg_color = (self.base_color[0]+20, self.base_color[1]+20, self.base_color[2]+20)
            border_color = self.accent_color
            border_width = 3
        elif is_hovered:
            bg_color = (60, 80, 100)
            border_color = (200, 200, 200)
            border_width = 1
        else:
            bg_color = self.base_color
            border_color = (100, 110, 120)
            border_width = 1

        # 3. رسم جسم الزرار الأساسي
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=12)
        
        # 4. رسم البرواز ( Border) - لو نشط يكون ملون ومضيء
        pygame.draw.rect(screen, border_color, self.rect, width=border_width, border_radius=12)

        # 5. رسم علامة ملونة صغيرة (Indicator) على اليسار
        indicator_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 12, 6, 20)
        pygame.draw.rect(screen, self.accent_color, indicator_rect, border_radius=3)

        # 6. رسم النص
        text_color = (255, 255, 255) if not is_active else self.accent_color
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=(self.rect.centerx + 5, self.rect.centery))
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False