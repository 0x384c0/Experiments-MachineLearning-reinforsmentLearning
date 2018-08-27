# number helpers
def clamp(n, smallest, largest): 
  return max(smallest, min(n, largest))

#env vars
import os

def is_human_player_mode():
  return os.getenv('HUMAN_PLAYER_MODE', "False") == "True"

def is_render():
  return os.getenv('RENDER', "False") == "True"
