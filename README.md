# 🌍 MetaLogistics: Adaptive AI Delivery Network

An AI-powered logistics simulation platform demonstrating real-time adaptive routing using Reinforcement Learning on real-world maps.

---

## 🚀 Overview

MetaLogistics is designed to simulate how modern delivery systems can operate under **uncertain and dynamic conditions** such as:

- Traffic congestion 🚦  
- Road closures / disasters 🌋  
- Fuel constraints ⛽  

Unlike traditional routing systems, this project focuses on **adaptive decision-making** using AI.

---

## 🧠 Core Idea

We model the delivery problem as a **Markov Decision Process (MDP)** and integrate:

- Reinforcement Learning (DQN / PPO ready)
- Real-world road networks
- Dynamic environment disruptions

The agent learns to:
- Optimize delivery routes  
- Adapt to real-time changes  
- Minimize fuel usage  
- Maximize successful deliveries  

---

## 🔑 Key Features

### 🌐 Real-World Routing
- Powered by Open Source Routing Machine (OSRM)
- Uses OpenStreetMap road network data

### 🧭 Global Geocoding
- Search and navigate any location using Nominatim API
- Dynamic map relocation anywhere in the world

### 🚚 Adaptive Delivery Agent
- Moves across real-world map coordinates
- Reacts to environment changes in real-time

### ⚡ Live Disruption System
Inject real-world challenges:
- Traffic zones (increased cost)
- Disaster blocks (road closures)
- Fuel leaks (resource constraint)

### 📊 RL-Ready Environment
- Compatible with Stable-Baselines3
- Structured observation space
- Normalized reward system (0.0 – 1.0)

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Mapping:** Leaflet.js
- **Routing:** OSRM API
- **Geocoding:** Nominatim (OpenStreetMap)
- **Backend / Simulation:** Python
- **AI Framework:** Reinforcement Learning (DQN / PPO ready)

---

## 🧪 Simulation Environment

```yaml
Environment: AdaptiveDeliveryEnv
Observation Space: Vector (agent, fuel, packages, targets)
Action Space: Discrete (Up, Down, Left, Right)
Reward Range: [0.0, 1.0]
