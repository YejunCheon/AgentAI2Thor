To address the task of putting an apple in the fridge and switching off the light, we need to correct the subplans based on the initial plan examination and allocation examination. Then, we'll merge the subtasks using a timed durative actions format in PDDL, ensuring that parallel tasks are performed simultaneously. Here's the corrected and merged plan:

### Corrected SubPlans

#### SubTask 1: Put an Apple in the Fridge
1. **GoToObject (Robot, Apple)**
   - **Parameters:** `?robot`, `?apple`
   - **Preconditions:** `(not (inaction ?robot))`
   - **Effects:** `(at ?robot ?apple)`, `(not (inaction ?robot))`

2. **PickupObject (Robot, Apple)**
   - **Parameters:** `?robot`, `?apple`
   - **Preconditions:** `(at ?robot ?apple)`, `(not (inaction ?robot))`
   - **Effects:** `(holding ?robot ?apple)`, `(not (inaction ?robot))`

3. **GoToObject (Robot, Fridge)**
   - **Parameters:** `?robot`, `?fridge`
   - **Preconditions:** `(not (inaction ?robot))`
   - **Effects:** `(at ?robot ?fridge)`, `(not (inaction ?robot))`

4. **OpenObject (Robot, Fridge)**
   - **Parameters:** `?robot`, `?fridge`
   - **Preconditions:** `(at ?robot ?fridge)`, `(is-fridge ?fridge)`, `(not (inaction ?robot))`
   - **Effects:** `(object-open ?fridge)`, `(not (inaction ?robot))`

5. **PutObject (Robot, Apple, Fridge)**
   - **Parameters:** `?robot`, `?apple`, `?fridge`
   - **Preconditions:** `(holding ?robot ?apple)`, `(at ?robot ?fridge)`, `(not (inaction ?robot))`
   - **Effects:** `(at-location ?apple ?fridge)`, `(not (holding ?robot ?apple))`, `(not (inaction ?robot))`

6. **CloseObject (Robot, Fridge)**
   - **Parameters:** `?robot`, `?fridge`
   - **Preconditions:** `(at ?robot ?fridge)`, `(object-open ?fridge)`, `(is-fridge ?fridge)`, `(not (inaction ?robot))`
   - **Effects:** `(object-close ?fridge)`, `(not (inaction ?robot))`

#### SubTask 2: Switch Off the Light
1. **GoToObject (Robot, LightSwitch)**
   - **Parameters:** `?robot`, `?lightSwitch`
   - **Preconditions:** `(not (inaction ?robot))`
   - **Effects:** `(at ?robot ?lightSwitch)`, `(not (inaction ?robot))`

2. **SwitchOff (Robot, LightSwitch)**
   - **Parameters:** `?robot`, `?lightSwitch`
   - **Preconditions:** `(at ?robot ?lightSwitch)`, `(not (inaction ?robot))`
   - **Effects:** `(switch-off ?lightSwitch)`, `(not (inaction ?robot))`

### Merged Plan in Timed Durative Actions Format (PDDL)

```lisp
; PDDL Plan
0.0: (gotoobject robot1 apple)
0.0: (gotoobject robot2 lightswitch)
1.0: (pickupobject robot1 apple)
2.0: (gotoobject robot1 fridge)
3.0: (openobject robot1 fridge)
4.0: (putobject robot1 apple fridge)
5.0: (closeobject robot1 fridge)
1.0: (switchoff robot2 lightswitch)
```

### Explanation
- The plan starts with both robots moving to their respective objects: `robot1` to the apple and `robot2` to the light switch.
- `robot1` picks up the apple and proceeds to the fridge, while `robot2` switches off the light.
- The actions are timed to reflect the parallel execution of independent tasks, ensuring efficient task completion.