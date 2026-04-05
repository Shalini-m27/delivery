import os
import asyncio
from openai import AsyncOpenAI
import numpy as np
from delivery_env import AdaptiveDeliveryEnv
from tasks import tasks

# Mandatory Runtime Variables from Check-list
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.getenv("HF_TOKEN", "fake-token")

if HF_TOKEN == "fake-token":
    raise ValueError("CRITICAL: Please set the HF_TOKEN environment variable before launching evaluating framework.")

TASK_NAME = os.getenv("TASK_NAME", "medium")
BENCHMARK = os.getenv("BENCHMARK", "adaptive-delivery-env")

# --- Strict Evaluation Logging Guidelines ---
def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: str = None):
    err_str = f" error={error}" if error else ""
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={done}{err_str}", flush=True)

def log_end(success: bool, steps: int, score: float, rewards: list):
    print(f"[END] success={success} steps={steps} score={score:.2f}", flush=True)

async def get_model_action(client, state_text, step):
    try:
        completion = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a logistics routing AI evaluating an MDP matrix. Valid actions are strictly single numbers: 0 (Up), 1 (Down), 2 (Left), 3 (Right). Reply ONLY with the single digit corresponding to the safest step."},
                {"role": "user", "content": f"Current Live Vector State: {state_text}"}
            ],
            temperature=0.0,
            max_tokens=10,
        )
        msg = completion.choices[0].message.content.strip()
        
        # Parse inference robustly
        if msg in ["0", "1", "2", "3"]:
            action = int(msg)
        else:
            action = int(np.random.choice([0,1,2,3]))
            
        # Basic heuristic backup preventing systemic logic loops
        if np.random.rand() < 0.2:
            action = int(np.random.choice([0,1,2,3]))
            
        return action, str(action)
    except Exception as exc:
        print(f"[DEBUG] Model request failed: {exc}", flush=True)
        return np.random.choice([0,1,2,3]), "error_survivor_action"

async def main():
    client = AsyncOpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)
    
    # Initialize the required OpenEnv format logic
    task_config = tasks.get(TASK_NAME, tasks["medium"])  # Fallback to medium safely
    env_instance = AdaptiveDeliveryEnv(**task_config)
    state = env_instance.reset()

    rewards = []
    steps_taken = 0
    score = 0.0
    success = False
    
    MAX_STEPS = 200

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

    try:
        for step in range(1, MAX_STEPS + 1):
            state_text = str(state.tolist() if hasattr(state, 'tolist') else state)
            
            # 1. Inference Call to LLM
            action_val, msg = await get_model_action(client, state_text, step)
            
            # 2. OpenEnv Physical Step Evaluation
            state, reward, done, _ = env_instance.step(action_val)
            
            rewards.append(reward)
            steps_taken = step
            
            # 3. Formatted Rubric Print
            log_step(step=step, action=msg, reward=reward, done=done, error=None)

            if done:
                break
                
        # Hackathon Spec Normalize validation (strictly [0.0, 1.0])
        score = sum(rewards) / len(rewards) if rewards else 0.0
        success = score > 0.0
        
    except Exception as error:
        print(f"[DEBUG] Runtime collision explicitly aborted: {error}")
        
    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

if __name__ == "__main__":
    asyncio.run(main())
