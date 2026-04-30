############################################
#               Parser Phase               #
############################################

namespace eval parser {

    variable tokens {}
    variable index 0

    proc parse {input_tokens} {
        variable tokens
        variable index

        set tokens $input_tokens
        set index 0
        set ast {}

        # Parse module declaration
        parse_module_declaration

        # Parse module body
        while {$index < [llength $tokens]} {
            set token [lindex $tokens $index]
            set value [lindex [split $token :] 1]

            switch -exact -- $value {
                "reg"        { lappend ast [parse_reg_declaration] }
                "assign"     { lappend ast [parse_assignment] }
                "if"         { lappend ast [parse_conditional] }
                "endmodule"  { incr index; break }
                ";"          { incr index }
                default      { parse_error "Unexpected token: $token" }
            }
        }

        return $ast
    }

    proc parse_module_declaration {} {
        variable index
        variable tokens

        if {[lindex [split [lindex $tokens $index] :] 1] eq "module"} {
            incr index
            set module_name [lindex [split [lindex $tokens $index] :] 1]
            incr index

            if {[lindex [split [lindex $tokens $index] :] 1] eq ";"} {
                incr index
            }
        }
    }

    ########################################
    # REG DECLARATION
    ########################################
    proc parse_reg_declaration {} {
        variable index
        variable tokens

        incr index
        set vars {}

        while {1} {
            set token_value [lindex [split [lindex $tokens $index] :] 1]

            if {$token_value eq ";"} break

            if {$token_value ne ","} {
                lappend vars $token_value
            }

            incr index
        }

        incr index
        return [list reg $vars]
    }

    ########################################
    # ASSIGNMENT
    ########################################
    proc parse_assignment {} {
        variable index
        variable tokens

        incr index
        set lhs [lindex [split [lindex $tokens $index] :] 1]

        incr index 2  ;# skip '='

        set rhs {}

        while {[lindex [split [lindex $tokens $index] :] 1] ne ";"} {
            lappend rhs [lindex [split [lindex $tokens $index] :] 1]
            incr index
        }

        incr index

        return [list assign $lhs $rhs]
    }

    ########################################
    # CONDITIONAL (IF)
    ########################################
    proc parse_conditional {} {
        variable index
        variable tokens

        incr index 2  ;# skip if (

        set condition {}

        while {[lindex [split [lindex $tokens $index] :] 1] ne ")"} {
            lappend condition [lindex [split [lindex $tokens $index] :] 1]
            incr index
        }

        incr index 2  ;# skip ) begin

        set body {}

        while {[lindex [split [lindex $tokens $index] :] 1] ne "end"} {
            set token_value [lindex [split [lindex $tokens $index] :] 1]

            if {$token_value eq "assign"} {
                lappend body [parse_assignment]
            } else {
                incr index
            }
        }

        incr index

        return [list if $condition $body]
    }

    proc parse_error {msg} {
        error "Parse error at token $::parser::index: $msg"
    }
}