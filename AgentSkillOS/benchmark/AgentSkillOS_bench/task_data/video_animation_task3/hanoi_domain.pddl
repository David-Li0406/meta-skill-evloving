(define (domain hanoi)
  (:requirements :strips)
  (:predicates
    (on ?disk ?below)
    (clear ?x)
    (smaller ?x ?y)
    (disk ?d)
    (peg ?p))

  ;; Move a disk from one disk to another disk
  (:action move-disk-to-disk
    :parameters (?disk ?from ?to)
    :precondition (and
      (disk ?disk)
      (disk ?from)
      (disk ?to)
      (clear ?disk)
      (clear ?to)
      (on ?disk ?from)
      (smaller ?disk ?to))
    :effect (and
      (on ?disk ?to)
      (clear ?from)
      (not (on ?disk ?from))
      (not (clear ?to))))

  ;; Move a disk from a disk to a peg
  (:action move-disk-to-peg
    :parameters (?disk ?from ?to)
    :precondition (and
      (disk ?disk)
      (disk ?from)
      (peg ?to)
      (clear ?disk)
      (clear ?to)
      (on ?disk ?from)
      (smaller ?disk ?to))
    :effect (and
      (on ?disk ?to)
      (clear ?from)
      (not (on ?disk ?from))
      (not (clear ?to))))

  ;; Move a disk from a peg to another disk
  (:action move-peg-to-disk
    :parameters (?disk ?from ?to)
    :precondition (and
      (disk ?disk)
      (peg ?from)
      (disk ?to)
      (clear ?disk)
      (clear ?to)
      (on ?disk ?from)
      (smaller ?disk ?to))
    :effect (and
      (on ?disk ?to)
      (clear ?from)
      (not (on ?disk ?from))
      (not (clear ?to))))

  ;; Move a disk from a peg to another peg
  (:action move-peg-to-peg
    :parameters (?disk ?from ?to)
    :precondition (and
      (disk ?disk)
      (peg ?from)
      (peg ?to)
      (clear ?disk)
      (clear ?to)
      (on ?disk ?from)
      (smaller ?disk ?to))
    :effect (and
      (on ?disk ?to)
      (clear ?from)
      (not (on ?disk ?from))
      (not (clear ?to))))
)
