source lexer.tcl
source parser.tcl
source ir.tcl
source optimization.tcl
source simulation.tcl

set code {
    module test;
    reg a, b;
    assign c = a + b;
endmodule
}

set tokens [lexer::lex $code]
set ast [parser::parse $tokens]
set ir_out [ir::generate $ast]
set opt [optimizer::optimize $ir_out]

simulator::run $opt