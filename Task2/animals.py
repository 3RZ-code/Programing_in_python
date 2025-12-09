import random

class sheep():
    def __init__(self, index, step, max_limit):
        self.step = step
        self.index = index
        self.position = [random.uniform(-max_limit, max_limit), random.uniform(-max_limit, max_limit)]
        self.moves = {0: self.up, 1: self.down, 2: self.left, 3: self.right}

    def move(self) -> None:
        direction = random.randint(0, 3)
        self.moves[direction]()

    def up(self) -> list:
        self.position[1] += self.step 
        return self.position
    
    def down(self) -> list:
        self.position[1] -= self.step
        return self.position
    
    def left(self) -> list:
        self.position[0] -= self.step
        return self.position
    
    def right(self) -> list:
        self.position[0] += self.step
        return self.position
    

class wolf():
    def __init__(self, step):
        self.step = step
        self.position = [0.0, 0.0]
        self.nearest_sheep_position = None
        self.nearest_sheep_distance = None
        self.nearest_sheep_index = None
    
    def nearest_sheep(self, sheeps) -> None:
        self.nearest_sheep_position = None
        self.nearest_sheep_distance = None
        self.nearest_sheep_index = None
        min_distance = None
        for sheep_loop in sheeps:
            dx = sheep_loop.position[0] - self.position[0]
            dy = sheep_loop.position[1] - self.position[1]
            dist = (dx*dx + dy*dy) ** 0.5

            if min_distance is None or dist < min_distance:
                min_distance = dist
                self.nearest_sheep_position = sheep_loop.position
                self.nearest_sheep_index = sheep_loop.index
        self.nearest_sheep_distance = min_distance
    
    def attack(self) -> tuple:
        if self.nearest_sheep_distance <= self.step and self.nearest_sheep_position is not None:
            self.position = self.nearest_sheep_position
            return True, self.nearest_sheep_index
        return False, None

    def move(self) -> None:
        if self.nearest_sheep_position is None:
            raise Exception("Nearest sheep not set")
        vector_x = (self.nearest_sheep_position[0] - self.position[0]) / self.nearest_sheep_distance
        vector_y = (self.nearest_sheep_position[1] - self.position[1]) / self.nearest_sheep_distance
        self.position[0] += vector_x * self.step
        self.position[1] += vector_y * self.step
