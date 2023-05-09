(begin
(define sqr (lambda 
		(x)
		(* x x)))

(define cube (lambda
		(x)
		(* x x x)))

(display	(+ 2 2))

(define walk (lambda (l f)(if (eq? (len l) 1) (f (car l)) (begin (f (car l ))(walk (cdr l) f)))))

(display "Hello, World")

(walk (lst 1 2 3) display)

)
