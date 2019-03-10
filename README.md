# Object-Counter
simple python program that counts the objects in an image file

# Algorithms
## Levialdi’s Shrinking Algorithm

> Levialdi’s shrinking algorithm shrinks every connected component in a binary image to a single isolated point to the upper right corner of its bounding rectangle and erases it.

Deletion Condition | Augmentation Condition
------------------ | ----------------------
Delete 1-valued-pixel if it has the following neighborhood ![Levialdi Deletion](Object-Counter/docs/levdel.png)|  Change a 0-valued-pixel p to a 1-valued pixel if it has a following neighborhood ![Levialdi Augmentation](Object-Counter/docs/levaug.png)


