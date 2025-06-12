#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Status Bar UI element for the game
"""

import pygame
from src.utils.constants import WHITE, BLACK, GRAY

class StatusBar:
    def __init__(self, x, y, width, height, label, value, max_value, color=(0, 255, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.value = value
        self.max_value = max_value
        self.color = color
        try:
            self.font = pygame.font.Font('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 16)
        except:
            self.font = pygame.font.SysFont('Arial', 16)
        
        # Pre-render label
        self.label_surface = self.font.render(self.label, True, WHITE)
        self.label_rect = self.label_surface.get_rect(midright=(self.rect.x - 10, self.rect.centery))
    
    def update_value(self, value):
        """Update the current value"""
        self.value = value
    
    def draw(self, surface):
        # Draw label
        surface.blit(self.label_surface, self.label_rect)
        
        # Draw background
        pygame.draw.rect(surface, GRAY, self.rect, border_radius=3)
        
        # Calculate fill width based on value
        fill_width = int(self.rect.width * (self.value / self.max_value))
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        
        # Draw fill
        if fill_width > 0:
            pygame.draw.rect(surface, self.color, fill_rect, border_radius=3)
        
        # Draw border
        pygame.draw.rect(surface, WHITE, self.rect, 1, border_radius=3)
        
        # Draw value text
        value_text = f"{self.value}/{self.max_value}"
        value_surface = self.font.render(value_text, True, WHITE)
        value_rect = value_surface.get_rect(center=self.rect.center)
        surface.blit(value_surface, value_rect)
