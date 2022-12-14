#!/usr/bin/env python3
"""This is an example to train a task with SAC algorithm written in PyTorch."""
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F

from garage import wrap_experiment
from garage.envs import GymEnv, normalize
from garage.experiment import deterministic
from garage.replay_buffer import PathBuffer
from garage.sampler import FragmentWorker, LocalSampler
from garage.torch import set_gpu_mode
from garage.torch.algos import SAC
from garage.torch.policies import TanhGaussianMLPPolicy
from garage.torch.q_functions import ContinuousMLPQFunction
from garage.trainer import Trainer

import robosuite as suite
from robosuite.wrappers import GymWrapper


@wrap_experiment(snapshot_mode="none")
def robosuite_sac(ctxt=None, seed=1):
    """Set up environment and algorithm and run the task.
    Args:
        ctxt (garage.experiment.ExperimentContext): The experiment
            configuration used by Trainer to create the snapshotter.
        seed (int): Used to seed the random number generator to produce
            determinism.
    """
    deterministic.set_seed(seed)
    trainer = Trainer(snapshot_config=ctxt)

    # Create the robosuite environment
    suite_env = GymWrapper(
        suite.make(
            env_name="Lift",  # try with other tasks like "Stack" and "Door"
            robots="Panda",  # try with other robots like "Sawyer" and "Jaco"
            has_renderer=False,
            has_offscreen_renderer=True,
            use_camera_obs=False,
        )
    )

    # load robosuite Env as gym.Env into garage
    env = normalize(GymEnv(suite_env, is_image=False, max_episode_length=10))

    policy = TanhGaussianMLPPolicy(
        env_spec=env.spec,
        hidden_sizes=[256, 256],
        hidden_nonlinearity=nn.ReLU,
        output_nonlinearity=None,
        min_std=np.exp(-20.0),
        max_std=np.exp(2.0),
    )

    qf1 = ContinuousMLPQFunction(
        env_spec=env.spec, hidden_sizes=[256, 256], hidden_nonlinearity=F.relu
    )

    qf2 = ContinuousMLPQFunction(
        env_spec=env.spec, hidden_sizes=[256, 256], hidden_nonlinearity=F.relu
    )

    replay_buffer = PathBuffer(capacity_in_transitions=int(1e1))

    sampler = LocalSampler(
        agents=policy,
        envs=env,
        max_episode_length=env.spec.max_episode_length,
        worker_class=FragmentWorker,
        worker_args={"n_envs": 2},
        n_workers=2,
    )

    sac = SAC(
        env_spec=env.spec,
        policy=policy,
        qf1=qf1,
        qf2=qf2,
        sampler=sampler,
        gradient_steps_per_itr=10,
        max_episode_length_eval=10,
        replay_buffer=replay_buffer,
        min_buffer_size=1e1,
        target_update_tau=5e-3,
        discount=0.99,
        buffer_batch_size=256,
        reward_scale=1.0,
        steps_per_epoch=1,
    )

    if torch.cuda.is_available():
        set_gpu_mode(True)
    else:
        set_gpu_mode(False)
    sac.to()
    trainer.setup(algo=sac, env=env)
    trainer.train(n_epochs=10, batch_size=10)


s = np.random.randint(0, 1000)
robosuite_sac(seed=521)
