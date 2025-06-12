#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Title Scene - The first screen players see when starting the game
"""

import pygame
from src.scenes.base_scene import BaseScene
from src.scenes.name_input_scene import NameInputScene
from src.ui.button import Button
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, WHITE, BLUE, LIGHT_BLUE

class TitleScene(BaseScene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        
        # Load font
        try:
            self.title_font = pygame.font.Font('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 48)
            self.subtitle_font = pygame.font.Font('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 24)
        except:
            # フォールバックとしてSysFontを使用
            self.title_font = pygame.font.SysFont('Arial', 48, bold=True)
            self.subtitle_font = pygame.font.SysFont('Arial', 24)
        
        # Create buttons
        button_width = 200
        button_height = 50
        button_x = (SCREEN_WIDTH - button_width) // 2
        
        self.start_button = Button(
            button_x, 
            SCREEN_HEIGHT // 2 + 50,
            button_width,
            button_height,
            "ゲームスタート",
            BLUE,
            LIGHT_BLUE,
            action=self.start_game
        )
        
        self.credits_button = Button(
            button_x,
            SCREEN_HEIGHT // 2 + 120,
            button_width,
            button_height,
            "クレジット",
            BLUE,
            LIGHT_BLUE,
            action=self.show_credits
        )
        
        self.exit_button = Button(
            button_x,
            SCREEN_HEIGHT // 2 + 190,
            button_width,
            button_height,
            "終了",
            BLUE,
            LIGHT_BLUE,
            action=self.exit_game
        )
        
        # Credits flag
        self.showing_credits = False
        
        # Try to load background image
        try:
            self.background = pygame.image.load("src/assets/images/title_bg.png")
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.background = None
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If showing credits, any click returns to title
            if self.showing_credits:
                self.showing_credits = False
                return
            
            # Otherwise, check button clicks
            self.start_button.check_click(event.pos)
            self.credits_button.check_click(event.pos)
            self.exit_button.check_click(event.pos)
    
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
        
        if self.showing_credits:
            self.draw_credits(screen)
        else:
            self.draw_title_screen(screen)
    
    def draw_title_screen(self, screen):
        # Draw title
        title_text = self.title_font.render(GAME_TITLE, True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_text = self.subtitle_font.render("AWSサービスの世界を冒険しよう！", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 60))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Draw buttons
        self.start_button.draw(screen)
        self.credits_button.draw(screen)
        self.exit_button.draw(screen)
    
    def draw_credits(self, screen):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        # Draw credits title
        credits_title = self.title_font.render("クレジット", True, WHITE)
        credits_title_rect = credits_title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(credits_title, credits_title_rect)
        
        # Draw credits content
        credits = [
            "アマゾン・フォレスト・クエスト：秘宝と七つのAWS守護者",
            "",
            "開発: Amazon Q CLI チーム",
            "グラフィック: Pygameとチームメンバー",
            "音楽: オープンソース素材",
            "",
            "このゲームはAWSサービスの学習を目的としています",
            "",
            "クリックして戻る"
        ]
        
        y_pos = 180
        for line in credits:
            credit_text = self.subtitle_font.render(line, True, WHITE)
            credit_rect = credit_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            screen.blit(credit_text, credit_rect)
            y_pos += 40
    
    def start_game(self):
        # Change to name input scene
        self.scene_manager.change_scene(NameInputScene(self.scene_manager))
    
    def show_credits(self):
        self.showing_credits = True
    
    def exit_game(self):
        pygame.quit()
        import sys
        sys.exit()
