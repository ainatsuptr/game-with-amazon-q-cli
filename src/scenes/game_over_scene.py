#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Game Over Scene - Shown when the player loses
"""

import pygame
from src.scenes.base_scene import BaseScene
from src.ui.button import Button
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, RED, BLUE, LIGHT_BLUE

class GameOverScene(BaseScene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        
        # Load fonts
        try:
            self.title_font = pygame.font.Font('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 72)
            self.text_font = pygame.font.Font('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 24)
        except:
            # フォールバックとしてSysFontを使用
            self.title_font = pygame.font.SysFont('Arial', 72, bold=True)
            self.text_font = pygame.font.SysFont('Arial', 24)
        
        # Create buttons
        button_width = 200
        button_height = 50
        button_spacing = 20
        total_height = (button_height * 2) + button_spacing
        start_y = (SCREEN_HEIGHT - total_height) // 2 + 100
        
        self.restart_button = Button(
            (SCREEN_WIDTH - button_width) // 2,
            start_y,
            button_width,
            button_height,
            "再挑戦",
            BLUE,
            LIGHT_BLUE,
            action=self.restart_game
        )
        
        self.quit_button = Button(
            (SCREEN_WIDTH - button_width) // 2,
            start_y + button_height + button_spacing,
            button_width,
            button_height,
            "終了",
            RED,
            (255, 100, 100),
            action=self.quit_game
        )
        
        # Try to load background image
        try:
            self.background = pygame.image.load("src/assets/images/game_over_bg.png")
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.background = None
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check button clicks
            self.restart_button.check_click(event.pos)
            self.quit_button.check_click(event.pos)
    
    def update(self):
        pass
    
    def draw(self, screen):
        # Draw background
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            # Fallback dark background
            screen.fill((20, 20, 40))
        
        # Draw game over text
        game_over_text = self.title_font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(game_over_text, game_over_rect)
        
        # Draw message
        message_text = self.text_font.render("やる気が尽きてしまった...", True, WHITE)
        message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(message_text, message_rect)
        
        # Draw buttons
        self.restart_button.draw(screen)
        self.quit_button.draw(screen)
    
    def restart_game(self):
        # Reset player data
        self.scene_manager.player_data = {
            "name": self.scene_manager.player_data["name"],  # Keep the name
            "motivation": 100,
            "aws_knowledge": 0,
            "concentration": 100,
            "level": 1,
            "items": [],
            "skills": ["基本コマンド"],
            "completed_trials": [],
        }
        
        # Return to title scene
        from src.scenes.title_scene import TitleScene
        self.scene_manager.change_scene(TitleScene(self.scene_manager))
    
    def quit_game(self):
        pygame.quit()
        import sys
        sys.exit()
