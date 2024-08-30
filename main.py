import pygame, random, math

from settings import *
from colors import *

# PyGame Setup
pygame.init()

if FULLSCREEN:
    SCREEN = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
else:
    SCREEN = pygame.display.set_mode(RESOLUTION)

pygame.display.set_caption(WINDOW_NAME)
clock = pygame.time.Clock()
delta_time = 0

particles = []

attraction_matrix = []


class Particle:
    def __init__(
        self,
        start_pos=(0, 0),
        start_vel=(0, 0),
        size=10,
        color=(255, 255, 255),
        a_m_index=0,
        radius=150.0,
    ):
        self.x, self.y = start_pos
        self.x_vel, self.y_vel = start_vel
        self.size = size
        self.color = color

        self.friction = 0.1
        self.max_vel = 5

        self.a_m_index = a_m_index

        self.radius = radius

        self.x_accel, self.y_accel = 0, 0

        self.safe_distance = self.size * 2
        self.repulsion_strenght_if_too_close = 100

    def force(self, r, a):
        self.BETA = 0.3

        if r < self.BETA:
            return r / self.BETA - 1
        elif self.BETA < r and r < 1:
            return a * (1 - abs(2 * r - 1 - self.BETA) / (1 - self.BETA))
        else:
            return 0

    def normalize(self, vector):
        magnitude = math.sqrt(vector[0] ** 2 + vector[1] ** 2)

        try:
            output = vector[0] / magnitude, vector[1] / magnitude
        except ZeroDivisionError:
            output = (0, 0)

        return output

    def calculate(self, particles, mouse_pos=None, attract=False, repel=False):
        output_x = 0
        output_y = 0

        for i in range(len(particles)):
            if particles[i] != self:
                dx = particles[i].x - self.x
                dy = particles[i].y - self.y

                if abs(dx) > WIDTH / 2:
                    if dx > 0:
                        dx -= WIDTH
                    else:
                        dx += WIDTH

                if abs(dy) > HEIGHT / 2:
                    if dy > 0:
                        dy -= HEIGHT
                    else:
                        dy += HEIGHT

                magnitude = math.sqrt(dx**2 + dy**2)
                attraction = attraction_matrix[particles[i].a_m_index][self.a_m_index]
                force = self.force(magnitude / self.radius, attraction)
                u_vec = self.normalize((dx, dy))

                if magnitude < self.safe_distance:
                    repulsion_strength = (
                        self.safe_distance - magnitude
                    ) / self.safe_distance
                    force -= repulsion_strength * self.repulsion_strenght_if_too_close

                output_x += u_vec[0] * force
                output_y += u_vec[1] * force

        # Add mouse attraction or repulsion
        if mouse_pos:
            mouse_dx = mouse_pos[0] - self.x
            mouse_dy = mouse_pos[1] - self.y
            mouse_dist = math.sqrt(mouse_dx**2 + mouse_dy**2)

            if mouse_dist > 0:
                mouse_u_vec = self.normalize((mouse_dx, mouse_dy))

                if attract:
                    output_x += mouse_u_vec[0] * self.radius / mouse_dist
                    output_y += mouse_u_vec[1] * self.radius / mouse_dist
                elif repel:
                    output_x -= mouse_u_vec[0] * self.radius / mouse_dist
                    output_y -= mouse_u_vec[1] * self.radius / mouse_dist

        return output_x * self.radius, output_y * self.radius

    def update(self, particles, mouse_pos=None, attract=False, repel=False):
        self.x_accel, self.y_accel = self.calculate(
            particles, mouse_pos, attract, repel
        )

        self.x_vel += self.x_accel * 0.01
        self.y_vel += self.y_accel * 0.01

        self.x_vel = max(-self.max_vel, min(self.x_vel, self.max_vel))
        self.y_vel = max(-self.max_vel, min(self.y_vel, self.max_vel))

        self.x += self.x_vel
        self.y += self.y_vel

        if self.x_vel > 0:
            self.x_vel -= self.friction
        if self.x_vel < 0:
            self.x_vel += self.friction

        if self.y_vel > 0:
            self.y_vel -= self.friction
        if self.y_vel < 0:
            self.y_vel += self.friction

        if self.x > WIDTH:
            self.x = -(self.size * 2)
        elif self.x < -(self.size * 2):
            self.x = WIDTH

        if self.y > HEIGHT:
            self.y = -(self.size * 2)
        elif self.y < -(self.size * 2):
            self.y = HEIGHT

    def draw(self):
        pygame.draw.circle(SCREEN, self.color, (self.x, self.y), self.size)


def draw():
    SCREEN.fill(BLACK)

    for i in range(len(particles)):
        particles[i].draw()

    pygame.display.flip()


def main():
    global delta_time, attraction_matrix

    running = True
    get_ticks_last_frame = 0.0

    # Create Particles
    amt_of_red_particles = 50
    amt_of_green_particles = 50
    amt_of_blue_particles = 50

    for _ in range(amt_of_red_particles):
        r = 10
        ptcl = Particle(
            start_pos=(random.randint(0, WIDTH - r), random.randint(0, HEIGHT - r)),
            size=r,
            color=RED,
            a_m_index=0,
            radius=r * 10,
        )
        particles.append(ptcl)

    for _ in range(amt_of_green_particles):
        r = 10
        ptcl = Particle(
            start_pos=(random.randint(0, WIDTH - r), random.randint(0, HEIGHT - r)),
            size=r,
            color=GREEN,
            a_m_index=1,
            radius=r * 10,
        )
        particles.append(ptcl)

    for _ in range(amt_of_blue_particles):
        r = 10
        ptcl = Particle(
            start_pos=(random.randint(0, WIDTH - r), random.randint(0, HEIGHT - r)),
            size=r,
            color=BLUE,
            a_m_index=2,
            radius=r * 10,
        )
        particles.append(ptcl)

    attraction_matrix = [
        [
            round(random.random() * 2 - 1, 1),
            round(random.random() * 2 - 1, 1),
            round(random.random() * 2 - 1, 1),
        ],
        [
            round(random.random() * 2 - 1, 1),
            round(random.random() * 2 - 1, 1),
            round(random.random() * 2 - 1, 1),
        ],
        [
            round(random.random() * 2 - 1, 1),
            round(random.random() * 2 - 1, 1),
            round(random.random() * 2 - 1, 1),
        ],
    ]

    print(attraction_matrix)

    mouse_pos = None
    attract = False
    repel = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:  # Left click
                    attract = True
                    repel = False
                elif event.button == 3:  # Right click
                    repel = True
                    attract = False
            if event.type == pygame.MOUSEBUTTONUP:
                attract = False
                repel = False

        if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
            mouse_pos = pygame.mouse.get_pos()
        else:
            mouse_pos = None

        for i in range(len(particles)):
            particles[i].update(particles, mouse_pos, attract, repel)

        draw()
        clock.tick(FPS)

        t = pygame.time.get_ticks()
        delta_time = (1 - get_ticks_last_frame) / 1000.0
        get_ticks_last_frame = t

    pygame.quit()


if __name__ == "__main__":
    main()
