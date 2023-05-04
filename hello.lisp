(begin
(define name (input "Name? "))
(define msg (combine-strings (combine-strings "Hello, " name) "!"))
(display msg)
)