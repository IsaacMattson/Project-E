(begin
;;; ===Math Procs=== ;;;
(define square (lambda 
		(x)
		(* x x)))
(define cube (lambda
		(x)
		(* x x x)))
		
(define ! (lambda (n)
		(if (= n 0)
		1
		(* n (! (- n 1))))))

;;; ===Other Procs=== ;;;
(define walk (lambda	(l f)
			(if (eq?	(len l) 1) 
					(f (car l)) 
					(begin (f (car l ))(walk (cdr l) f)))))

(define > (lambda (a b)
			(if (<  a b)
				#f
				#t)))
				
(define <=	(lambda (a b)
			(if (or (< a b) (= a b))
				#t
				#f)))

(define >=	(lambda (a b)
			(if (or (> a b) (= a b))
				#t
				#f)))
				
				

(display "Standered Library Loaded!") ;This is just to test if the lib has loaded

)
