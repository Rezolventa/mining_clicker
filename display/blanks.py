from display.helpers import get_scaled_image, AnimatedObject


class PickaxeHitPointer(AnimatedObject):
    """
    Скорее всего уже не пригодится, но пусть останется как пример анимированного объекта
    """
    def __init__(self):
        self.sprites = [
            get_scaled_image("sprites/hit_1.png", 4),
            get_scaled_image("sprites/hit_2.png", 4),
            get_scaled_image("sprites/hit_3.png", 4),
        ]
        self.animation_count = 0
        self.animation_duration_per_sprite = 4
        self.rect = self.sprites[0].get_rect()
        self.current_sprite_index = None
        self.max_index = len(self.sprites)

    def start(self, center_coords):
        self.set_next_sprite()
        self.move(center_coords)

    def add_animation_count(self):
        self.animation_count += 1
        if self.animation_count == self.animation_duration_per_sprite:
            self.animation_count = 0
            self.set_next_sprite()

    def set_next_sprite(self):
        if self.current_sprite_index is None:
            self.current_sprite_index = 0
        elif self.current_sprite_index == self.max_index - 1:
            self.current_sprite_index = None
        else:
            self.current_sprite_index += 1

    def move(self, center_coords):
        self.rect.center = center_coords

    def draw(self, surface):
        if self.show:
            surface.blit(self.sprite, self.rect)

    @property
    def sprite(self):
        if self.current_sprite_index is None:
            return None
        return self.sprites[self.current_sprite_index]

    @property
    def show(self):
        return self.current_sprite_index is not None
