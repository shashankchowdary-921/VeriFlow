############################################
#           Simulation (IR-based)          #
############################################

namespace eval simulator {

    proc run {ir} {

        puts "\n=== Simulation Results ==="

        array set state {}

        ########################################
        # Initialize variables
        ########################################
        foreach node $ir {
            lassign $node type arg1 arg2

            if {$type eq "DECLARE"} {
                foreach var $arg1 {
                    set state($var) 0
                    puts "Initialized: $var = 0"
                }
            }
        }

        ########################################
        # Evaluate assignments
        ########################################
        foreach node $ir {
            lassign $node type arg1 arg2

            if {$type eq "ASSIGN"} {

                set lhs $arg1
                set rhs $arg2

                set value [evaluate_expr $rhs state]

                set state($lhs) $value
                puts "Assignment: $lhs = $value"
            }
        }

        ########################################
        # Final values
        ########################################
        puts "\nFinal Values:"
        foreach var [lsort [array names state]] {
            puts "  $var = $state($var)"
        }
    }

    ########################################
    # Expression evaluator
    ########################################
    proc evaluate_expr {expr_list state_name} {

        upvar $state_name st

        set expr_str ""

        foreach token $expr_list {

            if {[string is integer -strict $token]} {
                append expr_str "$token "
            } elseif {[info exists st($token)]} {
                append expr_str "$st($token) "
            } else {
                append expr_str "$token "
            }
        }

        return [expr $expr_str]
    }
}