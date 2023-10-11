import pygame
import pyaudio
import numpy as np
import random

# Constants
WIDTH, HEIGHT = 800, 600
FRAMES_PER_BUFFER = 1024
MAX_SHAPES = 1  # Maximum number of shapes to display

SHAPE_TYPES = ['triangle', 'hexagon', 'rectangle']

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Microphone Visualizer")

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=44100,
    input=True,
    frames_per_buffer=1024
)
# List to store shape data
shapes = []

# Main loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    try:

        # Read audio data from the microphone
        audio_data = np.frombuffer(stream.read(FRAMES_PER_BUFFER), dtype=np.int16)

        # Calculate volume
        volume = np.abs(audio_data).mean()

        # Scale the size of the shapes based on volume
        size = int(volume / 2000 * 10)  # Adjust the scaling factor as needed
        print(volume)
        # Generate random shapes based on volume with random colors
        if volume > 2000:
            shape_type = random.choice(SHAPE_TYPES)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            if shape_type == 'triangle':
                new_shape = ('triangle', color, size)
            elif shape_type == 'hexagon':
                new_shape = ('hexagon', color, size)
            elif shape_type == 'rectangle':
                new_shape = ('rectangle', color, size)

            # Add the new shape to the list and limit the list to the last 20 shapes
            shapes.append(new_shape)
            if len(shapes) > MAX_SHAPES:
                shapes.pop(0)

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the shapes from the list
        for i, (shape_type, color, size) in enumerate(shapes):
            if shape_type == 'triangle':
                points = [
                    (random.randint(0, WIDTH), random.randint(0, HEIGHT)),
                    (random.randint(0, WIDTH), random.randint(0, HEIGHT)),
                    (random.randint(0, WIDTH), random.randint(0, HEIGHT))
                ]
                scaled_points = [(x, y) for x, y in points]

                scaled_size = int(size * (volume / 2000))  # Scale size based on volume

                for j in range(3):
                    scaled_points[j] = (points[j][0], points[j][1])

                pygame.draw.polygon(screen, color, scaled_points)
            elif shape_type == 'hexagon':
                points = [
                    (random.randint(0, WIDTH), random.randint(0, HEIGHT)),
                    (random.randint(0, WIDTH), random.randint(0, HEIGHT)),
                    (random.randint(0, WIDTH), random.randint(0, HEIGHT)),
                    (random.randint(0, WIDTH), random.randint(0, HEIGHT)),
                    (random.randint(0, WIDTH), random.randint(0, HEIGHT)),
                    (random.randint(0, WIDTH), random.randint(0, HEIGHT))
                ]
                scaled_points = [(x, y) for x, y in points]

                scaled_size = int(size * (volume / 2000))  # Scale size based on volume

                for j in range(6):
                    scaled_points[j] = (points[j][0], points[j][1])

                pygame.draw.polygon(screen, color, scaled_points)
            elif shape_type == 'rectangle':
                x = random.randint(0, WIDTH - size)
                y = random.randint(0, HEIGHT - size)

                scaled_size = int(size * (volume / 2000))  # Scale size based on volume

                rect = pygame.Rect(x, y, scaled_size, scaled_size)
                pygame.draw.rect(screen, color, rect)

        shapes = []

        pygame.display.flip()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Clean up
stream.stop_stream()
stream.close()
p.terminate()
pygame.quit()
