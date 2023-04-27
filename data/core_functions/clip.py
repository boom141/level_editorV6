import pygame

def clip_surface(surface,rect):
	surface_copy = surface.copy()
	rect_copy = rect.copy()       
	surface_copy.set_clip(rect_copy)
	new_surface = surface.subsurface(surface_copy.get_clip())

	return new_surface.copy()
