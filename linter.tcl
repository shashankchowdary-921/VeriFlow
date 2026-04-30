############################################
#              Linter Phase                #
############################################

namespace eval linter {

    variable declared_signals
    variable assigned_signals
    variable used_signals
    variable assign_targets

    proc reset {} {
        set ::linter::declared_signals {}
        set ::linter::assigned_signals {}
        set ::linter::used_signals {}
        set ::linter::assign_targets {}
    }

    proc check {ast} {

        reset

        variable declared_signals
        variable assigned_signals
        variable used_signals
        variable assign_targets

        set errors {}

        set operators {+ - * / == != < > <= >=}

        ########################################
        # Pass 1: Collect declarations
        ########################################
        foreach node $ast {

            lassign $node type arg1 arg2

            if {$type eq "reg"} {
                foreach var $arg1 {
                    lappend declared_signals $var
                }
            }
        }

        ########################################
        # Pass 2: Process assignments
        ########################################
        foreach node $ast {

            lassign $node type arg1 arg2

            if {$type eq "assign"} {

                set lhs $arg1
                set rhs $arg2

                # implicit wire
                if {[lsearch $declared_signals $lhs] == -1} {
                    lappend declared_signals $lhs
                }

                lappend assigned_signals $lhs
                lappend assign_targets $lhs

                foreach token $rhs {

                    # skip operators
                    if {[lsearch $operators $token] != -1} {
                        continue
                    }

                    # check identifier
                    if {![regexp {^[a-zA-Z_]\w*$} $token]} {
                        continue
                    }

                    if {[lsearch $declared_signals $token] == -1} {
                        lappend errors "Undeclared RHS signal: $token"
                    }

                    lappend used_signals $token
                }
            }
        }

        ########################################
        # Unused signals
        ########################################
        foreach sig $declared_signals {
            if {[lsearch $used_signals $sig] == -1 && [lsearch $assigned_signals $sig] == -1} {
                lappend errors "Warning: Unused signal: $sig"
            }
        }

        ########################################
        # Multiple drivers
        ########################################
        array set driver_counts {}

        foreach t $assign_targets {
            incr driver_counts($t)
        }

        foreach sig [array names driver_counts] {
            if {$driver_counts($sig) > 1} {
                lappend errors "Warning: Multiple drivers for $sig"
            }
        }

        ########################################
        # Output
        ########################################
        puts "\n=== Linter Report ==="

        if {[llength $errors] > 0} {
            foreach err $errors {
                puts "  $err"
            }
        } else {
            puts " No linting issues found"
        }

        return $errors
    }
}