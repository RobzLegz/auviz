import pygame
import numpy as np
import matplotlib.pyplot as plt
import pyaudio

# Parameters for audio capture and visualization
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
FPS = 30

# Initialize Pygame
pygame.init()
screen_width, screen_height = 800, 400
screen = pygame.display.set_mode((screen_width, screen_height))
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

    # Plot the waveform of the microphone input
    plt.plot(audio_array)
    plt.xlim(0, len(audio_array))
    plt.ylim(-32768, 32768)  # Adjust the y-axis range as needed
    plt.axis('off')

    # Save the plot to a temporary image file
    plt.savefig("./tmp/temp_plot.png", bbox_inches='tight', pad_inches=0, dpi=100, transparent=True)

    # Load and display the temporary image on the Pygame screen
    plot_img = pygame.image.load("./tmp/temp_plot.png")
    screen.blit(plot_img, (0, 0))

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(FPS)

# Clean up
stream.stop_stream()
stream.close()
audio.terminate()
pygame.quit()
