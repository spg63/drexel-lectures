---
theme: drexel
aspectRatio: 16/9
canvasWidth: 980
title: "CS 510 · Constraint Reasoning"
layout: cover
kicker: CS 510 · Week 6
---

<!-- source: slide 1 -->

# Constraint Reasoning

Artificial intelligence

<small>Sean Grimes · Some slides adapted from Ehsan Khosroshahi , Santiago Ontañón, Rachel Greenstadt, and Russell and Norvig’s website</small>

---
hide: true
---

<!-- source: slide 2 -->

# EC Presentations

- Sauransh Bhardwaj
   - Current state of tech, focus on future of AI as Deep Tech
- THURSDAY INSTEAD OF TODAY!

---

<!-- source: slide 3 -->

# Reminders

- Assignment 3 is due November 1<sup>st</sup>.
- Assignment 4 is out (after class), due November 15<sup>th</sup>.
   - Based on minimax / AB-pruning
   - Don’t wait to get started on this, we’re going far away from minimax logically, don’t forget how to do it!

---

<!-- source: slide 4 -->

# Assignment Note

- Make sure your code runs on tux as is, without modification.
- The working directory in PyCharm / other IDEs is *not* the same working directory when running from the command line!
- Your run.sh script must work. Some blank submissions, some nonsense submissions. Clearly these weren’t tested on tux. You will not receive credit for A3 and onwards if this doesn’t work.

---

<!-- source: slide 5 -->

# Exam Questions

- <u>Of the following environment descriptions, which is the most difficult for an agent to successfully operate (maximize performance) in</u>
- Answer: Partially observable, multi-agent, non-deterministic, sequential, dynamic, continuous
- Why (follow-up question)
   - **Partially observable**: is harder than fully observable. Try dodging a ball with a blindfold.
   - **Multi-agent:** indicates cooperation or competition, both require additional agent knowledge
   - **Non-deterministic:** means outcomes of your actions, or perhaps what action you take, is not 100% knowable, harder than knowing what action you take, and what the outcome will be
   - **Sequential:** actions from previous ‘episodes’ impact current decisions. Also need to take into account how current decision impacts future decisions. **We’re about to get to this in MDPs!**
   - **Dynamic:** Environmental changes while deciding on what decision to make is more difficult than the world stopping and waiting for you to make a decision
   - **Continuous:** By default, infinite search space, you will never find the exact perfect decision. E.g., turn the steering wheel 9.85927583904 degrees may be a bit worse than 9.85927583903 degrees. Good luck figuring that out!

---

<!-- source: slide 6 -->

# Exam Questions

- <u>Online sales website PEAS to determine high quality from low quality products & recommend which product to buy based on user preference (high, low quality / min. cost)</u>
- Performance: Some method to determine quality to cost ratio with maximizing this ratio
- Environment: Two paths (at least)
   - Online sales website
   - Price listings, brand names, seller names, item details (weight, materials, dimensions, etc…)
      - If general here, the percepts need to be more specific
      - If specific here, the percepts need to go a different direction
- Actions: Two paths (at least)
   - Recommend products, compare prices, compare quality, etc…
   - Query item details, read reviews, find price, compare other items for sale by seller, use search engine
- Percepts: Two paths (at least)
   - Price, quality, analyze reviews / ratings, check on other products from same seller
   - Database access & analysis, analyze search engine results regarding seller(s) and product(s)
- **Other answers would also be acceptable, as long as they make sense!!**

---
layout: split
flip: true
---

<!-- source: slide 7-12 -->

# Exam Questions

::left::

1. S

<div v-click>

2. S→A, S→B

</div>

<div v-click>

3. S→B, S→A→C, S→A→D

</div>

<div v-click>

4. S→A→C, S→A→D, S→B→G

</div>

<div v-click>

5. S→A→D, S→B→G

</div>

<div v-click>

6. Path found ^^ S→B→G is dequeued

<span class="dx-red">NOTE: Follow the directions, a final path was required.</span>

</div>

::right::

<img src="/img/s12-0.png" class="fig" style="max-height:253px" />

<div class="caption">

**Using BFS, show open list / fringe at each step from S→G**

</div>

---
layout: split
flip: true
---

<!-- source: slide 13 -->

# Exam Questions

::left::

I will show the node, and the f(n) [g(n) + h(n)] values, and closed list

1. S = 0 + 0 = **0** → note, this h(n) is admissible, but not helpful.

::right::

<img src="/img/s13-0.png" class="fig" style="max-height:253px" />

<div class="caption">

**Using A*, show open list / fringe at each step from S→G**

</div>

---
layout: split
flip: true
---

<!-- source: slide 14 -->

# Exam Questions

::left::

1. S = 0
2. S→A (6+6 = **12**); S→B(15 + 9 = **24**) [S]

::right::

<img src="/img/s14-0.png" class="fig" style="max-height:253px" />

<div class="caption">

**Using A*, show open list / fringe at each step from S→G**

</div>

---
layout: split
flip: true
---

<!-- source: slide 15 -->

# Exam Questions

::left::

1. S
2. S→A(12); S→B(24) [S]
3. S→A→C(6+6+3 = **15)**; S→B (24); S→A→D (6+12+3 = **21)** [S, A]

::right::

<img src="/img/s15-0.png" class="fig" style="max-height:253px" />

<div class="caption">

**Using A*, show open list / fringe at each step from S→G**

</div>

---
layout: split
flip: true
---

<!-- source: slide 16-17 -->

# Exam Questions

::left::

1. S
2. S→A(12); S→B(24) [S]
3. S→A→C(15); S→B(24); S→A→D(21) [S, A]
4. S→B(24); S→A→D(21) [S, A, C] → ‘C’ is expanded, but is a dead end

<div v-click>

5. S→A→D→G (6+12+6+0 = **24**), S→B (24) [S, A, C]

S→A→D→G <span class="dx-red">Popped, goal found</span>

</div>

::right::

<img src="/img/s17-0.png" class="fig" style="max-height:253px" />

<div class="caption">

**Using A*, show open list / fringe at each step from S→G**

</div>

---
layout: split
flip: true
zoom: 0.61
---

<!-- source: slide 18-20 -->

# Exam Questions

::left::

<span class="dx-red">**THE QUESTION WAS SPECIFIC WITH NUMBER OF LINES LEFT IN THE SEARCH BUT THIS IS ALSO A VALID PATH BASED ON TIE-BREAKING RULES YOU MAY HAVE BEEN USING**</span>

1. S
2. S→A(12); S→B(24) [S]
3. S→A→C(15); S→B(24); S→A→D(21) [S, A]
4. S→B(24); S→A→D(21) [S, A, C] → ‘C’ is expanded, but is a dead end
5. S→A→D→G (6+12+6+0 = **24**), S→B (24) [S, A, C]
6. S→B→G (15+15+0 = **30**), S→B→D (15+3+3 = **21**), S→A→D→G (24) [S, A, C, B]

<div v-click>

7. S→B→G (30), S→B→D→G (15+3+6+0 = **24**), S→A→D→G(24) [S, A, C, B, D]

</div>

<div v-click>

8. S→A→D→G (24) returned as lowest cost solution (it’s popped from open list)

Note(s):

9. S→B→D→G has the same cost, but would be popped second using tie-breaking rules

</div>

::right::

<img src="/img/s20-0.png" class="fig" style="max-height:253px" />

<div class="caption">

**Using A*, show open list / fringe at each step from S→G**

</div>

---
layout: split
flip: true
---

<!-- source: slide 21 -->

# Exam Questions

::left::

<span class="dx-red">Most common mistakes:</span>

1. Not tracking the open list correctly
   1. Not paying attention to the arrows for ‘C’
   2. Not supplying the final path
   3. Providing a path length longer than requested – A* question told you how many more moves were needed, e.g. ”The following table shows the contents of the open list for the first 2 steps. Fill in the remaining 3 lines.”

::right::

<img src="/img/s21-0.png" class="fig" style="max-height:253px" />

---
layout: split
---

<!-- source: slide 22 -->

# Exam Questions

::left::

- <u>Is the heuristic admissible?</u>
- Yes, it never over-estimates on any path
- You could tell me that, or show me all the examples, either way I just wanted some kind of proof you knew what admissibility meant

::right::

<img src="/img/s22-0.png" class="fig" style="max-height:253px" />

---

<!-- source: slide 23 -->

# Exam Questions

