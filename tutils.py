"""
Some utility functions for blog post on Turing Patterns.
"""

import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import os
class BaseStateSystem:
    """
    Base object for "State System".

    We are going to repeatedly visualise systems which are Markovian:
    the have a "state", the state evolves in discrete steps, and the next
    state only depends on the previous state.

    To make things simple, I'm going to use this class as an interface.
    """
    def __init__(self):
        raise NotImplementedError()

    def initialise(self):
        raise NotImplementedError()

    def initialise_figure(self):
        fig, ax = plt.subplots()
        return fig, ax

    def update(self):
        raise NotImplementedError()

    def draw(self, ax):
        raise NotImplementedError()

    def plot_time_evolution(self, filename, n_steps=30):
        """
        Creates a gif from the time evolution of a basic state syste.
        """
        self.initialise()
        fig, ax = self.initialise_figure()

        def step(t):
            self.update()
            self.draw(ax)

        anim = animation.FuncAnimation(fig, step, frames=np.arange(n_steps), interval=20)
        anim.save(filename=filename, dpi=60, fps=10, writer='imagemagick')
        plt.close()

    def plot_evolution_outcome(self, filename_prefix, n_steps):
        """
        Evolves the system for n_steps and saves three separate images
        for x1, x2, and x3, ensuring no negative values are displayed.
        """
        self.initialise()
        os.makedirs(save_dir, exist_ok=True)
        
        for _ in range(n_steps):
            self.update()
    
        # Generate figures for each variable separately
        for i, (data, title, filename) in enumerate(zip(
            [self.x1, self.x2, self.x3], 
            ["T^+", "T^p", "T^-"], 
            [f"{filename_prefix}_Tplus.png", f"{filename_prefix}_Tp.png", f"{filename_prefix}_Tminus.png"]
        )):
            fig, ax = plt.subplots(figsize=(6,6))
            
            data = np.maximum(data, 0)  # Remove negative values by setting them to zero
            
            im = ax.imshow(data, cmap='jet', origin='lower')  # 'lower' inverts y-axis
            ax.set_title(f"{title}, t = {self.t:.2f}")
            ax.set_xlabel("X-axis")
            ax.set_ylabel("Y-axis")
            ax.grid(False)  # Removes grid lines
            plt.colorbar(im, ax=ax)  # Add colorbar
            filepath = os.path.join(save_dir, filename)
            fig.savefig(filepath) 
            plt.close(fig)
