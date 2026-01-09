(define (problem move_to_trash_can_problem)
  (:domain robot2)
  (:objects
    robot2 - robot
    garbageCan - object
    counterTop - object
  )
  (:init
    (at robot2 counterTop)
    (at-location garbageCan counterTop)
    (inaction robot2)
  )
  (:goal
    (and
      (at robot2 garbageCan)
    )
  )
)