from delivery_env import AdaptiveDeliveryEnv
import numpy as np
from tasks import tasks

# Load the exact medium difficulty preset required by tasks.py
env = AdaptiveDeliveryEnv(**tasks["medium"])
state = env.reset()

total_reward = 0

for _ in range(200):
    action = np.random.choice(env.action_space)
    state, reward, done, _ = env.step(action)
    total_reward += reward
    if done:
        break

print("Final Score:", total_reward)
