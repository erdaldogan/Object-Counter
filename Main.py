import tkinter as tk
from tkinter.filedialog import *
from PIL import Image, ImageTk, ImageDraw
import numpy as np
import random
import string

# Written by Erdal S. Dogan on February 22nd, 2019
#
# COMP204 Programming Studio
# Instructor Muhittin Gokmen
#
# MEF University
# Sariyer, Istanbul
#


def isIsolated(array, i, j):
    if ((array[i][j] == 1) and (array[i][j - 1] == array[i][j + 1] == array[i - 1][j] ==
                                array[i - 1][j - 1] == array[i - 1][j + 1] ==
                                array[i + 1][j - 1] == array[i + 1][j] == array[i + 1][j + 1] == 0)):
        return True
    return False


def surroundWithZeros(array):
    dims = array.shape
    final_arr = np.zeros(dims)
    for m in range(1, dims[0] - 1):
        for n in range(1, dims[1] - 1):
            final_arr[m][n] = array[m][n]
    return final_arr


def np2binary(array):
    threshold = 150
    dims = array.shape
    for i in range(0, dims[0]):
        for j in range(0, dims[1]):
            if array[i][j] <= threshold:
                array[i][j] = 0
            else:
                array[i][j] = 1


def contains1(array):
    if 1 in array or 1 in array[1]:
        return True
    return False


######################################################################
########################         GUI          ########################
######################################################################
root = tk.Tk()
root.title("Object Counting")

# get dimensions of the user's display
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

print("Screen Width: {}px\nScreen Height: {}px".format(screen_width, screen_height))

# window's dimensions
window_width = int(screen_width / 1.5)
window_height = int(screen_height / 1.5)

# variables to center the main window when it's opened
center_x = int((screen_width - window_width) / 2)
center_y = int((screen_height - window_height) / 2)
size = "{}x{}+{}+{}".format(window_width, window_height, center_x, center_y)

frame_width = screen_width / 2
frame_height = screen_height / 2
frame_padx = (window_width - frame_width) / 2
frame_pady = (window_height - frame_height) / 2

button_cell_height = frame_height / 15

grid_cell_height = (frame_height - button_cell_height) / 2
grid_cell_width = frame_width / 3

root.geometry(size)

image_array = None
iteration = None
number_of_objects = None
algorithm = None
image_name = None


def displayImage(image):
    scaled_image = scale(image)

    image_tk = ImageTk.PhotoImage(scaled_image)

    # preview original image
    label1 = Label(preview, image=image_tk)
    label1.image = image_tk
    label1.grid(row=0, column=0)

    # preview binary image
    binary_image = binaryImage(scaled_image)
    binary_image = ImageTk.PhotoImage(binary_image)
    label2 = Label(binary_preview, image=binary_image)
    label2.image = binary_image
    label2.grid(row=0, column=0)

    # initialize the global variable image array,
    # in order to use it in different functions such as levialdi, tsf etc.
    global image_array
    image_array = np.array(image.convert("L"))
    np2binary(image_array)


def openImage():
    path = askopenfilename(parent=frame)
    sliced = path.split('/')  # extract the name of the file from the path
    global image_name
    image_name = sliced[-1]  # last variable of the array which is the file name
    raw_img = Image.open(path)
    displayImage(raw_img)


def scale(img):
    # 1- find the greater dimension of the image, height or width?
    # 2- change the greater dimension of the image as the corresponding dimension of the frame
    # e.g if the image is long and narrow, set the image height as the height of the frame and reset
    # the width value while protecting the aspect ratio
    #
    #
    dimension = img.size
    greater = max(dimension)
    aspectRatio = dimension[0] / dimension[1]
    index = dimension.index(greater)  # index of the grater dimension
    if index == 0:  # if width is greater than height
        x = int(grid_cell_width - 50)  # subtract 50 for visual improvement
        y = int(x / aspectRatio)
    elif index == 1:  # if height is greater than width
        y = int(grid_cell_height - 50)
        x = int(y * aspectRatio)
    img = img.resize((x, y))  # rescaled image
    return img

