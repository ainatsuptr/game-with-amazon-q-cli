#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Amazon Forest Quest: The Treasure and Seven AWS Guardians
A Pygame RPG game about AWS services
"""

import pygame
import sys
import os
from src.scenes.scene_manager import SceneManager
from src.scenes.title_scene import TitleScene
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE

def main():
    # Initialize pygame
    pygame.init()
    
    # Try to initialize audio, but continue if it fails
    try:
        pygame.mixer.init()
    except pygame.error:
        print("Warning: Audio initialization failed. Game will run without sound.")
    
    pygame.font.init()
    
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    
    # Set up the clock for a decent framerate
    clock = pygame.time.Clock()
    
    # Initialize scene manager with title scene
    scene_manager = SceneManager()
    scene_manager.change_scene(TitleScene(scene_manager))
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Pass events to current scene
            scene_manager.handle_event(event)
        
        # Update current scene
        scene_manager.update()
        
        # Clear the screen
        screen.fill((0, 0, 0))
        
        # Draw current scene
        scene_manager.draw(screen)
        
        # Update the display
        pygame.display.flip()
        
        # Cap the framerate
        clock.tick(FPS)
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
