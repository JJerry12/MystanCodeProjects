"""
File: babygraphics.py
Name: Jerry
--------------------------------
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950,
         1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index where the current year is in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                            with the current year.
    """
    return ((width - GRAPH_MARGIN_SIZE*2) / len(YEARS)) * year_index + GRAPH_MARGIN_SIZE


def draw_fixed_lines(canvas):
    """
    Draws the fixed background lines on the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # ----- Write your code below this line ----- #

    # Upper boundary
    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE,
                       CANVAS_WIDTH - GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, width=LINE_WIDTH)

    # Lower boundary
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE,
                       CANVAS_WIDTH - GRAPH_MARGIN_SIZE, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE,
                       width=LINE_WIDTH)

    # Draw the fixed vertical lines based on the number of years in the YEAR list
    for i in range(len(YEARS)):
        x_coordinate = get_x_coordinate(CANVAS_WIDTH, i)
        canvas.create_line(x_coordinate, 0, x_coordinate, CANVAS_HEIGHT, width=LINE_WIDTH)
        canvas.create_text(x_coordinate + TEXT_DX, CANVAS_HEIGHT - GRAPH_MARGIN_SIZE,
                           text=YEARS[i], anchor=tkinter.NW)


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    scale = (CANVAS_HEIGHT - 2*GRAPH_MARGIN_SIZE) / 1000    # The canvas is divided into 1000 parts to plot the data
    color_counts = 0                                    # This variable is used to fill the color of lines and texts

    for name in lookup_names:
        y_list = []                    # Used to store y coordinates(int) of the name data associated with that year
        rank_list = []                 # Used to store ranking(str) of the name data associated with that year
        for year in YEARS:
            if str(year) in name_data[name]:
                y_list.append((int((name_data[name][str(year)]))-1) * scale + GRAPH_MARGIN_SIZE)
                rank_list.append(str(name_data[name][str(year)]))
            else:                      # The name data is out of ranking associated with that year
                y_list.append(CANVAS_HEIGHT-GRAPH_MARGIN_SIZE)
                rank_list.append('*')

        # Plot the historical trend of names based on y_list and rank_list
        color = COLORS[color_counts % len(COLORS)]
        for i in range(len(YEARS)-1):
            x1_coordinate = get_x_coordinate(CANVAS_WIDTH, i)
            x2_coordinate = get_x_coordinate(CANVAS_WIDTH, i+1)

            canvas.create_line(x1_coordinate, y_list[i], x2_coordinate, y_list[i+1],
                               fill=color, width=LINE_WIDTH)
            canvas.create_text(x1_coordinate + TEXT_DX, y_list[i], text=name + rank_list[i],
                               anchor=tkinter.SW, fill=color)
        canvas.create_text(get_x_coordinate(CANVAS_WIDTH, len(YEARS)-1) + TEXT_DX,
                           y_list[len(YEARS)-1], text=name + rank_list[len(YEARS)-1], anchor=tkinter.SW, fill=color)
        color_counts += 1


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
