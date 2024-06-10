from locust import  LoadTestShape
import subprocess

class StagesShapeWithCustomUsers(LoadTestShape):
    
    lastStage = None
    
    # stages = [{'duration': 61, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 122, 'users': 71, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 183, 'users': 127, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 244, 'users': 171, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 305, 'users': 200, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 366, 'users': 210, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 427, 'users': 200, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 488, 'users': 171, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 549, 'users': 127, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 610, 'users': 71, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 671, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 732, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 793, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 854, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 915, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 976, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 1037, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 1098, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 1159, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 1220, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 1281, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 1342, 'users': 71, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 1403, 'users': 127, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 1464, 'users': 171, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 1525, 'users': 200, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 1586, 'users': 210, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 1647, 'users': 200, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 1708, 'users': 171, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 1769, 'users': 127, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 1830, 'users': 71, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 1891, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 1952, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 2013, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 2074, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 2135, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 2196, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 2257, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 2318, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 2379, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 2440, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 2501, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 2562, 'users': 71, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 2623, 'users': 127, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 2684, 'users': 171, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 2745, 'users': 200, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 2806, 'users': 210, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 2867, 'users': 200, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 2928, 'users': 171, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 2989, 'users': 127, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 3050, 'users': 71, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 3111, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 3172, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 3233, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 3294, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 3355, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 3416, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 3477, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 3538, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]},
    #  {'duration': 3600, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [220, 220], 'Conc': [220, 220]}]
    
    stages =[{'duration': 61, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 122, 'users': 71, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [10, 29], 'Conc': [5, 1]},
             {'duration': 183, 'users': 127, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [18, 51], 'Conc': [5, 1]},
             {'duration': 244, 'users': 171, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [24, 69], 'Conc': [5, 1]},
             {'duration': 305, 'users': 200, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [28, 80], 'Conc': [5, 1]},
             {'duration': 366, 'users': 210, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [29, 84], 'Conc': [5, 1]},
             {'duration': 427, 'users': 200, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [28, 80], 'Conc': [5, 1]},
             {'duration': 488, 'users': 171, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [24, 69], 'Conc': [5, 1]},
             {'duration': 549, 'users': 127, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [18, 51], 'Conc': [5, 1]},
             {'duration': 610, 'users': 71, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [10, 29], 'Conc': [5, 1]},
             {'duration': 671, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 732, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 793, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 854, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 915, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 976, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 1037, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 1098, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 1159, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 1220, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 1281, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 1342, 'users': 71, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [10, 29], 'Conc': [5, 1]},
             {'duration': 1403, 'users': 127, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [18, 51], 'Conc': [5, 1]},
             {'duration': 1464, 'users': 171, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [24, 69], 'Conc': [5, 1]},
             {'duration': 1525, 'users': 200, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [28, 80], 'Conc': [5, 1]},
             {'duration': 1586, 'users': 210, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [29, 84], 'Conc': [5, 1]},
             {'duration': 1647, 'users': 200, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [28, 80], 'Conc': [5, 1]},
             {'duration': 1708, 'users': 171, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [24, 69], 'Conc': [5, 1]},
             {'duration': 1769, 'users': 127, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [18, 51], 'Conc': [5, 1]},
             {'duration': 1830, 'users': 71, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [10, 29], 'Conc': [5, 1]},
             {'duration': 1891, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 1952, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 2013, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 2074, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 2135, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 2196, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 2257, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 2318, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 2379, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 2440, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 2501, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 2562, 'users': 71, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [10, 29], 'Conc': [5, 1]},
             {'duration': 2623, 'users': 127, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [18, 51], 'Conc': [5, 1]},
             {'duration': 2684, 'users': 171, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [24, 69], 'Conc': [5, 1]},
             {'duration': 2745, 'users': 200, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [28, 80], 'Conc': [5, 1]},
             {'duration': 2806, 'users': 210, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [29, 84], 'Conc': [5, 1]},
             {'duration': 2867, 'users': 200, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [28, 80], 'Conc': [5, 1]},
             {'duration': 2928, 'users': 171, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [24, 69], 'Conc': [5, 1]},
             {'duration': 2989, 'users': 127, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [18, 51], 'Conc': [5, 1]},
             {'duration': 3050, 'users': 71, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [10, 29], 'Conc': [5, 1]},
             {'duration': 3111, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 3172, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 3233, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 3294, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 3355, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 3416, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 3477, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 3538, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]},
             {'duration': 3600, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [2, 4], 'Conc': [5, 1]}]
    
         
    # stages = [{'duration': 61, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 122, 'users': 71, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [20, 23], 'Conc': [5, 1]},
    #          {'duration': 183, 'users': 127, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [35, 41], 'Conc': [5, 1]},
    #          {'duration': 244, 'users': 171, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [47, 55], 'Conc': [5, 1]},
    #          {'duration': 305, 'users': 200, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [55, 64], 'Conc': [5, 1]},
    #          {'duration': 366, 'users': 210, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [58, 68], 'Conc': [5, 1]},
    #          {'duration': 427, 'users': 200, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [55, 64], 'Conc': [5, 1]},
    #          {'duration': 488, 'users': 171, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [47, 55], 'Conc': [5, 1]},
    #          {'duration': 549, 'users': 127, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [35, 41], 'Conc': [5, 1]},
    #          {'duration': 610, 'users': 71, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [20, 23], 'Conc': [5, 1]},
    #          {'duration': 671, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 732, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 793, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 854, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 915, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 976, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 1037, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 1098, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 1159, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 1220, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 1281, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 1342, 'users': 71, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [20, 23], 'Conc': [5, 1]},
    #          {'duration': 1403, 'users': 127, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [35, 41], 'Conc': [5, 1]},
    #          {'duration': 1464, 'users': 171, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [47, 55], 'Conc': [5, 1]},
    #          {'duration': 1525, 'users': 200, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [55, 64], 'Conc': [5, 1]},
    #          {'duration': 1586, 'users': 210, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [58, 68], 'Conc': [5, 1]},
    #          {'duration': 1647, 'users': 200, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [55, 64], 'Conc': [5, 1]},
    #          {'duration': 1708, 'users': 171, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [47, 55], 'Conc': [5, 1]},
    #          {'duration': 1769, 'users': 127, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [35, 41], 'Conc': [5, 1]},
    #          {'duration': 1830, 'users': 71, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [20, 23], 'Conc': [5, 1]},
    #          {'duration': 1891, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 1952, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 2013, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 2074, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 2135, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 2196, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 2257, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 2318, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 2379, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 2440, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 2501, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 2562, 'users': 71, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [20, 23], 'Conc': [5, 1]},
    #          {'duration': 2623, 'users': 127, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [35, 41], 'Conc': [5, 1]},
    #          {'duration': 2684, 'users': 171, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [47, 55], 'Conc': [5, 1]},
    #          {'duration': 2745, 'users': 200, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [55, 64], 'Conc': [5, 1]},
    #          {'duration': 2806, 'users': 210, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [58, 68], 'Conc': [5, 1]},
    #          {'duration': 2867, 'users': 200, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [55, 64], 'Conc': [5, 1]},
    #          {'duration': 2928, 'users': 171, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [47, 55], 'Conc': [5, 1]},
    #          {'duration': 2989, 'users': 127, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [35, 41], 'Conc': [5, 1]},
    #          {'duration': 3050, 'users': 71, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [20, 23], 'Conc': [5, 1]},
    #          {'duration': 3111, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 3172, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 3233, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 3294, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 3355, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 3416, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 3477, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 3538, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]},
    #          {'duration': 3600, 'users': 10, 'spawn_rate': 1, 'functions': ['f3', 'f4'], 'Rep': [3, 4], 'Conc': [5, 1]}]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                #self.updateCrtl(stage)
                try:
                    tick_data = (stage["users"], stage["spawn_rate"], stage["user_classes"])
                except:
                    tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
    
    def updateCrtl(self, stage):
        if(stage != StagesShapeWithCustomUsers.lastStage):
            R = stage["Rep"]
            C = stage["Conc"]
            F = stage["functions"]
            for i in range(len(R)):
                ufile = open("../%s/update.sh" % (F[i]), "r")
                filestr = ufile.read()
                ufile.close()
                
                updatecmd=None
                
                if( StagesShapeWithCustomUsers.lastStage!=None and stage["users"]>StagesShapeWithCustomUsers.lastStage["users"] or StagesShapeWithCustomUsers.lastStage==None):
                    updatecmd = filestr.replace("$NT", "%d" % (C[i]))
                    updatecmd = updatecmd.replace("$REP_max", "%d" % (R[i]))
                    updatecmd = updatecmd.replace("$REP_min", "%d" % (R[i]))
                elif(stage["users"]<=StagesShapeWithCustomUsers.lastStage["users"]):
                    updatecmd = filestr.replace("$NT", "%d" % (C[i]))
                    updatecmd = updatecmd.replace("$REP_max", "%d" % (R[i]))
                    updatecmd = updatecmd.replace("$REP_min", "%d" % (0)) #nel caso scendono gli utenti faccio scendere il numero di isntanze in modo graduale
                    
                    
                
                ufile = open("../%s/update_cmd.sh" % (F[i]), "w+")
                filestr = ufile.write(updatecmd)
                ufile.close()
                
                subprocess.Popen(["sh", "../%s/update_cmd.sh" % (F[i])])
        
            StagesShapeWithCustomUsers.lastStage = stage