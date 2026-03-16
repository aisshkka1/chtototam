import pygame
import os
import datetime

# Set working directory to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

_image_library = {}

def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image is None:
        canonicalized_path = path.replace("/", os.sep).replace("\\", os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[canonicalized_path] = image
    return image

def blitRotate(screen, img, pos, angle):
    rotated_img = pygame.transform.rotate(img, angle)
    new_rect = rotated_img.get_rect(center=img.get_rect(center=pos).center)
    screen.blit(rotated_img, new_rect.topleft)

pygame.init()
done = False

screen = pygame.display.set_mode((1200, 800))
w, h = screen.get_size()
bg = pygame.transform.scale(get_image("images/mainclock.png"), (w, h))
pygame.display.set_caption("Mickey's Clock")

# Synchronize the clock time with the real time
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Get the current time
    current_time = datetime.datetime.now()

    # Calculate the minutes and seconds based on real-time
    minutes = current_time.minute
    seconds = current_time.second

    # Calculate angles for the minute and second hands
    angle_min = -6 * minutes +53  # Each minute = 6 degrees (360 degrees / 60 minutes)
    angle_sec = -6 * seconds-60  # Each second = 6 degrees

    pos = (screen.get_width() / 2, screen.get_height() / 2)
    screen.blit(bg, (0, 0))

    # Draw the rotated arms based on the calculated angles
    blitRotate(screen, get_image("images/leftarm.png"), pos, angle_sec)
    blitRotate(screen, get_image("images/rightarm.png"), pos, angle_min)

    pygame.display.flip()

    # Delay to maintain consistent frame rate (60 FPS)
    pygame.time.delay(16)  # 1000ms / 60 = ~16ms delay for 60fps
