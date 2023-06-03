(define test (macro (x y) (list `list (list `quote x) "evaluates to" x " : " (if (= x y) "PASS!" "FAIL!" ))))

