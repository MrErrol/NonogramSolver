# Nonogram datafiles

***

As you may noticed creating nonogram datafile is the most tedious part of using NonoGeek. Knowing that I tried to make those files as simple and detail-free as possible. How much I succeeded in doing so is up to you to judge.

***

## Simple example

One of the simplest examples possible is 3x3 nonogram.

![alt text][nono1]

Which is encoded in a file:

```
ROWS:
3
1
1 1
COLUMNS:
1 1
2
1 1
```

As you may see file contains just two codewords `ROWS:` and `COLUMNS:` and two blocks of data. Codewords mark begginings of the data blocks describing _hints_ for rows and columns of the nonogram. As you see blocks of data describes hints for rows and columns. In each block of hints every line describes list of hints for a given row or column. And ... that's all!

One cannot properly define a nonogram without specifing _all_ hints - so one cannot run away from it. In principle one may try to remove codewords, yet I believe clarity of datafile is worth using them.

***

## Presolved nonogram

While using hint mode to get a clue about next move or while using check mode to validate your work one needs to specify all identified (up to now) cells. For clarity NonoGeek requires to specify status of all (or none) of the cells. Below you may see example of valid datafile with presolved cells

```
ROWS:
3
1
1 1
COLUMNS:
1 1
2
1 1
CELLS:
ffu
efu
ueu
```

At the end of the already known file appeared strangely looking block of letters proceeded by a codeword `CELLS:`. This block represents the solved nonogram (table of cells) in the (probably) simplest possible way. Each letter represents single cell and each row in block represents row in a nonogram. The letters stand for `f`illed, `e`mpty or (yet) `u`ndefined cells. The above datafile corresponds to the following stage of solving (grey cells are not yet identified):

![alt text][nono2]

If you consider making such representation tedious, you are right. Nonetheless, workload may be mitigated - see the _Tips and Tricks_ section of this document.

***

## Strict rules

Having basic idea how the datafile should look like we may proceed to more precise rules:

- Each datafile have to contain two sections, namely `ROWS:` and `COLUMS:`
- Directly after mentioned codewords datafile must contain rows (columns) of space separated integers representing following filled cells block for each row (column) of the nonogram
- Each datafile may posses section `CELLS:`
- Directly after `CELLS:` codeword datafile must contain lines of signs representing cells in the row
    - Each line represents single line in the nonogram and every sign represents exactly one cell
    - You may use `feu` letters for `f`illed, `e`mpty or (yet) `u`ndefined cells, capital letters are fine
    - For your convenience you may also use numbers `0=u`, `1=f` and `2=e`
    - If you prefer NonoGeek will accept `+` for filled and `-` for empty cells
- Lines containing data should possess *only* neccessary data
- Sections may come in any order and may be separated (or proceeded) by any comment lines that do not contain mentioned codewords and do not contain _only_ numbers and whitespaces
- Obviously your data needs to represent valid nonogram

***

## Tips and Tricks

As filling hints for rows and columns just needs to be done, there are some tricks that might help you filling `CELLS:` section.

- Make sure your editor uses fixed-width font - that way you will have well adjusted rows _and_ columns of letters
- Start by creating full picture of `u`nknown cells (Ctrl-C + Ctrl-V is a really helpfull there). Once you have it press _Insert_ on your keyboard and enjoy magic of replacing letters instead of inserting them
- If you are solving a bigger picture and you've made a mistake it is very likely that you made it not so long ago. Try putting in last pieces of picture that you were working on and skip previous ones leaving them `u`nknown. NonoGeek will check all declared (`e`mpty or `f`illed) cells and provide information about them. Be aware that it will not be able to verify whether you make mistake in cells not provided (the `u`nknown ones)

_My editor does not react to the Insert button..._

Start using Vim. Or fix your keybord. Maybe both...

[nono1]: img/nono1.png "Solved nonogram"
[nono2]: img/nono2.png "Presolved (partially) nonogram"