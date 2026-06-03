import habitat_sim
import cv2
import os

# 1. Point Habitat to your brand new Custom Mesh!
backend_cfg = habitat_sim.SimulatorConfiguration()
backend_cfg.scene_id = "custom_scene.ply" 

# 2. Configure Agent and Custom Actions
agent_cfg = habitat_sim.agent.AgentConfiguration()

# By default, Habitat has forward, left, right. We need to manually add backward!
agent_cfg.action_space = {
    "move_forward": habitat_sim.agent.ActionSpec("move_forward", habitat_sim.agent.ActuationSpec(amount=0.25)),
    "move_backward": habitat_sim.agent.ActionSpec("move_backward", habitat_sim.agent.ActuationSpec(amount=0.25)),
    "turn_left": habitat_sim.agent.ActionSpec("turn_left", habitat_sim.agent.ActuationSpec(amount=10.0)),
    "turn_right": habitat_sim.agent.ActionSpec("turn_right", habitat_sim.agent.ActuationSpec(amount=10.0)),
}

# Add an RGB Sensor to see where we are going
rgb_sensor = habitat_sim.CameraSensorSpec()
rgb_sensor.uuid = "color_sensor"
rgb_sensor.sensor_type = habitat_sim.SensorType.COLOR
rgb_sensor.resolution = [480, 640]
rgb_sensor.position = [0.0, 1.0, 0.0]
agent_cfg.sensor_specifications = [rgb_sensor]

cfg = habitat_sim.Configuration(backend_cfg, [agent_cfg])
sim = habitat_sim.Simulator(cfg)

# 3. Recompute NavMesh for your custom scene so the robot can walk on the floor
print("Building NavMesh for Custom Scene...")
navmesh_settings = habitat_sim.NavMeshSettings()
navmesh_settings.set_defaults()
sim.recompute_navmesh(sim.pathfinder, navmesh_settings)

agent = sim.get_agent(0)
# Spawn robot at a valid location
agent.set_state(agent.get_state().position, agent.get_state().rotation)

print("\n--- HABITAT ROBOT CONTROL ---")
print("Controls: 'w' (forward), 's' (backward), 'a' (left), 'd' (right), 'q' (quit)")

# 4. Interactive Terminal Control Loop
os.makedirs("custom_outputs", exist_ok=True)
frame_count = 0

while True:
    keystroke = input("Action (w/a/s/d/q): ").strip().lower()
    
    if keystroke == 'q':
        break
    elif keystroke == 'w':
        action = "move_forward"
    elif keystroke == 's':
        action = "move_backward"
    elif keystroke == 'a':
        action = "turn_left"
    elif keystroke == 'd':
        action = "turn_right"
    else:
        print("Invalid key. Use w/a/s/d or q to quit.")
        continue

    # Take the step in the simulator
    observations = sim.step(action)
    
    # Save the frame to disk so you can see what the robot sees
    bgr_img = cv2.cvtColor(observations["color_sensor"], cv2.COLOR_RGBA2BGR)
    cv2.imwrite(f"custom_outputs/frame_{frame_count:04d}.png", bgr_img)
    print(f"Moved {action}. Saved view to custom_outputs/frame_{frame_count:04d}.png")
    frame_count += 1

sim.close()
