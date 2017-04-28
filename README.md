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