- <u>Memory usage for local search in large / infinite state spaces where systematic algorithms are unsuitable</u>
- <u>What is the memory usage for these algorithms?</u>
- Any kind of sentence that tell me memory usage for local search is very low, low space complexity. Environmental conditions don’t change the way the algorithms work! Extra happy if you mention that the path to the goal ain’t important.
- <span class="dx-red">PEAS: Serious, numbers for performance!</span>
- <span class="dx-red">Exam average: XX.XX%</span>

---
hide: true
---

<!-- source: slide 24 -->

# Exam Questions

- BFS might find a suboptimal solution
   - This was a bad question, and I had the wrong answer. All who saw it received full credit regardless of answer.
- A* is guaranteed to be complete only if used with an admissible heuristic
   - No. Consistent heuristics matter, reference slides from week 3, “A* Graph Search Gone Wrong?” and “Consistency of Heuristics” where I discussed the easy solution, <span class="dx-red">reopening</span>.
- Given enough time, Hill Climbing ensures it will explore the complete search space
   - No, infinite environments?
- DFS might find a suboptimal solution
   - Yes, frequently.

---
hide: true
---

<!-- source: slide 25 -->

# My Last Exam Comment(s)

- 64 people are taking the class
- 63 people took the midterm exam
- 13 people used AI on the exam in a way obvious enough that I could quickly identify it
- 20.313% is shit
- You should come talk to me sooner rather than later if you were one of those 13 people, starting with an email.
- As I mentioned before, the exam questions are designed in a way that makes it obvious when you use AI. They (ChatGPT, Gemini, etc…) answer them (incorrectly, sometimes) in very specific ways.

---
hide: true
---

<!-- source: slide 26 -->

# Exam Questions

<div class="figs">
<img src="/img/s26-0.png" class="fig" style="width:761px;max-height:342px" />
</div>

<!--
Which branch can get pruned? J! That’s the only one!
-->

---
hide: true
---

<!-- source: slide 27 -->

# Exam Questions

<div class="figs">
<img src="/img/s27-0.png" class="fig" style="width:761px;max-height:342px" />
</div>

<!--
Run through it with pen!

Max move???????
-->

---
zoom: 0.84
---

<!-- source: slide 28 -->

# Exam Questions

<div class="figs">
<img src="/img/s28-0.png" class="fig" style="width:396px;max-height:211px" />
<img src="/img/s28-1.png" class="fig" style="width:297px;max-height:313px" />
</div>

<span class="dx-red">NOTE:</span> Never again with this extra credit question, it takes a *long* time to grade. ~30 students in this class and somehow ~30 different approaches for me to try to figure out. Some explained better than others.

This is the question that caused the grading to be a bit slower than I usually am for getting exams back to you.

Yes, I got bored and wasted time on AI image generation.

<span class="dx-red">**REMINDER FOR SEAN: Canvas is weird about EC.**</span>

---
layout: split
---

<!-- source: slide 29 -->

# What is Search For?

::left::

- Assumptions about the world: a single agent, deterministic actions, fully observed state, discrete state space
- Planning: sequences of actions
   - The path to the goal is the important thing
   - Paths have various costs, depths
   - Heuristics give problem-specific guidance
- Identification: assignments to variables
   - The goal itself is important, not the path
   - <span class="dx-green">All paths at the same depth (for some formulations)</span>
   - CSPs are specialized for identification problems

::right::

<img src="/img/s29-fig.png" class="fig" style="max-height:130px" />

<!--
CSPs are the last bit of standard search, they’re a nice bridge to MDP and RL that we’re going to do next

CSPs are a specialized subset of general search problems that we can optimize for and come up with far more efficient solutions

We have a lot more rules now which lead to these optimizations

With previous search methods, we knew where we wanted to go, we just needed to know how to get there

Like we saw with local search, with CSPs we only care about getting to the goal, how we get there isn’t important
-->

---
layout: split
---

<!-- source: slide 30 -->

# Constraint Satisfaction Problems

::left::

- Standard search problems:
   - State is a “black box”: arbitrary data structure
   - Goal test can be any function over states
   - Successor function can also be anything
- Constraint satisfaction problems (CSPs):
   - A special subset of search problems
   - State is defined by <span class="dx-red">variables</span> <span class="dx-red">$X_{i}$</span>  with values from a <span class="dx-red">domain</span> <span class="dx-red">$D$</span> (sometimes $D$ depends on $i$)
   - Goal test is a <span class="dx-red">set of constraints</span> specifying allowable combinations of values for subsets of variables
- Allows useful general-purpose algorithms with more power than standard search algorithms

::right::

<img src="/img/s30-0.png" class="fig" style="max-height:252px" />
<img src="/img/s30-1.png" class="fig" style="max-height:185px" />

<!--
Previously, state was really just a black box, we couldn’t really reason about it in a useful way

The nodes were just a generic structure with data and we built out the search trees as we move through the search space

With CSPs the goal has a well-defined structure

The constraints are basically rules around what our goals are

The variables are what define the states, the variables can be assigned values from the domains

Sometimes the domains for variables are specific to certain variables, sometimes any domain can be assigned to any variable

The goal test is simply checking to see if we’ve satisfied all of the constraints

Before: states were nodes, no structure, just a set; they could be anything

Goal test – like a judge; just makes decisions; you don’t know how;

Now: The goal test has structure, it‘s more like a manual describing a set of constraints that have to hold true.

The basic idea behind CSP is to fix the representation of the states to a fixed set of the variable where each variable is from a specific Domain.

So we have a fixed set of variables and each variable can take values from a specific domain.

(write it on the board)

(e.g. imagine a problem that var 1 can take {1,2} and var 2 can take {A,B,C})
-->

---

<!-- source: slide 31 (override) -->

# Constraint Satisfaction Problems (CSPs)

- $n$ variables
- Domain $D_i$
- Constraints

<br>

- CSP:
   - <span class="dx-green">State</span> is defined by <span class="dx-blue">variables</span> $X_i$ with <span class="dx-blue">values</span> from <span class="dx-blue">domain</span> $D_i$
   - <span class="dx-green">Goal test</span> is a set of <span class="dx-blue">constraints</span> specifying allowable combinations of values for subsets of variables

<!--
All CSPs will have some ‘n’ number of variables, specific domains, or values for variables, and rules we need to satisfy

With CSPs, the state is defined by the variables and the values assigned to the variables

The goal test is, again, did we satisfy the constraints, or rules, for this problem, by assigning some values to the variables we have that satisfies the constraints

The goal of CSP is to find an assignment of Variables to values that satisfy certain constraints.

So this is very general, but the advantage here is that we can define search algorithms that are more efficient than the algorithms that we have seen so far.

So, What we are doing here is that we are writing an algorithm specific to a problem by defining a fixed set of variables and trying to satisfy a specific constraint.

The trade-off here is that by CSP problem, we can make it more efficient than the general algorithms, although we reduce the generality of the problem.
-->

---
hide: true
---

<!-- source: slide 32 -->

<div class="figs">
<img src="/img/s32-0.png" class="fig" style="width:485px;max-height:342px" />
</div>

<!--
The basic idea behind CSP is to fix the representation of the states to a fix set of variable where each variable is from a specific Domain.

e.g. imagine a problem that var 1 can take {1,2} and var 2 can take {A,B,C}

So we have a fix set of variable and each variable  can take values from a specific domain.

The goal in CSP is to find an assignments of Variable to values that satisfied a certain constraints.

So this is very general but the advantage here is that we can define search algorithms that are more efficient than the algorithms that we have seen so far.

So, What we are doing here is that we are writing an algorithm specific to a problem by defining a fix set of variable and trying to satisfy a specific constraint.

The trade-off here is a that by CSP problem we can make it more efficient than the general algorithms although we reduce the generality of the problem.
-->

---

<!-- source: slide 33 -->

# CSP Examples

<div class="figs">
<img src="/img/s33-0.png" class="fig" style="width:459px;max-height:342px" />
</div>

<!--
We can go through a quick example to visualize what we’re talking about

We have Australia here

The states need to be colorized for a map

No two adjacent states can have the same color

Notice that Tasmania is separate from the rest of Australia, this will become important later as we state looking at how we can optimize this problem

Our variables are the states (read them)

Our values in this domain – for all variables – are red, green, and blue

The constraints – no adjacent constraints can have the same values

I want you to practice formalizing real problems as search/csp problems

Let’s look at an example.

(Formulating the problem)

You have three colors, red / blue / green, and we want to apply this so no two adjacent states can have similar colors
-->

---
layout: split
ratio: 1.4fr 1fr
---

<!-- source: slide 34 (override) -->

# Example: Map Coloring

::left::

