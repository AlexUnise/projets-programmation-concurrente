import os,sys,time,random
import multiprocessing as mp




class GameOfLife():
    def __init__(self,DisplayHeight,DisplayWidth):
        self.__DisplayHeight = DisplayHeight
        self.__DisplayWidth = DisplayWidth
        self.__Display = []

    def DisplaySetup(self):
        for i in range(self.__DisplayHeight):
            for j in range(self.__DisplayWidth):
                
