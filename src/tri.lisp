(begin 
(define is-valid-tri (lambda (a b c) 
(if (= (+ a b c) 180 )
    (#t)
    (#f) )))

(define class-by-side (lambda (a b c)
(if (= a b c 60)
    "equilateral"
    (if (or (= a b) (or (= b c)(= c a))) 
	"isosceles"
	"scalene"))))
(display "Tri loaded")
)