#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Battle Scene - Handles battles with AWS Guardians
"""

import pygame
import random
from src.scenes.base_scene import BaseScene
from src.scenes.battle_result_scene import BattleResultScene
from src.ui.button import Button
from src.ui.text_input import TextInput
from src.ui.status_bar import StatusBar
from src.utils.constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, GREEN, BLUE, LIGHT_BLUE,
    SKILLS
)

class BattleScene(BaseScene):
    def __init__(self, scene_manager, guardian):
        super().__init__(scene_manager)
        
        self.guardian = guardian
        self.guardian_hp = guardian["hp"]
        self.max_guardian_hp = guardian["hp"]
        
        # Battle state
        self.battle_state = "intro"  # intro, player_turn, guardian_turn, command_input, result
        self.selected_action = None
        self.battle_message = f"{guardian['name']}が現れた！"
        self.command_input_active = False
        self.entered_command = ""
        
        # Animation timers
        self.animation_timer = 0
        self.animation_delay = 2000  # milliseconds
        
        # Load fonts
        try:
            self.title_font = pygame.font.Font('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 36)
            self.text_font = pygame.font.Font('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 24)
            self.message_font = pygame.font.Font('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 20)
        except:
            # フォールバックとしてSysFontを使用
            self.title_font = pygame.font.SysFont('Arial', 36, bold=True)
            self.text_font = pygame.font.SysFont('Arial', 24)
            self.message_font = pygame.font.SysFont('Arial', 20)
        
        # Create action buttons
        button_width = 150
        button_height = 50
        button_spacing = 20
        total_width = (button_width * 3) + (button_spacing * 2)
        start_x = (SCREEN_WIDTH - total_width) // 2
        button_y = SCREEN_HEIGHT - 100
        
        self.attack_button = Button(
            start_x,
            button_y,
            button_width,
            button_height,
            "攻撃",
            BLUE,
            LIGHT_BLUE,
            action=lambda: self.select_action("attack")
        )
        
        self.item_button = Button(
            start_x + button_width + button_spacing,
            button_y,
            button_width,
            button_height,
            "アイテム",
            BLUE,
            LIGHT_BLUE,
            action=lambda: self.select_action("item")
        )
        
        self.run_button = Button(
            start_x + (button_width + button_spacing) * 2,
            button_y,
            button_width,
            button_height,
            "逃げる",
            BLUE,
            LIGHT_BLUE,
            action=lambda: self.select_action("run")
        )
        
        # Create skill buttons (shown when attack is selected)
        self.skill_buttons = []
        skill_button_y = button_y - button_height - 10
        
        player_skills = self.scene_manager.get_player_data()["skills"]
        for i, skill_name in enumerate(player_skills):
            if i < 3:  # Limit to 3 skills per row
                skill_button = Button(
                    start_x + (button_width + button_spacing) * i,
                    skill_button_y,
                    button_width,
                    button_height,
                    skill_name,
                    GREEN,
                    (100, 255, 100),
                    action=lambda s=skill_name: self.select_skill(s)
                )
                self.skill_buttons.append(skill_button)
        
        # Create command input (shown when a skill is selected)
        self.command_input = TextInput(
            SCREEN_WIDTH // 4,
            SCREEN_HEIGHT - 150,
            SCREEN_WIDTH // 2,
            40,
            max_length=50,
            placeholder="AWSコマンドを入力..."
        )
        
        # Create item buttons (shown when item is selected)
        self.item_buttons = []
        item_button_y = button_y - button_height - 10
        
        player_items = self.scene_manager.get_player_data()["items"]
        for i, item_name in enumerate(player_items):
            if i < 3:  # Limit to 3 items per row
                item_button = Button(
                    start_x + (button_width + button_spacing) * i,
                    item_button_y,
                    button_width,
                    button_height,
                    item_name,
                    (255, 200, 0),
                    (255, 255, 0),
                    action=lambda item=item_name: self.use_item(item)
                )
                self.item_buttons.append(item_button)
        
        # Create back button (shown when in submenu)
        self.back_button = Button(
            start_x + (button_width + button_spacing) * 2,
            skill_button_y - button_height - 10,
            button_width,
            button_height,
            "戻る",
            RED,
            (255, 100, 100),
            action=self.go_back
        )
        
        # Create submit button (shown when command input is active)
        self.submit_button = Button(
            SCREEN_WIDTH // 2 - button_width // 2,
            SCREEN_HEIGHT - 100,
            button_width,
            button_height,
            "実行",
            GREEN,
            (100, 255, 100),
            action=self.submit_command
        )
        
        # Create status bars
        self.guardian_hp_bar = StatusBar(
            SCREEN_WIDTH // 2 - 100,
            100,
            200,
            20,
            "",
            self.guardian_hp,
            self.max_guardian_hp,
            RED
        )
        
        player_data = self.scene_manager.get_player_data()
        self.player_motivation_bar = StatusBar(
            20, 20, 200, 20, 
            "やる気", 
            player_data["motivation"], 
            100,
            (255, 100, 100)
        )
        
        self.player_concentration_bar = StatusBar(
            20, 50, 200, 20, 
            "集中力", 
            player_data["concentration"], 
            100,
            (100, 255, 100)
        )
        
        # Try to load background and guardian images
        try:
            self.background = pygame.image.load(f"src/assets/images/battle_{guardian['name'].lower()}_bg.png")
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.background = None
        
        try:
            self.guardian_image = pygame.image.load(f"src/assets/images/{guardian['name'].lower()}.png")
            # Scale guardian image to reasonable size
            max_size = min(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2)
            width, height = self.guardian_image.get_size()
            scale = min(max_size / width, max_size / height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            self.guardian_image = pygame.transform.scale(self.guardian_image, (new_width, new_height))
            self.guardian_image_rect = self.guardian_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        except:
            self.guardian_image = None
    
    def handle_event(self, event):
        if self.battle_state == "intro":
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                self.battle_state = "player_turn"
                self.battle_message = "どうする？"
        
        elif self.battle_state == "player_turn":
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check button clicks
                self.attack_button.check_click(event.pos)
                self.item_button.check_click(event.pos)
                self.run_button.check_click(event.pos)
        
        elif self.battle_state == "skill_select":
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check skill button clicks
                for button in self.skill_buttons:
                    button.check_click(event.pos)
                
                # Check back button click
                self.back_button.check_click(event.pos)
        
        elif self.battle_state == "item_select":
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check item button clicks
                for button in self.item_buttons:
                    button.check_click(event.pos)
                
                # Check back button click
                self.back_button.check_click(event.pos)
        
        elif self.battle_state == "command_input":
            # Handle command input events
            self.command_input.handle_event(event)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check submit button click
                self.submit_button.check_click(event.pos)
                
                # Check back button click
                self.back_button.check_click(event.pos)
            
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Submit on enter key
                self.submit_command()
        
        elif self.battle_state == "guardian_turn":
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                # Process guardian's attack and go back to player turn
                self.process_guardian_attack()
        
        elif self.battle_state == "result":
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                # Show battle result scene
                self.show_result()
    
    def update(self):
        # Update status bars
        player_data = self.scene_manager.get_player_data()
        self.player_motivation_bar.update_value(player_data["motivation"])
        self.player_concentration_bar.update_value(player_data["concentration"])
        self.guardian_hp_bar.update_value(self.guardian_hp)
        
        # Update command input if active
        if self.battle_state == "command_input":
            self.command_input.update()
        
        # Handle animation timers
        if self.battle_state in ["guardian_turn", "result"]:
            now = pygame.time.get_ticks()
            if now - self.animation_timer > self.animation_delay:
                if self.battle_state == "guardian_turn":
                    self.battle_state = "player_turn"
                    self.battle_message = "どうする？"
                elif self.battle_state == "result":
                    self.show_result()
    
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
        
        # Draw guardian
        if self.guardian_image:
            screen.blit(self.guardian_image, self.guardian_image_rect)
        else:
            # Fallback guardian representation
            pygame.draw.circle(screen, RED, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50), 50)
            guardian_name = self.text_font.render(self.guardian["name"], True, WHITE)
            guardian_name_rect = guardian_name.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(guardian_name, guardian_name_rect)
        
        # Draw guardian name and HP bar
        guardian_name = self.title_font.render(self.guardian["name"], True, WHITE)
        guardian_name_rect = guardian_name.get_rect(center=(SCREEN_WIDTH // 2, 70))
        screen.blit(guardian_name, guardian_name_rect)
        self.guardian_hp_bar.draw(screen)
        
        # Draw player status bars
        self.player_motivation_bar.draw(screen)
        self.player_concentration_bar.draw(screen)
        
        # Draw player name and level
        player_data = self.scene_manager.get_player_data()
        player_text = self.text_font.render(f"{player_data['name']} Lv.{player_data['level']}", True, WHITE)
        player_rect = player_text.get_rect(topleft=(20, 80))
        screen.blit(player_text, player_rect)
        
        # Draw battle message box
        message_box = pygame.Rect(50, SCREEN_HEIGHT - 200, SCREEN_WIDTH - 100, 80)
        pygame.draw.rect(screen, (0, 0, 0, 180), message_box, border_radius=10)
        pygame.draw.rect(screen, WHITE, message_box, 2, border_radius=10)
        
        # Draw battle message
        message_text = self.message_font.render(self.battle_message, True, WHITE)
        message_rect = message_text.get_rect(center=message_box.center)
        screen.blit(message_text, message_rect)
        
        # Draw UI based on battle state
        if self.battle_state == "player_turn":
            self.attack_button.draw(screen)
            self.item_button.draw(screen)
            self.run_button.draw(screen)
        
        elif self.battle_state == "skill_select":
            for button in self.skill_buttons:
                button.draw(screen)
            self.back_button.draw(screen)
        
        elif self.battle_state == "item_select":
            for button in self.item_buttons:
                button.draw(screen)
            self.back_button.draw(screen)
        
        elif self.battle_state == "command_input":
            self.command_input.draw(screen)
            self.submit_button.draw(screen)
            self.back_button.draw(screen)
    
    def select_action(self, action):
        if action == "attack":
            # Show skill selection
            self.battle_state = "skill_select"
            self.battle_message = "どのスキルを使う？"
            
            # Update skill buttons with current skills
            self.skill_buttons = []
            button_width = 150
            button_height = 50
            button_spacing = 20
            total_width = (button_width * 3) + (button_spacing * 2)
            start_x = (SCREEN_WIDTH - total_width) // 2
            button_y = SCREEN_HEIGHT - 160
            
            player_skills = self.scene_manager.get_player_data()["skills"]
            for i, skill_name in enumerate(player_skills):
                if i < 3:  # Limit to 3 skills per row
                    skill_button = Button(
                        start_x + (button_width + button_spacing) * i,
                        button_y,
                        button_width,
                        button_height,
                        skill_name,
                        GREEN,
                        (100, 255, 100),
                        action=lambda s=skill_name: self.select_skill(s)
                    )
                    self.skill_buttons.append(skill_button)
        
        elif action == "item":
            # Show item selection
            self.battle_state = "item_select"
            self.battle_message = "どのアイテムを使う？"
            
            # Update item buttons with current items
            self.item_buttons = []
            button_width = 150
            button_height = 50
            button_spacing = 20
            total_width = (button_width * 3) + (button_spacing * 2)
            start_x = (SCREEN_WIDTH - total_width) // 2
            button_y = SCREEN_HEIGHT - 160
            
            player_items = self.scene_manager.get_player_data()["items"]
            for i, item_name in enumerate(player_items):
                if i < 3:  # Limit to 3 items per row
                    item_button = Button(
                        start_x + (button_width + button_spacing) * i,
                        button_y,
                        button_width,
                        button_height,
                        item_name,
                        (255, 200, 0),
                        (255, 255, 0),
                        action=lambda item=item_name: self.use_item(item)
                    )
                    self.item_buttons.append(item_button)
            
            if not player_items:
                self.battle_message = "アイテムを持っていません"
                self.battle_state = "player_turn"
        
        elif action == "run":
            # Try to run away
            success = random.random() < 0.5
            
            if success:
                self.battle_message = "うまく逃げ出した！"
                self.battle_state = "result"
                self.animation_timer = pygame.time.get_ticks()
            else:
                self.battle_message = "逃げられなかった！"
                self.battle_state = "guardian_turn"
                self.animation_timer = pygame.time.get_ticks()
    
    def select_skill(self, skill_name):
        self.selected_action = skill_name
        
        # Find skill details
        skill_details = next((s for s in SKILLS if s["name"] == skill_name), None)
        
        if skill_details:
            # Show command input for this skill
            self.battle_state = "command_input"
            self.battle_message = f"{skill_name}を使用します。AWSコマンドを入力してください。"
            self.command_input.text = ""  # Clear any previous input
        else:
            # Fallback if skill not found
            self.battle_message = "そのスキルは使えません"
            self.battle_state = "player_turn"
    
    def submit_command(self):
        command = self.command_input.get_text().strip()
        
        if not command:
            return
        
        # Find skill details
        skill_details = next((s for s in SKILLS if s["name"] == self.selected_action), None)
        
        if not skill_details:
            self.battle_state = "player_turn"
            return
        
        # Calculate damage based on skill power and player level
        base_damage = skill_details["power"]
        player_level = self.scene_manager.get_player_data()["level"]
        damage = base_damage * (1 + (player_level - 1) * 0.2)
        
        # Check if command contains keywords related to guardian's weakness
        if self.guardian["weakness"].lower() in command.lower():
            damage *= 2
            critical_hit = True
        else:
            critical_hit = random.random() < 0.2
            if critical_hit:
                damage *= 1.5
        
        # Apply damage
        damage = int(damage)
        self.guardian_hp -= damage
        
        # Update battle message
        if critical_hit:
            self.battle_message = f"クリティカルヒット！{self.guardian['name']}に{damage}のダメージ！"
        else:
            self.battle_message = f"{self.guardian['name']}に{damage}のダメージ！"
        
        # Check if guardian is defeated
        if self.guardian_hp <= 0:
            self.guardian_hp = 0
            self.battle_message = f"{self.guardian['name']}を倒した！"
            self.battle_state = "result"
            self.animation_timer = pygame.time.get_ticks()
            
            # Mark trial as completed
            self.scene_manager.complete_trial(self.guardian["name"])
            
            # Award AWS knowledge
            self.scene_manager.update_player_stat("aws_knowledge", 50)
        else:
            # Guardian's turn
            self.battle_state = "guardian_turn"
            self.animation_timer = pygame.time.get_ticks()
    
    def use_item(self, item_name):
        from src.utils.constants import ITEMS
        
        # Find item details
        item_details = next((item for item in ITEMS if item["name"] == item_name), None)
        
        if not item_details:
            self.battle_message = "そのアイテムは使えません"
            self.battle_state = "player_turn"
            return
        
        # Apply item effects
        for stat, value in item_details["effect"].items():
            if stat == "damage_reduction":
                # Special case for damage reduction items
                self.battle_message = f"{item_name}を使った！次の攻撃のダメージが半減する！"
            else:
                # Apply stat changes
                self.scene_manager.update_player_stat(stat, value)
                self.battle_message = f"{item_name}を使った！{stat}が{value}回復した！"
        
        # Remove item from inventory
        self.scene_manager.remove_item(item_name)
        
        # Guardian's turn
        self.battle_state = "guardian_turn"
        self.animation_timer = pygame.time.get_ticks()
    
    def process_guardian_attack(self):
        # Select random attack pattern
        attack = random.choice(self.guardian["attack_patterns"])
        
        # Calculate damage
        base_damage = random.randint(10, 20)
        
        # Apply damage to player stats
        self.scene_manager.update_player_stat("motivation", -base_damage)
        self.scene_manager.update_player_stat("concentration", -base_damage // 2)
        
        # Update battle message
        self.battle_message = f"{self.guardian['name']}の{attack}！やる気が{base_damage}減少した！"
        
        # Check if player is defeated
        if self.scene_manager.is_game_over():
            self.battle_message = "やる気がなくなってしまった..."
            self.battle_state = "result"
            self.animation_timer = pygame.time.get_ticks()
        else:
            # Back to player turn
            self.battle_state = "player_turn"
    
    def go_back(self):
        # Return to player turn from any submenu
        self.battle_state = "player_turn"
        self.battle_message = "どうする？"
    
    def show_result(self):
        # Determine battle result
        if self.guardian_hp <= 0:
            result = "victory"
        elif self.scene_manager.is_game_over():
            result = "defeat"
        else:
            result = "escape"
        
        # Show battle result scene
        self.scene_manager.change_scene(
            BattleResultScene(self.scene_manager, self.guardian, result)
        )
