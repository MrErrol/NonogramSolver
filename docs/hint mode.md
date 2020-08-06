# Hint mode

***

Hint mode is designed to help _you_ solve the riddle, providing minimal additional information about the solution. It is meant to give you just the next step, rather than to solve the whole nonogram. If you want to get the full solution, you should use standard NonoGeek mode (without additional flags). Although, if you just want to be tipped what to do next, it is the very thing you are looking for.

***

## Motivation

While solving nonograms I have met situations where I was spending a lot of time trying to make the next step. When I find it, it usually happens to be a very simple step. The difficulty of it comes from _finding where I can make it_ and not from the difficulty of the reasoning itself.  As I was interested in reasoning rather than brute force checking everything I decided to make this mode to point me _where_ I should look while solving the riddle.

Hint mode:
- may give you information about state of ONE unidentified yet cell
- if you prefer it may give you just row or column number that is sufficient to analyze
- if you need to make assumption, it will point you the appropriate cell
- all information provided by this mode will point toward next human solvable cell - not the random one

***

## Usage and verbosity

In order to take advantage of that mode you need to provide NonoGeek with information about what you already managed to solve. This is done via then input file. Informations how to create such a file are provided (here: link to file making description). See especially _Tips and Tricks_ section, as it may help you significantly reduce the workload needed.

Once having the input file you may run NonoGeek in Hint mode with it to get information of the next cell state. If your partially solved nonogram is stored in a file *my_work.dat* you should type:

```
python3 nonogeek.py my_work.dat --hint
```

NonoGeek will response printing something like this:

```
Analyze row 2.
Cell at row=2 and col=1 may be deduced to be filled.
```

Such statement means that you may deduce the state of the next cell analyzing **solely** second row (I am printing row indices starting from 1). Moreover it tells you which cell in this row may be identified and whether it should be filled or empty.

If you want to see just the first line of the output you may reduce verbosity of the NonoGeek. You may specify it adding flag `--verbosity 0` or `-v 0` to command line arguments. Value `0` means that you want to obtain as little information as possible. The opposite is value `1`, which means that you want to be explicitly told which cell should be identified and whether it should be filled or empty (value `1` is default).

As you probably know in some cases it is not sufficient to analyze single row or column. In such a situation the simplest and most general approach is to make an assumption about some unknown cell (usually the most informative is the assumption that the cell is filled) and try to deduce discrepancy. By discrepancy I mean the situation that makes the nonogram impossible to be solved. Thus we may deduce that the cell is empty (or filled - the opposite of assumption we made) and proceed with solving the nonogram. In such a situation NonoGeek will give you more elaborate output:

```
Assume the cell at row=2 and col=1 to be filled and try to deduce consequences.
Cell at row=2 and col=1 may be deduced to be empty.
You will need to analyze more than just single row or column.
```

Again if you would like to suppress all but the first line of output you may pass `-v 0` flag.