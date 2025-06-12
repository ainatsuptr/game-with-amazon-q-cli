#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ending Scene - Shown when the player completes all trials
"""

import pygame
from src.scenes.base_scene import BaseScene
from src.ui.button import Button
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLUE, LIGHT_BLUE, YELLOW

class EndingScene(BaseScene):
    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        
        # Load fonts
        try:
            self.title_font = pygame.font.Font('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 48)
            self.text_font = pygame.font.Font('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 24)
        except:
            # フォールバックとしてSysFontを使用
            self.title_font = pygame.font.SysFont('Arial', 48, bold=True)
            self.text_font = pygame.font.SysFont('Arial', 24)
        
        # Ending text
        self.ending_title = "エピローグ：無限の拡張性"
        self.ending_text = [
            f"ついに、{self.scene_manager.get_player_data()['name']}は七人のAWS守護者全ての試練をクリアした。",
            "",
            "最後の守護者が消えると、眩い光が森の中心から放たれ、",
            "伝説の秘宝「無限の拡張性」が姿を現した。",
            "",
            "それは単なる物体ではなく、AWSの真髄そのものだった。",
            "",
            "「無限の拡張性」を手に入れた冒険者は、",
            "クラウドの真の力を理解し、どんな課題も乗り越えられるようになったという。",
            "",
            f"{self.scene_manager.get_player_data()['name']}の冒険は終わったが、",
            "AWSの世界での新たな冒険はこれからも続いていく..."
        ]
        
        self.current_line = 0
        self.text_speed = 3  # Characters per frame
        self.text_progress = 0
        self.text_complete = False
        
        # Create buttons (only shown when text is complete)
        button_width = 200
        button_height = 50
        button_spacing = 20
        total_height = (button_height * 2) + button_spacing
        start_y = SCREEN_HEIGHT - 150
        
        self.credits_button = Button(
            (SCREEN_WIDTH - button_width) // 2,
            start_y,
            button_width,
            button_height,
            "クレジット",
            BLUE,
            LIGHT_BLUE,
            action=self.show_credits
        )
        
        self.title_button = Button(
            (SCREEN_WIDTH - button_width) // 2,
            start_y + button_height + button_spacing,
            button_width,
            button_height,
            "タイトルへ",
            BLUE,
            LIGHT_BLUE,
            action=self.return_to_title
        )
        
        # Credits state
        self.showing_credits = False
        
        # Try to load background image
        try:
            self.background = pygame.image.load("src/assets/images/ending_bg.png")
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.background = None
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.showing_credits:
                # Return from credits on click
                self.showing_credits = False
                return
            
            if self.text_complete:
                # Check button clicks when text is complete
                self.credits_button.check_click(event.pos)
                self.title_button.check_click(event.pos)
            else:
                # Skip to end of text on click
                self.text_complete = True
                self.current_line = len(self.ending_text)
                self.text_progress = 0
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                if self.showing_credits:
                    # Return from credits on space/enter
                    self.showing_credits = False
                elif self.text_complete:
                    # Show credits on space/enter when text is complete
                    self.show_credits()
                else:
                    # Skip to end of text on space/enter
                    self.text_complete = True
                    self.current_line = len(self.ending_text)
                    self.text_progress = 0
    
    def update(self):
        # Update text animation
        if not self.text_complete:
            if self.current_line < len(self.ending_text):
                current_text = self.ending_text[self.current_line]
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
            # Fallback starry background
            screen.fill((0, 0, 40))
            for i in range(100):
                x = pygame.time.get_ticks() // 50 + i * 10
                y = i * 6
                pygame.draw.circle(screen, WHITE, (x % SCREEN_WIDTH, y % SCREEN_HEIGHT), 1)
        
        if self.showing_credits:
            self.draw_credits(screen)
        else:
            # Draw semi-transparent overlay for text readability
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            
            # Draw title
            title_text = self.title_font.render(self.ending_title, True, YELLOW)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
            screen.blit(title_text, title_rect)
            
            # Draw ending text
            if self.text_complete:
                # Draw all text at once
                y_pos = 150
                for line in self.ending_text:
                    if line:  # Skip empty lines
                        text_surface = self.text_font.render(line, True, WHITE)
                        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
                        screen.blit(text_surface, text_rect)
                    y_pos += 30
                
                # Draw buttons
                self.credits_button.draw(screen)
                self.title_button.draw(screen)
            else:
                # Draw animated text
                y_pos = 150
                for i in range(self.current_line):
                    if i < len(self.ending_text):
                        line = self.ending_text[i]
                        if line:  # Skip empty lines
                            text_surface = self.text_font.render(line, True, WHITE)
                            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
                            screen.blit(text_surface, text_rect)
                    y_pos += 30
                
                # Draw current line being animated
                if self.current_line < len(self.ending_text):
                    current_text = self.ending_text[self.current_line][:self.text_progress]
                    if current_text:
                        text_surface = self.text_font.render(current_text, True, WHITE)
                        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
                        screen.blit(text_surface, text_rect)
            
            # Draw hint text
            if self.text_complete:
                hint_text = self.text_font.render("スペースキーまたはクリックでクレジットを見る", True, (200, 200, 200))
            else:
                hint_text = self.text_font.render("スペースキーまたはクリックでスキップ", True, (200, 200, 200))
            
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
            screen.blit(hint_text, hint_rect)
    
    def draw_credits(self, screen):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        # Draw credits title
        credits_title = self.title_font.render("クレジット", True, YELLOW)
        credits_title_rect = credits_title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(credits_title, credits_title_rect)
        
        # Draw player stats
        player_data = self.scene_manager.get_player_data()
        stats = [
            f"冒険者: {player_data['name']}",
            f"最終レベル: {player_data['level']}",
            f"AWS知識: {player_data['aws_knowledge']}",
            f"クリア時間: {pygame.time.get_ticks() // 1000}秒",
            "",
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
        for line in stats:
            credit_text = self.text_font.render(line, True, WHITE)
            credit_rect = credit_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            screen.blit(credit_text, credit_rect)
            y_pos += 30
    
    def show_credits(self):
        self.showing_credits = True
    
    def return_to_title(self):
        # Reset player data
        self.scene_manager.player_data = {
            "name": "",
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
