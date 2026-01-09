To accomplish the task of putting an apple in the fridge and switching off the light, we can decompose it into two independent subtasks that can be executed in parallel. Given that all three robots have identical skills and mass capacities, any robot can perform either subtask. Here's how we can allocate the tasks:

### SubTask 1: Put an Apple in the Fridge
This subtask involves several steps:
1. **GoToObject (Robot, Apple)**
   - The robot moves to the location of the apple.
2. **PickupObject (Robot, Apple, AppleLocation)**
   - The robot picks up the apple from its current location.
3. **GoToObject (Robot, Fridge)**
   - The robot moves to the fridge.
4. **OpenObject (Robot, Fridge)**
   - The robot opens the fridge door.
5. **PutObject (Robot, Apple, Fridge)**
   - The robot places the apple inside the fridge.
6. **CloseObject (Robot, Fridge)**
   - The robot closes the fridge door.

### SubTask 2: Switch Off the Light
This subtask involves:
1. **GoToObject (Robot, LightSwitch)**
   - The robot moves to where the light switch is located.
2. **SwitchOff (Robot, LightSwitch)**
   - The robot switches off the light.

### Execution Plan
- Both subtasks are independent and can be executed in parallel since they do not depend on each other.

### Robot Assignment
- Assign `robot1` to SubTask 1: Put an Apple in the Fridge.
- Assign `robot2` to SubTask 2: Switch Off the Light.

Since all robots have identical skills and mass capacities:
- Each subtask is within their skill set as they all possess 'GoToObject', 'PickupObject', 'OpenObject', 'CloseObject', 'PutObject', and 'SwitchOff' skills required for these tasks.
- Each object involved has a mass well within each robot's capacity of 100 units.

By assigning one task per available robot and executing them concurrently where possible, we ensure efficient completion of both tasks using minimal resources while adhering to constraints on skills and object masses.