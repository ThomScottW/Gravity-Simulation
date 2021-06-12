import pygame
import SimModel
from math import floor




class Simulation:
    def __init__(self, env: SimModel.Environment):
        self._running = True

        self._env = env

        self._width, self._height = env.dimensions()
        self._surface = pygame.display.set_mode(env.dimensions())
        pygame.display.set_caption("Gravity Simulation")

    def _handle_events(self):
        # Read key inputs.

        for event in pygame.event.get():

            # If the user clicks the X on the window, then
            # this program will end.
            if event.type == pygame.QUIT:
                self._running = False

        # Handle events.
        env.update()

    def _draw_particle(self, p: SimModel.Particle):
        """Draw a particle on the surface using pygame's draw functions."""
        particle_color = (255, 255, 255)  # white
        # Here we use the math.floor functions because the pygame.draw.circle
        # function can only take the positions as integers. So if the particle's
        # current position consists of floats, it will cause an error.
        particle_position = (floor(p.x), floor(p.y))
        
        # Draw the particle.
        pygame.draw.circle(
            self._surface,
            particle_color,
            particle_position,
            p.radius
        )

    def _redraw_screen(self):
        # Fill the surface with a black background.
        self._surface.fill((0, 0, 0))

        # Display every particle in the environment.
        for particle in self._env:
            self._draw_particle(particle)

        # This will update the contents of the display.
        pygame.display.flip()

    def _select_particle(self):
        pass

    def run(self):
        while (self._running):
            self._handle_events()
            self._redraw_screen()




if __name__ == "__main__":
    env = SimModel.Environment((800, 800))
    Simulation(env).run()