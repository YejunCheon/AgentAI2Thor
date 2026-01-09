To modify the PDDL plan so that all 'variablelocation' references are corrected to the variable itself, we need to ensure that the object names are used directly without any location suffixes. Here's the corrected PDDL plan:

```pddl
; PDDL Plan for Slicing a Tomato

; Step 1: Go to the Knife
0.0: (GoToObject robot1 Knife)

; Step 2: Pick up the Knife
1.0: (PickupObject robot1 Knife)

; Step 3: Go to the Tomato
2.0: (GoToObject robot1 Tomato)

; Step 4: Pick up the Tomato
3.0: (PickupObject robot1 Tomato)

; Step 5: Slice the Tomato
4.0: (SliceObject robot1 Tomato)

; Note: The times are indicative and assume each action takes 1 time unit.
; Adjust the times based on the actual duration of each action in your domain.
```

### Explanation:

- The object names in the actions are directly referenced as `Knife` and `Tomato`, without any location suffixes.
- The plan maintains the sequence of actions necessary for the robot to slice the tomato, ensuring that each step is completed in order.
- The plan is structured to be executed by a single robot (`robot1`), following the constraints and requirements of the task.