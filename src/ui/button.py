#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Button UI element for the game
"""

import pygame
from src.utils.constants import WHITE

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action=None, font_size=24):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        try:
            self.font = pygame.font.Font('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', font_size)
        except:
            self.font = pygame.font.SysFont('Arial', font_size)
        self.is_hovered = False
        
        # Pre-render text
        self.text_surface = self.font.render(self.text, True, WHITE)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
    
    def draw(self, surface):
        # Determine color based on hover state
        current_color = self.hover_color if self.is_hovered else self.color
        
        # Draw button
        pygame.draw.rect(surface, current_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=10)  # Border
        
        # Draw text
        surface.blit(self.text_surface, self.text_rect)
    
    def check_hover(self, pos):
        """Check if mouse is hovering over button"""
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
    
    def check_click(self, pos):
        """Check if button was clicked and execute action if so"""
        if self.rect.collidepoint(pos) and self.action:
            self.action()
            return True
        return False
