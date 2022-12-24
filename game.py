import pygame as pg
import random
vec = pg.math.Vector2

import os

# Settings
WIDTH = 380
HEIGHT = 560
TITLE = 'My Game'
FPS = 60
DEBUG = False

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Properties
BIRD_VEL = 100
BIRD_ACC = 20
BIRD_JUMP_VEL = 350
BIRD_ROT_SPEED = 60
BIRD_JUMP_ROT = 18

# Folders
game_folder = os.path.dirname(__file__)
assets_folder = os.path.join(game_folder, "assets")
fonts_folder = os.path.join(assets_folder, "fonts")
sprites_folder = os.path.join(assets_folder, "sprites")
sounds_folder = os.path.join(assets_folder, "sounds")

# Sprite Coordinates
class Sprite:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

BG_DAY = Sprite(0, 0, 144, 256)
BG_NIGHT = Sprite(146, 0, 144, 256)
BASE = Sprite(292, 0, 168, 56)
BIRD_1 = Sprite(31, 491, 17, 12)
BIRD_2 = Sprite(59, 491, 17, 12)
BIRD_3 = Sprite(3, 491, 17, 12)
PIPE_TOP = Sprite(56, 323, 26, 160)
GET_READY = Sprite(295, 59, 92, 25)
FLAPPY_BIRD_TEXT = Sprite(351, 91, 89, 24)
GAME_OVER_TEXT = Sprite(395, 59, 96, 21)
LEADERBOARD = Sprite(414, 118, 52, 29)
YELLOW_BIRD = Sprite(31, 491, 17, 12)
PLAY_BTN = Sprite(354, 118, 52, 29)

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
			if self.pos.y <= 0:
				self.pos.y = 0
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


