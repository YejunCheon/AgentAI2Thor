(define (problem slice_tomato_problem)
  (:domain robot1)
  (:objects
    robot1 - robot
    robot2 - robot
    robot3 - robot
    tomato - object
    knife - object
    counterTop - object
  )
  (:init
    (at-location tomato counterTop)
    (at-location knife counterTop)
    ; Assuming we want one of the robots to be active initially:
    (not (inaction robot1))
    (inaction robot2)
    (inaction robot3)
  )
  (:goal
    (and
      (sliced tomato)
    )
  )
)