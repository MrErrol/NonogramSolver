# NonogramSolver
Solver for Nonograms - in development

***

# Simply solve

Got bored while solving nonogram and want a short cut? Made mistake just before finishing touch? Your doughter incessantly wants to *see nice picture*?

Summing up: *I want to see the solution!*

Clone, type `python solver.py nonograms/heart.dat` and thats all you need to get this

![alt text][heart]

If you want to solve your nonogram just substitute your datafile in place of `nonograms/heart.dat`.

***

# Live plotting mode

*I want to see it working step-by-step!*

Sure thing. Add flag `--live` or `-l` and enjoy!

![Alt Text][heartgif]

***

# Hint mode

*I don't want to have solution spoiled, yet I spend last 20 minutes (or whatever more...) on it and got nothing - I'm stucked.*

*Could you give me **just small hint** what to do next?*

I'm here for you. Put your work in a file and add flag `--hint`. Assuming you haven't done anything yet and you are solving heart nonogram (see first section) you will get a message (rows and columns are counted from 1):

```
Analyze row 2.
Cell at row=2 and col=1 may be deduced to be filled.
```

*I'm not **that** dumb. I wanted a **small** hint.*

Of course. My fault.

Add flag `--verbose 0` or `-v 0` on top of `--hint` and you will get just small hint:

```
Analyze row 1.
```

***

# Check mode

*I've spend 5 hours on it and find out I made a mistake. Do I have to start from the beggining or have solution spoiled?*

I will not leave you there. Put your work in a file and add flag `--check` or `-c`. You will get nice list of misfilled cells. It will look like that:

```
Whoops! You have made a mistake!
List of misclassified cells:
Counting from 1.
(row number, column number)
(2,3)
(4,6)
...
```

*Just asking. Imagine I'm solving a picture and just feel that something's wrong. May I ...*

Yes, you may. If there are no mistakes your self-confidence will be raised:

```
So far, so good!
No mistakes found.
```

[heart]: img/heart.png "Heart nonogram"
[heartgif]: img/heart-paused.gif