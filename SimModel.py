import math
import random


GRAVITATIONAL_CONSTANT = 0.01



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
    elasticity_coefficient = 0.5


    def __init__(
        self,
        radius: int,
        position: (int, int),
        vector: Vector,
        mass=1
    ):
        self.radius = radius
        self.x, self.y = position
        self.mass = mass
        self._vector = vector  # Not needed outside this class.
        self.absorbed = False

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

    def accelerate_towards(self, point: (int, int), p_mass=1):
        """Accelerate this particle towards a point."""
        dx = point[0] - self.x
        dy = point[1] - self.y
        dist = math.hypot(dx, dy)

        angle_between_particles = math.atan2(dy, dx)

        # Gravitational equation
        # This will be the magnitude of the vector we will add to this particle's
        # existing vector.
        force = (GRAVITATIONAL_CONSTANT * self.mass * p_mass) / dist ** 2

        # Calculate the x and y components of the force vector.
        force_x_comp = math.cos(angle_between_particles) * force
        force_y_comp = math.sin(angle_between_particles) * force

        # Add the force vector to this particle's vector.
        self._vector = self._vector + Vector(force_x_comp, force_y_comp)

    def coalesce(self, p2) -> None:
        """Collide with another particle, coalescing into a larger particle."""
        if not self._is_colliding_with(p2):
            return

        total_mass = self.mass + p2.mass

        # Case where p1 is larger and absorbs p2.
        if self.mass >= p2.mass:
            # Create a new position and vector that is based on the masses
            # of the particles.
            self.x = (self.x * self.mass + p2.x * p2.mass) / total_mass

            # The larger particle should stay moving in roughly the same direction, 
            # but can be diverted slightly by the smaller particle.
            smaller_vec_magnitude = (p2._vector.magnitude() * p2.mass) / total_mass
            smaller_vec_angle = p2._vector.angle()
            smaller_vec_x = math.cos(smaller_vec_angle) * smaller_vec_magnitude
            smaller_vec_y = math.sin(smaller_vec_angle) * smaller_vec_magnitude

            # Add this new weighted vector to p1's existing vector.
            self._vector = self._vector + Vector(smaller_vec_x, smaller_vec_y)

            # Apply "elasticity" to make it seem like the particle lost kinetic energy
            # from the collision.
            self._apply_elasticity()

            # Update the mass and radius for this particle.
            self.mass = total_mass
            self.radius = self._calculate_radius(total_mass)

            # Update p2 so that it has been "absorbed".
            p2.absorbed = True

        # Case where p2 is larger and absorbs p1.
        elif p2.mass > self.mass:
            p2.x = (p2.x * p2.mass + self.x * self.mass) / total_mass

            smaller_vec_magnitude = (self._vector.magnitude() * self.mass) / total_mass
            smaller_vec_angle = self._vector.angle()
            smaller_vec_x = math.cos(smaller_vec_angle) * smaller_vec_magnitude
            smaller_vec_y = math.sin(smaller_vec_angle) * smaller_vec_magnitude

            p2._vector = p2._vector + Vector(smaller_vec_x, smaller_vec_y)

            p2._apply_elasticity()

            p2.mass = total_mass
            p2.radius = self._calculate_radius(total_mass)

            self.absorbed = True
    
    def distance_from(self, point: (int, int)) -> float:
        """Return the distance from this particle's center to a point."""
        return math.hypot(point[0] - self.x, point[1] - self.y)


    def _is_colliding_with(self, p2) -> bool:
        """Return True if colliding with p2, else return False."""
        if self.distance_from(p2.coordinates()) < self.radius + p2.radius:
            return True
        else:
            return False
    
    def _calculate_radius(self, mass):
        """Given a mass, calculate the radius of a particle with that mass."""
        return mass ** 0.5
    
    def _apply_elasticity(self):
        self._vector = self._vector * Particle.elasticity_coefficient
        
        

class Environment:
    """The environment that contains all the particles and constants
    which govern the simulation."""

    # Define environment Constants.

    def __init__(self, dimensions: (int, int), num_particles=10):
        self._width, self._height = dimensions
        self._particles = []

        # Create random particles.
        self._generate_particles(num_particles)

    def __iter__(self):
        """Allow this environment to be iterated over, by giving
        access to the list of particles in the environment."""
        return iter(self._particles)

    def _generate_particles(self, num=1):
        """Generate a number of particles with the provided attributes in **kargs.

        Any arguments that are not provided will be randomly generated.
        
        Populate the self._particles list attribute with these particles.
        """
        for _ in range(num):

            rand_num = random.random()

            if rand_num < 0.98:
                mass = random.randint(1, 3)
            else:
                mass = random.randint(50, 100)

            radius =  mass ** 0.5
            x = random.uniform(radius, self._width - radius)
            y = random.uniform(radius, self._height - radius)
            speed = 0
            angle = random.uniform(0, 2 * math.pi)
            new_vector = Vector(math.cos(angle) * speed, math.sin(angle) * speed)
            new_particle = Particle(radius, (x, y), new_vector, mass)
            self._particles.append(new_particle)

    def add_particle(self, position: (int, int), p_radius=5, p_mass=25):
        """Add a particle to the simulation, given some attributes."""
        new_particle = Particle(p_radius, position, Vector(0, 0), p_mass)
        self._particles.append(new_particle)
        

    def dimensions(self):
        return (self._width, self._height)

    def update(self) -> None:
        """Update the simulation to move particles, resolve collisions, etc."""
        # First, check for and remove any absorbed particles from the simulation.
        self._particles = [p for p in self._particles if not p.absorbed]

        for p in self._particles:
            p.move()

            for other_p in self._particles:
                if p != other_p:
                    p.accelerate_towards(other_p.coordinates(), other_p.mass)
                    p.coalesce(other_p)
                

    def _bounce(self, particle) -> None:
        """Bounce a particle off the boundaries of the Environment."""
        pass

    def find_particle(self, coordinates: (int, int)) -> Particle:
        """Given coordinates, return a Particle if there is one at those coordinates."""
        pass
