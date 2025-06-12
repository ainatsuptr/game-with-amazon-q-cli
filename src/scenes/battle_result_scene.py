#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Battle Result Scene - Shows the result of a battle
"""

import pygame
from src.scenes.base_scene import BaseScene
from src.ui.button import Button
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLUE, LIGHT_BLUE, GREEN, RED

class BattleResultScene(BaseScene):
    def __init__(self, scene_manager, guardian, result):
        super().__init__(scene_manager)
        
        self.guardian = guardian
        self.result = result  # "victory", "defeat", or "escape"
        
        # Load fonts
        try:
            self.title_font = pygame.font.Font('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 48)
            self.text_font = pygame.font.Font('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 24)
        except:
            # フォールバックとしてSysFontを使用
            self.title_font = pygame.font.SysFont('Arial', 48, bold=True)
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
            self.background = pygame.image.load("src/assets/images/result_bg.png")
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
        
        # Draw result window
        result_rect = pygame.Rect(SCREEN_WIDTH // 6, SCREEN_HEIGHT // 6, 
                               SCREEN_WIDTH * 2 // 3, SCREEN_HEIGHT * 2 // 3)
        pygame.draw.rect(screen, (50, 50, 80), result_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, result_rect, 2, border_radius=10)
        
        # Draw title based on result
        if self.result == "victory":
            title_text = self.title_font.render("勝利！", True, GREEN)
        elif self.result == "defeat":
            title_text = self.title_font.render("敗北...", True, RED)
        else:  # escape
            title_text = self.title_font.render("逃走成功", True, WHITE)
        
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 + 40))
        screen.blit(title_text, title_rect)
        
        # Draw result text
        y_pos = SCREEN_HEIGHT // 6 + 100
        
        if self.result == "victory":
            result_lines = [
                f"{self.guardian['name']}の試練をクリアした！",
                "",
                f"「{self.guardian['service']}の力を認めよう。」",
                "",
                "AWS知識が50ポイント増加した！",
                f"残りの試練: {7 - len(self.scene_manager.get_player_data()['completed_trials'])}/7"
            ]
        elif self.result == "defeat":
            result_lines = [
                f"{self.guardian['name']}に敗北してしまった...",
                "",
                "やる気が尽きてしまったが、また挑戦することができる。",
                "",
                "次は{self.guardian['weakness']}について調べてから挑もう。"
            ]
        else:  # escape
            result_lines = [
                f"{self.guardian['name']}から逃げ出した。",
                "",
                "準備を整えてから再挑戦しよう。",
                "",
                f"ヒント: {self.guardian['name']}の弱点は{self.guardian['weakness']}だ。"
            ]
        
        for line in result_lines:
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
