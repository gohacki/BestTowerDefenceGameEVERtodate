import pygame
from math import sqrt
from .tower import Tower


# TowerManager Class handles pressing of keys and mouse movement in order to place towers
class TowerManager:
    # initialize towers to be a list of set towers
    def __init__(self, screen, enemy_path, game_manager, path_mask):
        self.towers = []
        self.the_tower = None
        self.selected_tower_type = None
        self.enemy_path = enemy_path
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()  # stores screen size
        self.game_manager = game_manager
        # initialize path that towers cannot be placed on
        self.path_mask = path_mask
        self.bullets = []
        self.freeze_to_animate = []
        self.multi_to_animate = []
        self.selected_tower = None
        self.freeze_sprite = pygame.image.load("Assets/freeze_animation.png").convert()
        self.freeze_sprite = self.freeze_sprite.convert_alpha(screen)

    # handle_event responds to user interaction such as pressing keys or moving/clicking the mouse
    def handle_event(self, event):
        # if the escape key is pushed while at a tower
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and self.the_tower:
                # unselect the current tower
                self.the_tower = None
                self.selected_tower_type = None
        # if the mouse is pressed down enable placement or selection of given tower
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # if user has selected a tower and wants to potentially place it
            if self.the_tower:
                # ensure that the tower can be placed according to bounds of map
                if self.is_tower_placeable(self.the_tower.rect):
                    tower_cost = self.the_tower.cost
                    # ensure user has enough dabloons to place tower
                    if self.game_manager.currency >= tower_cost:
                        self.game_manager.currency -= tower_cost
                        self.towers.append(self.the_tower)
                        # This fixes issue of - tower position only being set when the user first clicked on the tower.
                        self.the_tower.position = self.the_tower.rect.center
                        self.the_tower = None
                        self.selected_tower_type = None
                    else:
                        self.game_manager.ui_manager.set_notification("Not enough gold!")

                else:
                    self.game_manager.ui_manager.set_notification("Cannot place tower here!")

            # if there is no tower being placed, take into account for upgrades
            else:
                mouse_pos = pygame.mouse.get_pos()
                # loop through all the towers
                for tower in self.towers:
                    # if mouse is hovering and selecting a given tower pass into selection function
                    if tower.rect.collidepoint(mouse_pos):
                        self.selected_tower = tower
                        self.game_manager.set_selected_tower(tower)
                        return
                self.selected_tower = None
                self.game_manager.set_selected_tower(None)

        # if the tower is selected, and you want to drop it off back at home instead of placing it
        elif event.type == pygame.MOUSEBUTTONUP and self.the_tower:
            mouse_position = pygame.mouse.get_pos()
            distance_to_home = sqrt((mouse_position[0] - self.the_tower.home_position[0]) ** 2 +
                                    (mouse_position[1] - self.the_tower.home_position[1]) ** 2)
            if distance_to_home < 20:
                self.the_tower = None
                self.selected_tower_type = None
            else:
                pass

    # is_tower_placeable asks if the tower can be placed at current mouse location given bounds of the path
    def is_tower_placeable(self, tower_rect):
        # check to see if the tower is overlapping the given path
        tower_mask = pygame.mask.from_surface(self.the_tower.image)
        tower_offset = tower_rect.topleft
        if self.path_mask.overlap(tower_mask, tower_offset):
            return False

        # check to see if the tower is overlapping with any other placed towers
        for tower in self.towers:
            if tower.rect.colliderect(tower_rect):
                return False

        # check to ensure that the tower is still on the playable screen
        screen_rect = pygame.Rect(0, 0, self.screen_width, self.screen_height)
        return screen_rect.contains(tower_rect)

    # set a selected tower to be "the_tower"
    def select_tower(self, tower_type):
        self.selected_tower_type = tower_type
        mouse_position = pygame.mouse.get_pos()
        self.the_tower = Tower(mouse_position, tower_type)

    # manage the new tower being placed by following the mouse cursor
    def update(self):
        if self.the_tower:
            mouse_position = pygame.mouse.get_pos()
            self.the_tower.rect.center = mouse_position

        # Update bullets
        for bullet in self.bullets[:]:
            # Move bullet towards target
            dx = bullet['target_pos'][0] - bullet['current_pos'][0]
            dy = bullet['target_pos'][1] - bullet['current_pos'][1]
            distance = sqrt(dx ** 2 + dy ** 2)
            if distance != 0:
                dx /= distance
                dy /= distance
            speed = 25  # pixels per frame
            bullet['current_pos'] = (bullet['current_pos'][0] + dx * speed, bullet['current_pos'][1] + dy * speed)

            # Check if bullet has reached or passed the target
            if ((dx >= 0 and bullet['current_pos'][0] >= bullet['target_pos'][0]) or
                (dx < 0 and bullet['current_pos'][0] <= bullet['target_pos'][0])) and \
                    ((dy >= 0 and bullet['current_pos'][1] >= bullet['target_pos'][1]) or
                     (dy < 0 and bullet['current_pos'][1] <= bullet['target_pos'][1])):
                self.bullets.remove(bullet)

        # this increases the size of the freeze attack animation
        freeze_animation_frames = 15
        for animation in self.freeze_to_animate:

            animation["size"] += animation["max_size"]/freeze_animation_frames
            # the animation is greater than it's max size
            if animation["size"] > animation["max_size"]:
                self.freeze_to_animate.remove(animation)

        # TODO: update multi_attack


    # render is display the placed towers, and the currently being placed tower
    def render(self, screen):
        for tower in self.towers:
            tower.draw(screen)

        # highlight the selected tower and its corresponding range
        if self.selected_tower:
            pygame.draw.circle(screen, (0, 255, 0), self.selected_tower.position, self.selected_tower.range, 2)

        # render the tower that is being placed and its potential conflicts with the path
        if self.the_tower:
            self.the_tower.draw(screen)
            # display range of the tower as translucent either white or red according to validity
            if self.is_tower_placeable(self.the_tower.rect):
                range_color = (255, 255, 255, 100)  # white color when valid

            else:
                range_color = (255, 0, 0, 100)  # red to show it is invalid

            range_surface = pygame.Surface((self.the_tower.range * 2, self.the_tower.range * 2), pygame.SRCALPHA)
            pygame.draw.circle(range_surface, range_color, (self.the_tower.range, self.the_tower.range),
                               self.the_tower.range)
            screen.blit(range_surface, (
            self.the_tower.rect.centerx - self.the_tower.range, self.the_tower.rect.centery - self.the_tower.range))

        # render bullets
        for bullet in self.bullets:
            tower_type = self.towers[bullet['tower_id']].get_type()
            if tower_type == 1:
                color = (128, 30, 232)
                width = 3
            elif tower_type == 2:
                color = (255, 255, 0)
                width = 4
            elif tower_type == 3:
                color = (255, 0, 0)
                width = 6
            elif tower_type == 5:
                color = (255, 0, 0)
                width = 11
            pygame.draw.line(screen, color, self.towers[bullet['tower_id']].get_position(), bullet['current_pos'],
                             width)

        # render freeze animations
        for animation in self.freeze_to_animate:
            sprite = pygame.transform.scale(self.freeze_sprite, (animation["size"]*2, animation["size"]*2))
            rect = sprite.get_rect(center=animation['tower_position'])
            screen.blit(sprite, rect)

        # render multi_animations
        for animation in self.multi_to_animate:
            if animation["frames_drawn"] < 10:
                start_pos = animation["start_pos"]
                end_pos = animation["end_pos"]
                pygame.draw.line(screen, (255, 255, 0), start_pos, end_pos, 4)
                animation["frames_drawn"] += 1
            else:
                self.multi_to_animate.remove(animation)

    # Returns a list of dictionaries, which themselves contain next checkpoint, current x and y coordinates plus an id
    def get_attacking_towers(self):
        attacking_towers = []
        for index, tower in enumerate(self.towers):
            if tower.can_attack():
                attacking_towers.append(tower.get_attack(index))
            else:
                attacking_towers.append(False)
        return attacking_towers

    # takes a tower id (the index of the tower in self.towers) and resets it's attack cooldown
    def reset_attack_cooldown(self, tower_id):
        try:
            self.towers[tower_id].reset_attack_cooldown()
            return True
        except IndexError:
            return False

    def prepare_attack_animations(self, bullets, multi_animations, freeze_animations):
        for bullet in bullets:
            start_pos = self.towers[bullet['id']].get_position()
            target_pos = bullet['position']
            self.bullets.append({
                'current_pos': start_pos,
                'target_pos': target_pos,
                'tower_id': bullet['id']
            })
            # This code calculates the angle to the enemy so the tower can be rotated to face the enemy
            vec_enemy = pygame.math.Vector2(target_pos)
            vec_attack = vec_enemy - start_pos
            vec_attack = vec_attack.as_polar()
            degrees = vec_attack[1]

            self.towers[bullet['id']].rotate(degrees)

        for animation in multi_animations:
            self.multi_to_animate.append({
                "start_pos": animation["start_position"],
                "end_pos": animation["end_position"],
                "frames_drawn": 0
            })

        for animation in freeze_animations:
            self.freeze_to_animate.append({
                "tower_position": self.towers[animation["id"]].get_position(),
                "size": 0,
                "max_size":  self.towers[animation["id"]].get_range()
            })
