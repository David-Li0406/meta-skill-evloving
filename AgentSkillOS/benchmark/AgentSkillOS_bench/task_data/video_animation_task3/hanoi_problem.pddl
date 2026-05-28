(define (problem hanoi-3)
  (:domain hanoi)
  (:objects
    peg-a peg-b peg-c - object
    d1 d2 d3 - object)

  (:init
    (peg peg-a) (peg peg-b) (peg peg-c)
    (disk d1) (disk d2) (disk d3)

    ;; d1 is smallest, d3 is largest
    ;; smaller means: first arg can be placed on second arg
    (smaller d1 d2) (smaller d1 d3)
    (smaller d1 peg-a) (smaller d1 peg-b) (smaller d1 peg-c)
    (smaller d2 d3)
    (smaller d2 peg-a) (smaller d2 peg-b) (smaller d2 peg-c)
    (smaller d3 peg-a) (smaller d3 peg-b) (smaller d3 peg-c)

    ;; Initial state: all disks on peg-a, d1 on d2 on d3 on peg-a
    (on d1 d2)
    (on d2 d3)
    (on d3 peg-a)
    (clear d1)
    (clear peg-b)
    (clear peg-c))

  (:goal (and
    (on d1 d2)
    (on d2 d3)
    (on d3 peg-c)))
)
