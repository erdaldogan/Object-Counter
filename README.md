# Object-Counter
simple python program that counts the objects in an image file

# Algorithms
## Levialdi’s Shrinking Algorithm
Article: [S. Levialdi. 1972. On shrinking binary picture patterns. Commun. ACM 15, 1 (January 1972), 7-10.](http://dx.doi.org/10.1145/361237.361240)


> Levialdi’s shrinking algorithm shrinks every connected component in a binary image to a single isolated point to the upper right corner of its bounding rectangle and erases it.

Deletion Condition | Augmentation Condition
:------------------: | :----------------------:
Delete 1-valued-pixel if it has the following neighborhood <br/> ![Levialdi Deletion][lev_del] | Change a 0-valued-pixel p to a 1-valued pixel if it has a following neighborhood <br/> ![Levialdi Augmentation][lev_aug]


[lev_del]: https://raw.githubusercontent.com/erdaldogan/Object-Counter/master/docs/levdel.png "Logo Title Text 2"
[lev_aug]: https://raw.githubusercontent.com/erdaldogan/Object-Counter/master/docs/levaug.png "Logo Title Text 2"

## Two Sub-fields Algorithm
Article: [Gökmen, Muhittin & W Hall, Richard. (1990). Parallel shrinking algorithms using 2-subfield approaches. Computer Vision, Graphics, and Image Processing. 52. 191-209. ](http://dx.doi.org/10.1016/0734-189X(90)90054-Y)


>In this approach, the image space is partitioned like a checkerboard into two disjoint sets  <p align="center"> <img src="https://raw.githubusercontent.com/erdaldogan/Object-Counter/master/docs/tsf_subfields.png" width="499"></p> where 1 and 2 denote the two distinct subfields

Before going into the conditions, we have to define some variables.

* 8-neighbors of the pixel p = Surrounding pixels of p.
<p align="center"> <img src="https://raw.githubusercontent.com/erdaldogan/Object-Counter/master/docs/8neighbors.png" width="100"> <br/> p1, p2, p3, ...., pn are 8 neighbors of p.
</p>

* B(p) = Number of 1's in pixel p's 8-neighborhood.
* C(p) = Number of distinct sets of 1's in pixel p's 8-neighborhood. *(Can be calculated from T(p))*
* T(p) = Number of 0-to-1 transition in the 8-neighbors.

For instance;
<p align="center">
<img src="https://raw.githubusercontent.com/erdaldogan/Object-Counter/master/docs/tsf_example.png" width="450">
</p>


### Deletion Condition
