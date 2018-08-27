from timeit import default_timer as timer
import datetime

from game_th.Game import Game
from game_th.Env import Env
from game_th.AgentWrapper import AgentWrapper


game = Game()
env = Env(game)

agentWrapper = AgentWrapper(env,game.state_shape(),game.get_num_actions())

start = timer()

agentWrapper.load_weights()
agentWrapper.train()
agentWrapper.save_weights()

end = timer()
print("Train time: " + str(datetime.timedelta(seconds=end - start)))