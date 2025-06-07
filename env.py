from typing import Optional
import pygame
import numpy as np
import gymnasium as gym


VIDE = -1
ROUGE = 0 #premier joueur
JAUNE = 1 #second joueur




class Puissance_4(gym.Env):
    def __init__(self, width=800, height=600, title="Puissance 4", render=True):
        super().__init__()
        self.width = width
        self.height = height
        self.title = title
        self.render_mode = "human" if render else None
        self.action_space = gym.spaces.Discrete(7)
        self.obs_dict = {}
        self.obs_dict["grid"] = gym.spaces.Box(low=0, high=2, shape=(6, 7), dtype=np.int8)
        self.obs_dict["turn"] = gym.spaces.Discrete(2)
        self.observation_space = gym.spaces.Dict(self.obs_dict)
        self.grid = np.ones((6, 7), dtype=np.int8) * (-1)
        self.turn = 0
        self.to_play = 0
        self.heights = [6] * 7



    def _get_obs(self):
        return {
            "grid": self.grid.copy(),
            "to_play": self.to_play
        }

    def _get_info(self):
        return {}



    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        super().reset(seed=seed)
        self.grid = np.ones((6, 7), dtype=np.int8) * (-1)
        self.to_play = 0
        self.turn = 0        
        self.heights = [6] * 7   

        return self._get_obs(), {}

    def step(self, action):
        reward = 0 
        jeton = self.to_play
        action = np.clip(action, 0, 6)
        if self.grid[0][action] != VIDE :
            reward = -100
            terminated = True
        else:
            self.heights[action] -=1
            pos = np.array([self.heights[action], action])
            

            self.grid[tuple(pos)] = jeton


            def check_direction(env, pos, jeton, direction):
                s = 0
                for i in range(1,4):
                    to_check = pos + i * direction 
                    print(to_check)
                    if to_check[0] > 5 or to_check[0] < 0 or to_check[1] > 6 or to_check[1] < 0 :
                        
                        print('pass')
                        break 
                    
                    print(env.grid[tuple(to_check)])
                    if env.grid[tuple(to_check)] == jeton:
                        s += 1
                    else:
                        break
                return s
            
            directions = [[1, 0], [1, 1], [0, 1], [-1, 1]]
            
            terminated = False

            for dir in directions:
                score = check_direction(self, pos, jeton, np.array(dir)) + check_direction(self, pos, jeton, -np.array(dir)) 

                if score >= 3:
                    terminated = True 
                    reward = 100
        info = self._get_info()

                    
        self.to_play = (self.to_play +1 ) % 2

        return self._get_obs(), reward , terminated, False, info 


    def display(self):
        for i in range(6):
            l = []
            for j in range(7):
                l.append(str(self.grid[i,j]))
                if self.grid[i,j] != -1:
                    l.append(' ')
                l.append('  ')
            print(''.join(l))
            print()
        if self.to_play == 0:
            print(f'Choix du joueur rouge')
        elif self.to_play == 1:
            print(f'Choix du joueur jaune')

if __name__ == "__main__":
    a = Puissance_4()
    a.reset()
    a.display()
    while True :
        action = int(input())
        obs, rew, terminated, _, info = a.step(action)
        a.display()
        print(rew)
        if terminated :
            break
    print("Everything went fine")
