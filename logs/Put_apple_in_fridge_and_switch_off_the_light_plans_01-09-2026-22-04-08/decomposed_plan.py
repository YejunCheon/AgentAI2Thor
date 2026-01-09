To accomplish the task of putting an apple in the fridge and switching off the light, we can decompose the task into two independent subtasks that can be executed in parallel:

### SubTask 1: Put an Apple in the Fridge
This subtask involves the following steps:

1. **GoToObject (Robot, Apple)**
   - **Parameters:** `?robot`, `?apple`
   - **Preconditions:** `(not (inaction ?robot))`
   - **Effects:** `(at ?robot ?apple)`, `(not (inaction ?robot))`

2. **PickupObject (Robot, Apple, AppleLocation)**
   - **Parameters:** `?robot`, `?apple`, `?appleLocation`
   - **Preconditions:** `(at-location ?apple ?appleLocation)`, `(at ?robot ?appleLocation)`, `(not (inaction ?robot))`
   - **Effects:** `(holding ?robot ?apple)`, `(not (inaction ?robot))`

3. **GoToObject (Robot, Fridge)**
   - **Parameters:** `?robot`, `?fridge`
   - **Preconditions:** `(not (inaction ?robot))`
   - **Effects:** `(at ?robot ?fridge)`, `(not (inaction ?robot))`

4. **OpenObject (Robot, Fridge)**
   - **Parameters:** `?robot`, `?fridge`
   - **Preconditions:** `(not (inaction ?robot))`, `(at ?robot ?fridge)`, `(is-fridge ?fridge)`
   - **Effects:** `(object-open ?robot ?fridge)`, `(increase (fridge-state ?fridge) 1)`, `(not (inaction ?robot))`

5. **PutObject (Robot, Apple, Fridge)**
   - **Parameters:** `?robot`, `?apple`, `?fridge`
   - **Preconditions:** `(holding ?robot ?apple)`, `(at ?robot ?fridge)`, `(not (inaction ?robot))`
   - **Effects:** `(at-location ?apple ?fridge)`, `(not (holding ?robot ?apple))`, `(not (inaction ?robot))`

6. **CloseObject (Robot, Fridge)**
   - **Parameters:** `?robot`, `?fridge`
   - **Preconditions:** `(not (inaction ?robot))`, `(at ?robot ?fridge)`, `(object-open ?robot ?fridge)`, `(is-fridge ?fridge)`
   - **Effects:** `(object-close ?robot ?fridge)`, `(decrease (fridge-state ?fridge) 1)`, `(not (inaction ?robot))`

### SubTask 2: Switch Off the Light
This subtask involves the following steps:

1. **GoToObject (Robot, LightSwitch)**
   - **Parameters:** `?robot`, `?lightSwitch`
   - **Preconditions:** `(not (inaction ?robot))`
   - **Effects:** `(at ?robot ?lightSwitch)`, `(not (inaction ?robot))`

2. **SwitchOff (Robot, LightSwitch)**
   - **Parameters:** `?robot`, `?lightSwitch`
   - **Preconditions:** `(not (inaction ?robot))`, `(at ?robot ?lightSwitch)`
   - **Effects:** `(switch-off ?robot ?lightSwitch)`, `(not (inaction ?robot))`

### Execution Plan
- **Parallel Execution:** SubTask 1 and SubTask 2 can be executed in parallel as they do not depend on each other.
- **Robot Assignment:** Assign one robot to each subtask to maximize efficiency.

By following this decomposition and execution plan, the task of putting an apple in the fridge and switching off the light can be efficiently completed.