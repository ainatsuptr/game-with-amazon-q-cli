#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Text Input UI element for the game
"""

import pygame
from src.utils.constants import WHITE, BLACK, GRAY

class TextInput:
    def __init__(self, x, y, width, height, max_length=20, placeholder="", font_size=24):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.max_length = max_length
        self.placeholder = placeholder
        try:
            self.font = pygame.font.Font('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', font_size)
        except:
            self.font = pygame.font.SysFont('Arial', font_size)
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_blink_speed = 500  # milliseconds
        
        # Pre-render placeholder text
        self.placeholder_surface = self.font.render(self.placeholder, True, GRAY)
        self.placeholder_rect = self.placeholder_surface.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state based on click
            self.active = self.rect.collidepoint(event.pos)
        
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                # Remove last character
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                # Deactivate on enter
                self.active = False
            elif len(self.text) < self.max_length:
                # Add character if not at max length
                # Filter out non-printable characters
                if event.unicode.isprintable():
                    self.text += event.unicode
    
    def update(self):
        # Update cursor blink
        now = pygame.time.get_ticks()
        if now - self.cursor_timer > self.cursor_blink_speed:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = now
    
    def draw(self, surface):
        # Draw input box
        border_color = WHITE if self.active else GRAY
        pygame.draw.rect(surface, BLACK, self.rect, border_radius=5)
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=5)
        
        # Draw text or placeholder
        if self.text:
            text_surface = self.font.render(self.text, True, WHITE)
            text_rect = text_surface.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
            surface.blit(text_surface, text_rect)
            
            # Draw cursor if active
            if self.active and self.cursor_visible:
                cursor_x = text_rect.right + 2
                cursor_y = text_rect.y
                cursor_height = text_rect.height
                pygame.draw.line(surface, WHITE, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)
        else:
            # Draw placeholder
            surface.blit(self.placeholder_surface, self.placeholder_rect)
    
    def get_text(self):
        return self.text
