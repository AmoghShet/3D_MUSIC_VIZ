import numpy as np
import pygame
from pygame.math import Vector3
from OpenGL.GL import *
from OpenGL.GLU import *
from scipy.io import wavfile
from scipy.signal import resample

# Initialize Pygame and OpenGL
pygame.init()
pygame.mixer.init()
display = (800, 600)
pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

# Set up the 3D view
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# Enable point smoothing
glEnable(GL_POINT_SMOOTH)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# Load and play the audio file
pygame.mixer.music.load('VeridisQuo.mp3')
pygame.mixer.music.play()

# Load the audio data for analysis
sample_rate, audio_data = wavfile.read('VeridisQuo.wav')
audio_data = audio_data.astype(float)
if len(audio_data.shape) > 1:
    audio_data = np.mean(audio_data, axis=1)

# Resample audio data to match the frame rate
target_sample_rate = 60  # Matches our frame rate
audio_data = resample(audio_data, int(len(audio_data) * target_sample_rate / sample_rate))

# Generate particles
num_particles = 5000
particles = [Vector3(*(np.random.rand(3) * 2 - 1)) for _ in range(num_particles)]

# Main loop
def main():
    clock = pygame.time.Clock()
    frame = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if frame >= len(audio_data):
            break
        
        # Get the current audio amplitude
        amplitude = np.abs(audio_data[frame]) / 32767.0  # Normalize to [0, 1]
        
        # Clear the screen and prepare for rendering
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBegin(GL_POINTS)
        
        # Render and update particles
        for particle in particles:
            # Create a unique deformation for each particle based on its position and the audio
            deformation = amplitude * 5 * (1 + np.sin(particle.x * 5 + frame * 0.1) * 
                                           np.cos(particle.y * 5 + frame * 0.1) * 
                                           np.sin(particle.z * 5 + frame * 0.1))
            
            # Update particle position
            particle *= 1 + deformation * 0.1
            
            # Bring particles back towards center if they drift too far
            if particle.magnitude() > 2:
                particle.normalize()
                particle *= 2
            
            # Color based on position and amplitude
            r = 0.5 + 0.5 * np.sin(particle.x + amplitude * 5)
            g = 0.5 + 0.5 * np.sin(particle.y + amplitude * 5)
            b = 0.5 + 0.5 * np.sin(particle.z + amplitude * 5)
            
            glColor3f(r, g, b)
            glVertex3f(particle.x, particle.y, particle.z)
        
        glEnd()
        
        # Rotate the view
        glRotatef(amplitude * 5, 3, 1, 1)
        
        pygame.display.flip()
        clock.tick(60)
        frame += 1

main()