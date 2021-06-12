import math
import random

GRAVITATIONAL_CONSTANT = 10

TEST = 1




class Vector:
    """A 2-dimensional vector used for keeping
    track of the speeds of particles."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def magnitude(self) -> float:
        """Return the magnitude of the Vector."""
        return math.sqrt(self.x**2 + self.y**2)
    
    def unit(self):
        """Return a unit vector in the same direction as this Vector."""
        if self.magnitude() == 0:
            return Vector(0, 0)
        else:
            return Vector(self.x / self.magnitude(), self.y / self.magnitude())

    def angle(self):
        """Return the angle (in radians) of this vector based on the current
        x and y components."""

        # First, find this vector's corresponding unit vector
        # We do this because if we make the vector similar ot the unit
        # circle in that distance from the origin to the edge is 1, 
        # we can use equations like arctangent to manipulate the angle.
        unit = self.unit()

        # Return arctangent(y/x) to get the angle in radians.
        return math.atan2(unit.y, unit.x)

    def dot_product(self, right) -> int or float:
        """Perform the dot product operation between two vectors."""
        if type(right) != Vector:
            raise NotImplemented(f"Dot product not supported between Vector and {type(right)}.")
        else:
            return self.x * right.x + self.y * right.y
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, right):
        """Add this vector to another."""
        if type(right) != Vector:
            raise NotImplemented(f"Addition not supported between Vector and {type(right)}.")
        else:
            return Vector(self.x + right.x, self.y + right.y)

    def __mul__(self, right):
        """Multiply the x and y components of the Vector by a factor."""
        if type(right) not in (int, float):
            raise NotImplemented(f"Multiplication not supported between Vector and {type(right)}.")
        else:
            return Vector(self.x * right, self.y * right)
            


class Particle:
    def __init__(
        self,
        radius: int,
        position: (int, int),
        vector: Vector,
        mass=1
    ):
        self.radius = radius
        self.x, self.y = position
        self.mass = 1
        self._vector = vector  # Not needed outside this class.

    def coordinates(self) -> (int):
        """Return the pixel coordinates of this Particle."""
        return (self.x, self.y)

    def move(self) -> None:
        """Move the particle based on its vector's direction and speed."""
        # Find the angle that this particle is moving.
        vec_angle = self._vector.angle()
        vec_magnitude = self._vector.magnitude() * 0.1

        # Calculate the amount that this particle will travel,
        # based on the angle and magnitude of the vector.
        dx = vec_magnitude * math.cos(vec_angle)
        dy = vec_magnitude * math.sin(vec_angle)

        # Move the particle by the calculated amounts.
        self.x += dx
        self.y += dy
        

    def accelerate_towards(self, p2):
        """Accelerate this particle towards another, based on
        the masses of each particle."""
        dx = self.x - p2.x
        dy = self.y - p2.y
        dist = math.hypot(dx, dy)

        angle_between_particles = math.atan2(dy, dx) + math.pi

        # Gravitational equation
        # This will be the magnitude of the vector we will add to this particle's
        # existing vector.
        force = (GRAVITATIONAL_CONSTANT * self.mass * p2.mass) / dist ** 2

        # Calculate the x and y components of the force vector.
        force_x_comp = math.cos(angle_between_particles) * force
        force_y_comp = math.sin(angle_between_particles) * force

        # Add the force vector to this particle's vector.

        global TEST

        if TEST > 0:
            print(f"In particle with radius {self.radius} acc towards particle with radius {p2.radius}")
            print(f"The calculated angle was {angle_between_particles}")
            print(f"Adding self vector {self._vector} to calculated vector {Vector(force_x_comp, force_y_comp)}")
            

        self._vector = self._vector + Vector(force_x_comp, force_y_comp)

        if TEST > 0:
            print(f'For result {self._vector}')
            TEST -= 1

        # print(f'After: {self._vector}')
    

    def collide_with(self, p2) -> None:
        """Resolve a collision with another particle."""
        pass

    def _is_colliding_with(self, p2) -> bool:
        """Return True if colliding with p2, else return False."""
        pass


class Environment:
    """The environment that contains all the particles and constants
    which govern the simulation."""

    # Define environment Constants.

    def __init__(self, dimensions: (int, int)):
        self._width, self._height = dimensions
        self._particles = []

        # Create random particles.
        self._generate_particles(4)

    def __iter__(self):
        """Allow this environment to be iterated over, by giving
        access to the list of particles in the environment."""
        return iter(self._particles)

    def _generate_particles(self, num=1, **kargs):
        """Generate a number of particles with the provided attributes in **kargs.

        Any arguments that are not provided will be randomly generated.
        
        Populate the self._particles list attribute with these particles.
        """
        for _ in range(num):
            # mass = kargs.get("mass", random.randint(100, 10000))
            # radius = kargs.get("size", random.randint(10, 20))
            # x = kargs.get("x", random.uniform(radius, self._width - radius))
            # y = kargs.get("y", random.uniform(radius, self._height - radius))
            # speed = kargs.get("speed", random.random())
            # angle = kargs.get("angle", random.uniform(0, 2 * math.pi))
            # color = kargs.get("color", (255, 0, 0))

            radius = random.randint(5, 30)
            mass = radius * 10
            x = random.uniform(radius, self._width - radius)
            y = random.uniform(radius, self._height - radius)
            speed = 0
            angle = random.uniform(0, 2 * math.pi)

            new_vector = Vector(math.cos(angle) * speed, math.sin(angle) * speed)
            new_particle = Particle(radius, (x, y), new_vector, mass)
            self._particles.append(new_particle)

    def dimensions(self):
        return (self._width, self._height)

    def update(self) -> None:
        """Update the simulation to move particles, resolve collisions, etc."""
        for p in self._particles:
            p.move()

            for other_p in self._particles:
                if p != other_p:
                    p.accelerate_towards(other_p)

    def _bounce(self, particle) -> None:
        """Bounce a particle off the boundaries of the Environment."""
        pass

    def find_particle(self, coordinates: (int, int)) -> Particle:
        """Given coordinates, return a Particle if there is one at those coordinates."""
        pass