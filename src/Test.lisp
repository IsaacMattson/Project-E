(let 
	;; Test Procedure
	((test-code (lambda (expected code)
				(if (= expected code)
					(display "PASSED!")
					(display "FAILED!")) )))
	;; Tests to run
	(begin(
	
		(test-code 5 (+ 4 1) )
		(test-code 9 (square 3))
	
	))
)