class Game:

	def __init__(self):  # Initialize game window, etc
		self.running = True # pygame state
		pg.init()
		pg.mixer.init()  # For sound or music
		self.screen = pg.display.set_mode((WIDTH, HEIGHT),
				flags=pg.SCALED, vsync=1)
		pg.display.set_caption(TITLE)
		self.icon_surf = pg.image.load(os.path.join(sprites_folder, "icon.png")).convert_alpha()
		pg.display.set_icon(self.icon_surf)
		self.clock = pg.time.Clock()
		self.spritesheet = Spritesheet(os.path.join(sprites_folder, "sprites.png"))
		self.dt = 0
		self.score = 0
		self.font = pg.font.Font(os.path.join(fonts_folder, "flappy-font.ttf"), 30)
		self.background = Background(self.spritesheet, BG_DAY)
		self.background_day = Background(self.spritesheet, BG_DAY)
		self.background_night = Background(self.spritesheet, BG_NIGHT)
		self.groups()
		self.sounds()
	
	def sounds(self):
		self.hit_snd = pg.mixer.Sound(os.path.join(sounds_folder, "hit.wav"))
		self.die_snd = pg.mixer.Sound(os.path.join(sounds_folder, "die.wav"))
		self.point_snd = pg.mixer.Sound(os.path.join(sounds_folder, "point.wav"))
		self.wing_snd = pg.mixer.Sound(os.path.join(sounds_folder, "wing.wav"))
		self.background_music = pg.mixer.Sound(os.path.join(sounds_folder, "happytune.ogg"))
		self.background_music.play(-1)

	def new(self):  # Start a new game
		self.playing = True # Player is playing
		self.hit_pipe = False
		self.hit_base = False
		self.clear()
		self.timers()
		self.base = Base(self.base_grp, self.spritesheet, self.get_dt)
		self.bird = Bird(self.bird_grp, self.spritesheet, self.get_dt)
		self.run()
		
	def clear(self):
		self.score = 0
		self.bird_grp.empty()
		self.base_grp.empty()
		self.pipe_grp.empty()
		self.static_grp.empty()
		self.pipe_timer = None
	
	def timers(self):
		self.pipe_timer = pg.event.custom_type()
		pg.time.set_timer(self.pipe_timer, 2000)

	def groups(self):
		self.static_grp = pg.sprite.Group()
		self.bird_grp = pg.sprite.GroupSingle()
		self.base_grp = pg.sprite.GroupSingle()
		self.pipe_grp = pg.sprite.Group()
	
	def get_dt(self):
		return self.dt

	def run(self):  # Game loop

		while self.playing:
			# Keep loop running at the right speed
			self.dt = self.clock.tick(FPS)/1000
			self.check_collisions()
			self.update()
			self.events()
			self.draw()

	def update(self):  # Game loop - update
		if self.hit_base:
			self.show_game_over_screen()
			return
		self.bird_grp.update()
		self.base_grp.update()
		self.pipe_grp.update()

	def events(self):  # Game loop - events
		# Process input (events)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.running = False
				self.playing = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_SPACE:
					self.bird.jump()
					self.wing_snd.play()
			if event.type == self.pipe_timer and not self.hit_base and not self.hit_pipe:
				height = random.randint(-150, 100)
				self.pipe = Pipe(self.pipe_grp, self.spritesheet, 1, WIDTH, HEIGHT/2 + height, self.get_dt)
				self.pipe = Pipe(self.pipe_grp, self.spritesheet, -1, WIDTH, HEIGHT/2 + height, self.get_dt)
				self.score += 1
				self.point_snd.play()
				if self.score % 10 == 0:
					self.background = self.background_day if self.background == self.background_night else self.background_night
				
			if event.type == pg.KEYDOWN and (self.hit_base or self.hit_pipe):
					if event.key == pg.K_p:
						self.new()
				
 
	def check_collisions(self):
		self.bird_base_collision()
		self.bird_pipes_collision()
	
	def clear_groups(self):
		self.bird_grp.empty()
		self.base_grp.empty()
		self.pipe_grp.empty()
	
	def bird_base_collision(self):
		if not self.hit_base and self.bird.rect.colliderect(self.base):
			self.bird.is_gravity = False
			self.bird.is_animate = False
			self.bird.is_rotate = False
			self.hit_base = True
			if not self.hit_pipe:
				self.hit_snd.play()

	def bird_pipes_collision(self):
		if not self.hit_pipe and pg.sprite.spritecollide(self.bird, self.pipe_grp, False, pg.sprite.collide_mask):
			self.bird.is_jump = False
			self.bird.is_animate = False
			self.bird.is_rotate = False
			self.hit_pipe = True
			if not self.hit_base:
				self.hit_snd.play()


	def draw(self):  # Game loop - draw
		self.background.draw(self.screen)
		self.pipe_grp.draw(self.screen)
		self.bird_grp.draw(self.screen)
		self.base_grp.draw(self.screen)
		self.static_grp.draw(self.screen)
		self.display_txt(f"{self.score}", (WIDTH/2, 50))
		if self.hit_base:
				self.display_txt("Press p to play again", pos=(WIDTH/2, 250))
		if DEBUG:
			pg.draw.rect(self.screen, "red", self.bird.rect, width=1)
			for p in self.pipe_grp:
				pg.draw.rect(self.screen, "blue", p.rect, width=1)

		# *after* drawing everything flip the display
		pg.display.flip()  # or pg.display.update()
	
	def display_txt(self, text, pos):
		text_surf = self.font.render(text, True, WHITE)
		text_rect = text_surf.get_rect(center=pos)
		self.screen.blit(text_surf, text_rect)

	def show_start_screen(self):
		self.static = Static(self.static_grp, self.spritesheet, 1, (WIDTH/2, 150), FLAPPY_BIRD_TEXT)
		self.static = Static(self.static_grp, self.spritesheet, 2, (0, HEIGHT-80), BASE, sprite_name="base")
		self.bird = Bird(self.static_grp, self.spritesheet, self.get_dt, pos=(WIDTH/2, 250), is_static=True)
		self.play_btn = Static(self.static_grp, self.spritesheet, 1, (WIDTH/2, 350), PLAY_BTN)
		self.play_btn_clicked = False
		self.wait_for_key()
		self.static_grp.empty()
	
	def wait_for_key(self):
		waiting = True
		while waiting:
			mouse_pos = pg.mouse.get_pos()
			self.clock.tick(FPS)
		
			self.background.draw(self.screen)
			if self.play_btn.rect.collidepoint(mouse_pos):
				if pg.mouse.get_pressed()[0] and not self.play_btn_clicked:
					waiting = False
					self.playing = True
				
			if self.play_btn_clicked and not pg.mouse.get_pressed()[0]:
				self.play_btn_clicked = False
			self.static_grp.update()
			self.static_grp.draw(self.screen)

			for event in pg.event.get():
				if event.type == pg.QUIT:
					waiting = False
					self.playing = False
					self.running = False
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_p:
						waiting = False
						self.playing = True
			
			pg.display.flip()


	def show_game_over_screen(self):
		if not self.running:
			return
		self.static = Static(self.static_grp, self.spritesheet, 1, (WIDTH/2, 150), GAME_OVER_TEXT)
		# self.wait_for_key()
		


g = Game()
g.show_start_screen()
while g.running:
	g.new()

pg.quit()
