import pyaudio
import numpy as np
import pygame
import librosa

class Geometry(object):
    def __init__(self):
        self.WINDOW_WIDTH = 1080
        self.WINDOW_HEIGHT = 720
        self.FPS = 60

    def go(self):
        # Pygame initialization
        pygame.init()
        screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Audio Visualizer")
        clock = pygame.time.Clock()

        # Initialize the microphone input
        p = pyaudio.PyAudio()
        input_stream = p.open(format=pyaudio.paFloat32,
                            channels=1,
                            rate=44100,
                            input=True,
                            frames_per_buffer=1024)

        # List to store lines
        lines = []

        # Function to draw lines
        def draw_lines():
            for line in lines:
                x1, y1, x2, y2, color = line
                pygame.draw.line(screen, color, (x1, y1), (x2, y2), 2)

        # Function to update the plot
        def update_plot(frame):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # Read audio data
            audio_data = np.frombuffer(frame, dtype=np.float32)

            # Calculate the volume (root mean square)
            volume = np.sqrt(np.mean(audio_data**2))
            
            if volume > 0:
                # Random starting point
                line_x1 = np.random.randint(0, self.WINDOW_WIDTH)
                line_y1 = np.random.randint(0, self.WINDOW_HEIGHT)
                
                # Random color
                color = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
                
                # Calculate line length based on volume
                line_length = int(volume * 200)  # Adjust the multiplier for line length
                
                # Random line angle
                line_angle = np.random.uniform(0, 2 * np.pi)
                
                line_x2 = line_x1 + line_length * np.cos(line_angle)
                line_y2 = line_y1 + line_length * np.sin(line_angle)
                
                # Add the new line to the list
                lines.append((line_x1, line_y1, line_x2, line_y2, color))
                
                # Limit the list to 100 lines
                if len(lines) > 200:
                    lines.pop(0)
                
                screen.fill((0, 0, 0))
                draw_lines()
                pygame.display.update()

        # Start audio streaming and visualization
        running = True
        while running:
            try:
                frame = input_stream.read(1024)
                update_plot(frame)
                clock.tick(self.FPS) 
            except KeyboardInterrupt:
                running = False

        # Close the audio stream and Pygame
        input_stream.stop_stream()
        input_stream.close()
        p.terminate()
        pygame.quit()

if __name__ == "__main__":
    anim = Geometry()
    anim.go()