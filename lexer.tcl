############################################
#                Lexer Phase               #
############################################

namespace eval lexer {

    variable keywords {module input output reg wire assign always begin end if else endmodule}
    variable operators {+ - * / = , ; : ( ) { } [ ] < > <= >= == !=}

    proc lex {code} {
        variable keywords
        variable operators
        
        set tokens {}
        set i 0
        set len [string length $code]
        
        while {$i < $len} {
            set char [string index $code $i]
            
            # Skip whitespace
            if {[string is space $char]} {
                incr i
                continue
            }
            
            # Skip comments /* */
            if {[string match "/*" [string range $code $i [expr {$i+1}]]]} {
                incr i 2
                while {$i < $len && [string range $code $i [expr {$i+1}]] ne "*/"} {
                    incr i
                }
                incr i 2
                continue
            }
            
            # IDENTIFIER / KEYWORD
            if {[string is alpha $char] || $char eq "_"} {
                set start $i
                while {$i < $len && ([string is alnum [string index $code $i]] || 
                      [string index $code $i] eq "_")} {
                    incr i
                }
                set token [string range $code $start [expr {$i-1}]]
                
                if {[lsearch -exact $keywords $token] >= 0} {
                    lappend tokens "KEYWORD:$token"
                } else {
                    lappend tokens "IDENTIFIER:$token"
                }

            # NUMBER
            } elseif {[string is digit $char]} {
                set start $i
                while {$i < $len && [string is digit [string index $code $i]]} {
                    incr i
                }
                lappend tokens "NUMBER:[string range $code $start [expr {$i-1}]]"

            # OPERATORS
            } else {
                set two_char [string range $code $i [expr {$i+1}]]
                
                if {[lsearch -exact $operators $two_char] >= 0} {
                    lappend tokens "OPERATOR:$two_char"
                    incr i 2
                } elseif {[lsearch -exact $operators $char] >= 0} {
                    lappend tokens "OPERATOR:$char"
                    incr i
                } else {
                    error "Unknown character: '$char' at position $i"
                }
            }
        }

        # Print output (simple version)
        puts "\n=== Lexer Output ==="
        foreach token $tokens {
            lassign [split $token :] type value
            puts [format "%-12s %s" $type $value]
        }

        return $tokens
    }
}