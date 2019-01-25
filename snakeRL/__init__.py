from gym.envs.registration import register

register(
    id='snakeRL-v0',
    entry_point='snakeRL.envs:SnakeEnv',
)