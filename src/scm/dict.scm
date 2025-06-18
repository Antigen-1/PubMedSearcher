(#%scm-procedure 
    (lambda (supported-string:accessor make-exn)
        (let ((new-make-exn (#%vm-procedure make-exn 1))
              (tuple (make-procedure (lambda (t) t))))
            (#%scm-procedure 
                (lambda (needed)
                    (let/cc exit
                        (let ((nl (length needed)))
                            (let loop ((i 0))
                                (if (equal? i nl)
                                    'none
                                    (if (? supported-string:accessor (@ needed i))
                                        (loop (+ i 1))
                                        (exit (make-exn (+ (@ needed i) ": not supported"))))))
                            (#%scm-procedure 
                                (lambda (value)
                                    (let ((result #hasheq{}))
                                        (let loop ((i 0))
                                            (if (equal? i nl)
                                                result
                                                (let ((field (@ needed i)))
                                                    (! result field 
                                                       (vm-apply (@ supported-string:accessor field)
                                                                    (tuple value)))
                                                    (loop (+ i 1)))))))
                                1))))
        1)))
    2)