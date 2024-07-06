import numpy as np
import pygame
from pygame.math import Vector3
from OpenGL.GL import *
from OpenGL.GLU import *
from scipy.io import wavfile
from scipy.signal import resample
from scipy.ndimage import gaussian_filter1d
from PyQt5.QtWidgets import QApplication, QFileDialog

# Function to open a file dialog and return the selected file path
def get_audio_file():
    app = QApplication([])  # Initialize the Qt application
    options = QFileDialog.Options()  # Set options for the file dialog
    file_path, _ = QFileDialog.getOpenFileName(None, "Select an Audio File", "", "Audio Files (*.wav)", options=options)
    return file_path

# Select and load the audio file (WAV)
audio_file = get_audio_file()
if not audio_file:
    print("No audio file selected. Exiting.")  # Exit if no file is selected
    quit()

# Initialize Pygame and OpenGL
pygame.init()
pygame.mixer.init()
info = pygame.display.Info()
display = (info.current_w, info.current_h)  # Get the current screen resolution
pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL | pygame.FULLSCREEN)
pygame.display.set_caption("3D Music Viz")

# Set up the 3D view
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)  # Set the perspective projection
glTranslatef(0.0, 0.0, -5)  # Move the camera back

# Load and play the selected audio file
pygame.mixer.music.load(audio_file)
pygame.mixer.music.play()

# Load the audio data for analysis
sample_rate, audio_data = wavfile.read(audio_file)  # Read the audio file
audio_data = audio_data.astype(float)  # Convert audio data to float
if len(audio_data.shape) > 1:
    audio_data = np.mean(audio_data, axis=1)  # Convert stereo to mono if necessary

# Resample audio data to match the frame rate
target_sample_rate = 60  # Matches our frame rate
audio_data = resample(audio_data, int(len(audio_data) * target_sample_rate / sample_rate))

# Apply smoothing to the audio data
audio_data = gaussian_filter1d(np.abs(audio_data), sigma=2)

# Normalize audio data
audio_data = audio_data / np.max(np.abs(audio_data))

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
            
            vertices.append(Vector3(x, y, z))  # Append the vertex to the list
    
    return vertices

# Create the initial sphere
sphere_vertices = create_sphere(1, 40, 40)

# Main loop
def main():
    clock = pygame.time.Clock()  # Create a clock object to control the frame rate
    frame = 0  # Initialize the frame counter
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit the program if the window is closed
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()  # Quit the program if the Escape key is pressed
                    quit()

        if frame >= len(audio_data):
            break  # Exit the loop if all audio data has been processed
        
        # Get the current audio amplitude
        amplitude = audio_data[frame]
        
        # Clear the screen and prepare for rendering
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBegin(GL_POINTS)
        
        # Render deformed sphere
        for i, vertex in enumerate(sphere_vertices):
            # Create a unique deformation for each vertex based on its position and the audio
            deformation = amplitude * 0.75 * (1 + np.sin(vertex.x * 10 + frame * 0.1) * 
                                           np.cos(vertex.y * 10 + frame * 0.1) * 
                                           np.sin(vertex.z * 10 + frame * 0.1))
            deformed_vertex = vertex * (1 + deformation)
            
            # Dynamic color based on deformation and position
            r = 0.5 + 0.5 * np.sin(deformation * 5 + frame * 0.05)
            g = 0.5 + 0.5 * np.cos(deformation * 5 + frame * 0.03)
            b = 0.5 + 0.5 * np.sin(deformation * 5 + frame * 0.07)
            
            glColor3f(r, g, b)
            glVertex3f(deformed_vertex.x, deformed_vertex.y, deformed_vertex.z)
        
        glEnd()
        
        # Rotate the view
        glRotatef(1, 3, 1, 1)
        
        pygame.display.flip()  # Update the display
        clock.tick(60)  # Maintain a frame rate of 60 FPS
        frame += 1  # Increment the frame counter

main()  # Run the main loop
