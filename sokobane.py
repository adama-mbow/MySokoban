import pygame
from pygame.locals import *

# initialisation de pygame

pygame.init()

#configuration de la fenetre de jeu
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Sokoban Game")

#chargement des ressources
player_image =  pygame.image.load("worker.png")
box_image = pygame.image.load("box.png")
wall_image = pygame.image.load("wall.png")
destination_image = pygame.image.load("floor.png")
background_image = pygame.image.load("dock.png")

# Classe pour représenter le joueur
class Player:
    def __init__(self, x, y):
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self, dx, dy):
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        # Vérifier la collision avec les murs
        for wall in walls:
            if wall.rect.collidepoint(new_x, new_y):
                return  # Ne pas déplacer si collision
            
         # Vérifier la collision avec les boîtes
        for box in boxes:
            if box.rect.collidepoint(new_x, new_y):
                # Vérifier si la boîte peut être déplacée
                new_box_x = box.rect.x + dx
                new_box_y = box.rect.y + dy
                for wall in walls:
                    if wall.rect.collidepoint(new_box_x, new_box_y):
                        return  # Ne pas déplacer si collision avec un mur

                # Vérifier si la boîte peut être poussée sur une destination
                for destination in destinations:
                    if destination.rect.collidepoint(new_box_x, new_box_y):
                        # Déplacer la boîte
                        box.rect.x = new_box_x
                        box.rect.y = new_box_y

                        # Déplacer le joueur
                        self.rect.x = new_x
                        self.rect.y = new_y
                        return

                return  # Ne pas déplacer si aucune condition rempli    

        self.rect.x = new_x
        self.rect.y = new_y
        
    def push_box(self, dx, dy):
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy

        # Vérifier la collision avec les boîtes
        for box in boxes:
            if box.rect.collidepoint(new_x, new_y):
                # Vérifier si la boîte peut être déplacée
                new_box_x = box.rect.x + dx
                new_box_y = box.rect.y + dy
                for wall in walls:
                    if wall.rect.collidepoint(new_box_x, new_box_y):
                        return  # Ne pas pousser si collision avec un mur

                # Vérifier si la boîte peut être poussée sur une destination
                for destination in destinations:
                    if destination.rect.collidepoint(new_box_x, new_box_y):
                        # Déplacer la boîte
                        box.rect.x = new_box_x
                        box.rect.y = new_box_y
                        return

                return  # Ne pas pousser si aucune condition remplie

        return  # Ne rien faire si aucune boîte à pousser

            
            

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    

# Classe pour représenter les boîtes
class Box:
    def __init__(self, x, y):
        self.image = box_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Classe pour représenter les murs
class Wall:
    def __init__(self, x, y):
        self.image = wall_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Classe pour représenter les destinations
class Destination:
    def __init__(self, x, y):
        self.image = destination_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Chargement du niveau à partir d'une liste
def load_level(level_data):
    walls = []
    boxes = []
    destinations = []
    player = None

    for y, row in enumerate(level_data):
        for x, cell in enumerate(row):
            if cell == "#":  # Mur
                walls.append(Wall(x * 50, y * 50))
            elif cell == "$":  # Boîte
                boxes.append(Box(x * 50, y * 50))
            elif cell == ".":  # Destination
                destinations.append(Destination(x * 50, y * 50))
            elif cell == "@":  # Joueur
                player = Player(x * 50, y * 50)

    return walls, boxes, destinations, player

# Définition du niveau
level = [
    "#####",
    "#.@.#",
    "#$$.#",
    "#..*#",
    "#####"
]

# Chargement des éléments du niveau
walls, boxes, destinations, player = load_level(level)

# Boucle de jeu principale
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                player.move(-50, 0)
            elif event.key == K_RIGHT:
                player.move(50, 0)
            elif event.key == K_UP:
                player.move(0, -50)
            elif event.key == K_DOWN:
                player.move(0, 50)

    # Effacement de l'écran
    window.fill((0, 0, 0))

    # Affichage des éléments du jeu
    window.blit(background_image, (0, 0))

    for wall in walls:
        wall.draw(window)

    for destination in destinations:
        destination.draw(window)

    for box in boxes:
        box.draw(window)

    player.draw(window)

    # Mise à jour de l'écran
    pygame.display.update()

# Fermeture de Pygame
pygame.quit()