# convert the array to binary array. if the rgb value is below a cer
def binaryImage(image):
    image_array = np.array(image.convert("L"))
    np2binary(image_array)
    final_image = Image.fromarray(np.uint8(image_array) * 255)

    return final_image


frame = Frame(root, width=frame_width, height=frame_height, borderwidth=1,
              relief=RIDGE)
frame.grid_propagate(0)
frame.pack(padx=0, pady=frame_pady / 2)

for i in range(3):
    frame.grid_columnconfigure(i, minsize=grid_cell_width)

#  frames for widgets
openButtons_frame = Frame(frame, width=grid_cell_width, height=button_cell_height, relief=RAISED)
openButtons_frame.grid(row=0, column=0)

preview = Frame(frame, width=grid_cell_width, height=grid_cell_height, borderwidth=2, relief=RAISED)
preview.grid(row=1, column=0)

binary_preview = Frame(frame, width=grid_cell_width, height=grid_cell_height, borderwidth=2, relief=RAISED)
binary_preview.grid(row=2, column=0)

runButtons_frame = Frame(frame, width=grid_cell_width, height=button_cell_height, relief=RAISED)
runButtons_frame.grid(row=0, column=1)

saveButtons_frame = Frame(frame, width=grid_cell_width, height=button_cell_height, relief=RAISED)
saveButtons_frame.grid(row=0, column=2)

levialdi_frame = Frame(frame, width=grid_cell_width, height=grid_cell_height, borderwidth=2, relief=RAISED)
levialdi_frame.grid(row=1, column=1)

tsf_frame = Frame(frame, width=grid_cell_width, height=grid_cell_height, borderwidth=2, relief=RAISED)
tsf_frame.grid(row=2, column=1)

levialdi_result_frame = Frame(frame, width=grid_cell_width, height=grid_cell_height, borderwidth=2, relief=RAISED)
levialdi_result_frame.grid(row=1, column=2)

tsf_result_frame = Frame(frame, width=grid_cell_width, height=grid_cell_height, borderwidth=2, relief=RAISED)
tsf_result_frame.grid(row=2, column=2)


# create random image
def createRandom():
    def randomLetter(): # create random letter
        return random.choice(string.ascii_letters)  # return random letter

    img = Image.new('RGB', (200, 200), color=(0, 0, 0))
    for i in range(random.randint(0, 75)):
        d = ImageDraw.Draw(img)

        # choose a random letter and random position
        # d.text(x-coordinate, y-coordinate, string, color)
        d.text((random.randint(0, 255), random.randint(0, 255)), randomLetter(), fill=(255, 255, 255))

    displayImage(img)
    global image_name
    image_name = 'random-out.jpg'
    img.save('random-out.jpg')


def levialdi():
    global algorithm
    algorithm = 'Levialdi'  # set used algorithm name as Levialdi

    def levialdi_deletion_condition(array, i, j):
        if (array[i][j] == 1) and (array[i][j - 1] == array[i + 1][j - 1] == array[i + 1][j] == 0):
            return True
        return False

    def levialdi_augmentation_condition(array, i, j):
        if (array[i][j] == 0) and (array[i][j - 1] == array[i + 1][j] == 1):
            return True
        return False

    global image_array, iteration, number_of_objects
    iteration = 0  # store number of iterations
    lev_array = image_array.copy()  # work with the copy of the array
    temp = lev_array.copy()  # overwrite on the temp array
    size = lev_array.shape
    number_of_objects = 0
    while contains1(lev_array):
        for i in range(1, size[0] - 1):
            for j in range(1, size[1] - 1):
                if isIsolated(lev_array, i, j):
                    number_of_objects += 1
                    temp[i][j] = 0
                elif levialdi_deletion_condition(lev_array, i, j):
                    temp[i][j] = 0
                elif levialdi_augmentation_condition(lev_array, i, j):
                    temp[i][j] = 1
        iteration += 1
        lev_array = temp.copy()

        lev_array = surroundWithZeros(lev_array)
        final_image = Image.fromarray(np.uint8(lev_array) * 255)
        final_image = scale(final_image)
        final_image = ImageTk.PhotoImage(final_image)
        label_im = Label(levialdi_frame, image=final_image)
        label_im.image = final_image
        label_im.grid(row=0, column=0)
        frame.update()

        result = "Levialdi Iterations {}\n Number of Objects {}".format(iteration, number_of_objects)
        text = Label(levialdi_result_frame, text=result)
        text.grid(row=0, column=0)
        tsf_result_frame.update()