- **Variables:** WA, NT, Q, NSW, V, SA, T
- **Domains:** $D = \{\text{red}, \text{green}, \text{blue}\}$
- **Constraints:** adjacent regions must have different colors
   - Implicit: $\text{WA} \neq \text{NT}$
   - Explicit: $(\text{WA}, \text{NT}) \in \{(\text{red}, \text{green}), (\text{red}, \text{blue}), \ldots\}$
- **Solutions** are assignments satisfying all constraints, e.g.:
   - {WA=red, NT=green, Q=red, NSW=green, V=red, SA=blue, T=green}

::right::

<img src="/img/s34-0.png" class="fig" style="max-height:230px" />
<img src="/img/s34-4.png" class="fig" style="max-height:140px" />

<!--
We can look at some different ways to represent this, informally and formally

Read the variables and domains

Implicit vs explicit

I don’t care how you represent these things

Solutions as a set

Ask the students about what the variables and domains are.

How do you specify constraints in code/math? Implicit vs explicit.

What might be explicit?
-->

---
hide: true
---

<!-- source: slide 35 -->

# Example: N-Queens

- Can you formulate the n-queens problem as a CSP?
   - Consider a fixed n scenario, e.g. n = 4
- Variables
- Domains
- Constraints

<!--
(Ask student students)
-->

---
hide: true
---

<!-- source: slide 36 -->

# Example: N-Queens

- Formulation 1:
   - Variables:
   - Domains:
   - Constraints

<div class="figs">
<img src="/img/s36-fig.png" class="fig" style="width:65px;max-height:56px" />
<img src="/img/s36-0.png" class="fig" style="width:156px;max-height:165px" />
<img src="/img/s36-1.png" class="fig" style="width:134px;max-height:56px" />
<img src="/img/s36-2.png" class="fig" style="width:469px;max-height:29px" />
<img src="/img/s36-3.png" class="fig" style="width:534px;max-height:101px" />
</div>

<!--
X_ij shows the locations of the queens

Domains are 0 or 1, when it’s 1 then there’s a queen there.

For every I, j, k there’s a tuple X_ij X_ij we want to say that no two queens are in a position to attach another

This shows rows, column, and the diagonals.

Are these constraints enough? No, there should be N queens there.
-->

---
hide: true
---

<!-- source: slide 37 -->

# Example: N-Queens

- Formulation 2:
   - Variables:
   - Domains:
   - Constraints:

<div class="figs">
<img src="/img/s37-fig.png" class="fig" style="width:464px;max-height:101px" />
<img src="/img/s37-0.png" class="fig" style="width:30px;max-height:25px" />
<img src="/img/s37-1.png" class="fig" style="width:150px;max-height:25px" />
<img src="/img/s37-2.png" class="fig" style="width:156px;max-height:165px" />
<img src="/img/s37-3.png" class="fig" style="width:30px;max-height:24px" />
<img src="/img/s37-4.png" class="fig" style="width:31px;max-height:24px" />
<img src="/img/s37-5.png" class="fig" style="width:31px;max-height:24px" />
<img src="/img/s37-6.png" class="fig" style="width:31px;max-height:24px" />
<img src="/img/s37-7.png" class="fig" style="width:42px;max-height:6px" />
</div>

<!--
Variables:

X1, X2, X3, X4

Since we can only have 1 queen per row, we just need to specify the X coordinate of the queen in each of the 4 rows

Domains:

{1,2,3,4} for all four variables

Constraints:

Vertical attacks: X1 != X2, X1 != X3, X1 != X4, etc.

Diagonal attacks, e.g. |(X1-X2)| ≠ 1, |(X1-X2)| ≠ 2, etc.

Horizontal attacks can never happen, as we only have 1 queen per row ☺︎
-->

---
hide: true
---

<!-- source: slide 38 -->

# Example: N-Queens

- Can you formulate the n-queens problem as a CSP?
   - Consider a fixed n scenario, e.g. n = 4
- Variables:
   - <span class="dx-blue">X1, X2, X3, X4</span>
   - <span class="dx-blue">Since we can only have 1 queen per row, we just need to specify the X coordinate of the queen in each of the 4 rows</span>
- Domains:
   - <span class="dx-blue">{1,2,3,4} for all four variables</span>
- Constraints:
   - <span class="dx-blue">Vertical attacks: X1 != X2, X1 != X3, X1 != X4, etc.</span>
   - <span class="dx-blue">Diagonal attacks, e.g. |(X1-X2)| ≠ 1, |(X1-X2)| ≠ 2, etc.</span>
   - <span class="dx-blue">Horizontal attacks can never happen, as we only have 1 queen per row ☺︎</span>

---
layout: split
---

<!-- source: slide 39 -->

# Constraint Graphs

::left::

- Binary CSP: each constraint relates to (at most) two variables
- Binary constraint graph: nodes are variables, arcs show constraints
- General-purpose CSP algorithms use the graph structure to speed up search. E.g., Tasmania is an independent subproblem!

::right::

<img src="/img/s39-0.png" class="fig" style="max-height:268px" />

<!--
One way to visualize this is as a constraint graph

The nodes represent the variables

And the constraints are represented by edges

This is a binary CSP where we’re looking at pair-wise comparisons between variables

Notice Tasmania again, represented here as a separate graph

In a small problem like this that’s not a big deal, but splitting the graph into multiple components can lead to dramatic speedups for larger problems

Sub problems, cut-sets, graphs, linearized graphs

One way to visualize a CSP is to show it as a constraint graph.

Here the nodes represents the variables and constraint are represented as edges. In this particular example we have a Binary CSP which means that each constraint relates at most to two variables. That’s why we could visualize it in this simple graph structure.

So some thing interesting by looking at this graph is that we can find subproblems for this graph.

For example here we have Tasmania which is disconnected from the rest of the graph, so it does not matter what color we are assigning to it. Using the graph structure, we can easily define algorithms that could find these subproblems and solve them independently. (Which usually has linear time)
-->

---
layout: split
flip: true
---

<!-- source: slide 40 -->

# Example: Sudoku

::left::

- Variables:
   - Each (open) square
- Domains:
   - {1,2,…,9}
- Constraints:

9-way alldiff for each column

9-way alldiff for each row

9-way alldiff for each region

**alldiff means all different numbers in that direction**

::right::

<img src="/img/s40-fig.png" class="fig" style="max-height:400px" />

<!--
Ask students who knows the rules for sudoku when it comes to constraint then ask about constraints then watch as they realize that constraints are just rules.

Draw some of the rules for students

Then show off the constraints just match up with the rules of the game

Don’t need to get fancy with how you list the constraints, just make them obvious
-->

---

<!-- source: slide 41 -->

# Varieties of CSPs

- Discrete Variables
   - Finite domains
      - Size $d$ means O($d^{n}$) complete assignments
      - E.g., Boolean CSPs, including Boolean satisfiability (NP-complete)
   - Infinite domains (integers, strings, etc.)
      - E.g., job scheduling, variables are start/end times for each job
      - Linear constraints solvable, nonlinear undecidable
- Continuous variables
   - E.g., start/end times for Hubble Telescope observations
   - Linear constraints solvable in polynomial time by LP methods

<!--
There’s plenty of different kinds of CSPs

The simplest ones have discrete variables with finite domains

An example of this is the map coloring problem we’re looking at tonight

Some NP-hard problems fall into this category, SAT problems (Boolean satisfiability problems), which can be formulated as a CSP problem

Some also have infinite domains like scheduling problems with different tasks that need to be done given specific start and end times

Continuous variables – not really going to get into this, there’s different methods involved and different goals, the background to get here doesn’t really fit in with where we’re moving to next in the material

SO we have different type of CSPs which have different variables and constraints

In term of variable the simplest one is discrete variables that have finite domains .

E.g. the map-coloring problem that we saw

In this category we also have the SAT problems (Boolean satisfiability problem) which is NP-complete (if remember from algorithm) and we can formulate that with a CSP structure.

Then there are discrete variables that have infinite domains, such as integers or strings.

E.g., we can say scheduling a job that consists of different tasks and tasks that have a start/end day is discrete.

Similar to project management algorithms.

……

Continuous domain

At then we have Vars that have a continuous domain like scheduling the start/ end time for the Hubble Telescope observations.

The difference here is that we have to define the schedule at a very fine grain at a precise moment of time.

There are different algorithm for non-continuous and continuous, but we are just covering the non-continuous algorithms today.
-->

---

<!-- source: slide 42 (override) -->

# Varieties of Constraints

