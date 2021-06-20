import pygame
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.deepq.policies import MlpPolicy, CnnPolicy, LnMlpPolicy
from stable_baselines import DQN
from stable_baselines.common.evaluation import evaluate_policy
from Construction3DEnv_h import Construct3DEnvObs
from Construction3DEnv_run import Construct3DEnvObsRun

# it is from fang
# from interface import Construct3DEnvObs

# IMPORT PYGAME AND OPENGL
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from drawSite import draw_site

# IMPORT SYS
import time
import os

import gym
import numpy as np
import matplotlib.pyplot as plt

from stable_baselines import results_plotter
from stable_baselines.bench import Monitor
from stable_baselines.results_plotter import load_results, ts2xy
from stable_baselines.common.noise import AdaptiveParamNoiseSpec
from stable_baselines.common.callbacks import BaseCallback
from callback import SaveOnBestTrainingRewardCallback




class SaveOnBestTrainingRewardCallback(BaseCallback):
    """
    Callback for saving a model (the check is done every ``check_freq`` steps)
    based on the training reward (in practice, we recommend using ``EvalCallback``).

    :param check_freq: (int)
    :param log_dir: (str) Path to the folder where the model will be saved.
      It must contains the file created by the ``Monitor`` wrapper.
    :param verbose: (int)
    """
    def __init__(self, check_freq: int, log_dir: str, verbose=1):
        super(SaveOnBestTrainingRewardCallback, self).__init__(verbose)
        self.check_freq = check_freq
        self.log_dir = log_dir
        self.save_path = os.path.join(log_dir, 'best_model')
        self.save_test_path = os.path.join(log_dir, 'test_model')
        self.best_mean_reward = -np.inf

    def _init_callback(self) -> None:
        # Create folder if needed
        if self.save_path is not None:
            os.makedirs(self.save_path, exist_ok=True)

    def _on_step(self) -> bool:
        if self.n_calls % self.check_freq == 0:

          # Retrieve training reward
          x, y = ts2xy(load_results(self.log_dir), 'timesteps')
          if len(x) > 0:
              # Mean training reward over the last 100 episodes
              mean_reward = np.mean(y[-100:])
              if self.verbose > 0:
                print("Num timesteps: {}".format(self.num_timesteps))
                print("Best mean reward: {:.2f} - Last mean reward per episode: {:.2f}".format(self.best_mean_reward, mean_reward))

              # New best model, you could save the agent here
              if mean_reward > self.best_mean_reward:
                  self.best_mean_reward = mean_reward
                  # Example for saving best model
                  if self.verbose > 0:
                    print("Saving new best model to {}".format(self.save_path))
                  self.model.save(self.save_path)

          if self.num_timesteps%100 == 0:
              print("Saving new test model to {}".format(self.save_test_path))
              self.model.save(self.save_test_path)

        return True


learn = False
test = True
test_success_rate = False
display = True

# Create log dir
log_dir = "C:\\Users\\PANDZAY\\Desktop\\model\\column"
os.makedirs(log_dir, exist_ok=True)

# Create and wrap the environment
env = Construct3DEnvObs()
env = Monitor(env, log_dir)

# if learn
if learn is True:

    # # Create the callback: check every 1000 steps
    callback = SaveOnBestTrainingRewardCallback(check_freq=10000, log_dir=log_dir)
    param_noise = AdaptiveParamNoiseSpec(initial_stddev=0.1, desired_action_stddev=0.1)
    model = DQN(LnMlpPolicy, env, prioritized_replay=True, double_q=True, batch_size=64,)
    # model = DQN.load("deep_construction3D_unit", env)
    # model = DQN.load("deep_construction3D_all_site_beam.zip")   # Train the agent
    time_steps = 500000
    model.learn(total_timesteps=int(time_steps), callback=callback, feedback_success=20000, feedback_reward=20000, env_id=2)

    # Draw picture
    plt.plot(np.arange(len(env.success_rate)), env.success_rate)
    plt.ylabel('Episode Success Rate')
    plt.xlabel('Episodes')
    results_plotter.plot_results([log_dir], time_steps, results_plotter.X_TIMESTEPS, "DQN column learning part")
    plt.show()

    model.save("deep_construction3D_col")