def twosubfields():
    global algorithm
    algorithm = 'TSF'

    def get_bp(array, i, j):
        neighbors = [array[i - 1][j - 1], array[i - 1][j], array[i - 1][j + 1],
                     array[i][j + 1], array[i + 1][j + 1], array[i + 1][j], array[i + 1][j - 1], array[i][j - 1]]
        return np.sum(neighbors)

    def get_cp(array, i, j):
        #  in order to make the array circular, 0th element set to be equal to last element,
        #  which is p8 in two-subfields algorithm
        #  p_array consist 8-neighbors of a pixel
        neighbors = [array[i - 1][j - 1], array[i - 1][j], array[i - 1][j + 1],
                     array[i][j + 1], array[i + 1][j + 1], array[i + 1][j], array[i + 1][j - 1], array[i][j - 1]]
        cp = 0
        b1, b2, b3, b4, b5, b6, b7, b8 = neighbors[0], neighbors[1], neighbors[2], neighbors[3], neighbors[4], \
                                         neighbors[5], neighbors[6], neighbors[7]

        if b2 == 1 and b4 == 1:
            b3 = 1
        if b4 == 1 and b6 == 1:
            b5 = 1
        if b6 == 1 and b8 == 1:
            b7 = 1
        if b8 == 1 and b2 == 1:
            b1 = 1

        list1 = [b1, b2, b3, b4, b5, b6, b7, b8, b1]
        length = len(list1)

        for p in range(length - 1):
            if list1[p] == 0 and list1[p + 1] == 1:
                cp += 1

        if cp == 0 and 1 in list1:
            return 1
        return cp

    # return true if neighbors of the pixel contains length 3 or more run of zeros
    # this function only checks if the neighbors contains 3 consequent zeros
    def contains3lengthzeros(array, i, j):
        # 8 neighbors of the pixel
        b1, b2, b3, b4, b5, b6, b7, b8 = [array[i - 1][j - 1], array[i - 1][j], array[i - 1][j + 1],
                                          array[i][j + 1], array[i + 1][j + 1], array[i + 1][j], array[i + 1][j - 1],
                                          array[i][j - 1]]

        neighbors = [b1, b2, b3, b4, b5, b6, b7, b8, b1, b2]
        length = len(neighbors)
        for m in range(length):
            if neighbors[m - 2] == neighbors[m - 1] == neighbors[m] == 0:
                # negative index is reading the array in reverse in python
                # neighbors[-1] = neighbors[length - 1]
                return True
        return False

    def deletion_condition(array, i, j):
        if array[i][j] != 1:
            return False
        elif get_cp(array, i, j) == 1:
            flag = True
            if get_bp(array, i, j) == 1:
                flag = False
                if array[i - 1][j - 1] == array[i + 1][j - 1] == 0:
                    flag = True
            if flag:
                if contains3lengthzeros(array, i, j):
                    return True
            return False

    def augmentation_condition(array, i, j):
        if array[i][j] != 0:
            return False
        b2, b6, b8 = array[i - 1][j], array[i + 1][j], array[i][j - 1]
        if get_cp(array, i, j) == 1:
            if (b8 == b2 == 1) or (b8 == b6 == 1):
                return True
        return False

    global image_array
    image_array = surroundWithZeros(image_array)  # set most outer frame of the image as 0
    tsf_array = image_array.copy()
    temp = tsf_array.copy()
    size = tsf_array.shape
    global number_of_objects, iteration
    number_of_objects = 0
    iteration = 0
    while contains1(tsf_array):
        # 4 for loops for subfield 1
        for i in range(1, size[0] - 1, 2):
            for j in range(1, size[1] - 1, 2):
                if isIsolated(tsf_array, i, j):
                    number_of_objects += 1
                    temp[i][j] = 0
                elif deletion_condition(tsf_array, i, j):
                    temp[i][j] = 0
                elif augmentation_condition(tsf_array, i, j):
                    temp[i][j] = 1
        for k in range(2, size[0] - 1, 2):
            for l in range(2, size[1] - 1, 2):
                if isIsolated(tsf_array, k, l):
                    number_of_objects += 1
                    temp[k][l] = 0
                elif deletion_condition(tsf_array, k, l):
                    temp[k][l] = 0
                elif augmentation_condition(tsf_array, k, l):
                    temp[k][l] = 1
        tsf_array = temp.copy()

        # 4 for loops for subfield 2
        for m in range(1, size[0] - 1, 2):
            for n in range(2, size[1] - 1, 2):
                if isIsolated(tsf_array, m, n):
                    number_of_objects += 1
                    temp[m][n] = 0
                elif deletion_condition(tsf_array, m, n):
                    temp[m][n] = 0
                elif augmentation_condition(tsf_array, m, n):
                    temp[m][n] = 1
        for o in range(2, size[0] - 1, 2):
            for p in range(1, size[1] - 1, 2):
                if isIsolated(tsf_array, o, p):
                    number_of_objects += 1
                    temp[o][p] = 0
                elif deletion_condition(tsf_array, o, p):
                    temp[o][p] = 0
                elif augmentation_condition(tsf_array, o, p):
                    temp[o][p] = 1
        iteration += 1
        tsf_array = temp.copy()

        final_image = Image.fromarray(np.uint8(tsf_array) * 255)  # create image from array
        final_image = scale(final_image)  # scale the image so it fits the frames
        final_image = ImageTk.PhotoImage(final_image)  # PIL Image to tkinter image
        label_im = Label(tsf_frame, image=final_image)  # create new label which contains the image itself only
        label_im.image = final_image
        label_im.grid(row=0, column=0)

        frame.update()

        result = "TSF Iterations {}\n Number of Objects {}".format(iteration, number_of_objects)
        text = Label(tsf_result_frame, text=result)
        text.grid(row=0, column=0)
        tsf_result_frame.update()