- **Unary** constraints involve a single variable (equivalent to reducing domains), e.g. $\text{SA} \neq \text{green}$
- **Binary** constraints involve pairs of variables, e.g. $\text{SA} \neq \text{WA}$
- **Preferences** (soft constraints):
   - E.g., red is better than green
   - Often represented by a cost for each variable assignment
   - Gives constrained optimization problems
   - (We’ll ignore these until we get to Bayes’ nets)

<!--
Unary constraints only apply to a single variable

Like saying that south Australia cannot be green

Binary constraints apply to pairs

Like saying that south Australia cannot be the same color as western Australia

You can also have soft constraints which don’t need to be satisfied but are things you would prefer to be satisfied
-->

---
layout: split
---

<!-- source: slide 43 -->

# Real-World CSPs

::left::

- Assignment problems: e.g., who teaches what class
- Timetabling problems: e.g., which class is offered when and where?
- Hardware configuration
- Transportation scheduling
- Factory scheduling
- Circuit layout
- Fault diagnosis
- … lots more!
- Many real-world problems involve real-valued variables…

::right::

<img src="/img/s43-0.png" class="fig" style="max-height:257px" />

<!--
Here’s a handful of examples of where they’re used

Explain some of them
-->

---

<!-- source: slide 44 -->

# Solving CSPs

<div class="figs">
<img src="/img/s44-0.png" class="fig" style="width:677px;max-height:342px" />
</div>

<!--
SO how we solve CSPs! What algorithm we use for solving such a problem.
-->

---

<!-- source: slide 45 -->

# CSPs as Local Search

<div class="figs">
<img src="/img/s45-0.png" class="fig" style="width:674px;max-height:342px" />
</div>

<!--
We can think about how to solve these problems in a few different ways

Looking at it from a local search standpoint first

We learned about local search last week: Hill climbing, simulated annealing.

These work for complete states, where all var are assigned.

Here we can use the same idea for CSPs
-->

---
layout: split
---

<!-- source: slide 46 -->

# Iterative Algorithms for CSPs

::left::

- Local search methods typically work with “complete” states, i.e., all variables assigned
- To apply to CSPs:
   - Take an assignment with unsatisfied constraints
   - Operators *reassign* variable values
   - No fringe!  Live on the edge.
- Algorithm: While not solved,
   - Variable selection: randomly select any conflicted variable
   - Value selection: min-conflicts heuristic:
      - Choose a value that violates the fewest constraints
      - I.e., hill climb with h(n) = total number of violated constraints

::right::

<img src="/img/s46-fig.png" class="fig" style="max-height:42px" />

<!--
The only thing I’m going to say about this is it’s generally a bad way to solve these problems. On small problems like we’ll see, it works reasonably well and is a simple algorithm. The little demo that we’re going to see is a bit misleading on that, since with any larger problems, either in number or variables, domains, or constraints, it typically has very poor performance since you’re not really using the information about the constraints

You’re doing things randomly

Basically you just randomly assign different domains to different variables until you find a set of assignments that work

Yes, you can get a bit more complex than this, but big picture, this is what you’re doing with local search based algorithsm
-->

---

<!-- source: slide 47 -->

# Demo – Iterative Algorithm (Complex Graph)

