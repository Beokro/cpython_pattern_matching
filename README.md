# Python with pattern matching

## If none of the cases matches, it will throw an exception. We may want match to be an expression but not a statement.

	def haha(arg):
		x = match(arg):
		with 1 or 2:
			3
		with 3:
			7
		with y : Int:
			2
		with _:
			throws Exception("Not an Int")
		return x

	def yosh(arg):
		x = match(arg):
		with []:
			[3]
		with {}:
			{3}
		with _:
			print "nima" None
		return x

# Actual Implementation

## Grammar/Frammar
	// somehow keyword 'match' will cause the compile error, not sure why but I will use pmatch instead
  // start with something simple, match expr instead of exprlist
	match_stmt: 'pmatch' expr ':' 'with' or_test ':' expr ('with' or_test ':' expr)*

## AST

* for now, create multiple comparsion and return value pair.  in Parser/Python.asdl add
* Match(Expr* tests, Expr* returns)

   asdl_int_seq *ops = asdl_int_seq_new(1, c->c_arena);
   expr_ty expression = ast_for_expr(c, CHILD(n, 0));
   asdl_seq * cmps = asdl_seq_new(1, c->c_arena);

   asdl_seq_SET(ops, 0, Eq);
   asdl_seq_SET(cmps, 0, expression);    
   Compare(expression, ops, cmps, LINENO(n),
           n->n_col_offset, c->c_arena);

## Compiler

* Based on Match(Expr* tests, Expr* returns), Match node contains equal number of tests and return values
* visit test and return in pairs. call Visit function on both
* use asdl_seq_LEN to determine the length of the match statement
* sue asdl_seq_GET to access the individual test and return
   

Note on pypy grammer
=====================
*  file directory: pypy / pypy / interpreter / pyparser / data / Grammar2.7
*  http://stackoverflow.com/questions/19351065/how-is-the-python-grammar-used-internally is very helpful in understanding the grammar file
*  
Symbol | Meaning
------------ | -------------
'*' | repetition-symbol
'+' | repeatition-at-least-one
'-' | except-symbol
, | concatenate-symbol
'|' | definition-separator-symbol
= | defining-symbol
; | terminator-symbol
. | terminator-symbol

Symbol | Meaning | Meaning | Symbol
------------ | ------------- | ------------ | -------------
' | first-quote-symbol | first-quote-symbol | '
" | second-quote-symbol      |    second-quote-symbol | "
(* |start-comment-symbol     |     end-comment-symbol | *)
( | start-group-symbol       |       end-group-symbol | )
[ | start-option-symbol      |      end-option-symbol | ]
{ | start-repeat-symbol      |      end-repeat-symbol | }
? | special-sequence-symbol | special-sequence-symbol | ?

*  a non-terminal is any lowercase word and a terminal is all uppercase or surrounded by quotes
*  Start symbols for the grammar = single_input, file_input , eval_input 
*  'simple_stmt' can be used to build multiple 'small_stmt'
*  'small_stmt' contains statments that can be write in one line. Examples would be import statement and print statement
*  'test' contains bunch of expressions that can eventully be evaulated to a expr ( boolean? )
*  'flow_stmt' contains statments  that can change program's flow, like return and break
*  'compound_stmt' contains all of the long statments, including if statement and all the loops
*  'suite' can be any 'simple_stmt' or a line of any statement
*  'exprlist', 'testlist' contians bunch of expr or test

# Note on Parse Trees

## Important functions in Python/ast.c
* CHILD(node *, int):    Returns the nth child of the node using zero-offset indexing
* RCHILD(node *, int):   Returns the nth child of the node from the right side; use negative numbers!
* NCH(node *): 		 Number of children the node has
* STR(node *):           String representation of the node; e.g., will return : for a COLON token
* TYPE(node *):          The type of node as specified in Include/graminit.h
* REQ(node *, TYPE):     Assert that the node is the type that is expected
* LINENO(node *):        retrieve the line number of the source code that led to the creation of the parse rule; defined in Python/ast.c
* asdl_seq_SET:          set the node to become a node it created

## Examples

while_stmt: 'while' test ':' suite ['else' ':' suite]
* TYPE(node) == while_stmt
* number of children can be 4 or 7 depending on whether there is an ‘else’ statement
* REQ(CHILD(node, 2), COLON) can be used to access what should be the first : and require it be an actual : token

# How to handle Grammar contains '*'

* use NCH( const node* n ) to determine the number of chiild and number of time that ( xxx ) * repeated itself, sset it to x
* use asdl_seq_new to create a container seq that will hold x elements
* use asdl_seq_set to set each element in seq
* return the node


# Note on Code generation

* we are dealing with AST to CFG( control flow graph ). CFG have basic blocks that contain the intermediate representation
* Basic blocks themselves are a block of IR that has a single entry point but possibly multiple exit points.
* Code is directly generated from the basic blocks
* From blocks to bytecode, first creates the namespace and then pass essentially flattens the CFG into a list and calculates jump offsets for final output of bytecode.
* each node type will have a function named compiler_visit_xx where xx is the name of the node type
* Each function receives a struct compiler * and xx_ty where xx is the AST node type.

## opcode realted methods
* ADDOP() - add a specified opcode
* ADDOP_I() - add an opcode that takes an argument
* ADDOP_O(struct compiler *c, int op, PyObject *type, PyObject *obj) - add an opcode with the proper argument based on the position of the specified PyObject in PyObject sequence object, but with no handling of mangled names; used for when you need to do named lookups of objects such as globals, consts, or parameters where name mangling is not possible and the scope of the name is known
* ADDOP_NAME() - just like ADDOP_O, but name mangling is also handled; used for attribute loading or importing based on name
* ADDOP_JABS() - create an absolute jump to a basic block
* ADDOP_JREL() - create a relative jump to a basic block

## block related methods
* NEW_BLOCK() - create block and set it as current
* NEXT_BLOCK() - basically NEW_BLOCK() plus jump from current block
* compiler_new_block() - create a block but don’t use it (used for generating jumps)
* compiler_use_next_block(struct compiler *c, basicblock *block) - set the block to be current block
* compiler_push_fblock(struct compiler *c, enum fblocktype t, basicblock *b) - push a block to compiler, if too mnay block will return 0, otherwise return 1
* compiler_pop_fblock(struct compiler *c, enum fblocktype t, basicblock *b) - similar to previous one, but pop the block instead

## take a look at compiler_if
* create two block 'end' and 'next', initialize next as a new block
* use expr_constant to check the if test. If value is 0, visit else. If value if 1, visit if body
* if value is negative
  * if contains else, initalize next to be a new block, otherwise set it to end
  * visit test. If test value is false jump to next
  * visit if body. Jump to end
  * visit else
* set current block to end, which is a empty new block


