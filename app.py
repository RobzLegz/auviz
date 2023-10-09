import pygame
import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import os
import random

def random_rgb_color():
    r = random.random()
    g = random.random()
    b = random.random()
    return (r, g, b)

# Parameters for audio capture and visualization
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
FPS = 60

# Initialize Pygame and set the display mode to fullscreen
pygame.init()
screen_info = pygame.display.Info()
screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h))
pygame.display.set_caption("Real-time Audio Visualizer")

# Create a clock object to control frame rate
clock = pygame.time.Clock()

# Initialize PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE)

# Main visualization loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read audio data from the microphone
    audio_data = stream.read(CHUNK_SIZE)
    audio_array = np.frombuffer(audio_data, dtype=np.int16)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Create a new Matplotlib figure for each frame
    plt.figure(figsize=(screen_info.current_w / 100, screen_info.current_h / 100), facecolor='black')

    # Plot the waveform of the microphone input with a random color
    c = random_rgb_color()
    plt.plot(audio_array, color=c)
    plt.xlim(0, len(audio_array))
    plt.ylim(-32768, 32768)  # Adjust the y-axis range as needed
    plt.axis('off')

    # Save the plot to a temporary image file
    plt.savefig("./tmp/temp_plot.png", bbox_inches='tight', dpi=100, transparent=True)

    # Load and display the temporary image on the Pygame screen
    plot_img = pygame.image.load("./tmp/temp_plot.png")
    screen.blit(plot_img, (0, 0))

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

    # Close the Matplotlib figure to avoid overlapping
    plt.close()

# Clean up
stream.stop_stream()
stream.close()
audio.terminate()
pygame.quit()
