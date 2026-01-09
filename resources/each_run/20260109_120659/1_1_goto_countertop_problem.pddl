(define (problem goto_countertop_problem)
  (:domain robot1)
  (:objects
    robot1 - robot
    lettuce - object
    countertop - object
  )
  (:init
    (holding robot1 lettuce)
    (at-location lettuce countertop)
    ; Removed (inaction robot1) because it prevents any action from being taken.
  )
  (:goal
    (and
      (at robot1 countertop)
    )
  )
)