#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Event Scene - Shows random events during exploration
"""

import pygame
from src.scenes.base_scene import BaseScene
from src.ui.button import Button
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLUE, LIGHT_BLUE

class EventScene(BaseScene):
    def __init__(self, scene_manager, title, event_text):
        super().__init__(scene_manager)
        
        self.title = title
        self.event_text = event_text
        
        # Load fonts
        try:
            self.title_font = pygame.font.Font('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 36)
            self.text_font = pygame.font.Font('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 24)
        except:
            # フォールバックとしてSysFontを使用
            self.title_font = pygame.font.SysFont('Arial', 36, bold=True)
            self.text_font = pygame.font.SysFont('Arial', 24)
        
        # Create continue button
        button_width = 200
        button_height = 50
        button_x = (SCREEN_WIDTH - button_width) // 2
        
        self.continue_button = Button(
            button_x,
            SCREEN_HEIGHT - 100,
            button_width,
            button_height,
            "続ける",
            BLUE,
            LIGHT_BLUE,
            action=self.continue_adventure
        )
        
        # Try to load background image
        try:
            self.background = pygame.image.load("src/assets/images/event_bg.png")
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.background = None
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check button click
            self.continue_button.check_click(event.pos)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                # Continue on space/enter
                self.continue_adventure()
    
    def update(self):
        pass
    
    def draw(self, screen):
        # Draw background
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            # Fallback gradient background
            for y in range(SCREEN_HEIGHT):
                color_value = int(255 * (1 - y / SCREEN_HEIGHT))
                blue_value = min(255, color_value * 2)  # 255を超えないようにする
                pygame.draw.line(screen, (0, color_value, blue_value), (0, y), (SCREEN_WIDTH, y))
        
        # Draw semi-transparent overlay for text readability
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # Draw event window
        event_rect = pygame.Rect(SCREEN_WIDTH // 6, SCREEN_HEIGHT // 6, 
                               SCREEN_WIDTH * 2 // 3, SCREEN_HEIGHT * 2 // 3)
        pygame.draw.rect(screen, (50, 50, 80), event_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, event_rect, 2, border_radius=10)
        
        # Draw title
        title_text = self.title_font.render(self.title, True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 + 40))
        screen.blit(title_text, title_rect)
        
        # Draw event text
        y_pos = SCREEN_HEIGHT // 6 + 100
        for line in self.event_text:
            text_surface = self.text_font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            screen.blit(text_surface, text_rect)
            y_pos += 40
        
        # Draw continue button
        self.continue_button.draw(screen)
    
    def continue_adventure(self):
        # Return to map scene
        from src.scenes.map_scene import MapScene
        self.scene_manager.change_scene(MapScene(self.scene_manager))
