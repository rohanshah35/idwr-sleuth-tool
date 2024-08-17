# Constants for universal use

from screeninfo import get_monitors

primary_monitor = get_monitors()[0]
screen_width = primary_monitor.width
screen_height = primary_monitor.height

FRAME_WIDTH = int(screen_width * 0.8)
FRAME_HEIGHT = int(screen_height * 0.8)

SUB_FRAME_WIDTH = int(FRAME_WIDTH * 0.8)
SUB_FRAME_HEIGHT = int(FRAME_HEIGHT * 0.9)
