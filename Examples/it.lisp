(define walk-list (lambda (lst fun)
   (if (not (list? lst))
      (fun lst)
      (if (not (null? lst))
         (begin
            (walk-list (car lst) fun)
            (walk-list (cdr lst) fun))))))