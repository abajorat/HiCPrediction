#!/usr/bin/env python3

from hicprediction.configurations import *


@click.argument('filename', type=click.Path(exists=True))
@click.command()
def showH5(filename):
    # df = pd.read_csv(filename)
    # print(df.iloc[:,:26].head(50))
    with h5py.File(filename, 'r') as f:
        f.visit(printName)


def repair():
    with h5py.File(filename, 'r') as f:
        with h5py.File("new" + filename, 'w') as m:
            for name  in f.keys():
                if name.startswith("proteins_"):
                    new =  name.split("proteins_")[-1]
                else:
                    new = name
                f.copy(name, m,name=new)

def printName(name):
    print(name)

if __name__ == '__main__':
    showH5()
