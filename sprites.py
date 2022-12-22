# Sprite classes
import pygame as pg
from settings import *

vec = pg.math.Vector2

class Spritesheet:
	def __init__(self, filename):
		self.spritesheet = pg.image.load(filename).convert_alpha()
	
	def get_image(self, x, y, width, height):
		image = pg.Surface((width, height))
		image.set_colorkey(BLACK)
		image.blit(self.spritesheet, (0, 0), (x, y, width, height))
		return image

class Background():
	def __init__(self, spritesheet, BG):
		self.image = spritesheet.get_image(BG.x, BG.y, BG.width, BG.height)
		self.image = pg.transform.scale(self.image, (WIDTH, HEIGHT))
		self.rect = self.image.get_rect(topleft=(0, 0))
	
	def draw(self, screen):
		screen.blit(self.image, self.rect)

class Base(pg.sprite.Sprite):
	def __init__(self, group, spritesheet, get_dt):
		super().__init__(group)
		self.image = spritesheet.get_image(BASE.x, BASE.y, BASE.width, BASE.height)
		self.image = pg.transform.scale(self.image, (WIDTH*2, 80))
		self.rect = self.image.get_rect()
		self.rect.left = 0
		self.rect.bottom = HEIGHT
		self.pos = vec(0, 0)
		self.dir = vec(-1, 0)
		self.speed = 100
		self.get_dt = get_dt
		self.mask = pg.mask.from_surface(self.image)
	
	def update(self):
		self.pos += self.dir * self.speed * self.get_dt()
		self.rect.x = round(self.pos.x)
		if self.rect.x < -WIDTH:
			self.pos.x = 0
		
		self.mask = pg.mask.from_surface(self.image)
	
class Bird(pg.sprite.Sprite):
	def __init__(self, group, spritesheet, get_dt, pos=(100, HEIGHT/3), is_static=False):
		super().__init__(group)
		self.image = spritesheet.get_image(BIRD_1.x, BIRD_1.y, BIRD_1.width, BIRD_1.height)
		self.image = pg.transform.scale2x(self.image)
		self.rect = self.image.get_rect(center=pos)

		# For bird movement
		self.is_gravity = True
		self.is_jump = True
		self.pos = vec(self.rect.topleft)
		self.direction = vec(0, 1)
		self.vel = BIRD_VEL
		self.acc = BIRD_ACC
		self.get_dt = get_dt
		self.is_static = is_static


		# For flap animation
		self.is_animate = True
		self.frame = 0
		self.images = [
			spritesheet.get_image(BIRD_1.x, BIRD_1.y, BIRD_1.width, BIRD_1.height),
			spritesheet.get_image(BIRD_2.x, BIRD_2.y, BIRD_2.width, BIRD_2.height),
			spritesheet.get_image(BIRD_3.x, BIRD_3.y, BIRD_3.width, BIRD_3.height)
		]

		# For rotate animation
		self.is_rotate = True
		self.rot_speed = BIRD_ROT_SPEED
		self.rotation = 0
		self.mask = pg.mask.from_surface(self.image)

	def update(self):
		if self.is_static:
			return
		self.mask = pg.mask.from_surface(self.image)
		if self.is_gravity:
			self.vel += self.acc
			self.pos += self.direction * self.vel * self.get_dt()
			self.rect.y = round(self.pos.y)
		self.animations()
		
	
	def animations(self):
		self.flap_animation()
		self.rotate_animation()
		
	def jump(self):
		if not self.is_jump:
			return
		self.vel = -BIRD_JUMP_VEL
		self.rotation = BIRD_JUMP_ROT
	
	def flap_animation(self):
		if not self.is_animate:
			return
		self.frame += 0.1
		self.frame_int = int(self.frame)
		if self.frame_int >= len(self.images):
			self.frame = 0
			self.frame_int = 0
		self.old_rect = self.rect
		self.image = pg.transform.scale2x(self.images[self.frame_int])
		self.rect = self.image.get_rect(center=self.old_rect.center)
		

	def rotate_animation(self):
		if not self.is_rotate:
			return
		self.rotation -= (self.rot_speed * self.get_dt()) % 360
		self.old_rect = self.rect
		self.image = pg.transform.rotate(self.image, self.rotation)
		self.rect = self.image.get_rect(center=self.old_rect.center)

class Pipe(pg.sprite.Sprite):
	def __init__(self, group, spritesheet, position, x, y, get_dt):
		super().__init__(group)
		self.gap = 150
		self.image = spritesheet.get_image(PIPE_TOP.x, PIPE_TOP.y, PIPE_TOP.width, PIPE_TOP.height)
		self.image = pg.transform.scale2x(self.image)
		self.rect = self.image.get_rect()
		self.get_dt = get_dt
		self.position = position

		# Pipe Top = 1, Pipe Bottom = -1
		if position == -1:
			self.image = pg.transform.flip(self.image, False, True)
			self.rect.topleft = [x, y + int(self.gap/2)]
		else:
			self.rect.bottomleft = [x, y - int(self.gap/2)]
		
		self.pos = vec(self.rect.topleft)
		self.direction = vec(-1, 0)
		self.vel = 100
		self.mask = pg.mask.from_surface(self.image)

	def update(self):
		self.pos += self.direction *self.vel * self.get_dt()
		self.rect.x = round(self.pos.x)
		if self.rect.right < 0:
			self.kill()
	


class Static(pg.sprite.Sprite):
	def __init__(self, group, spritesheet, pos_type, pos, sprite, sprite_name=""):
		super().__init__(group)
		self.image = spritesheet.get_image(sprite.x, sprite.y, sprite.width, sprite.height)
		if sprite_name == "":
			self.image = pg.transform.scale2x(self.image)
		else:
			self.image = pg.transform.scale(self.image, (WIDTH*2, 80))
		if pos_type == 1:
			self.rect = self.image.get_rect(center=pos)
		if pos_type == 2:
			self.rect = self.image.get_rect(topleft=pos)