- [https://www.cs.cmu.edu/~15281/demos/csp_backtracking/](https://www.cs.cmu.edu/~15281/demos/csp_backtracking/)
- Complex
- Iterative
- Ordering: none
- Filtering: none

<!--
Settings:

Complex

Iterative improvement

Ordering: none

Filtering: none

You randomly initialize the environment

Edges highlights in orange have a conflict based on no two adjacent nodes having the same color

Edges that are just black have no conflict
-->

---

<!-- source: slide 48 -->

# Example: 4-Queens

<div class="figs">
<img src="/img/s48-0.png" class="fig" style="width:539px;max-height:168px" />
</div>

- States: 4 queens in 4 columns (4<sup>4</sup> = 256 states)
- Operators: move queen in column
- Goal test: no attacks
- Evaluation: c(n) = number of attacks

<!--
A lot of problems can be simplified to CSPs instead of using local search

In most cases, if you can turn something into a CSP, it’s going to be solved more quickly than with local search

What do you need? Fully observable environment
-->

---
hide: true
layout: split
flip: true
---

<!-- source: slide 49 -->

# Performance of Min-Conflicts

::left::

- Given random initial state, can solve n-queens in almost constant time for arbitrary n with high probability (e.g., n = 10,000,000)!
- The same appears to be true for any randomly-generated CSP *except* in a narrow range of the ratio

::right::

<img src="/img/s49-0.png" class="fig" style="max-height:196px" />
<img src="/img/s49-1.png" class="fig" style="max-height:50px" />

<!--
So using this min-conflict problem, We can solve it in constant time even for 10,000,000

So very quick.

So one interesting thing here is that people ran these experiments and computed the average CPU time as a function of the ratio of # of constraints over # of vars.

(type of problem basically and how hard the problem is)

And this is what they found there is this spot where the CPU time is very high.

So if your number of constraints is high compared to the # of vars, then you will be backtracking very early in the tree.

You don’t have to go all the down to see there are no solutions.

If there are very few constraints, things will be easy. Things are closer to a tree of instructions

In the tricky spot, There are a few solutions that are out there, and you really need to work out to figure that out.
-->

---

<!-- source: slide 50 -->

# CSPs as Standard Search

<div class="figs">
<img src="/img/s50-0.png" class="fig" style="width:462px;max-height:260px" />
</div>

<!--
While local search may seem like the more advanced algorithm, standard search actually works better for CSPs

In particular, we’re going to use DFS as the basis for all of the CSP algorithms we’re going to run, but we’re going to do a lot to improve it

Remember way back when I talked about ordering the search tree to better match up with the data….well now we’re finally going to learn about a couple of different ways to do that
-->

---
layout: split
---

<!-- source: slide 51 -->

# Standard Search Formulation

::left::

- Standard search formulation of CSPs
- States defined by the values assigned so far (partial assignments)
   - Initial state: the empty assignment, {}
   - Successor function: assign a value to an unassigned variable
   - Goal test: the current assignment is complete and satisfies all constraints
- We started with the straightforward, naïve approach, then improved it

::right::

<img src="/img/s51-0.png" class="fig" style="max-height:189px" />

<!--
When we go through this process, we start assigning different values to the variables and build out the tree from there

The tree gets built out from here
-->

---
layout: split
---

<!-- source: slide 52 -->

# Search Methods

::left::

- What would BFS do?

::right::

<img src="/img/s52-fig.png" class="fig" style="max-height:400px" />

<!--
What would BFS do? Layer by layer by layer

What about DFS? In CSP problems, is it possible to find a solution that’s not on the bottom layer of the tree?

Draw the three states with the options R, G, B

It is impossible to find a solution not on the bottom layer, layers that aren’t the bottom have unassigned variables
-->

---
layout: split
---

<!-- source: slide 53 -->

# Search Methods

::left::

- What would DFS do?

::right::

<img src="/img/s53-fig.png" class="fig" style="max-height:400px" />

<!--
Thus, we will always be using DFS for these problems
-->

---

<!-- source: slide 54 -->

# Demo - DFS

- [https://www.cs.cmu.edu/~15281/demos/csp_backtracking/](https://www.cs.cmu.edu/~15281/demos/csp_backtracking/)
- Simple
- Naïve
- Ordering: none
- Filtering: none

<!--
Settings:

Simple

Naïve Search

Ordering: none

Filtering: none

We will sit here until next class before this finishes

DFS with a 9 node problem is terrible, yet it’s what we will be basing all of the algorithms on that we’re going to talk about
-->

---
layout: split
ratio: 1.3fr 1fr
---

<!-- source: slide 55 (override) -->

# Standard Search Formulation

::left::

A few points:

1. This is the same for all CSPs! ☺
2. Every solution appears at depth $n$ with $n$ variables<br>→ use depth-first search
3. Path is irrelevant, so we can also use a complete-state formulation
4. $b = (n - \ell)\,d$ at depth $\ell$, hence $n!\,d^n$ leaves!!! ☹

::right::

<img src="/img/s55-0.png" class="fig" style="max-height:260px" />

<!--
A few points before we talk about how we can improve on standard DFS

All CSP solutions are found at depth ‘n’ with ‘n’ variables

We don’t care about the path, we just need a solution that satisfies the constraints

The branching factor isn’t very good
-->

---

<!-- source: slide 56 -->

# Backtracking Search

<div class="figs">
<img src="/img/s56-0.png" class="fig" style="width:558px;max-height:342px" />
</div>

<!--
The first thing we’re going to talk about is backtracking. We can use this as a standalone improvement, or as a foundation for further improvements as we increase our algorithm complexity
-->

---

<!-- source: slide 57 -->

# Backtracking Search

- Backtracking search is the basic uninformed algorithm for solving CSPs
- Idea 1: One variable at a time
   - Variable assignments are commutative, so fix ordering
   - I.e., [WA = red then NT = green] same as [NT = green then WA = red]
   - Only need to consider assignments to a single variable at each step
- Idea 2: Check constraints as you go
   - I.e. consider only values which do not conflict previous assignments
   - Might have to do some computation to check the constraints
   - “Incremental goal test”
- Depth-first search with these two improvements

is called *backtracking search* (not the best name)

<!--
With backtracking we still assign variables the same way but variable assignment is commutative, we can learn information about possible states that will work just by assigning variables and following the rules we have in our constraints

The 2nd part is, we only look at assignments that don’t violate the constraints, if we violate a constraint, we bail on that part of the search tree since there’s no point in continuing down that path

This is called back tracking

Only assign a value to one variable at each node.

Because variable assignment is commutative, for example, WA=red, then NT=green is the same is NT=green then WA=red.

(So now we have a branching factor of d, and there will be d^m leaves  at the end.)

Check constraints as you go

I.e., consider only values which do not conflict with previous assignments

some computation

DFS for CSP in this way is called backtracking.

We can reasonably solve an n-queens problem for n=25 with this algorithm.
-->

---

<!-- source: slide 58 -->

# Backtracking Search

<div class="figs">
<img src="/img/s58-fig.png" class="fig" style="width:424px;max-height:342px" />
</div>

<!--
If we look at this example, assign red in bottom right and tell them we cannot possibly find a solution down that path so we backtrack
-->

---

<!-- source: slide 59 -->

# Demo - Backtracking

- [https://www.cs.cmu.edu/~15281/demos/csp_backtracking/](https://www.cs.cmu.edu/~15281/demos/csp_backtracking/)
- Simple
- Backtracking
- Ordering: none
- Filtering: none

<!--
Settings:

Simple

Backtracking

Ordering: none

Filtering: none

We’ve introduced no real intelligence to the search, yet we went from what would have taken a week to what took a second or two, a massive improvement for no real extra work

Now run through this a bit more slowly &#8209;&#8209;→ NEVERMIND IT DOES SOME WEIRD SHIT!!!
-->

---

<!-- source: slide 60 -->

# Backtracking Search

<div class="figs">
<img src="/img/s60-0.png" class="fig" style="width:599px;max-height:308px" />
</div>

- Backtracking = DFS + variable-ordering + fail-on-violation
- What are the choice points?

<!--
This is the basic algorithm for backtracking

The basis for the next few algorithms that we look at will use is DFS w/ backtracking
-->

---
hide: true
---

<!-- source: slide 61 -->

# Exercise

* [https://forms.gle/7V7ConVNUrN1N5ze7](https://forms.gle/7V7ConVNUrN1N5ze7)

- We’re not doing this exercise, you don’t need to do it. **Break time.**

<!--
This is the first of two exercises we’re going to do tonight

You need to think about a CSP and give a formulation that a computer might understand

You have a set of differently sized tiles to tile a rectangular room

You need to tile the room so the room is completely tiled and there is no overlap of any tiles

Give me a formulation that shows how to represent the variables, domains, and constraints → NOT HOW TO SOLVE IT, just how to formulate this problem

&#8209;&#8209;- AFTER SOME TIME &#8209;&#8209;-

This is a tricky problem, it’s continuous since there’s infinite locations in the room, something I said we wouldn’t be solving (and we’re not)…we’re just thinking about how to formulate it

It’s still a binary CSP, you’re just looking at adjacent tiles

How you would solve it: start in a corner and start laying tiles until you tile the room or use up all of the tiles. If you have overlaps, you haven’t satisfied the constraints, start the search over

For the graph: just tell me what the nodes and edges would be, that is, what do the nodes and edges represent in this problem

You need variables, domains, and constraints

Think about this from the perspective of math – you want to code it up, how do you represent these things

Is this discrete or continuous? It’s continuous! Infinite locations within the room.

Binary constraints or higher order? It’s binary!

What are the variables? All of the tiles → the values are based on the coordinate system, 4 numbers per tile to represent the corners

How can you check the constraints?  Make sure that the numbers aren’t overlapping.

For each tile you need to check if it’s overlapping with another tile or not

Sometimes there may not be a solution, why? More tiles than you can fit in the space

Start with a search algorithm, put one at the corner of the room and then start putting all the tiles in and make sure you keep the constrains as you go. If there are still tiles remaining tiles that means you can’t satisfy the constraints.
-->

---

<!-- source: slide 62 -->

# Improving Backtracking

- General-purpose ideas give huge gains in speed
- Filtering: Can we detect inevitable failure early?
- Ordering:
   - Which variable should be assigned next?
   - In what order should its values be tried?
- Structure: Can we exploit the problem structure?

<!--
Time to start thinking on how we can improve back-tracking

Two ways are fundamental to the tree structure

The first is filter which you can think of as forward checking

The second is ordering, deciding which variables we should assign next based on the knowledge we have so far

The third way will be looking at how we can exploit what we know about the structure of the variables

So, so far, if you pay attention, the algorithm is uninformed.

Meaning that there is no additional information, like which states is promising.

So how we can improve the backtracking algorithm?

There were functions that we did not define in the algorithm like SELECT-UNASSIGNED-VARIABLE or ORDER-DOMAIN-VALUES.

SO by making these functions more efficient we give huge gains in speed. Basically, by answering questions like ….

(in a sense make it informed using some kind of a heuristic)?
-->

---

<!-- source: slide 63 -->

# Filtering

<div class="figs">
<img src="/img/s63-fig.png" class="fig" style="width:866px;max-height:37px" />
<img src="/img/s63-0.png" class="fig" style="width:552px;max-height:326px" />
</div>

<!--
With filtering, we want to detect failure as early as possible, well before what basic backtracking can detect

We need to keep track of the domains for all unassigned variables and eliminate any of the values which will violate a constraint
-->

---

<!-- source: slide 64 (override) -->

# Filtering: Forward Checking

- **Filtering:** keep track of domains for unassigned variables and cross off bad options
- **Forward checking:** cross off values that violate a constraint when added to the existing assignment

<div class="figs"><img src="/img/ov64.png" class="fig" style="width:820px" /></div>

<!-- TODO: original is an animation; rebuild as v-click steps -->

<!--
We can look at a basic example here

Each variable has all of the possible values available initially

We first assign red to western Australia, given this, what do we know about norther territory and south Australia ?

They cannot be red!!!

We go through and remove those as possible options

Keep in mind that it looks simple here, but if you think about it from a search tree standpoint, this means we don’t go down those branches, and better yet, those branches never even get built to be explored

We then assign green to queensland and can remove additional values from the domains for south Australia, northern territory, and also new south wales

Right away, what is something you notice now?

NT and SA both only have blue left, this is a violation! Now back-tracking takes over and we move back up a node to where we assigned green to Queensland and we have to assign something different

Forward checking doesn’t eliminate back-tracking, but it does help prune away as much of tree as possible
-->

---

<!-- source: slide 65 -->

# Demo - Backtracking with Forward Checking

- [https://www.cs.cmu.edu/~15281/demos/csp_backtracking/](https://www.cs.cmu.edu/~15281/demos/csp_backtracking/)
- Complex
- Backtracking
- Ordering: none
- Filtering: forward checking

<!--
Settings:

Complex

Backtracking

Ordering: none

Filtering: forward checking

The algorithm now keeps track of what colors can be assigned, go step-wise to show some things and hopefully show something on backtracking as well

Show it without filtering and that it’s slower even though we’re still using back-tracking

Backtracking search

As soon as we switch to forward checking, there is this extra notion: the remaining domains.

When a domain goes empty, we backtrack
-->

---
hide: true
---

<!-- source: slide 66 -->

# Consistency of A Single Arc

- An arc X → Y is <span class="dx-red">consistent</span> iff for *every* x in the tail there is *some* y in the head which could be assigned without violating a constraint
- Forward checking: Enforcing consistency of arcs pointing to each new assignment

<div class="figs">
<img src="/img/s66-fig.png" class="fig" style="width:686px;max-height:123px" />
</div>

<!--
So for propagation the algorithm in forward search uses arc consistency.

arc consistency says: variable X is consistent with variable Y iff every value x of X there is some allowed y in Y other wise we eliminate x and reduce the domain of X

For finding the conflict early, we should look a head and propagates the consistency to all the variables.

AT each stage of coloring. First we start with the immediate neighbors and then neighbors of neighbors and so on so fort.

So think that we are at this stage…
-->

---

<!-- source: slide 67 -->

# Filtering: Constraint Propagation

- Forward checking propagates information from assigned to unassigned variables, but doesn't provide early detection for all failures:
- NT and SA cannot both be blue!
- Why didn’t we detect this yet?
- *Constraint propagation:* reason from constraint to constraint

<div class="figs">
<img src="/img/s67-fig.png" class="fig" style="width:135px;max-height:120px" />
<img src="/img/s67-0.png" class="fig" style="width:486px;max-height:132px" />
</div>

<!--
The theme of tonight is what can we keep doing to solve CSPs more efficiently

Filtering can’t check for constraints violations early on, it just helps prune the tree

We can use an idea of constraint propagation, or arc consistency, to help detect these failures even earlier

Think of this is looking ahead so we can back-track as early as possible
-->

---

<!-- source: slide 68 -->

# Consistency of A Single Arc

- An arc X → Y is <span class="dx-red">consistent</span> iff for *every* x in the tail there is *some* y in the head which could be assigned without violating a constraint

<span class="dx-green">Forward checking?</span>

Enforcing consistency of arcs pointing to each new assignment

<div class="figs">
<img src="/img/s68-fig.png" class="fig" style="width:686px;max-height:123px" />
</div>

<!--
Consistency for a single arc

An arc ‘X’ to ‘Y’ is consistent iff for every ‘x’ in the tail there is some ‘y’ in the head which can be assigned without violating a constraint

Show the head and tail

In the first case, the ‘X’s in the tail are R, G, B. In WA our only ‘Y’ is red

This is consistent for G and B but not for R, so we go through and remove red from the tail section

It’s impossible for NT to be red give WA is already Red

You then need to go through and run this in reverse

For every ‘x’ in the tail, there’s some Y in the head

Can you do this for an entire CSP?
-->

---

<!-- source: slide 69 (override) -->

# Arc Consistency of an Entire CSP

- A simple form of propagation makes sure <span class="dx-red">all</span> arcs are consistent:

<div class="figs"><img src="/img/ov69.png" class="fig" style="width:760px" /></div>

- Important: if X loses a value, neighbors of X need to be rechecked!
- Arc consistency detects failure earlier than forward checking
- Can be run as a preprocessor or after each assignment
- What’s the downside of enforcing arc consistency?

<div class="aside">Remember: delete from the tail!</div>

<!--
Yes, we can go through and check out other constraints for the other variables

Very important: whenever you remove something from the tail, you need to re-run it for any variables that are adjacent to the variable you just removed a value from

What’s the downside? It’s not free, it cost time and energy to run…it’s similar conceptually to a heuristic in A*. You need to find the right balance between running this and allowing the search to progress like normal

What that balance is will depend on your state space

Most of the time it makes sense to go through and enforce this, in particular when you have a high branching factor but if you don’t have a high branching factory, it probably doesn’t make sense.

But there is more arcs that we can consider.

So for finding the conflict early, we should look ahead and propagates the consistency to all the variables.

AT each stage of coloring. First, we start enforcing consistency with the immediate neighbors and then neighbors of neighbors, and so on and so forth.

And every time we delete a var, we have to consider the consistency again to that node, Meaning arc that goes to that node.

So think that we are at this stage we assigned WA and Q …

What’s the downside of enforcing arc consistency?

reminds you of a* - heuristic takes time
-->

---

<!-- source: slide 70 -->

# Enforcing Arc Consistency in a CSP

<div class="figs">
<img src="/img/s70-0.png" class="fig" style="width:525px;max-height:329px" />
</div>

- Runtime: O(n<sup>2</sup>d<sup>3</sup>), can be reduced to O(n<sup>2</sup>d<sup>2</sup>)
- … but detecting all possible future problems is NP-hard – why?

<!--
This is how the algorithm looks, which is called AC-3. I’m not going into detail. (Auto-consistency)

(The time complexity is polynomial but if you want to detect all of it is going to be NP-Complete)

(O(n^2*d^3)

D : domain size

N : number of variables

With some tricks -&gt; (O(n^2*d^2)

(Assume a CSP with n variables, each with domain size at most d, and with c binary constraints (arcs). Each arc (Xk,Xi) can be inserted in the queue only d times because Xi has at most d values to delete. Checking consistency of an arc can be done in O(d^2 ) time, so we get O(cd^3) total worst-case time. C = n^2 )
-->

---
hide: true
---

<!-- source: slide 71 -->

# Demo - Backtracking with Forward Checking (Complex Graph)

- [https://inst.eecs.berkeley.edu/~cs188/fa21/assets/demos/csp/csp_demos.html](https://inst.eecs.berkeley.edu/~cs188/fa21/assets/demos/csp/csp_demos.html)

<!--
Backtracking search

Ordering: none

Filtering: forward checking
-->

---

<!-- source: slide 72 -->

# Demo - Backtracking with Arc Consistency (Complex Graph)

- [https://www.cs.cmu.edu/~15281/demos/csp_backtracking/](https://www.cs.cmu.edu/~15281/demos/csp_backtracking/)
- Complex
- Backtracking
- Ordering: none
- Filtering: arc consistency

<!--
Settings:

Complex

Backtracking

Ordering: none

Filtering: arc consistency

We still had some back-tracking, arc consistency hasn’t eliminated this entirely, even if you enforce it on the entire graph
-->

---
layout: split
---

<!-- source: slide 73 -->

# Limitations of Arc Consistency

::left::

- After enforcing arc consistency:
   - Can have one solution left
   - Can have multiple solutions left
   - Can have no solutions left (and not know it)
- Arc consistency still runs inside a backtracking search!

::right::

<img src="/img/s73-fig.png" class="fig" style="max-height:331px" />

<!--
Here’s a perfect example

The top graph has arc consistency with no back tracking

The bottom graph has arc consistency but we have three variables which are adjacent and only two possible values, it’s impossible for this to work so even though it’s consistent, you will still need to back-track

What is the limitation here?

(the top) all arcs are consistent. 2 values remain

One thing is that enforcing Arc consistency does not solve your problem. It just pruning the domains and help you in your search.

(the bottom)

Arc consistency is ok, but there is no solution.

So since after enforcing arc consistency, we have values that remain does not mean that we have a solution in that branch. No guarantee.

So we still have to backtrack the search.
-->

---
hide: true
layout: split
---

<!-- source: slide 74 -->

# K-Consistency

::left::

- Increasing degrees of consistency
   - 1-Consistency (Node Consistency): Each single node’s domain has a value which meets that node’s unary constraints
   - 2-Consistency (Arc Consistency): For each pair of nodes, any consistent assignment to one can be extended to the other
   - K-Consistency: For each k nodes, any consistent assignment to k-1 can be extended to the k<sup>th</sup> node.
- Higher k more expensive to compute
- (You need to know the k=2 case: arc consistency)

::right::

<img src="/img/s74-fig.png" class="fig" style="max-height:400px" />

<!--
We also have the idea of ‘k’ consistency basically arc consistency for more than a single arc

The more ‘k’ you have, the more compute you need

This might make sense in problems where you have a lot more nodes adjacent to one another, again, it all depends on your state space and problem requirements

You could theoretically insist on consistency for all of the variables in your problem. If you do this, it’s guaranteed to be at least as slow as DFS with back-tracking, and often times slower than that since enforcing consistency is usually more computationally complex than simple back-tracking search

So what is going to happen is we increase the degree of consistency.

1-consistency: enforcing consistency for each var. Unary constraint

2-consistency: look s at each pair of variables. Look at the constraints and consistency of the 2 vars.

And you can repeat:

K-consistency: checking any subset of K nodes (can be a lot of nodes if k is large), you take any subset of K-1, and for every consistent assignment of that k-1,  you check if there is a consistent assignment to the extracted kth variable from that set.

If they are not consistent, then that combination of assignments to k-1 var is not valid, and you through it out.

Much bigger representation to run the consistency.

It’s more expensive to do this
-->

---
hide: true
---

<!-- source: slide 75 -->

# Strong K-Consistency

- Strong k-consistency: also k-1, k-2, … 1 consistent
- Claim: strong n-consistency means we can solve without backtracking!
- Why?
   - Choose any assignment to any variable
   - Choose a new variable
   - By 2-consistency, there is a choice consistent with the first
   - Choose a new variable
   - By 3-consistency, there is a choice consistent with the first 2
   - …
- Lots of middle ground between arc consistency and n-consistency!  (e.g. k=3, called path consistency)

<!--
And strong K consistency: you’re k consistent for k= 1, 2 ,3, …, k

And here is the claim: strong n-consistency means we can solve without backtracking!

The catch: n-consistency is very expensive.

A lot of time, you do something that computationally makes sense.
-->

---

<!-- source: slide 76 -->

# Ordering

<div class="figs">
<img src="/img/s76-0.png" class="fig" style="width:780px;max-height:342px" />
</div>

<!--
We’ve talked about how we can eliminate some of the values, reducing the number of paths in the search tree

Now we’re going to talk a bit about how we order the tree, basically how we can more intelligently select which moves to make next
-->

---

<!-- source: slide 77 -->

# Ordering: Minimum Remaining Values

- Variable Ordering: Minimum remaining values (MRV):
   - Choose the variable with the fewest legal left values in its domain
- Why min rather than max?
- Also called “most constrained variable”
- “Fail-fast” ordering
- MRV operates at the level of “which variable do I branch on next?”

<div class="figs">
<img src="/img/s77-fig.png" class="fig" style="width:649px;max-height:137px" />
</div>

<!--
We can think of the next two examples as heuristic functions, basically guiding our search through the possible nodes

By doing this, we’re changing the order that different branches get generated by our search algorithm, re-ordering the tree such that it’s more likely the branches we generate and search early on will have a solution that satisfies the constraints

We’re looking for which variable to assign a value to next

The first way we’re going to do this is with minimum remaining values

We choose the variable with the fewest legal values in it’s domain

Why do we assign the upper right corner? It can only have a single value (red), there’s nothing else it can be.

Why min instead of max? It allows us to back track more quickly

There is a collection of heuristics that are commonly used in CSPs

and the first one is called minimum value heuristics which says that we should choose the variable with the fewest legal values.

for example :

…

So why min rather than max?
-->

---
hide: true
---

<!-- source: slide 78 -->

# Ordering: Degree Heuristic

- Tie-breaker among MRV variables
- Degree heuristic:
   - Choose the variable with the most constraint on remaining variables

<div class="figs">
<img src="/img/s78-0.png" class="fig" style="width:644px;max-height:116px" />
</div>

<!--
The second is for resolving ties and is called Degree heuristic:  it says choose the variable with the most constraints on remaining variables

It’s basically tie breaker

This is because by choosing that one we reduce the search by reducing the most legal value.

( BY choosing blue we can’t pick that color for 5 states)
-->

---
layout: split
---

<!-- source: slide 79 -->

# Ordering: Least Constraining Value

::left::

- Value Ordering: Least Constraining Value
   - Given a choice of variable, choose the *least constraining value*
   - I.e., the one that rules out the fewest values in the remaining variables
   - Note that it may take some computation to determine this!  (E.g., rerunning filtering)
- Why least rather than most?
- LCV operates at the level of “in what order do I try values for this variable?” and may require extra work (e.g., simulating forward checking per candidate value) to count how many neighbor values each candidate prunes.

::right::

<img src="/img/s79-0.png" class="fig" style="max-height:228px" />

<div class="caption">

Allows 1 value for SA

Allows 0 value for SA

</div>

<!--
There’s a second option when we’re looking for guidance on the search through the tree called least constraining value

LCV tells us to pick a value that is least constraining, basically we want the search to continue as long as possible

You pick the path through the tree which gives the least constraining value to the search

Typically minimum remaining values will run faster, but if you have a very high branching factor than LCV may be a better choice since it’s unlikely you will be able to fail quickly

So far we have heuristics about the variables. now a heuristic about which value to pick for each variable:  Least Constraining Value

…

So in conclusion, We can apply these general heuristics to any CSP problem and by applying them we could make the algorithm much faster and more efficient.

e.g. as we said, with Uniformed search of Backtracking for n-queens : we can handle 25 queens

However, by combining these heuristics and making the problem informed: we can handle up to 1000 queens
-->

---

<!-- source: slide 80 -->

# Demo - Backtracking with Arc Consistency and Ordering (Complex Graph)

- [https://www.cs.cmu.edu/~15281/demos/csp_backtracking/](https://www.cs.cmu.edu/~15281/demos/csp_backtracking/)
- Complex
- Backtracing
- Ordering: MRV
- Filtering: arc consistency

<!--
Settings:

Complex

Backtracking

MRV

Arc consistency

This goes faster, but is it as big of a speedup as something like arc consistency? No, arc consistency and filtering cut out roughly half the search tree, giving a massive speedup, but with much bigger problems, all of these optimizations can add up to make a big differene

Backtracking search

Ordering: none

Filtering: arc consistency

Back tracking still exist but is much more limited and much more local.
-->

---

<!-- source: slide 81 -->

# Using MRV and LCV together

- Typical backtracking search uses MRV to pick which variable to assign next, then LCV to pick which value to try first for that variable.
- MRV mainly reduces depth before failure (early detection of dead ends); LCV mainly reduces branching factor by making it more likely the first few values you try lead to a solution.

<!--
Settings:

Complex

Backtracking

MRV

Arc consistency

This goes faster, but is it as big of a speedup as something like arc consistency? No, arc consistency and filtering cut out roughly half the search tree, giving a massive speedup, but with much bigger problems, all of these optimizations can add up to make a big differene

Backtracking search

Ordering: none

Filtering: arc consistency

Back tracking still exist but is much more limited and much more local.
-->

---

<!-- source: slide 82 -->

# Structure

<div class="figs">
<img src="/img/s82-0.png" class="fig" style="width:494px;max-height:342px" />
</div>

<!--
* The last thing to look at is how we can improve upon the structure of the problem
-->

---
layout: split
---

<!-- source: slide 83 -->

# Problem Structure

::left::

- Extreme case: independent subproblems
   - Example: Tasmania and mainland do not interact
- Independent subproblems are identifiable as connected components of constraint graph
- Suppose a graph of n variables can be broken into subproblems of only c variables:
   - Worst-case solution cost is O((n/c)(d<sup>c</sup>)), linear in n
   - E.g., n = 80, d = 2, c =20
   - 2<sup>80</sup> = 4 billion years at 10 million nodes/sec
   - (4)(2<sup>20</sup>) = 0.4 seconds at 10 million nodes/sec

::right::

<img src="/img/s83-0.png" class="fig" style="max-height:293px" />

<!--
In the case where we can naturally split the graph, we do and we can treat them as independent sub-problems

The same constraints still apply, but to each individual sub-problem

Victoria and Tasmania can both be the same color here since they’re not connected, they’re not adjacent

If this was a bigger problem, you can see how this would be helpful, it basically cuts the tree depth in half, on average

Which results in a significant speedup in solving the problem

first thing to consider regarding the structure is to find the subproblem. Like Tasmania here which is disconnected from the mainland.

So just give you how this structure can be helpful suppose that …

C= cluster size
-->

---
hide: true
---

<!-- source: slide 84 (override) -->

# Tree-Structured CSPs

<div class="figs"><img src="/img/s84-0.png" class="fig" style="max-height:190px" /></div>

- **Theorem:** if the constraint graph has no loops, the CSP can be solved in $O(n\,d^2)$ time
   - Compare to general CSPs, where worst-case time is $O(d^n)$
- This property also applies to probabilistic reasoning (later): an example of the relation between syntactic restrictions and the complexity of reasoning

---
hide: true
zoom: 0.84
---

<!-- source: slide 85 -->

# Tree-Structured CSPs

- Algorithm for tree-structured CSPs:
   - Order: Choose a root variable, order variables so that parents precede children
   - Remove backward: For i = n : 2, apply RemoveInconsistent(Parent(X<sub>i</sub>),X<sub>i</sub>)
   - Assign forward: For i = 1 : n, assign X<sub>i</sub> consistently with Parent(X<sub>i</sub>)
- Runtime: O(n d<sup>2</sup>)  (why?)

<div class="figs">
<img src="/img/s85-fig.png" class="fig" style="width:779px;max-height:271px" />
<img src="/img/s85-0.png" class="fig" style="width:411px;max-height:88px" />
</div>

<!--
We’re going to pick some node as the root node, I would go with A or C

We can put this on it’s end, but notice that none of the paths are actually changing, the graph is just being linearized

When we organize the graph like this, we can run arc consistency looking backwards

We do this backwards because in the next step we can then do a forward assignment of values to variables and with backwards arc consistency, we’re guaranteed to have valid assignments

So the algorithm that can solve it in polynomial time goes like this:

1- pick any var as root. Hold up the tree by that root and let everything hang down. (linearization)

( very similar to in-order Traversals for trees in algorithm class)

2- and then, from the end to the beginning, we run the RemoveInconsistency function.

What is happening here is that when we make E and F consistent and D and F. then automatically, E and F will be consistent too because there is no arch (constraint) between them.

3 – from the beginning to the end, we assign values

O(n d2) :

forcing consistency of an arc: O(d2)

the Number of arcs we have to consider is n because, in the linearized graph, every var has at most one arc coming in.

and assignments from the beginning are also ordered n.
-->

---
hide: true
---

<!-- source: slide 86 -->

# Tree-Structured CSPs

- Claim 1: After backward pass, all root-to-leaf arcs are consistent
- Proof: Each X→Y was made consistent at one point and Y’s domain could not have been reduced thereafter (because Y’s children were processed before Y)
- Claim 2: If root-to-leaf arcs are consistent, forward assignment will not backtrack
- Proof: Induction on position
- Why doesn’t this algorithm work with cycles in the constraint graph?
- Note: we’ll see this basic idea again with Bayes’ nets

<div class="figs">
<img src="/img/s86-0.png" class="fig" style="width:439px;max-height:94px" />
</div>

<!--
We’re not doing proofs in this class, but as a general overview claim 1 is supported by what we already know with arc consistency

Claim 2 is a new concept but this is the benefit we get with backwards checking, if we guarantee consistency there, then we guarantee that forward assignment of values to the variables will not back track

Why no cycles? Well 1, a tree structured CSP has no cycles by definition, but more importantly, why won’t it work? You can’t enforce consistency with cycles

We’ll come back to this when we get into ML, but mentioning it now for what comes up on the next slide
-->

---

<!-- source: slide 87 -->

# Nearly Tree-Structured CSPs

<div class="figs">
<img src="/img/s87-0.png" class="fig" style="width:537px;max-height:223px" />
</div>

- Conditioning: instantiate a variable, prune its neighbors' domains
- Cutset conditioning: instantiate (in all ways) a set of variables such that the remaining constraint graph is a tree
- Cutset size c gives runtime O( (d<sup>c</sup>) (n-c) d<sup>2</sup> ), very fast for small c

<!--
We have a graph here which has potential cycles with south Australia, we can’t linearize this graph

With cutsets, we want to figure out what we can remove to get a linearized graph, in this case that’s south Australia
-->

---

<!-- source: slide 88 -->

# Cutset Conditioning

<div class="figs">
<img src="/img/s88-fig.png" class="fig" style="width:808px;max-height:342px" />
</div>

<!--
We then have to run the problem with all possible variations of value for south Australia

Now there’s 3 CSPs to solve, but we greatly simplified the problem

Yes, with a simple problem like this, we could find all the other variable values and pick something for SA, but in a more complex problem that’s not an option, you need to consider all the possible values for the variables being removed
-->

---

<!-- source: slide 89 -->

# Exercise

- Find the smallest cutset for the graph below.

<div class="figs">
<img src="/img/s89-0.png" class="fig" style="width:426px;max-height:269px" />
</div>

<!--
As a small little exercise, what can we remove here to turn the major graph into something that can be linearized
-->

---
hide: true
zoom: 0.6
---

<!-- source: slide 90 -->

# Tree Decomposition*

<div class="figs">
<img src="/img/s90-fig.png" class="fig" style="width:814px;max-height:227px" />
<img src="/img/s90-0.png" class="fig" style="width:266px;max-height:185px" />
</div>

- Idea: create a tree-structured graph of mega-variables
- Each mega-variable encodes part of the original CSP
- Subproblems overlap to ensure consistent solutions

<span class="dx-purple">Agree on    shared vars</span>

<span class="dx-red">{(WA=r,SA=g,NT=b),</span>

<span class="dx-red">(WA=b,SA=r,NT=g),</span>

<span class="dx-red">…}</span>

<span class="dx-blue">{(NT=r,SA=g,Q=b),</span>

<span class="dx-blue">(NT=b,SA=g,Q=r),</span>

<span class="dx-blue">…}</span>

<span class="dx-purple">Agree:</span> (<span class="dx-red">M1</span>,<span class="dx-blue">M2</span>) ∈

{(<span class="dx-red">(WA=g,SA=g,NT=g)</span>, <span class="dx-blue">(NT=g,SA=g,Q=g)</span>),  …}

---
layout: split
flip: true
---

<!-- source: slide 91 -->

# Performance of Min-Conflicts

::left::

- Given random initial state, can solve n-queens in almost constant time for arbitrary n with high probability (e.g., n = 10,000,000)!
- The same appears to be true for any randomly-generated CSP *except* in a narrow range of the ratio

::right::

<img src="/img/s91-0.png" class="fig" style="max-height:196px" />
<img src="/img/s91-1.png" class="fig" style="max-height:50px" />

<!--
A final and important part of CSPs to consider

There’s a specific ratio of constraints to number of variables where the runtime is very high

Let’s say we have a large number of constraints and a low number of variables, this will run much more quickly than an equal number of variables and values

Why? It will backtrack very quickly since you have so many constraints you need to satisfy. Early failures!

Let’s say we have a small number of constraints and a large number of variables, this will also run quickly

Why? You will find a solution quickly, you have plenty of variables and not many rules that need to be satisfied

If there’s anyway for you to reformulate a CSP so the ratio isn’t around 1:1, you will dramatically increase the efficiency of your search
-->

---
layout: split
---

<!-- source: slide 92 -->

# Summary: CSPs

::left::

- CSPs are a special kind of search problem:
   - States are partial assignments
   - Goal test defined by constraints
- Basic solution: backtracking search
- Speed-ups:
   - Ordering
   - Filtering
   - Structure
- Iterative min-conflicts is often effective in practice

::right::

<img src="/img/s92-0.png" class="fig" style="max-height:258px" />

<!--
Summary

CSPs are a specialized and optimized kind of search problem

The basic search is built on DFS and uses back-tracking anytime a constraint violation is discovered

We can use additional optimizations with filtering / forward checking, ordering, arc consistency, and changing the structure of the graph

In summary: we learn

CSPs are special type of problems. The advantage is that we can exploit the structure of the problem. But not all the problems can be defined as CSPs.

In CSPs  the state is defines by values of a fix set of variables

The goal test is defined by constraints of variable values.

The simplest algorithm used is backtracking algorithm that uses DFS with one var assigned per node

We can improve the algorithm by order and value selection heuristic

And forward checking helps us detect failure early on.

And by graph visualization we can exploit the structure of the tree for example finding subproblems or using special algorithms when we have a tree structure.
-->

---

<!-- source: slide 93 -->

# Exercise

[https://forms.gle/a2dx2Pycnyr1Tt2g8](https://forms.gle/a2dx2Pycnyr1Tt2g8)

<!--
Write this on the slide!!

2 possible solutions!

C1 = Prof. C

C2 = Prof. B

C3 = Prof. C

C4 = Prof. A

C5 = Prof. B

C3 & C4 can be swapped

Looking at it from arc consistency, professor C teaching class 5 isn’t ruled out, but it’s not possible given the remaining schedule
-->

---
hide: true
---

<!-- source: slide 94 -->

# Exercise

[https://forms.gle/ZwkDMjVohKaty9LR7](https://forms.gle/ZwkDMjVohKaty9LR7)

<!--
Write this on the slide!!

2 possible solutions!

C1 = Prof. C

C2 = Prof. B

C3 = Prof. C

C4 = Prof. A

C5 = Prof. B

C3 & C4 can be swapped

Looking at it from arc consistency, professor C teaching class 5 isn’t ruled out, but it’s not possible given the remaining schedule
-->

---
hide: true
---

<!-- source: slide 95 -->

# Reading for next Week

- David Silver, Aja Huang, Chris J. Maddison, Arthur Guez, Laurent Sifre, George van den Driessche, Julian Schrittwieser, Ioannis Antonoglou, Veda Panneershelvam, Marc Lanctot, Sander Dieleman, Dominik Grewe, John Nham, Nal Kalchbrenner, Ilya Sutskever, Timothy Lillicrap, Madeleine Leach, Koray Kavukcuoglu, Thore Graepel and Demis Hassabis. **Mastering the Game of Go with deep neural networks and tree search**, Nature 529, 2016.

<!--
A paper published by Google Deep Mind. It describes alpha go (The system that defeated the world champion of the game go. Which was an impressive achievement.)
-->

---
hide: true
---

<!-- source: slide 96 -->

# Reminders

- Pre-proposals due today!
- Next Monday: **HW1 due**

<!--
Next week we will talk about adversarial search and game theory. When we have two agents for our environment.
-->
