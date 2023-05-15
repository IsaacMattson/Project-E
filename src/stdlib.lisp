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
(define one-true? (lambda	(l)
				(let (w (lambda (l) ()) ) () )))			  		

(display "Standered Library Loaded!") ;This is just to test if the lib has loaded

)
