"""
TILESET GENERATOR V1

key bindings*
	r:switch mode:
	g:group selection list:
	z:undo selection:
	s:save seletion list:

"""

import pygame, sys, os, random, math
from pygame.locals import*
pygame.init()

from data.core_functions.clip import*

pygame.display.set_caption("SPRITESHEET GENERATOR")
FPS = pygame.time.Clock()

SCALE = 2
BLACK = (0,0,0,255)

image_path = "./data/images/sketch.png"
SCREEN = pygame.display.set_mode((200,200), 0, 32)

session_image = pygame.image.load(image_path).convert()
SCREEN_DIMENSION = [session_image.get_width()*SCALE,session_image.get_height()*SCALE]
SCREEN = pygame.display.set_mode(SCREEN_DIMENSION, 0, 32)

image = session_image.copy()

click_once = True
group_tileset = False
free_selection_mode = False


initial_point = None
current_selection = None
points = None

selection_list = []
surface_clips = []

def calc_new_dimension(surface_clips):
	clips_width = [clips.get_width() for clips in surface_clips]
	clips_height = [clips.get_height() for clips in surface_clips]
	
	new_width = max(clips_width)
	max_height = 0
	for height in clips_height:
		max_height += height
	
	return [new_width,max_height]

def generate_border(image,initial_point,offset=0):
	surface_copy = image.copy()
	origin = initial_point.copy()

	mapping_direction = [[-1,0,1],[1,0,-2]]
	image_edges = []
	borders = []

	#locating edges
	for direction in mapping_direction:
		while 1:
			pixel_color = surface_copy.get_at(origin)
			
			if pixel_color != BLACK:
				origin[0] += direction[0]
				origin[1] += direction[1]
			else:
				origin[0] = origin[0] + direction[2]
				image_edges.append(origin.copy())
				origin[0] = initial_point[0]
				origin[1] = initial_point[1]
				break
	
	#topleft/bottomleft
	left_edge = image_edges[0].copy()
	for i in [1,-2]:
		while 1:
			pixel_color = surface_copy.get_at(left_edge)

			if pixel_color == BLACK:
				borders.append(pygame.Rect(left_edge[0] - 1,left_edge[1],SCALE,SCALE))
				left_edge = image_edges[0].copy()
				break
			else:
				left_edge[1] = left_edge[1] + i
	
	#topright/bottomright
	right_edge = image_edges[1].copy()
	for i in [1,-2]:
		while 1:
			pixel_color = surface_copy.get_at(right_edge)

			if pixel_color == BLACK:
				borders.append(pygame.Rect(right_edge[0] + 1,right_edge[1],SCALE,SCALE))
				right_edge = image_edges[1].copy()
				break
			else:
				right_edge[1] = right_edge[1] + i
	
	#calculating dimentions
	x = borders[0].x
	y = min([borders[1].y,borders[3].y]) 
	width = abs(borders[1].topleft[0] - borders[3].topright[0])
	height = abs(max([borders[0].bottomleft[1],borders[2].bottomright[1]]) - y)

	return pygame.Rect(x,y,width,height),borders

while 1:
	# mouse fucntions
	if group_tileset == False:
		image.fill((0,0,0))
		image.blit(session_image,(0,0))

	mx, my = pygame.mouse.get_pos()
	mx = mx//SCALE
	my = my//SCALE

	mouse_clicked = pygame.mouse.get_pressed()
	keys = pygame.key.get_pressed()

	if free_selection_mode == False:
		#auto-select rectangular sprite
		if mouse_clicked[0] and click_once:
			click_once = False
			border,points = generate_border(image,[mx,my])
			selection_list.append(border)
		
		#locating points
		# if points:
		# 	for data in points:
		# 		pygame.draw.rect(image, (255,0,0), data)
		
	else:
		#rectangular selector
		if mouse_clicked[0] and pygame.MOUSEMOTION:
			if click_once:
				click_once = False
				initial_point = [mx,my]

			scale_width = mx-initial_point[0]
			scale_height = my-initial_point[1]
			current_selection = pygame.Rect(initial_point[0],initial_point[1],scale_width,scale_height)
			pygame.draw.rect(image, (255,0,0), current_selection, 1)

	if selection_list and group_tileset == False:
		for selection in selection_list:
			pygame.draw.rect(image, (0,255,0), selection, 1)

	if keys[K_r] and click_once:
		click_once = False
		free_selection_mode = not free_selection_mode

	if keys[K_z] and click_once:
		click_once = False
		selection_list = selection_list[:-1]

	if keys[K_g] and click_once:
		click_once = False
		group_tileset = True
		surface_clips = [clip_surface(image,selection) for selection in selection_list]
		new_dimension = calc_new_dimension(surface_clips)
		SCREEN = pygame.display.set_mode((new_dimension[0]*SCALE,new_dimension[1]*SCALE),0,32)
		group_surface = pygame.Surface(new_dimension)
		image.fill((0,0,0))
		current_y_position = 0
		for clips in surface_clips:
			clips.set_colorkey((0,255,0))
			current_surface = group_surface.blit(clips,(0,current_y_position))
			current_y_position = current_surface.bottom
		image.blit(group_surface,(0,0))

	if keys[K_s] and click_once:
		click_once = False
		new_filename = input("[ENTER FILENAME] : ")
		pygame.image.save(group_surface, f"./data/images/{new_filename}.png")
		print("[TILESET SAVED!]")

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.MOUSEBUTTONUP:
			click_once = True
			if free_selection_mode:
				selection_list.append(current_selection)

		if event.type == pygame.KEYUP:
			click_once = True

	SCREEN.blit(pygame.transform.scale(image,SCREEN_DIMENSION),(0,0))
	FPS.tick(100)
	pygame.display.update()


