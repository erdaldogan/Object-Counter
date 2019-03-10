# Object-Counter
simple python program that counts the objects in an image file

# Algorithms
## Levialdi’s Shrinking Algorithm

> Levialdi’s shrinking algorithm shrinks every connected component in a binary image to a single isolated point to the upper right corner of its bounding rectangle and erases it.

Deletion Condition | Augmentation Condition
------------------ | ----------------------
Delete 1-valued-pixel if it has the following neighborhood | Change a 0-valued-pixel p to a 1-valued pixel if it has a following neighborhood 
                              |                         
![Levialdi Deletion][lev_del] |![Levialdi Augmentation][lev_aug] 

[lev_del]: https://raw.githubusercontent.com/erdaldogan/Object-Counter/master/docs/levdel.png "Logo Title Text 2"

[lev_aug]: https://raw.githubusercontent.com/erdaldogan/Object-Counter/master/docs/levaug.png "Logo Title Text 2"

