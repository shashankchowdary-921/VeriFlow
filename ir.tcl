############################################
#       Intermediate Representation        #
############################################

namespace eval ir {

    proc generate {ast} {
        set ir_output {}

        puts "\n=== Intermediate Representation ==="

        foreach node $ast {

            lassign $node type arg1 arg2

            ########################################
            # REG DECLARATION
            ########################################
            if {$type eq "reg"} {
                set decls [join $arg1 ", "]
                lappend ir_output [list DECLARE $arg1]

                puts "DECLARE $decls"
            }

            ########################################
            # ASSIGNMENT
            ########################################
            if {$type eq "assign"} {
                set lhs $arg1
                set rhs [join $arg2 " "]

                lappend ir_output [list ASSIGN $lhs $arg2]

                puts "ASSIGN $lhs = $rhs"
            }
        }

        return $ir_output
    }
}