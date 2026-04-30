############################################
#         Semantic Analysis Phase          #
############################################

namespace eval sem {

    variable symbol_table

    proc analyze {ast} {
        variable symbol_table
        array unset symbol_table
        array set symbol_table {}

        set errors {}

        ########################################
        # Pass 1: Collect declarations
        ########################################
        foreach node $ast {
            if {[string match "reg declaration:*" $node]} {
                set lines [split $node "\n"]
                foreach var [lrange $lines 1 end] {
                    set var [string trim $var]
                    if {$var ne ""} {
                        set symbol_table($var) "reg"
                    }
                }
            }
        }

        ########################################
        # Pass 2: Handle assignments (implicit wires)
        ########################################
        foreach node $ast {
            if {[string match "assign statement:*" $node]} {
                set lines [split $node "\n"]

                set lhs_line [lindex $lines 1]
                set lhs [string trim [string map {"LHS:" ""} $lhs_line]]

                if {![info exists symbol_table($lhs)]} {
                    set symbol_table($lhs) "wire"
                }
            }
        }

        ########################################
        # Pass 3: Validate RHS variables
        ########################################
        foreach node $ast {
            if {[string match "assign statement:*" $node]} {
                set lines [split $node "\n"]

                set rhs_line [lindex $lines 2]
                set rhs [string trim [string map {"RHS:" ""} $rhs_line]]

                foreach token [regexp -all -inline {\w+} $rhs] {
                    if {![info exists symbol_table($token)] && ![string is integer -strict $token]} {
                        lappend errors "Undeclared variable in RHS: $token"
                    }
                }
            }
        }

        ########################################
        # Output
        ########################################
        puts "\n=== Semantic Analysis ==="

        if {[llength $errors] == 0} {
            puts "✔ All checks passed successfully"
        } else {
            puts "✗ Errors detected:"
            foreach err $errors {
                puts "  - $err"
            }
        }

        return $errors
    }
}