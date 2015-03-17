
import pygame

import Person


class Character:
	
	# attack_keys
	NO_ATTACK = 0
	SLASH = pygame.K_SPACE
	REBUKE = pygame.K_e
	
	def __init__(self, (x, y), path_image, death_blood, name=""):
		# essential
		self.x = x
		self.y = y
		self.setPosition((x, y))
		self.initial_position = (x, y)
		self.id = 0
		self.name = name
		self.life = 100
		# speed
		self.px = 1
		self.fast = False
		
		self.image = path_image

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
		check = True
		if self.x == x and self.y == y:
			check = False
		self.x = x
		self.y = y
		return check
	
	def getEnemy(self):
		return self.enemy
	
	def getImage (self):
		return self.image
	
	def setEnemy(self, enemy):
		if (not isinstance(enemy, Bot)):
			self.enemy = enemy
	
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
			return self.setPosition(position)
			
	def left(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.side = 'left'
			self.movement = True
			position = Person.Person.changePersonLocation(self, self.x - self.px, self.y)
			return self.setPosition(position)
	
	def down(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.side = 'down'
			self.movement = True
			position = Person.Person.changePersonLocation(self, self.x, self.y + self.px);
			return self.setPosition(position)
	
	def right(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.side = 'right'
			self.movement = True
			position = Person.Person.changePersonLocation(self, self.x + self.px , self.y);
			return self.setPosition(position)
	
	def upLeft(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.side = 'left'
			self.movement = True
			position = Person.Person.changePersonLocation(self, self.x - self.px, self.y - self.px);
			return self.setPosition(position)
	
	def upRight(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.side = 'right'
			self.movement = True
			position = Person.Person.changePersonLocation(self, self.x + self.px, self.y - self.px);
			return self.setPosition(position)
	
	def downLeft(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.side = 'left'
			self.movement = True
			position = Person.Person.changePersonLocation(self, self.x - self.px, self.y + self.px);
			return self.setPosition(position)
	
	def downRight(self):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.side = 'right'
			self.movement = True
			position = Person.Person.changePersonLocation(self, self.x + self.px, self.y + self.px);
			return self.setPosition(position)
	
	def stopped(self):
		self.movement = False
	
	# attack handle
	def attack(self, key):
		if self.attack_key == Character.NO_ATTACK and self.life != 0:
			self.attack_keys[key] = True
			self.attack_key = key
			self.hit()
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
	
	# child overrides this
	def checkAttack(self, x, y):
		pass
	
	# life handle
	def dead(self):
		Person.Person.setDead(self)
	
	# speed handle
	def updateSpeed(self, fast):
		if fast:
			self.fast = True
			self.px = 2
		else:
			self.fast = False
			self.px = 1


class Player(Character):
	
	def __init__(self, (x, y)=(0, 0), normal_path='../characters/sprites/ordan.png', transform_path='../characters/sprites/skeleton.png', death_blood='../characters/img/death_vamp.png', name=""):
		
		Character.__init__(self, (x, y), normal_path, death_blood)
		
		self.name = name
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
				self.death = time"""
		if self.fast and not self.transformed:
			if time - self.death >= (self.death_interval / 5):
				self.life -= 1
				if self.life < 0:
					self.life = 0
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
				if self.transformed and isinstance(enemy, Bot):
					enemy.life = 0
				else:
					enemy.life -= self.stranger
				if enemy.life <= 0:
					enemy.life = 0
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
	def dead(self):
		Person.Person.setDead(self)


class Bot(Character):
	
	def __init__(self, (x, y)=(0, 0), image='../characters/sprites/ordan.png', death_blood='../characters/img/death_blood.png', movement_range=25, name=""):
		
		Character.__init__(self, (x, y), image, death_blood)
		self.name = name
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
					if enemy.life < 0:
						enemy.life = 0
	
