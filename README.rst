I had a friend ask me about automated theorem provers in  python and  realized that I had never built one in python. In the languages that I usually use to build theorem provers there's generally either a rich type system to take advantage of or the language is so fluid that you construct class like objects as you go. This was an experiment in building a satisfaction solver. It is currently in no way optimized but I hope to  use it for experimentation. 

Requirements
------------

None. This should work with out-of-the-box python.

Installation
------------

This can be  installed on an environment by calling 

.. code-block :: bash

    pip install . 

Usage 
-----

Once installed you can create a python script and import the package with 
   
..  code-block :: python

    import sat_solver

or your favorite variant of that import statement. 

Formulas a created as instances of classes. There are currently five subclasses of formula: Atom, Not, And, Or, and If. Atom takes a string as its only attribute.  Not  takes another Formula. If takes two formulas, and  And and Or take a list of Formulas. For example: 

.. code-block :: python

    If(Atom("p"), And([Or([Atom("p"), Atom("q")]), Not(Atom("q"))]))

specifies a formula. The TruthTable  class takes a formula and constructs a truth table for that formula. That truth table (call it "tt") can be printed to the terminal with the show_resolution method: 
 
.. code-block :: python

    tt.show_resolution()

Truth tables can also report whether or not their formula is a tautology: 

.. code-block :: python

    tt.tautology()



