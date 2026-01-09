(define (problem place_lettuce_problem)
  (:domain robot1)
  (:objects
    robot1 - robot
    lettuce - object
    countertop - object
  )
  (:init
    (at robot1 countertop)
    (at-location lettuce robot1)
    (holding robot1 lettuce)
    (not (inaction robot1))
  )
  (:goal
    (and
      (at-location lettuce countertop)
    )
  )
)