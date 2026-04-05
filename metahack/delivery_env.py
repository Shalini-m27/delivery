"""
OPENENV METADATA (openenv.yaml structure)
-----------------------------------------
name: adaptive-delivery-env
version: 1.0

observation_space:
  type: vector
  description: agent position, fuel, package & delivery states

action_space:
  type: discrete
  actions: [0,1,2,3]

reward_range: [0.0, 1.0]
"""

import numpy as np

# EXPLICIT TASKS DEFINITION
tasks = {
    "easy": {"num_packages": 1, "max_fuel": 100},
    "medium": {"num_packages": 2, "max_fuel": 80},
    "hard": {"num_packages": 3, "max_fuel": 60}
}

class AdaptiveDeliveryEnv:
    def __init__(self, grid_size=10, num_packages=3, max_fuel=100):
        self.grid_size = grid_size
        self.num_packages = num_packages 
        self.max_fuel = max_fuel 
        
        # Action space: 0: Up, 1: Down, 2: Left, 3: Right
        self.action_space = [0, 1, 2, 3]
        
        # Reward Range strictly parameterized
        self.reward_range = (0.0, 1.0)
        
        self.reset()
        
    def reset(self):
        self.fuel = self.max_fuel
        self.agent_pos = np.array([0, 0])
        
        self.package_locations = []
        self.delivery_locations = []
        for _ in range(self.num_packages):
            self.package_locations.append(np.random.randint(0, self.grid_size, size=2))
            self.delivery_locations.append(np.random.randint(0, self.grid_size, size=2))
            
        self.picked_up = [False] * self.num_packages
        self.delivered = [False] * self.num_packages
        
        self.packages_carried = 0
        self.delivered_count = 0
        
        return self.state()
        
    def step(self, action):
        if np.random.rand() < 0.1:
            action = np.random.choice(self.action_space)
            
        reward = 0.0  
        self.fuel -= 1
        
        if action == 0:   self.agent_pos[1] = min(self.grid_size - 1, self.agent_pos[1] + 1)
        elif action == 1: self.agent_pos[1] = max(0, self.agent_pos[1] - 1)
        elif action == 2: self.agent_pos[0] = max(0, self.agent_pos[0] - 1)
        elif action == 3: self.agent_pos[0] = min(self.grid_size - 1, self.agent_pos[0] + 1)
            
        for i, pkg_loc in enumerate(self.package_locations):
            if not self.picked_up[i] and np.array_equal(self.agent_pos, pkg_loc):
                self.picked_up[i] = True
                self.packages_carried += 1
                reward += 0.2  
                
        for i, del_loc in enumerate(self.delivery_locations):
            if self.picked_up[i] and not self.delivered[i] and np.array_equal(self.agent_pos, del_loc):
                self.delivered[i] = True
                self.packages_carried -= 1
                self.delivered_count += 1
                reward += 0.5  
                
        # Ceiling bounds
        reward = min(reward, 1.0)
                
        done = False
        if self.delivered_count == self.num_packages:
            done = True
            reward = 1.0   
        elif self.fuel <= 0:
            done = True
            reward = 0.0   
            
        return self.state(), reward, done, {}
        
    def state(self):
        state_vec = [self.agent_pos[0], self.agent_pos[1], self.fuel]
        for i in range(self.num_packages):
            state_vec.extend([
                self.package_locations[i][0], self.package_locations[i][1], int(self.picked_up[i]),
                self.delivery_locations[i][0], self.delivery_locations[i][1], int(self.delivered[i])
            ])
        return np.array(state_vec, dtype=np.float32)

if __name__ == "__main__":
    # BASELINE RUN SCRIPT
    print("--- Running Adaptive Delivery Baseline Test ---")
    
    # Implementing the 'medium' task preset explicitly from tasks lookup
    env = AdaptiveDeliveryEnv(**tasks["medium"])
    state = env.reset()

    total_reward = 0

    # Max iteration baseline test
    for _ in range(200):
        # Random step choice mimicking baseline agent behavior
        action = np.random.choice(env.action_space)
        state, reward, done, _ = env.step(action)
        total_reward += reward
        if done:
            break

    print(f"Test Evaluation Final Score: {total_reward:.2f}")
