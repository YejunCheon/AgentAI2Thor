(define (problem locate_pickup_spatula_problem)
  (:domain robot2)
  (:objects
    robot2 - robot
    spatula - object
    counterTop - object
  )
  (:init
    (at robot2 counterTop)
    (at-location spatula counterTop)
    (not (inaction robot2)) ; Corrected from (inaction robot2) to match precondition requirements
  )
  (:goal
    (and
      (holding robot2 spatula)
    )
  )
)