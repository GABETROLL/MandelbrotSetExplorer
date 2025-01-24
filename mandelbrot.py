RADIUS = 2


class Mandelbrot:
    """Iterable that shows where point c in the complex plane goes in an amount of iterations
    iterating z = z ** 2 + c.
    Breaks loop if z is out of circle of radius 2 in origin."""

    def __init__(self, c: complex, iterations: int):
        self.c = c
        self.iterations = iterations
        self.z = complex(0, 0)
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.z = self.z ** 2 + self.c
        self.count += 1

        if self.z.real ** 2 + self.z.imag ** 2 > 4 or self.count == self.iterations:
            raise StopIteration
        return self.z


def point(c, iterations):
    """Iterates z = z ** 2 + c using complex point c.
    Returns the amount of iterations it took to escape a circle of radius 2 if it escaped.
    Otherwise, returns False. Also returns z (where complex point ended).

    (count if escaped else False, z)"""

    z = 0

    cache = {}

    for iteration in range(1, iterations + 1):
        z = z ** 2 + c

        if z.real ** 2 + z.imag ** 2 > RADIUS ** 2:
            # if z escapes
            return iteration, z
        else:
            if cache.get(z):
                # If we've looped.
                return False, z
            cache[z] = c
            # If we haven't looped, we add to the cache.
    else:
        return False, z
