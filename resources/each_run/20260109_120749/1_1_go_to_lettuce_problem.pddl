(define (problem go_to_lettuce_problem)
  (:domain robot1)
  (:objects
    robot1 - robot
    lettuce - object
    counterTop - object
  )
  (:init
    (at robot1 counterTop)
    (at-location lettuce counterTop)
    ;; Removed (inaction robot1) to satisfy precondition of GoToObject action
  )
  (:goal
    (and
      (at robot1 lettuce)
    )
  )
)