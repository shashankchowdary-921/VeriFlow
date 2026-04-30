############################################
#            Optimization Phase            #
############################################

namespace eval optimizer {

    proc optimize {ir} {

        puts "\n=== Optimized Code ==="

        set optimized {}
        array set vars {}

        foreach node $ir {

            lassign $node type arg1 arg2

            ########################################
            # DECLARE
            ########################################
            if {$type eq "DECLARE"} {
                foreach var $arg1 {
                    set vars($var) ""
                }
                lappend optimized $node
            }

            ########################################
            # ASSIGN
            ########################################
            if {$type eq "ASSIGN"} {

                set lhs $arg1
                set rhs $arg2   ;# list form

                # Convert RHS to string for comparison
                set rhs_str [join $rhs " "]

                # Remove redundant assignment
                if {![info exists vars($lhs)] || $vars($lhs) ne $rhs_str} {

                    set vars($lhs) $rhs_str
                    lappend optimized $node
                }
            }
        }

        ########################################
        # Print optimized IR
        ########################################
        foreach node $optimized {

            lassign $node type arg1 arg2

            if {$type eq "DECLARE"} {
                puts " DECLARE [join $arg1 ", "]"
            }

            if {$type eq "ASSIGN"} {
                puts " ASSIGN $arg1 = [join $arg2 " "]"
            }
        }

        return $optimized
    }
}