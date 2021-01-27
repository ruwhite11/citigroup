import argparse
from importlib import import_module
from inspect import signature
import os
import sys


parser = argparse.ArgumentParser()

parser.add_argument("etl", type=str)

namespace, extra = parser.parse_known_args()
for arg in vars(namespace):
    etl = getattr(namespace,arg)


mod = import_module(etl,"pipelines")
met = getattr(mod, "etl")

p = signature(met)
for a, b in p.parameters.items():
    parser.add_argument(b.name, type=str, nargs='?')

args = parser.parse_args()

# Loop through the arguments and pass to ETL (try casting to int)
l = []
for arg in vars(args):
    print(arg, getattr(args, arg))
    if arg != "etl":
        l.append(getattr(args, arg))
        # try:
        #     l.append(int(getattr(args, arg)))
        # except:
        #     l.append(getattr(args, arg))

met(*l)