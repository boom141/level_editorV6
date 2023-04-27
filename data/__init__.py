import pygame, sys, os, random, time, json
from pygame.locals import*
pygame.init()

pygame.display.set_caption("LEVEL EDITOR V6")
DIMENSIONS = (800,500)
SCREEN = pygame.display.set_mode(DIMENSIONS, 0, 32)

FPS = pygame.time.Clock()

def draw_text(surface,position=(0,0),font=None,font_size=15,font_color=(255,255,255),text='hello world!'):
    font = pygame.font.Font("./fonts/"+font,font_size)
    message = font.render(text,False,font_color)
    return surface.blit(message,position)
