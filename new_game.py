import pygame as pg
from settings import *
from sprites import *
import random

class Game:

	def __init__(self):  # Initialize game window, etc
		self.running = True
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
		self.font = pg.font.Font(os.path.join(fonts_folder, "flappy-font.ttf"), 40)
	

	def new(self):  # Start a new game
		self.groups()
		self.timers()
		self.background = Background(self.spritesheet)
		self.base = Base(self.all_sprites, self.spritesheet)
		self.bird = Bird(self.all_sprites, self.spritesheet, self.get_dt)
		self.run()
	
	def timers(self):
		self.pipe_timer = pg.event.custom_type()
		pg.time.set_timer(self.pipe_timer, 2000)

	def groups(self):
		self.all_sprites = pg.sprite.Group()
		self.pipe_grp = pg.sprite.Group()
	
	def get_dt(self):
		return self.dt

	def run(self):  # Game loop
		self.playing = True
		while self.playing:
			# Keep loop running at the right speed
			self.dt = self.clock.tick(FPS)/1000
			self.events()
			self.check_collisions()
			self.update()
			self.draw()

	def update(self):  # Game loop - update
		self.all_sprites.update()
		self.pipe_grp.update()

	def events(self):  # Game loop - events
		# Process input (events)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.playing = False
				self.running = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_SPACE:
					self.bird.jump()
			if event.type == self.pipe_timer:
				height = random.randint(-150, 100)
				self.pipe = Pipe(self.pipe_grp, self.spritesheet, 1, WIDTH, HEIGHT/2 + height, self.get_dt)
				self.pipe = Pipe(self.pipe_grp, self.spritesheet, -1, WIDTH, HEIGHT/2 + height, self.get_dt)
				if not self.bird.is_jump:
					self.score += 1


	def check_collisions(self):
		self.bird_base_collision()
		self.bird_pipes_collision()
	

	def bird_base_collision(self):
		if self.bird.rect.colliderect(self.base):
			self.bird.is_gravity = False
			self.bird.is_animate = False
			self.bird.is_rotate = False

	def bird_pipes_collision(self):
		if pg.sprite.spritecollide(self.bird, self.pipe_grp, False, pg.sprite.collide_mask):
			self.bird.is_jump = False
			self.bird.is_animate = False
			self.bird.is_rotate = False

	def draw(self):  # Game loop - draw
		self.background.draw(self.screen)
		self.pipe_grp.draw(self.screen)
		self.all_sprites.draw(self.screen)
		self.display_txt(f"{self.score}", (WIDTH/2, 50))
		

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
		pass

	def show_game_over_screen(self):
		pass


g = Game()
g.show_start_screen()

while g.running:
	g.new()
	g.show_game_over_screen()

pg.quit()
