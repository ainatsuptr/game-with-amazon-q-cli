#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Name Input Scene - For entering the player's name
"""

import pygame
from src.scenes.base_scene import BaseScene
from src.scenes.prologue_scene import PrologueScene
from src.ui.button import Button
from src.ui.text_input import TextInput
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLUE, LIGHT_BLUE

class NameInputScene(BaseScene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        
        # Load fonts
        try:
            self.title_font = pygame.font.Font('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 36)
            self.text_font = pygame.font.Font('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 24)
        except:
            # フォールバックとしてSysFontを使用
            self.title_font = pygame.font.SysFont('Arial', 36, bold=True)
            self.text_font = pygame.font.SysFont('Arial', 24)
        
        # Create text input
        input_width = 300
        input_height = 40
        input_x = (SCREEN_WIDTH - input_width) // 2
        input_y = SCREEN_HEIGHT // 2 - 20
        
        self.name_input = TextInput(
            input_x,
            input_y,
            input_width,
            input_height,
            max_length=15,
            placeholder="名前を入力してください"
        )
        
        # Create buttons
        button_width = 200
        button_height = 50
        button_x = (SCREEN_WIDTH - button_width) // 2
        
        self.confirm_button = Button(
            button_x,
            input_y + input_height + 30,
            button_width,
            button_height,
            "決定",
            BLUE,
            LIGHT_BLUE,
            action=self.confirm_name
        )
        
        self.back_button = Button(
            button_x,
            input_y + input_height + 100,
            button_width,
            button_height,
            "戻る",
            BLUE,
            LIGHT_BLUE,
            action=self.go_back
        )
        
        # Error message
        self.error_message = ""
        self.show_error = False
        
        # Try to load background image
        try:
            self.background = pygame.image.load("src/assets/images/name_input_bg.png")
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.background = None
    
    def handle_event(self, event):
        # Handle text input events
        self.name_input.handle_event(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check button clicks
            self.confirm_button.check_click(event.pos)
            self.back_button.check_click(event.pos)
        
        elif event.type == pygame.MOUSEMOTION:
            # Check button hover
            self.confirm_button.check_hover(event.pos)
            self.back_button.check_hover(event.pos)
    
    def update(self):
        # Update text input
        self.name_input.update()
    
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
        
        # Draw title
        title_text = self.title_font.render("冒険者の名前を入力してください", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(title_text, title_rect)
        
        # Draw text input
        self.name_input.draw(screen)
        
        # Draw buttons
        self.confirm_button.draw(screen)
        self.back_button.draw(screen)
        
        # Draw error message if needed
        if self.show_error:
            error_text = self.text_font.render(self.error_message, True, (255, 100, 100))
            error_rect = error_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            screen.blit(error_text, error_rect)
    
    def confirm_name(self):
        name = self.name_input.get_text().strip()
        
        if not name:
            self.error_message = "名前を入力してください"
            self.show_error = True
            return
        
        # Set player name and proceed to prologue
        self.scene_manager.set_player_name(name)
        self.scene_manager.change_scene(PrologueScene(self.scene_manager))
    
    def go_back(self):
        # Import here to avoid circular import
        from src.scenes.title_scene import TitleScene
        self.scene_manager.change_scene(TitleScene(self.scene_manager))
