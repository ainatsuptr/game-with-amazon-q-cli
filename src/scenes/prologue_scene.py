#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Prologue Scene - Introduces the game story
"""

import pygame
from src.scenes.base_scene import BaseScene
from src.scenes.map_scene import MapScene
from src.ui.button import Button
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLUE, LIGHT_BLUE

class PrologueScene(BaseScene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        
        # Load fonts
        try:
            self.title_font = pygame.font.Font('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 36)
            self.text_font = pygame.font.Font('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 22)
        except:
            # フォールバックとしてSysFontを使用
            self.title_font = pygame.font.SysFont('Arial', 36, bold=True)
            self.text_font = pygame.font.SysFont('Arial', 22)
        
        # Prologue text
        self.prologue_title = "プロローグ：アマゾンの森の伝説"
        self.prologue_text = [
            "遥か昔、アマゾンの森の奥深くには「無限の拡張性」と呼ばれる伝説の秘宝が隠されていたという。",
            "その秘宝は持ち主に無限の可能性と力をもたらすと言われていた。",
            "",
            "しかし、秘宝は七人のAWS守護者によって厳重に守られており、",
            "彼らの試練を乗り越えた者だけが秘宝を手に入れることができるという。",
            "",
            f"あなた、{self.scene_manager.get_player_data()['name']}は、この伝説を聞き、",
            "アマゾンの森への冒険を決意した。",
            "",
            "AWS知識を武器に、七つの試練に挑み、伝説の秘宝を手に入れることができるだろうか？",
            "",
            "あなたの冒険が今、始まる..."
        ]
        
        self.current_line = 0
        self.text_speed = 3  # Characters per frame
        self.text_progress = 0
        self.text_complete = False
        
        # Create button (only shown when text is complete)
        button_width = 200
        button_height = 50
        button_x = (SCREEN_WIDTH - button_width) // 2
        
        self.continue_button = Button(
            button_x,
            SCREEN_HEIGHT - 100,
            button_width,
            button_height,
            "冒険を始める",
            BLUE,
            LIGHT_BLUE,
            action=self.start_adventure
        )
        
        # Try to load background image
        try:
            self.background = pygame.image.load("src/assets/images/prologue_bg.png")
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.background = None
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.text_complete:
                # Check button click when text is complete
                self.continue_button.check_click(event.pos)
            else:
                # Skip to end of text on click
                self.text_complete = True
                self.current_line = len(self.prologue_text)
                self.text_progress = 0
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                if self.text_complete:
                    # Start adventure on space/enter when text is complete
                    self.start_adventure()
                else:
                    # Skip to end of text on space/enter
                    self.text_complete = True
                    self.current_line = len(self.prologue_text)
                    self.text_progress = 0
    
    def update(self):
        # Update text animation
        if not self.text_complete:
            if self.current_line < len(self.prologue_text):
                current_text = self.prologue_text[self.current_line]
                if self.text_progress < len(current_text):
                    self.text_progress += self.text_speed
                    if self.text_progress >= len(current_text):
                        self.text_progress = 0
                        self.current_line += 1
                else:
                    self.text_progress = 0
                    self.current_line += 1
            else:
                self.text_complete = True
    
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
        
        # Draw title
        title_text = self.title_font.render(self.prologue_title, True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(title_text, title_rect)
        
        # Draw prologue text
        if self.text_complete:
            # Draw all text at once
            y_pos = 150
            for line in self.prologue_text:
                if line:  # Skip empty lines
                    text_surface = self.text_font.render(line, True, WHITE)
                    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
                    screen.blit(text_surface, text_rect)
                y_pos += 30
            
            # Draw continue button
            self.continue_button.draw(screen)
        else:
            # Draw animated text
            y_pos = 150
            for i in range(self.current_line):
                if i < len(self.prologue_text):
                    line = self.prologue_text[i]
                    if line:  # Skip empty lines
                        text_surface = self.text_font.render(line, True, WHITE)
                        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
                        screen.blit(text_surface, text_rect)
                y_pos += 30
            
            # Draw current line being animated
            if self.current_line < len(self.prologue_text):
                current_text = self.prologue_text[self.current_line][:self.text_progress]
                if current_text:
                    text_surface = self.text_font.render(current_text, True, WHITE)
                    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
                    screen.blit(text_surface, text_rect)
        
        # Draw hint text
        if self.text_complete:
            hint_text = self.text_font.render("スペースキーまたはクリックで続ける", True, (200, 200, 200))
        else:
            hint_text = self.text_font.render("スペースキーまたはクリックでスキップ", True, (200, 200, 200))
        
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
        screen.blit(hint_text, hint_rect)
    
    def start_adventure(self):
        # Change to map scene to start the adventure
        self.scene_manager.change_scene(MapScene(self.scene_manager))
