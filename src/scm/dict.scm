(#%scm-procedure 
    (lambda (supported-string:constructor make-exn)
        (let ((new-make-exn (#%vm-procedure make-exn 1))
              (tuple (make-procedure (lambda (t) t))))
            (#%scm-procedure 
                (lambda (value needed)
                    (let/cc exit
                        (let ((nl (length needed))
                              (result #hasheq{}))
                            (let loop ((i 0))
                                (if (equal? i nl)
                                    'none
                                    (if (? supported-string:constructor (@ needed i))
                                        (loop (+ i 1))
                                        (exit (make-exn (+ (@ needed i) ": not supported"))))))
                            (let loop ((i 0))
                                (if (equal? i nl)
                                    result
                                    (let ((field (@ needed i)))
                                        (! result field 
                                           (vm-apply (@ supported-string:constructor field)
                                                     (tuple value)))
                                        (loop (+ i 1))))))))
        2)))
    2)