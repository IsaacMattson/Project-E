(define walk 
	(lambda (lst fun)
 	  (if	(null? lst))
		()
		(begin (fun (car lst))(walk (cdr lst)))))