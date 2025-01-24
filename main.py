import pygame
from mandelbrot import *

RAINBOW = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255)]
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Display:
    def __init__(self, width, iterations):
        self.WINDOW = pygame.display.set_mode((width, width))
        pygame.display.set_caption("Mandelbrot Set Explorer")
        self.running = True
        self.width = width

        self.iterations = iterations

        self.center = (0, 0)
        # Where in the mandelbrot set the center of the screen is
        self.radius = 2
        # Radius from center in the complex plane to edge of the screen
        self.zoom_factor = 1/2

        self.cache = {}

        self.__previous_click = False
        # To check if user clicked in previous and current frame.

        self.clicked_path_pos = False

        self.display()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.check_for_zooming()
            self.draw_path()

            pygame.display.update()

        pygame.quit()

    @property
    def scaling_factor(self):
        """How big the screen is compared to the mandelbrot set's 2 radius"""
        return self.width // 2 // self.radius

    def check_for_zooming(self):
        """Checks for user zooming and zooms in that point."""
        clicked = pygame.mouse.get_pressed(3)[0]

        if clicked and not self.__previous_click:
            # If user clicks in the screen and they didn't click (to prevent constant clicking),

            xpos, ypos = pygame.mouse.get_pos()
            # Get the mouse's position.

            self.center = ((xpos - self.width // 2) / self.scaling_factor + self.center[0],
                           (ypos - self.width // 2) / self.scaling_factor + self.center[1])
            self.radius *= self.zoom_factor
            # and zoom in that position.

            self.display()
            # Then we display he new changes.
            self.__previous_click = True
            return

        self.__previous_click = False
        # We continue the queue of clicks.

    def display(self):
        """displays the fractal in self.WINDOW."""
        self.WINDOW.fill(WHITE)

        self.cache = {}

        for xpos in range(self.width):
            for ypos in range(self.width):
                # We iterate over all pixels in the screen

                pos = complex((xpos - self.width // 2) / self.scaling_factor + self.center[0],
                              (ypos - self.width // 2) / self.scaling_factor + self.center[1])

                # And find their position in the complex plane.

                result = self.cache.get(complex(pos.real, -pos.imag))
                # Check if we've already calculated the mirror of that position.
                if not result:
                    result = point(pos, self.iterations)
                    self.cache[pos] = result
                pygame.draw.rect(self.WINDOW,
                                 RAINBOW[result[0] % len(RAINBOW)] if result[0] else BLACK,
                                 pygame.Rect(xpos, ypos, 1, 1))
                # Top and bottom of the set are the same, so we check if we've already calculated the position before.

    def draw_path(self):
        right_clicked = pygame.mouse.get_pressed(3)[2]

        if right_clicked and not self.clicked_path_pos:
            # If we started clicking on the screen,
            self.display()
            # We update the display to prevent circles from piling up.

            xpos, ypos = pygame.mouse.get_pos()
            self.clicked_path_pos = (xpos, ypos)
            # We mark the position we clicked in.

            c_pos = complex((xpos - self.width // 2) / self.scaling_factor + self.center[0],
                            (ypos - self.width // 2) / self.scaling_factor + self.center[1])
            # We calculate where in the complex plane that position is.

            previous_z_screen_pos = False

            for z in Mandelbrot(c_pos, self.iterations):
                # We look at the path where complex point c_pos goes in the mandelbrot set

                z_screen_pos = (int((z.real - self.center[0]) * self.scaling_factor) + self.width // 2,
                                int((z.imag - self.center[1]) * self.scaling_factor) + self.width // 2)

                if previous_z_screen_pos:
                    pygame.draw.line(self.WINDOW, WHITE, previous_z_screen_pos, z_screen_pos)

                previous_z_screen_pos = z_screen_pos
                # And graph it's route in the screen, connecting the current point to the previous one.

        elif not right_clicked and self.clicked_path_pos:
            # If we stopped clicking after we selected a path point,
            self.clicked_path_pos = False
            # We reset that path_pos to False.


Display(500, 20)
