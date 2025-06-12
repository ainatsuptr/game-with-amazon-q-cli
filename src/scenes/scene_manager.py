#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Scene Manager for handling different game scenes
"""

class SceneManager:
    def __init__(self):
        self.current_scene = None
        self.player_data = {
            "name": "",
            "motivation": 100,
            "aws_knowledge": 0,
            "concentration": 100,
            "level": 1,
            "items": [],
            "skills": ["基本コマンド"],
            "completed_trials": [],
        }
    
    def change_scene(self, scene):
        """Change to a new scene"""
        self.current_scene = scene
    
    def handle_event(self, event):
        """Pass events to the current scene"""
        if self.current_scene:
            self.current_scene.handle_event(event)
    
    def update(self):
        """Update the current scene"""
        if self.current_scene:
            self.current_scene.update()
    
    def draw(self, screen):
        """Draw the current scene"""
        if self.current_scene:
            self.current_scene.draw(screen)
    
    def get_player_data(self):
        """Get the player data"""
        return self.player_data
    
    def set_player_name(self, name):
        """Set the player name"""
        self.player_data["name"] = name
    
    def update_player_stat(self, stat, value):
        """Update a player stat"""
        if stat in self.player_data:
            self.player_data[stat] += value
            
            # Ensure stats don't go below 0
            if self.player_data[stat] < 0:
                self.player_data[stat] = 0
                
            # Check for level up based on AWS knowledge
            if stat == "aws_knowledge":
                new_level = 1 + (self.player_data["aws_knowledge"] // 100)
                if new_level > self.player_data["level"]:
                    self.player_data["level"] = new_level
                    return True  # Indicates level up
        
        return False
    
    def add_item(self, item_name):
        """Add an item to the player's inventory"""
        self.player_data["items"].append(item_name)
    
    def remove_item(self, item_name):
        """Remove an item from the player's inventory"""
        if item_name in self.player_data["items"]:
            self.player_data["items"].remove(item_name)
            return True
        return False
    
    def add_skill(self, skill_name):
        """Add a skill to the player's skills"""
        if skill_name not in self.player_data["skills"]:
            self.player_data["skills"].append(skill_name)
    
    def complete_trial(self, guardian_name):
        """Mark a trial as completed"""
        if guardian_name not in self.player_data["completed_trials"]:
            self.player_data["completed_trials"].append(guardian_name)
    
    def is_game_over(self):
        """Check if the game is over (motivation = 0)"""
        return self.player_data["motivation"] <= 0
    
    def is_game_completed(self):
        """Check if all trials are completed"""
        from src.utils.constants import AWS_GUARDIANS
        all_guardians = [guardian["name"] for guardian in AWS_GUARDIANS]
        return all(guardian in self.player_data["completed_trials"] for guardian in all_guardians)
