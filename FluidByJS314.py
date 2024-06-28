from vpython import *
import random

BOX_SIZE = 3
PARTICLE_RADIUS = 0.2
DIPOLE_STRENGTH = 5
LONDON_STRENGTH = 2
FORCE_RANGE = 1
PARTICLE_MASS = 1
BOUNCE_FACTOR = 0.2
COLLISION_FACTOR = 1

class Particle:
    def __init__(self, pos, radius, color):
        self.obj = sphere(pos=pos, radius=radius, color=color)
        self.velocity = vector(0, 0, 0)
        self.acceleration = vector(0, 0, 0)
        self.force = vector(0, 0, 0)
        self.velocityBounceFactor = 1

class Fluid:
    def __init__(self, number_of_particles):
        self.particles = []
        self.box = box(pos=vector(0, 0, 0), size=vector(BOX_SIZE, BOX_SIZE, BOX_SIZE), opacity=0.2)
        for _ in range(number_of_particles):
            x = random.uniform(-BOX_SIZE/2, BOX_SIZE/2)
            y = random.uniform(-BOX_SIZE/2, BOX_SIZE/2)
            z = random.uniform(-BOX_SIZE/2, BOX_SIZE/2)
            particle = Particle(vector(x, y, z), PARTICLE_RADIUS, color.blue)
            self.particles.append(particle)
    def apply_interaction(self):
        for firstObj in range(len(self.particles)-1):
            for secondObj in range(firstObj+1, len(self.particles)):
                r = self.particles[firstObj].obj.pos - self.particles[secondObj].obj.pos
                distance = mag(r)
                if distance < 0.2:
                    distance = 0.2
                dpl_dpl_frc = -r * DIPOLE_STRENGTH / distance**3
                ldn_frc = -r / distance**6
                self.particles[firstObj].force += dpl_dpl_frc + ldn_frc
                self.particles[secondObj].force -= dpl_dpl_frc + ldn_frc
    def check_collision(self):
        for firstObj in range(len(self.particles) - 1):
            for secondObj in range(firstObj + 1, len(self.particles)):
                r = self.particles[firstObj].obj.pos - self.particles[secondObj].obj.pos
                distance = mag(r)
                if distance < 2 * PARTICLE_RADIUS:
                    colision_vector = hat(r)

                    u1 = self.particles[firstObj].velocity
                    u2 = self.particles[secondObj].velocity

                    collision_u1 = dot(u1, colision_vector) * colision_vector
                    collision_u2 = dot(u2, colision_vector) * colision_vector

                    collsion_v1 =  ((collision_u1 + collision_u2) - COLLISION_FACTOR * (collision_u1 - collision_u2)) / 2
                    collsion_v2 =  ((collision_u1 + collision_u2) + COLLISION_FACTOR * (collision_u1 - collision_u2)) / 2

                    self.particles[firstObj].velocity += collsion_v1 - collision_u1
                    self.particles[secondObj].velocity += collsion_v2 - collision_u2

    def apply_gravity(self):
        for particle in self.particles:
            particle.force += vector(0, -98, 0)
    def update(self, dt):
        # Apply gravity and intermolecular forces
        for i in self.particles:
            i.force = vector(0, 0, 0)
            i.velocityBounceFactor = 1
        self.apply_interaction()
        self.apply_gravity()
        
        # Make forces into accelerations and update velocities
        for particle in self.particles:
            # F = ma, a = F/m
            particle.acceleration = particle.force / PARTICLE_MASS
            particle.velocity *= particle.velocityBounceFactor
            particle.velocity += particle.acceleration * dt
        
        # Check for collisions with other particles
        self.check_collision()

        # Check for collisions with container walls
        for particle in self.particles:
            print("{}\t{}\t{}".format(particle.obj.pos, particle.velocity, particle.force))
            if particle.obj.pos.x > BOX_SIZE/2 - PARTICLE_RADIUS:
                particle.velocity.x *= -BOUNCE_FACTOR
                particle.obj.pos.x -= 2 * (particle.obj.pos.x - (BOX_SIZE/2 - PARTICLE_RADIUS))
            if particle.obj.pos.x < -BOX_SIZE/2 + PARTICLE_RADIUS:
                particle.velocity.x *= -BOUNCE_FACTOR
                particle.obj.pos.x -= 2 * (particle.obj.pos.x + (BOX_SIZE/2 - PARTICLE_RADIUS))
            if particle.obj.pos.y > BOX_SIZE/2 - PARTICLE_RADIUS:
                particle.velocity.y *= -BOUNCE_FACTOR
                particle.obj.pos.y -= 2 * (particle.obj.pos.y - (BOX_SIZE/2 - PARTICLE_RADIUS))
            if particle.obj.pos.y < -BOX_SIZE/2 + PARTICLE_RADIUS:
                particle.velocity.y *= -BOUNCE_FACTOR
                particle.obj.pos.y -= 2 * (particle.obj.pos.y + (BOX_SIZE/2 - PARTICLE_RADIUS))
            if particle.obj.pos.z > BOX_SIZE/2 - PARTICLE_RADIUS:
                particle.velocity.z *= -BOUNCE_FACTOR
                particle.obj.pos.z -= 2 * (particle.obj.pos.z - (BOX_SIZE/2 - PARTICLE_RADIUS))
            if particle.obj.pos.z < -BOX_SIZE/2 + PARTICLE_RADIUS:
                particle.velocity.z *= -BOUNCE_FACTOR
                particle.obj.pos.z -= 2 * (particle.obj.pos.z + (BOX_SIZE/2 - PARTICLE_RADIUS))

        # Update position
        for particle in self.particles:
            particle.obj.pos += particle.velocity * dt

def main():
    fluid = Fluid(3)
    dt = 0.01
    while True:
        rate(200)
        #print(fluid.particles[0].obj.pos, '\t', fluid.particles[0].velocity, '\t', fluid.particles[0].force)
        fluid.update(dt)

if __name__ == "__main__":
    main()