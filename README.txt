CS4306 - Algorithm Analysis - Assignment 1
Modified Gale-Shapley Algorithm for the Hospital/Residents Problem

Team Members:
- A.J. Robinson - arobi268@students.kennesaw.edu
- Amir Aissat - aaissat@students.kennesaw.edu
- Geza Martiny - Gmartiny@students.kennesaw.edu
- Noor Muhammad - nmuham22@students.kennesaw.edu

FILES THAT ARE INCLUDED:
- Assignment_1.py               : the main program (algorithm, parsing, output, stability check)
- sample_input_1.txt            : sample test case 1 for input
- sample_output_1.txt           : sample test case 1 for output
- sample_input_2.txt            : sample test case 2 for input
- sample_output_2.txt           : sample test case 2 for output
- sample_input_edge_case.txt    : edge case test for input
- sample_output_edge_case.txt   : edge case test for output
- README.txt                    : this current file

HOW TO RUN THE PROGRAM:
1. Run: python Assignment_1.py
2. When you are prompted "Enter input file name:", type the
   name of on of the input files, e.g. sample_input_1.txt
3. The program will print the final matching, then reports
   whether the matching is stable or not.

INPUT FORMAT SHOULD BE:
    HOSPITAL_1, SLOTS, RESIDENT_a, RESIDENT_b, ...
    ...
    <blank line>
    RESIDENT_1, HOSPITAL_x, HOSPITAL_y, ...
    ...

Each hospital line should list its name, the number of open slots, and its
preference list of the residents (most preferred first). A blank line would
separate the hospital block from the resident block. Each resident line
should list their name and their preference list of hospitals (most preferred first).

THE ALGORITHM:
We implemented a modified version of the Gale-Shapley algorithm to be able
to handle the Hospital/Residents version of the Stable Matching Problem,
this is where hospitals can have more than one open slot and there is
also a surplus of residents compared to the total slots that are available.

Each resident should propose to hospitals in order of their own preference
list, one at a time. If the hospital they propose to still does have an open
slot, the resident should be accepted immediately. Instead, if the hospital is
already full, the hospital should then compare the new proposer to the
least-preferred resident that it is currently holding. If the hospital prefers
the new proposer over the currently holding one, that resident is accepted and
the previously-held resident is displaced back into the pool of free residents
to be able to keep proposing elsewhere. Although If the hospital prefers the
resident it already has, the new proposer is then rejected and moves on to their
next choice. This will continue until no free resident has any hospital left that
they can propose to. But because there are more residents than slots, some
residents may end up permanently unmatched.

Full pseudocode is included as a comment block that can be seen at the top of
Assignment_1.py.

STABILITY CHECK:
After the matching is fully completed, the program should then independently verify
the stability by checking for two kinds of instability, that are defined in the
assignment handout:

  The first one: An assigned resident s is at the hospital h, an unassigned
  resident s' exists, and h prefers s' over the assigned s.

  The second one: Resident s is at the hospital h, resident s' is at the hospital
  h', h prefers s' over the resident s, and s' prefers h over the hospital h'.

The program also checks that every hospital's slots was completely filled as
well. If no instabilities are found and all the slots are filled, then the
program should report "Stable Matching: YES"; otherwise it should report "NO"
and prints which instability was found.

SAMPLE TEST CASES:

1. sample_input_1.txt
   3 hospitals that are MERCY, CITY, GENERAL and 6 residents, with a total of 5 slots
   are available. This tests a straightforward multi-hospital case where every hospital
   ranks every resident and also the other way around, and there is exactly one resident
   (NINA) who ends up completely unmatched due to the amount of surplus.

2. sample_input_2.txt
   3 hospitals That are NORTH, SOUTH, WEST and 5 residents, with a total
   of 4 slots. This tests a different configuration of preferences that lead
   to a different resident (ZARA) being left completely unmatched, to confirm
   that the algorithm isn't just working for only one specific arrangement.

3. sample_input_edge_case.txt
   3 hospitals that are ALPHA, BETA, GAMMA and 6 residents. This is our edge case:
   several residents such as CARLA, DAN, ERIC list only one hospital in their
   preferences list instead of ranking all of them. This tests what happens when a
   resident has a very short preference list and even may be rejected by their only
   choice, leaving them with absolutely nowhere else to propose to and confirming
   that the program handles this without any errors.

All three test cases were ran through the program and produced the outputs
that are shown in their corresponding sample_output files, and were confirmed
to be stable by both the program's own stability checker and an independent
manual check done by someone in the team.