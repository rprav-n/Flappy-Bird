import pygame as pg
from settings import *
from sprites import *
import random

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

			if event.type == pg.KEYDOWN:
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
