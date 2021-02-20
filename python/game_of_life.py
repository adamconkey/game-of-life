#!/usr/bin/env python
import os
import sys
import argparse
import threading
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

DEFAULT_CONFIG_DIR = "../config"


class GameOfLife:

    def __init__(self, grid_height=64, grid_width=64, on_squares=[], update_interval=50, toroidal=True):
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.update_interval = update_interval
        self.toroidal = toroidal

        if on_squares:
            self.grid = np.zeros((grid_height, grid_width))
            for on_square in on_squares:
                self.grid[on_square[0], on_square[1]] = 1
        else:
            self.grid = np.random.choice([0, 1], (grid_height, grid_width))

    def update_grid(self):
        grid = np.zeros((self.grid_height, self.grid_width))
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                n_live = self.count_live_neighbors(i, j)
                live_and_stay_alive = self.grid[i, j] and n_live in [2, 3]
                dead_and_become_alive = (not self.grid[i, j]) and n_live == 3
                grid[i, j] = int(live_and_stay_alive or dead_and_become_alive)
        self.grid = grid
                
    def count_live_neighbors(self, i, j):
        count = 0
        count += self.get_value(i-1, j-1)
        count += self.get_value(i-1, j)
        count += self.get_value(i-1, j+1)
        count += self.get_value(i, j-1)
        count += self.get_value(i, j+1)
        count += self.get_value(i+1, j-1)
        count += self.get_value(i+1, j)
        count += self.get_value(i+1, j+1)
        return count

    def get_value(self, i, j):
        if self.toroidal:
            if i < 0:
                i = self.grid_height - 1
            if i >= self.grid_height:
                i = 0
            if j < 0:
                j = self.grid_width - 1
            if j >= self.grid_width:
                j = 0
            return self.grid[i, j]
        else:
            if i < 0 or i > self.grid_height - 1 or j < 0 or j > self.grid_height - 1:
                return 0
            else:
                return self.grid[i, j]
                
    def run(self):
        fig = plt.figure()
        fig.set_size_inches(8, 8)
        fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
        img = plt.imshow(self.grid, animated=True)

        def update(*args):
            self.update_grid()
            img.set_data(self.grid)
            return img,

        ani = animation.FuncAnimation(fig, update, interval=self.update_interval, blit=True)
        plt.show()
        
    def generate_data(self):
        while True:
            self.update_grid()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str)
    parser.add_argument('--config_dir', type=str, default=DEFAULT_CONFIG_DIR)
    parser.add_argument('--update_interval', type=int, default=1)
    parser.add_argument('--toroidal', dest='toroidal', action='store_true')
    parser.add_argument('--no_toroidal', dest='toroidal', action='store_false')
    parser.set_defaults(toroidal=True)
    args = parser.parse_args()

    if args.config:
        filename = os.path.join(args.config_dir, args.config)
        with open(filename, 'r') as f:
            config = json.load(f)
        game = GameOfLife(config['grid_height'], config['grid_width'], config['on_squares'],
                          args.update_interval, args.toroidal)
    else:
        game = GameOfLife(update_interval=args.update_interval, toroidal=args.toroidal)
        
    game.run()
