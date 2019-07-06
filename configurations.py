from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import auc

from hicmatrix import HiCMatrix as hm
from hicexplorer import hicPlotMatrix as hicPlot

import sys
import argparse
import math
import time
import datetime
import shutil
import pickle
import os
import numpy as np
import logging as log
import pandas as pd
from copy import copy, deepcopy

import cooler
import pybedtools

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import LogNorm

from scipy import sparse
from scipy import signal
from scipy import misc
from scipy.stats.stats import pearsonr

log.basicConfig(level=log.DEBUG)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
np.set_printoptions(threshold=sys.maxsize)
np.set_printoptions(precision=3, suppress=True)

# global constants
BIN_D = "5B/"
DATA_D = "Data2e/"
RESULT_D = "Data2e/Results/"
RESULTPART_D = "Data2e/Results/Part/"
CHROM_D = DATA_D +BIN_D+ "Chroms/"
ARM_D = DATA_D +BIN_D+ "Arms/"
SET_D = DATA_D + BIN_D +"Sets/"
SETC_D = DATA_D + BIN_D +"SetsCombined/"
PRED_D = DATA_D +BIN_D+ "Predictions/"
MODEL_D  = DATA_D + BIN_D+"Models/"
IMAGE_D = DATA_D +  "Images/"
PLOT_D = DATA_D +BIN_D +  "Plots/"
ORIG_D = DATA_D +  "BaseData/Orig/"
PROTEIN_D = DATA_D + BIN_D+"Proteins/"
PROTEINORIG_D = DATA_D +"BaseData/ProteinOrig/"



def parseArguments(args=None):
    print(args)

    parser = argparse.ArgumentParser(description='HiC Prediction')

    parserRequired = parser.add_argument_group('Required arguments')

    # define the arguments
    parserRequired.add_argument('--action', '-a',
                                choices=['train','allCombs',
     'predictAll','predict','combine', 'split','trainAll', 'createAllWindows','plotAll',
    'loadProtein','plot','plotPred','createArms','mergeAndSave','loadAllProteins','trainPredictAll',
    'createWindows' ], help='Action to take', required=True)

    parserOpt = parser.add_argument_group('Optional arguments')
    parserOpt.add_argument('--arms', '-ar',type=str, default="AB")
    parserOpt.add_argument('--binSize', '-bs',type=int, default=5000)
    parserOpt.add_argument('--chrom', '-c',type=str, default="4")
    parserOpt.add_argument('--chroms', '-cs',type=str, default="1_2")
    parserOpt.add_argument('--conversion', '-co',type=str, default="default")
    parserOpt.add_argument('--directConversion', '-d',type=int, default=1)
    parserOpt.add_argument('--equalizeProteins', '-ep',type=bool, default=False)
    parserOpt.add_argument('--estimators', '-e',type=int, default=10)
    parserOpt.add_argument('--grid', '-g',type=int, default=0)
    parserOpt.add_argument('--log', '-l',type=bool, default=True)
    parserOpt.add_argument('--loss', '-lf',type=str, default="mse")
    parserOpt.add_argument('--mergeOperation', '-mo',type=str, default='avg')
    parserOpt.add_argument('--model', '-m',type=str, default="rf")
    parserOpt.add_argument('--normalizeProteins', '-np',type=bool, default=False)
    parserOpt.add_argument('--reach', '-r',type=str, default="200")
    parserOpt.add_argument('--region', '-re',type=str, default=None)
    parserOpt.add_argument('--regionIndex1', '-r1',type=int, default=None)
    parserOpt.add_argument('--regionIndex2', '-r2',type=int, default=None)
    parserOpt.add_argument('--sourceFile', '-sf',type=str, default="")
    parserOpt.add_argument('--windowOperation', '-wo',type=str, default="avg")
    args = parser.parse_args(args)
    print(args)
    return args


