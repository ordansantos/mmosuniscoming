
import pygame

import Person
import Sound

class Character:
	
	# attack_keys
	NO_ATTACK = 0
	SLASH = pygame.K_SPACE
	REBUKE = pygame.K_e
	
	def __init__(self, (x, y), path_image, death_blood):
		# essential
		self.setPosition((x, y))
		self.initial_position = (x, y)
		self.id = 0
		self.name = 'Example'
		self.life = 100
		# speed
		self.px = 1
		self.fast = False
		# sprites
		self.sprites = self.readSprites(path_image)
		self.blood_bar = pygame.image.load(file('../characters/img/blood_bar.png')).convert()
		self.death_blood = pygame.image.load(file(death_blood)).convert_alpha()
		self.blood_squirt = pygame.image.load(file('../characters/img/blood_squirt.png')).convert_alpha()
		# sprites control
		self.interval = 100
		self.cycletime = 0
		self.picnr = [3, 0]  # picture on right
		self.lenPic = 9
		self.squirt_time = 0
		# movement control
		self.side = 'right'
		self.movement = False
		# attack control
		self.attack_keys = {
			Character.SLASH: False,
			Character.REBUKE: False
		}
		self.attack_key = Character.NO_ATTACK
		self.attacked = False
		self.enemy = None
		
	# utilities for the id
	def setId(self, p_id):
		self.id = p_id
	
	def getId(self):
		return self.id
	
	# utilities for the position
	def toPosition(self, x, y):	
		self.x = x
		self.y = y
	
	def getPosition(self):
		return (self.x, self.y)
	
	def getInitialPosition(self):
		return self.initial_position
	
	def setPosition(self, (x, y)):
		self.x = x
		self.y = y
	
	def getEnemy(self):
		return self.enemy
	
	def setEnemy(self, enemy):
		self.enemy = enemy
		
	# images handle
	def readSprites(self, path):
		# one full day to do this function
		spritesheet = pygame.image.load(file(path))
		spritesheet.convert()
		sprites = []
		
		# walk
		for x in xrange(4):
			sprites.append([])
			for y in xrange(9):
				sprites[x].append((spritesheet.subsurface((y * 64, (x + 8) * 64, 64, 64))))
		
		# slash
		for x in xrange(4):
			sprites.append([])
			for y in xrange(6):
				sprites[x + 4].append((spritesheet.subsurface((y * 64, (x + 12) * 64, 64, 64))))
		
		# rebuke
		for x in xrange(4):
			sprites.append([])
			for y in xrange(7):
				sprites[x + 8].append((spritesheet.subsurface((y * 64, x * 64, 64, 64))))
		
		# dying
		sprites.append([])
		for y in xrange(6):
			sprites[12].append((spritesheet.subsurface((y * 64, 20 * 64, 64, 64))))
		
		return sprites
	
	def getImage(self):
		x, y = self.picnr
		if self.movement or self.attack_key != Character.NO_ATTACK or self.life == 0:
			self.updatePicnr()
			if self.updateTime():
				self.picnr[1] += 1
				if self.picnr[1] == self.lenPic:
					if self.picnr[0] == 12:
						self.isDead()
					elif self.life != 0:
						self.updateAttack()
					self.picnr[1] = 0
		return self.sprites[x][y]
	
	def updatePicnr(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			if self.side == 'up':
				self.picnr[0] = 0
			elif self.side == 'left':
				self.picnr[0] = 1
			elif self.side == 'down':
				self.picnr[0] = 2
			elif self.side == 'right':
				self.picnr[0] = 3
	
	def updateTime(self):
		time = pygame.time.get_ticks()
		if time < self.cycletime:
			self.cycletime = 0
		if (time - self.cycletime) >= self.interval:
			self.cycletime = pygame.time.get_ticks()
			return True
		return False
	
	def getLifeBar(self):
		return self.blood_bar.subsurface(32 - int(self.life * 0.32), 0, 32, 3)
	
	def getDeathBlood(self):
		if self.life == 0:
			return self.death_blood
		return None
	
	def getBloodSquirt(self):
		time = pygame.time.get_ticks()
		if time - self.squirt_time >= 1500:
			self.attacked = False
			self.squirt_time = time
		if self.attacked and self.life != 0:
			return self.blood_squirt
		return None
	
	# movement handle
	def doAMovement(self, (x1, y1)):
		x, y = self.getPosition()

		if (x1 > x):
			if (y1 > y):
				self.downRight()
			elif (y1 < y):
				self.upRight()
			else:
				self.right()

		elif (x1 < x):
			if (y1 > y):
				self.downLeft()
			elif (y1 < y):
				self.upLeft()
			else:
				self.left()

		else:
			if (y1 > y):
				self.down()
			elif (y1 < y):
				self.up()
	
	def up(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.side = 'up'
			self.movement = True
			position = Person.Person.changePersonLocation(self, self.x, self.y - self.px);
			self.setPosition(position)
			
	def left(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.side = 'left'
			self.movement = True
			position = Person.Person.changePersonLocation(self, self.x - self.px, self.y)
			self.setPosition(position)
	
	def down(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.side = 'down'
			self.movement = True
			position = Person.Person.changePersonLocation(self, self.x, self.y + self.px);
			self.setPosition(position)
	
	def right(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.side = 'right'
			self.movement = True
			position = Person.Person.changePersonLocation(self, self.x + self.px , self.y);
			self.setPosition(position)
	
	def upLeft(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.side = 'left'
			self.movement = True
			position = Person.Person.changePersonLocation(self, self.x - self.px, self.y - self.px);
			self.setPosition(position)
	
	def upRight(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.side = 'right'
			self.movement = True
			position = Person.Person.changePersonLocation(self, self.x + self.px, self.y - self.px);
			self.setPosition(position)
	
	def downLeft(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.side = 'left'
			self.movement = True
			position = Person.Person.changePersonLocation(self, self.x - self.px, self.y + self.px);
			self.setPosition(position)
	
	def downRight(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.side = 'right'
			self.movement = True
			position = Person.Person.changePersonLocation(self, self.x + self.px, self.y + self.px);
			self.setPosition(position)
	
	def stopped(self):
		self.movement = False
		self.picnr[1] = 0
	
	# attack handle
	def attack(self, key):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.attack_keys[key] = True
			self.attack_key = key
			if key == Character.SLASH:
				Sound.Sound.attackPlay()
				self.slash()
			elif key == Character.REBUKE:
				Sound.Sound.attackPlay()
				self.rebuke()
	
	def updateAttack(self):
		if self.attack_key != Character.NO_ATTACK and self.life != 0:
			if self.side == 'up':  # up
				self.picnr = [0, 0]
			elif self.side == 'left':  # left
				self.picnr = [1, 0]
			elif self.side == 'down':  # down
				self.picnr = [2, 0]
			elif self.side == 'right':  # right
				self.picnr = [3, 0]
			self.attack_keys[self.attack_key] = False
			self.lenPic = 9
			self.interval = 100
			self.attack_key = Character.NO_ATTACK
	
	def hit(self):
		if self.side == 'up':
			for x in xrange(self.x - 8, self.x + 8):
				for y in xrange(self.y - 12, self.y):
					self.checkAttack(x, y)
		elif self.side == 'left':
			for x in xrange(self.x - 12, self.x):
				for y in xrange(self.y - 8, self.y + 8):
					self.checkAttack(x, y)
		elif self.side == 'down':
			for x in xrange(self.x - 8, self.x + 8):
				for y in xrange(self.y, self.y + 12):
					self.checkAttack(x, y)
		elif self.side == 'right':
			for x in xrange(self.x, self.x + 12):
				for y in xrange(self.y - 8, self.y + 8):
					self.checkAttack(x, y)
	
	def checkAttack(self, x, y):
		pass
	
	def slash(self):
		if self.side == 'up':
			self.picnr = [4, 0]
		elif self.side == 'left':
			self.picnr = [5, 0]
		elif self.side == 'down':
			self.picnr = [6, 0]
		elif self.side == 'right':
			self.picnr = [7, 0]
		self.lenPic = 6
		self.interval = 80
		self.hit()
	
	def rebuke(self):
		if self.side == 'up':
			self.picnr = [8, 0]
		elif self.side == 'left':
			self.picnr = [9, 0]
		elif self.side == 'down':
			self.picnr = [10, 0]
		elif self.side == 'right':
			self.picnr = [11, 0]
		self.lenPic = 7
		self.interval = 150
		self.hit()
	
	# life handle
	def isDead(self):
		Person.Person.setDead(self)
	
	def dying(self):
		Sound.Sound.deathPlay()
		Person.Person.freeLocation(self)
		self.picnr = [12, 0]
		self.lenPic = 6
		self.interval = 500
	
	# speed handle
	def updateSpeed(self, fast):
		if fast:
			self.fast = True
			self.px = 2
		else:
			self.fast = False
			self.px = 1


class Player(Character):
	
	def __init__(self, (x, y)=(0, 0), normal_path='../characters/sprites/ordan.png', transform_path='../characters/sprites/skeleton.png', death_blood='../characters/img/death_vamp.png'):
		
		Character.__init__(self, (x, y), normal_path, death_blood)
		
		# sprites
		self.normal_sprites = self.readSprites(normal_path)
		self.transformed_sprites = self.readSprites(transform_path)
		
		# attack control
		self.stranger = 25
		self.all_killed = 0
		
		# transformation control
		self.partial_killed = 0
		self.number_transformation = 2
		self.transform_interval = 26000
		self.last_transformation = 0L
		self.transformed = False
		
		# death
		self.death = pygame.time.get_ticks()
		self.death_interval = 7000  # 7 seconds
	
	def updateDeath(self, period):
		time = pygame.time.get_ticks()
		"""if period == "morning" and self.life != 0 and not self.transformed:
			if time - self.death >= self.death_interval:
				self.life -= self.stranger
				if self.life < 0:
					self.life = 0
					self.dying()
				self.death = time"""
		if self.fast and not self.transformed:
			if time - self.death >= (self.death_interval / 5):
				self.life -= 1
				if self.life < 0:
					self.life = 0
					self.dying()
				self.death = time
	
	# movement handle
	def move(self, arrow):
		if self.attack_key == Character.NO_ATTACK:
			if arrow == [0, -1]:
				self.up()
			elif arrow == [0, 1]:
				self.down()
			elif arrow == [-1, 0]:
				self.left()
			elif arrow == [1, 0]:
				self.right()
			elif arrow == [-1, -1]:
				self.upLeft()
			elif arrow == [1, -1]:
				self.upRight()
			elif arrow == [-1, 1]:
				self.downLeft()
			elif arrow == [1, 1]:
				self.downRight()
			else:
				self.stopped()
	
	# attack handle
	def checkAttack(self, x, y):
		if self.getPosition() != (x, y):
			enemy = Person.Person.getPersonByPosition(x, y)
			
			if enemy != None:
				enemy.setEnemy(self)
				enemy.attacked = True
				if self.transformed:
					enemy.life = 0
				else:
					enemy.life -= self.stranger
				if enemy.life <= 0:
					enemy.life = 0
					enemy.dying()
					self.partial_killed += 1
					self.all_killed += 1
		
				self.life += self.stranger
				if self.life > 100:
					self.life = 100
	
	def updateTransform(self):
		time = pygame.time.get_ticks()
		if self.partial_killed == self.number_transformation:
			self.sprites = self.transformed_sprites
			self.last_transformation = time
			self.partial_killed = 0
			self.transformed = True
			return 'S'
		
		if self.transformed:
			if time - self.last_transformation >= self.transform_interval:
				self.sprites = self.normal_sprites
				self.last_transformation = time
				self.transformed = False
				return 'N'
		
		return None
	
	# life handle
	def isDead(self):
		Person.Person.setDead(self)
		self.death = -1


class Bot(Character):
	
	def __init__(self, (x, y)=(0, 0), image='../characters/sprites/ordan.png', death_blood='../characters/img/death_blood.png', movement_range=25):
		
		Character.__init__(self, (x, y), image, death_blood)
		
		# attack control
		self.stranger = 10
		
		# bot
		self.movement_range = movement_range
	
	def getMovementRange(self):
		return self.movement_range
	
	def checkAttack(self, x, y):
		if self.getPosition() != (x, y):
			enemy = Person.Person.getPersonByPosition(x, y)
			if enemy != None:
				enemy.setEnemy(self)
				if isinstance(enemy, Player) and not enemy.transformed:
					enemy.attacked = True
					enemy.life -= self.stranger
					if enemy.life <= 0:
						enemy.life = 0
						enemy.dying()
	
	