#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Map Scene - Shows the game map and allows area selection
"""

import pygame
import random
from src.scenes.base_scene import BaseScene
from src.scenes.battle_scene import BattleScene
from src.scenes.event_scene import EventScene
from src.ui.button import Button
from src.ui.status_bar import StatusBar
from src.utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, BLUE, LIGHT_BLUE, 
    AREAS, AWS_GUARDIANS, ITEMS, INITIAL_MOTIVATION, INITIAL_AWS_KNOWLEDGE, INITIAL_CONCENTRATION
)

class MapScene(BaseScene):
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
        
        # Create area buttons
        self.area_buttons = []
        
        # Calculate button positions in a circular pattern
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        radius = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 3
        
        for i, area in enumerate(AREAS):
            angle = 2 * 3.14159 * i / len(AREAS)
            x = center_x + int(radius * 0.8 * pygame.math.Vector2(1, 0).rotate(angle * 180 / 3.14159).x)
            y = center_y + int(radius * 0.8 * pygame.math.Vector2(1, 0).rotate(angle * 180 / 3.14159).y)
            
            # Create button
            button = Button(
                x - 75,  # Center the button on the calculated position
                y - 25,
                150,
                50,
                area,
                BLUE,
                LIGHT_BLUE,
                action=lambda a=area: self.select_area(a)
            )
            self.area_buttons.append(button)
        
        # Create status bars
        self.motivation_bar = StatusBar(
            20, 20, 200, 20, 
            "やる気", 
            self.scene_manager.get_player_data()["motivation"], 
            INITIAL_MOTIVATION,
            (255, 100, 100)
        )
        
        self.aws_knowledge_bar = StatusBar(
            20, 50, 200, 20, 
            "AWS知識", 
            self.scene_manager.get_player_data()["aws_knowledge"], 
            100,  # Level up at 100
            (100, 100, 255)
        )
        
        self.concentration_bar = StatusBar(
            20, 80, 200, 20, 
            "集中力", 
            self.scene_manager.get_player_data()["concentration"], 
            INITIAL_CONCENTRATION,
            (100, 255, 100)
        )
        
        # Create inventory button
        self.inventory_button = Button(
            SCREEN_WIDTH - 150,
            20,
            130,
            40,
            "インベントリ",
            BLUE,
            LIGHT_BLUE,
            action=self.show_inventory
        )
        
        # Inventory state
        self.showing_inventory = False
        
        # Try to load background image
        try:
            self.background = pygame.image.load("src/assets/images/map_bg.png")
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.background = None
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.showing_inventory:
                # Close inventory on click outside
                inventory_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, 
                                           SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                if not inventory_rect.collidepoint(event.pos):
                    self.showing_inventory = False
                return
            
            # Check area button clicks
            for button in self.area_buttons:
                button.check_click(event.pos)
            
            # Check inventory button click
            self.inventory_button.check_click(event.pos)
    
    def update(self):
        # Update status bars with current player data
        player_data = self.scene_manager.get_player_data()
        self.motivation_bar.update_value(player_data["motivation"])
        self.aws_knowledge_bar.update_value(player_data["aws_knowledge"] % 100)  # Show progress to next level
        self.concentration_bar.update_value(player_data["concentration"])
        
        # Check for game over
        if self.scene_manager.is_game_over():
            from src.scenes.game_over_scene import GameOverScene
            self.scene_manager.change_scene(GameOverScene(self.scene_manager))
        
        # Check for game completion
        if self.scene_manager.is_game_completed():
            from src.scenes.ending_scene import EndingScene
            self.scene_manager.change_scene(EndingScene(self.scene_manager))
    
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
        
        # Draw map title
        title_text = self.title_font.render("アマゾンの森マップ", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 40))
        screen.blit(title_text, title_rect)
        
        # Draw player info
        player_data = self.scene_manager.get_player_data()
        player_text = self.text_font.render(f"冒険者: {player_data['name']}   レベル: {player_data['level']}", True, WHITE)
        player_rect = player_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(player_text, player_rect)
        
        # Draw completed trials info
        completed = len(player_data["completed_trials"])
        total = len(AWS_GUARDIANS)
        progress_text = self.text_font.render(f"試練達成: {completed}/{total}", True, WHITE)
        progress_rect = progress_text.get_rect(center=(SCREEN_WIDTH // 2, 110))
        screen.blit(progress_text, progress_rect)
        
        # Draw area buttons
        for button in self.area_buttons:
            button.draw(screen)
        
        # Draw status bars
        self.motivation_bar.draw(screen)
        self.aws_knowledge_bar.draw(screen)
        self.concentration_bar.draw(screen)
        
        # Draw inventory button
        self.inventory_button.draw(screen)
        
        # Draw inventory if showing
        if self.showing_inventory:
            self.draw_inventory(screen)
    
    def draw_inventory(self, screen):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        # Draw inventory window
        inventory_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, 
                                   SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.draw.rect(screen, (50, 50, 80), inventory_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, inventory_rect, 2, border_radius=10)
        
        # Draw inventory title
        inv_title = self.title_font.render("インベントリ", True, WHITE)
        inv_title_rect = inv_title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 30))
        screen.blit(inv_title, inv_title_rect)
        
        # Draw items
        player_items = self.scene_manager.get_player_data()["items"]
        if player_items:
            y_pos = SCREEN_HEIGHT // 4 + 80
            for item_name in player_items:
                # Find item details
                item_details = next((item for item in ITEMS if item["name"] == item_name), None)
                if item_details:
                    item_text = self.text_font.render(f"{item_name}: {item_details['description']}", True, WHITE)
                    item_rect = item_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
                    screen.blit(item_text, item_rect)
                    y_pos += 40
        else:
            no_items_text = self.text_font.render("アイテムを持っていません", True, WHITE)
            no_items_rect = no_items_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(no_items_text, no_items_rect)
        
        # Draw close hint
        close_text = self.text_font.render("クリックして閉じる", True, (200, 200, 200))
        close_rect = close_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + SCREEN_HEIGHT // 2 - 30))
        screen.blit(close_text, close_rect)
    
    def select_area(self, area):
        # Determine if we trigger a battle, event, or nothing
        event_type = random.choices(
            ["battle", "item", "hint", "nothing"],
            weights=[0.4, 0.3, 0.2, 0.1],
            k=1
        )[0]
        
        if event_type == "battle":
            # Find guardian for this area
            guardian = next((g for g in AWS_GUARDIANS if g["area"] == area), None)
            
            # Check if guardian is already defeated
            if guardian and guardian["name"] in self.scene_manager.get_player_data()["completed_trials"]:
                # If defeated, show a different event instead
                self.trigger_random_event(area)
            else:
                # Start battle with guardian
                self.scene_manager.change_scene(BattleScene(self.scene_manager, guardian))
        else:
            # Trigger random event
            self.trigger_random_event(area)
    
    def trigger_random_event(self, area):
        event_type = random.choice(["item", "hint", "rest"])
        
        if event_type == "item":
            # Random item event
            item = random.choice(ITEMS)
            self.scene_manager.add_item(item["name"])
            
            event_text = [
                f"{area}を探索していると、キラリと光るものが目に入った。",
                f"{item['name']}を見つけた！",
                f"「{item['description']}」"
            ]
            
            self.scene_manager.change_scene(EventScene(self.scene_manager, "アイテム発見！", event_text))
        
        elif event_type == "hint":
            # Random hint event
            guardian = random.choice(AWS_GUARDIANS)
            
            event_text = [
                f"{area}で休憩していると、通りがかりの旅人から情報を聞いた。",
                f"「{guardian['name']}は{guardian['service']}の力を使うらしい。」",
                f"「{guardian['weakness']}が弱点だと噂されているよ。」"
            ]
            
            self.scene_manager.change_scene(EventScene(self.scene_manager, "情報入手！", event_text))
        
        else:  # rest
            # Rest event to recover stats
            self.scene_manager.update_player_stat("motivation", 20)
            self.scene_manager.update_player_stat("concentration", 20)
            
            event_text = [
                f"{area}の美しい景色に癒やされた。",
                "少し休憩することで、やる気と集中力が回復した！",
                "冒険を続ける準備が整った。"
            ]
            
            self.scene_manager.change_scene(EventScene(self.scene_manager, "休憩", event_text))
    
    def show_inventory(self):
        self.showing_inventory = True
