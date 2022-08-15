#!/usr/bin/env python3
"""Example of how to load, step, and visualize an environment."""
import argparse

from garage.envs import GymEnv
from robosuite.wrappers import GymWrapper

import robosuite as suite


parser = argparse.ArgumentParser()
parser.add_argument("--n_steps", type=int, default=1000, help="Number of steps to run")
args = parser.parse_args()

# Create the robosuite environment
suite_env = GymWrapper(
    suite.make(
        env_name="Lift",  # try with other tasks like "Stack" and "Door"
        robots="Panda",  # try with other robots like "Sawyer" and "Jaco"
        has_renderer=True,
        has_offscreen_renderer=False,
        use_camera_obs=False,
    )
)

# load robosuite Env as gym.Env into garage
env = GymEnv(suite_env)

# Reset the environment and launch the viewer
env.reset()
env.visualize()

step_count = 0
es = env.step(env.action_space.sample())

while not es.last and step_count < args.n_steps:
    es = env.step(env.action_space.sample())
    step_count += 1

env.close()
