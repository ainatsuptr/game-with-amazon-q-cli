#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Base Scene class that all game scenes inherit from
"""

class BaseScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
    
    def handle_event(self, event):
        """Handle pygame events"""
        pass
    
    def update(self):
        """Update scene logic"""
        pass
    
    def draw(self, screen):
        """Draw scene elements"""
        pass
