TEAM MEMBERS:
- Amir Aissat - aaissat@kennesaw.edu
- Geza Martiny - Gmartiny@student.kennesaw.edu
- Noor Muhammad - nmuham22@students.kennesaw.edu
- A.J. Robinson  - arobi265@students.kennesaw.edu

FILES THAT ARE INCLUDED: 
- Input1.txt     : sample test case 1 for input
- Ouput1.txt     : sample test case 1 for output
- Input2.txt     : sample test case 2 for input
- Ouput2.txt     : sample test case 2 for output
- Input3.txt     : sample test case 3 for input
- Ouput3.txt     : sample test case 3 for output
- Input4.txt     : sample test case 4 for input
- Ouput4.txt     : sample test case 4 for output
- Input5.txt     : sample test case 5 for input
- Ouput5.txt     : sample test case 5 for output
- assignment2.py : the main program (algorithm, file parsing, heap-based skyline solver)


HOW TO RUN THE PROGRAM:
1. Open a terminal or command prompt.
2. Run the program using python by providing absolute paths to the input and output files

Example:
   python assignment2.py /path/to/InputsOutputs/Input1.txt /path/to/InputsOutputs/Ouput1.txt


INPUT FORMAT SHOULD BE:
    H1, Lx1, Rx1
    H2, Lx2, Rx2
    ...
    Hn, Lxn, Rxn

Each line represents a building in comma-delimited format with non-negative integers:
- Height (H): height of the building
- Left_X (Lx): left x-coordinate where the building begins
- Right_X (Rx): right x-coordinate where the building ends (0 < Lx < Rx)

THE ALGORITHM:
We implemented an O(n log n) sweep-line algorithm using a Max-Heap (Priority Queue) to 
find the outer skyline shape of n rectangular buildings.

First, the program processes each building into two critical event points: a "Start" event 
at the left x-coordinate and an "End" event at the right x-coordinate. All event points 
are placed into a list and sorted primarily by their x-coordinates. Tie-breaking rules ensure 
that taller starting buildings are processed before shorter ones, and overlapping start events 
are processed before end events.

As the algorithm sweeps across the sorted x-coordinates, it pushes new active buildings 
onto a Max-Heap ordered by height. When an end event occurs or a building falls behind the 
current x-coordinate, expired buildings are lazily removed from the top of the heap. 

At each event point, the algorithm inspects the top of the Max-Heap to determine the current 
maximum height. If the maximum height changes from the previous point, a new key point (height, x) 
is added to the output skyline.

Full pseudocode is included as a comment block directly at the top of assignment2.py.

SAMPLE TEST CASES:

1. Input1.txt / Ouput1.txt
   Baseline example directly from the assignment handout. Tests 5 overlapping 
   buildings of varying heights to verify the standard case against the handout output.

2. Input2.txt / Ouput2.txt
   Tests disjoint buildings with empty gaps in between, as well as two buildings 
   that touch edge-to-edge at x=13. Verifies that the skyline correctly drops to height 0 
   in empty space without creating redundant zero-height strips.

3. Input3.txt / Ouput3.txt
   Tests fully nested buildings where a tall building (h=12) completely covers three 
   shorter buildings beneath it. Also tests adjacent equal-height buildings at x=18 
   to confirm they merge smoothly into a single strip.

4. Input4.txt / Ouput4.txt
   Tests duplicate identical buildings (7, 1, 5) sharing boundaries and buildings with 
   the same left edge x=12 but different heights and lengths. Confirms that duplicate points 
   are eliminated and the max-heap tracks active building durations accurately.

5. Input5.txt / Ouput5.txt
   A larger stress test consisting of 12 buildings, including nested staircases, narrow spikes, 
   and complex multi-level overlapping chains. Confirms O(n log n) performance and correctness 
   across dense event queues.
