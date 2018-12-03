import sys
sys.path.append("game_th")

from timeit import default_timer as timer
import datetime

from game_th.Game import Game
from game_th.Env import Env
from game_th.AgentWrapper import AgentWrapper
from game_th.nnet.NNet import NNet


game = Game()
env = Env(game)
# nnet = NNet( (env.STATE_HISTORY_SIZE,) + game.state_shape(), game.get_num_actions())
nnet = NNet( (1,) + env.get_shape_with_history(), game.get_num_actions())

agentWrapper = AgentWrapper(env,nnet,game.get_num_actions())

start = timer()

agentWrapper.load_weights()
agentWrapper.train()
agentWrapper.save_weights()
agentWrapper.save_model()

end = timer()
print("Train time: " + str(datetime.timedelta(seconds=end - start)))