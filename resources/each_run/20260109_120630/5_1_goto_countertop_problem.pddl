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
    (inaction robot1)
  )
  (:goal
    (and
      (at robot1 countertop)
    )
  )
)