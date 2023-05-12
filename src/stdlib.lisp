(begin
;;; ===Math Procs=== ;;;
(define sqr (lambda 
		(x)
		(* x x)))
(define cube (lambda
		(x)
		(* x x x)))

;;; ===Other Procs=== ;;;
(define walk (lambda 	(l f)
			(if (eq?	(len l) 1) 
					(f (car l)) 
					(begin (f (car l ))(walk (cdr l) f)))))

(display "Hello, World") ;This is just to test if the lib has loaded

(walk (lst 1 2 3) display)

)
