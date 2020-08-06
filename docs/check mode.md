# Check mode

***

Check mode is desiged to validate whether you have made a mistake, while solving nonogram. It is also capable of pointing misclassified cells. May be used at any solving stage.

***

## Motivation

Making mistakes is inherent part of human life. It happens to everyone, and may happen while solving a nonogram. It is almost always possible to spot the mistake, sooner or later. Fortunately, it usually happens rather sooner than later, making the number of following mistakes arguably small. A common approach in such cases is to drop all the work done and start from the beginning. It might be discouraging, especially when happens just before finishing touch. To make situation even worse, the bigger the nonogram, the higher the probability of making a mistake (as one have more opportunities to do so) and the bigger the amount of workload lost.

In such a situation I wanted to have a magic button that rewinds me to the moment I made a mistake. Unfortunately, without whole history of changes it is impossible. However, it is possible to point the cells that has been misclassified. This mode does exactly that thing.

***

## Usage

In order to take advantage of check mode you need to provide NonoGeek with information about what you already managed to solve. This is done via then input file. Informations how to create such a file are provided (here: link to file making description). See especially _Tips and Tricks_ section, as it may help you significantly reduce the workload needed.

Having the file, your job is almost over. You need just to type (assuming your datafile is called *my_work.dat*):

```
python3 nonogeek.py my_work.dat --check
```

or simply

```
python3 nonogeek.py my_work.dat -c
```

then NonoGeek will give you list of misclassified cells:

```
Whoops! You have made a mistake!
List of misclassified cells:
Counting from 1.
(row number, column number)
(2,3)
(4,6)
...
```

Note that as always row and column indices start from 1.

Obviously it is possible to use this mode to check not where but whether you made a mistake, possibly multiple times during single solution. In case you have made not a single mistake, you will get a message:

```
So far, so good!
No mistakes found.
```
