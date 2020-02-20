import matplotlib.pyplot as plt
from matplotlib import animation
import logging

logging.basicConfig(level=logging.DEBUG)


class Visualizer(object):
    """Class that handles all aspects of visualization.
    Attributes:
        maze: The maze that will be visualized
        cell_size (int): How large the cells will be in the plots
        height (int): The height of the maze
        width (int): The width of the maze
        ax: The axes for the plot
        lines:
        squares:
        media_filename (string): The name of the animations and images
    """
    def __init__(self, grid, cell_size, media_filename):
        self.grid = grid
        self.cell_size = cell_size
        self.height = grid.ny * cell_size
        self.width = grid.nx * cell_size
        self.ax = None
        self.lines = dict()
        self.squares = dict()
        self.media_filename = media_filename

    def set_media_filename(self, filename):
        """Sets the filename of the media
            Args:
                filename (string): The name of the media
        """
        self.media_filename = filename

    def show_maze(self):
        """Displays a plot of the maze without the solution path"""

        # Create the plot figure and style the axes
        fig = self.configure_plot()

        # Plot the walls on the figure
        self.plot_walls()
        self.plot_sg()

        # Display the plot to the user
        plt.show()

        

        # Handle any potential saving
        if self.media_filename:
            fig.savefig("{}{}.png".format(self.media_filename, "_generation"), frameon=None)



    def configure_plot(self):
        """Sets the initial properties of the maze plot. Also creates the plot and axes"""

        # Create the plot figure
        fig = plt.figure(figsize = (15, 15*self.grid.ny/self.grid.nx))

        # Create the axes
        self.ax = plt.axes()

        # Set an equal aspect ratio
        self.ax.set_aspect("equal")

        # Remove the axes from the figure
        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.axes.get_yaxis().set_visible(False)

        title_box = self.ax.text(0, self.grid.ny + self.cell_size + 0.1,
                            r"{}$\times${}".format(self.grid.ny, self.grid.nx),
                            bbox={"facecolor": "gray", "alpha": 0.5, "pad": 4}, fontname="serif", fontsize=15)

        return fig

    def plot_walls(self):
        for j in range(self.grid.ny):
            for i in range(self.grid.nx):
                self.ax.plot([i*self.cell_size, (i+1)*self.cell_size],[j*self.cell_size, j*self.cell_size], color= "k")
                self.ax.plot([i*self.cell_size, i*self.cell_size],[j*self.cell_size, (j+1)*self.cell_size], color= "k")
                self.ax.plot([i*self.cell_size, (i+1)*self.cell_size],[(j+1)*self.cell_size, (j+1)*self.cell_size], color= "k")
                self.ax.plot([(i+1)*self.cell_size, (i+1)*self.cell_size],[j*self.cell_size, (j+1)*self.cell_size], color= "k")
                if self.grid.cells[i][j].blocked == True:
                    self.ax.add_patch(plt.Rectangle((i*self.cell_size, j*self.cell_size), self.cell_size,self.cell_size, color ="k", alpha = 0.6))

    def plot_sg(self):
        self.ax.add_patch(plt.Rectangle((self.grid.start.x*self.cell_size, self.grid.start.y*self.cell_size), self.cell_size,self.cell_size, color = "g", alpha = 0.6))
        self.ax.add_patch(plt.Rectangle((self.grid.goal.x*self.cell_size, self.grid.goal.y*self.cell_size), self.cell_size,self.cell_size, color = "y", alpha = 0.6))
        self.ax.text(self.grid.start.x*self.cell_size, self.grid.start.y*self.cell_size, "S", fontsize = 7, weight = "bold")
        self.ax.text(self.grid.goal.x*self.cell_size, self.grid.goal.y*self.cell_size, "G", fontsize = 7, weight = "bold")
        

    def animate_maze_solution(self):
        fig = self.configure_plot()
        self.plot_walls()
        self.plot_sg()

        def animate(frame):
            animate_path_plan(frame)
            animate_move(frame)
            self.ax.set_title("Step: {}".format(frame+1), fontname="serif", fontsize = 19)
            return []

        def animate_path_plan(frame):
            for i, j in self.grid.path_plan_list[frame]:
                self.ax.plot([i*self.cell_size, (i+1)*self.cell_size],[j*self.cell_size, j*self.cell_size], linewidth=3, color= "b")
                self.ax.plot([i*self.cell_size, i*self.cell_size],[j*self.cell_size, (j+1)*self.cell_size], linewidth=3, color= "b")
                self.ax.plot([i*self.cell_size, (i+1)*self.cell_size],[(j+1)*self.cell_size, (j+1)*self.cell_size], linewidth=3, color= "b")
                self.ax.plot([(i+1)*self.cell_size, (i+1)*self.cell_size],[j*self.cell_size, (j+1)*self.cell_size], linewidth=3, color= "b")
            for i, j in self.grid.path_plan_center[frame]:
                self.ax.add_patch(plt.Rectangle((i*self.cell_size, j*self.cell_size), self.cell_size,self.cell_size, color ="r", alpha = 0.6))
                self.ax.text(i*self.cell_size, j*self.cell_size, "{}".format(frame+1), fontsize = 7, weight = "bold")

        def animate_move(frame):
            for i, j in self.grid.move_list[frame]:
                self.ax.add_patch(plt.Rectangle((i*self.cell_size, j*self.cell_size), self.cell_size,self.cell_size, color ="g", alpha = 0.6))

        anim = animation.FuncAnimation(fig, animate, frames=self.grid.frame,
                                       interval=100, blit=True, repeat=False)

        plt.show()

        if self.media_filename:
            print("Saving solution animation. This may take a minute....")
            mpeg_writer = animation.FFMpegWriter(fps=24, bitrate=1000,
                                                 codec="libx264", extra_args=["-pix_fmt", "yuv420p"])
            anim.save("{}{}{}x{}.mp4".format(self.media_filename, "_solution_", self.grid.ny,
                                           self.grid.nx), writer=mpeg_writer)
