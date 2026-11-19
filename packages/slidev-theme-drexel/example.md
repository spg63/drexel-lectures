---
theme: ./
aspectRatio: 16/9
canvasWidth: 980
title: "slidev-theme-drexel · style guide"
layout: cover
kicker: Style guide · v1
---

# Drexel Lite

The lecture theme: Drexel blue and gold, minus the letterhead

<small>Every layout, list level, color and component, on real content. If a deck needs something this file doesn't show, add it here first.</small>

---
layout: section
kicker: Part 1
---

# Text

Lists, emphasis, semantic color

---

# Default layout: bullets

- Top level gets a gold square
- Keep top-level bullets to about **six** per slide
   - Second level gets a blue dash and drops to 88%
   - Two levels is the norm
      - Three is allowed, sparingly
- Use `inline code` for identifiers like `select_unassigned_variable`
- Links look like this: [CS 188 CSP demos](https://www.cs.cmu.edu/~15281/demos/csp_backtracking/)

<!--
Speaker notes go in an HTML comment at the end of the slide. Every content slide should have them.
-->

---

# Ordered lists and emphasis

1. **Bold** is for terms being defined; it turns Drexel blue
2. *Italic* is for stress, or a term used as a word
3. <span class="mark">Highlighter</span> is for the one thing on the slide they must remember
4. Nested ordered lists switch to letters:
   1. like this
   2. and this

<Aside label="Rule">One highlighter per slide. Two means neither matters.</Aside>

---

# Semantic color

- State is defined by <span class="dx-blue">variables</span> $X_i$ with <span class="dx-blue">values</span> from <span class="dx-blue">domain</span> $D_i$
- <span class="dx-green">Goal test</span> is a set of <span class="dx-blue">constraints</span>
- <span class="dx-red">Red</span> is for warnings and wrong answers
- <span class="dx-purple">Purple</span> exists for legacy decks; avoid in new material

<Aside>Classes are <code>dx-red</code>, <code>dx-blue</code>, <code>dx-green</code>, <code>dx-purple</code>. Never <code>c-*</code> or <code>text-*</code>: UnoCSS owns those prefixes and will silently override them.</Aside>

---
layout: section
kicker: Part 2
---

# Layouts

default · split · figure · statement · section · cover

---
layout: split
---

# Split: text left, figure right

::left::

- **Binary CSP:** each constraint relates at most two variables
- **Constraint graph:** nodes are variables, arcs are constraints
- General-purpose algorithms exploit the graph structure
   - Tasmania is an independent subproblem!

::right::

<img src="/example/constraint-graph.png" class="fig" style="max-height:300px" />

---
layout: split
flip: true
ratio: 1fr 1.2fr
---

# Split, flipped, with a custom ratio

::left::

- `flip: true` puts the figure on the left
- `ratio` sets the columns, text first: here `1fr 1.2fr`
- A caption goes under the image in the right slot

::right::

<img src="/example/map.png" class="fig" style="max-height:280px" />

<div class="caption">Map coloring: adjacent regions differ</div>

---
layout: figure
caption: "A tree-structured CSP solves in O(n d²)"
---

# Figure: the picture is the point

<img src="/example/tree.png" />

---
layout: statement
kicker: Discuss
---

# Why pick the variable with the *fewest* legal values left?

Thirty seconds with your neighbor, then we'll hear answers.

---
layout: section
kicker: Part 3
---

# Code, math, builds

---

# Code

```python {2-3|5-8|all}
def backtrack(assignment, csp):
    if len(assignment) == len(csp.variables):
        return assignment
    var = select_unassigned_variable(assignment, csp)   # MRV
    for value in order_domain_values(var, assignment, csp):  # LCV
        if csp.consistent(var, value, assignment):
            result = backtrack({**assignment, var: value}, csp)
            if result: return result
    return None
```

Line highlights step on click: `{2-3|5-8|all}`.

---

# Math

Inline: a CSP with $n$ variables and domain size $d$ has $O(d^n)$ complete assignments.

Display:

$$
b = (n - \ell)\,d \quad\Rightarrow\quad n!\,d^{\,n} \text{ leaves}
$$

- Variable names in math use `\text{}`: $\text{SA} \neq \text{WA}$
- Sets: $D = \{\text{red}, \text{green}, \text{blue}\}$ (braces are safe: MDC is off)

---

# Builds: reveal on click

The BFS fringe, one expansion per click:

<v-clicks>

1. S
2. S→A, S→B
3. S→B, S→A→C, S→A→D
4. S→A→C, S→A→D, S→B→G

</v-clicks>

<Aside label="Handout">PDF export shows every build fully revealed, with your ink on top.</Aside>
