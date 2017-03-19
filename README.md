# SATPLAN

This was an university project for an AI subject. The objective for this project was to create a planner and a solver to solve boolean satisfiability problems.
This should be seen as an exercise most of all, as it was not meant to be optimized (wasn't written in C/C++, doesn't implement threading, etc) and other solvers such as the MiniSat vastly outperform this solving algorithm. This code however, unlike the MiniSat also implements a planner, that encodes a PDDL problem to a SAT problem in the DIMACS format.
To test this code run
```
python3 Main.py <input_file_name>
```
Where the input file name should specify the initial and final states (I and G) as well as the possible actions as such


I on (A,B) on (B ,C) on (C , Tabe ) clear(A)

A move (b,f,t) : on (b ,f ) clear (b) clear (t) −> −on (b ,f ) on ( b , t ) −clear( t ) clear ( f )

A move2table ( b , f ) : on ( b , f ) clear ( b ) −> −on ( b , f ) on ( b , Table ) clear ( f )

G on (C ,B) on (B ,A) on (A, Tab le ) clear (C)

A more in depth descripton of the project can be found on the project report