# if test
if test is True:
    env_test = Construct3DEnvObs()
    success = 0
    success_rate = []

    # del model  # remove to demonstrate saving and loading
    # model = DQN.load("deep_construction3D.zip")
    model = DQN.load("C:\\Users\\PANDZAY\\Desktop\\model\\column\\test_model.zip",env=env_test)
    # model.set_env(env)

    # testing
    if test_success_rate is True:
        times = 0
        obs = env_test.reset()
        while times < 500:
            action, _states = model.predict(obs)
            obs, rewards, dones, info = env_test.step(action)
            # print("reward", rewards)
            if dones is True:
                times += 1
                if rewards == 1:
                    success += 1
                rate = success / times
                success_rate.append(rate)
                obs = env_test.reset()
        plt.plot(np.arange(len(success_rate)), success_rate)
        plt.ylabel('Success rate (%) of testing')
        plt.xlabel('Episodes of training')
        plt.show()


        #
        # success = 0
        # times = 0
        # success_rate = []
        # # unit = str(feedback_success)
        # obs = env.reset()
        # while times < 100:
        #     action, _states = model.predict(obs)
        #     obs, rewards, dones, info = env.step(action)
        #     print("reward",rewards)
        #     if dones is True:
        #         times += 1
        #         if rewards == 1:
        #             success += 1
        #             print('success', success)
        #             rate = success / times
        #             print('rate', rate)
        #     obs = env.reset()
        # print(rate)
        # success_rate.append(rate)
        # plt.plot(np.arange(len(success_rate)), success_rate)
        # # plt.legend(loc='upper right')
        # plt.ylabel('Success rate (%) of testing')
        # plt.xlabel( 'steps of training')
        # plt.show()




    if display is True:
        # #
        obs = env_test.reset()
        # INIT PYGAME
        pygame.init()
        display = (1200, 800)

        # INIT PYGAME DISPLAY AND OPENGL
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        gluPerspective(25, display[0] / display[1], 0.1, 50.0)
        glTranslate(1, 0, -5)
        glRotatef(35, 1, 0, 0)
        glOrtho(0, 1000, 0, 1000, 0, 1000)
        glEnable(GL_DEPTH_TEST)

        # RENDER POSITION
        rotate_x = 0
        rotate_y = 0
        translate_x = 0
        translate_y = 0
        z_position = 0

        # MOUSE INPUTS
        mouse_rotate = False
        mouse_move = False

        # MAIN GAME LOOP
        pygame.key.set_repeat(16, 100)
        in_game = True
        open_map = False
        show_steps = True
        # time.sleep(6)

        while in_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    in_game = False
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_rotate = True
                    elif event.button == 3:
                        mouse_move = True
                    elif event.button == 5:
                        translate_y -= 50
                    elif event.button == 4:
                        translate_y += 50
                elif event.type == MOUSEBUTTONUP:
                    mouse_rotate = False
                    mouse_move = False
                elif event.type == MOUSEMOTION:
                    i, j = event.rel
                    if mouse_move:
                        translate_x += i
                        translate_y += j
                    elif mouse_rotate:
                        rotate_x += i
                        rotate_y += j
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        z_position -= 50
                    elif event.key == K_DOWN:
                        z_position += 50
                    elif event.key == K_LEFT:
                        translate_x -= 50
                    elif event.key == K_RIGHT:
                        translate_x += 50
                    elif event.key == 113:
                        rotate_x -= 50
                    elif event.key == 101:
                        rotate_x += 50

            if in_game:
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

                action, _states = model.predict(obs)
                # print('it is action', action)
                obs, rewards, dones, info = env_test.step(action)
                # print('it is crash', env_test.siteEnv.sco.crash)
                if env_test.siteEnv.sco.crash is True:
                    callback = SaveOnBestTrainingRewardCallback(check_freq=1000, log_dir=log_dir)
                    time_steps = 5000000
                    model.learn(total_timesteps=int(time_steps), callback=callback, feedback_reward=2000,feedback_success=2000,env_id=2)
                # print('it is rewards', rewards)
                draw_site(env_test.state_render)
                if dones is True:
                    # time.sleep(1)
                    obs = env_test.reset()
                time.sleep(1)
                # TRANSLATE OBJECT IF MOUSE MOVED
                glTranslatef(translate_x, translate_y, -z_position)
                glRotatef(rotate_y / 20., 1, 0, 0)
                glRotatef(rotate_x / 20., 0, 1, 0)

                # RESET ROTATE
                rotate_x = 0
                rotate_y = 0
                translate_x = 0
                translate_y = 0
                z_position = 0
                pygame.display.flip()

            else:
                pygame.quit()






