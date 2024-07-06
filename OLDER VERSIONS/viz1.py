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

# Generate the sphere vertices
def create_sphere(radius, num_slices, num_stacks):
    vertices = []
    for i in range(num_stacks + 1):
        theta = np.pi * i / num_stacks
        sin_theta = np.sin(theta)
        cos_theta = np.cos(theta)
        
        for j in range(num_slices + 1):
            phi = 2 * np.pi * j / num_slices
            sin_phi = np.sin(phi)
            cos_phi = np.cos(phi)
            
            x = radius * sin_theta * cos_phi
            y = radius * sin_theta * sin_phi
            z = radius * cos_theta
            
            vertices.append(Vector3(x, y, z))
    
    return vertices

# Create the initial sphere
sphere_vertices = create_sphere(1, 30, 30)

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
        
        # Render deformed sphere
        for i, vertex in enumerate(sphere_vertices):
            # Create a unique deformation for each vertex based on its position and the audio
            deformation = amplitude * (1 + np.sin(vertex.x * 5 + frame * 0.1) * 
                                           np.cos(vertex.y * 5 + frame * 0.1) * 
                                           np.sin(vertex.z * 5 + frame * 0.1))
            deformed_vertex = vertex * (1 + deformation)
            
            # Color based on deformation
            glColor3f(deformation, 0.5 * deformation, 1 - deformation)
            glVertex3f(deformed_vertex.x, deformed_vertex.y, deformed_vertex.z)
        
        glEnd()
        
        # Rotate the view
        glRotatef(1, 3, 1, 1)
        
        pygame.display.flip()
        clock.tick(60)
        frame += 1

main()