def save():
    f = open('outputs.csv', 'a')
    f.write('\nFile: {}, Algorithm: {}, NCC: {}, Iterations: {}'.format(image_name, algorithm,
                                                                        number_of_objects, iteration))
    f.close()

def draw():
    pane = Tk()
    pane.title("Draw Image(Beta)")
    image = Image.new("RGB", (400, 400), 'white')
    draw = ImageDraw.Draw(image)

    def motion(event):
        canvas.create_rectangle(event.x - 5, event.y - 5, event.x, event.y, fill='white')
        draw.rectangle((event.x - 5, event.y - 5, event.x, event.y), fill='white')

    canvas = Canvas(pane, width=400, height=400, background='black')
    canvas.bind("<B1-Motion>", motion)
    canvas.pack()
    canvas.unbind("<Enter>")
    displayImage(image)


#  buttons
open_button = Button(openButtons_frame, text='Open', command=openImage)
open_button.pack(side=LEFT)

create_button = Button(openButtons_frame, text='Create', command=createRandom)
create_button.pack(side=RIGHT)

levialdi_button = Button(runButtons_frame, text='Levialdi', command=levialdi)
levialdi_button.pack(side=LEFT)

tsf_button = Button(runButtons_frame, text='TSF', command=twosubfields)
tsf_button.pack(side=RIGHT)

save_button = Button(saveButtons_frame, text='Save', command=save)
save_button.pack(side=LEFT)

draw_button = Button(openButtons_frame, text='Draw', command=draw)
draw_button.pack()

root.mainloop()

# TODO
# delete previous image before opening a new picture
# image saved notification pop-up
# improve the draw feature
# date stamp to the output file
# separate front-end and back-end
