# Some Use Cases (may not be the same syntax)

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
	match_stmt: 'pmatch' exprlist ':' 'with' or_test ':' expr ( 'with' or_test ':' expr )*

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
