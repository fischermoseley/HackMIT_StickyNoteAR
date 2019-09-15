import numpy as np

def interpreter():
    orangeM = ''
    blueM = ''
    pinkM = ''
    greenM = ''

    orangeL = getOrange()
    blueL = getBlue() 
    pinkL = getPink()
    greenL = getGreen()
    if(in orangeL):
        for i in orangeL:
            for j in range(len(i[j])):
                orangeM = orangeM + str(i[j])
    if(in blueL):
        for i in blueL:
            for j in range(len(i[j])):
                blueM = blueM + str(i[j])
    if(in pinkL):
        for i in pinkL:
            for j in range(len(i[j])):
                pinkM = pinkM + str(i[j])
    if(in greenL):
        for i in greenL:
            for j in range(len(i[j])):
                greenM = greenM + str(i[j])
    
    return (orangeM, blueM, pinkM, greenM)

