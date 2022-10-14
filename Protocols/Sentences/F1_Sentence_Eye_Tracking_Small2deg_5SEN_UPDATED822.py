from __future__ import absolute_import, division
import psychopy
psychopy.useVersion('latest')
from psychopy import locale_setup, prefs, sound, gui, visual, core, data, event, logging, clock, monitors
import numpy as np
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
from psychopy.hardware import keyboard
import os, time, csv, random
import subprocess, zmq

import ctypes
lib = ctypes.windll.kernel32

angles = [0]
directions = [0, 2] #0 is right, 2 is left
trials = 5
sentences = [[] for i in range(10)]

sentences[0].append('I wrote a letter to my grandmother.')
sentences[0].append('She lives in another country.')
sentences[0].append('She does not have a phone.')
sentences[0].append('She does have a mailbox.')
sentences[0].append('It is the only way to contact her.')
sentences[1].append('The sky is cloudy and gray.')
sentences[1].append('The wind is blowing.')
sentences[1].append('It might rain today.')
sentences[1].append('I do not want to get wet.')
sentences[1].append('I should bring an umbrella.')
sentences[2].append('The nervous system is made of neurons.')
sentences[2].append('It connects our brain and body.')
sentences[2].append('The brain has many functions.')
sentences[2].append('The mind is very complex.')
sentences[2].append('We are still learning about it.')
sentences[3].append('I want to become a doctor.')
sentences[3].append('I am applying to medical schools.')
sentences[3].append('The application is very long.')
sentences[3].append('I am feeling very tired.')
sentences[3].append('It is due in June.')
sentences[4].append('There is a dictionary open on the table.')
sentences[4].append('I pick up the dictionary.')
sentences[4].append('The word "gazebo" is highlighted.')
sentences[4].append('I read the definition.')
sentences[4].append('It is a type of garden structure.')
sentences[5].append('I went to the movies yesterday.')
sentences[5].append('It was fun and exciting.')
sentences[5].append('I want to see the film again.')
sentences[5].append('I will bring my friends.')
sentences[5].append('We will eat popcorn together.')
sentences[6].append('My family likes to eat pasta everyday.')
sentences[6].append('We will eat spaghetti for dinner.')
sentences[6].append('Yesterday, we ate lasagna.')
sentences[6].append('Tomorrow, we will eat ravioli.')
sentences[6].append('Italian food is our favorite.')
sentences[7].append('I prefer ice cream over cake.')
sentences[7].append('Sally likes cake over ice cream.')
sentences[7].append('John likes cookies over both.')
sentences[7].append('Lisa likes cookie-flavored ice cream')
sentences[7].append('Justin does not like food that is sweet.')
sentences[8].append('He used a knife to cut the turkey.')
sentences[8].append('She used a fork to eat the cake.')
sentences[8].append('The baby ate cranberry sauce.')
sentences[8].append('The dog bumped into the table.')
sentences[8].append('They used napkins to clean the mess.')
sentences[9].append('I got a job as the new librarian.')
sentences[9].append('I like the smell of old books.')
sentences[9].append('It is very quiet inside.')
sentences[9].append('The hours are very flexible.')
sentences[9].append('I am being paid very well.')


['I wrote a letter to my grandmother.', \
'Bravo romeo oscar whiskey november echo.', \
'The sky is cloudy and gray.', \
'Delta romeo echo alpha mike yankee.', \
'A neuron is a type of cell.', \
'November echo uniform romeo oscar.', \
'I want to become a doctor.', \
'Foxtrot oscar lima delta echo romeo.', \
'There is a dictionary open on the table.', \
'Tango romeo india bravo alpha lima.', \
'I want to see the film again.', \
'India november delta india golf oscar.', \
'We will eat spaghetti for dinner.', \
'Lima yankee mike papa hotel.', \
'I prefer ice cream over cake.', \
'Delta echo sierra echo romeo tango.', \
'He used a knife to cut the cake.', \
'Kilo india tango charlie hotel.', \
'I got a job as the new librarian.', \
'Papa yankee tango hotel oscar november.']


def upTime():
    t = lib.GetTickCount64()
    return t

def csvOutput(output, fileName):
    with open(fileName, 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(output)
    csvFile.close()
    
def csvInput(fileName):
    with open(fileName) as csvFile:
        reader = csv.DictReader(csvFile, delimiter = ',')
        dict = next(reader)
    csvFile.close()
    return dict

_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)  
gaborfile = os.path.join(os.getcwd(), 'eccentricity_monitor_calibration.csv')
if not os.path.isfile(gaborfile):
    print('You must run the eccentricity_calibration.py script to set up your monitor')
    time.sleep(5)
    core.quit()

tvInfo = csvInput(gaborfile)

distToScreen = float(tvInfo['Distance to screen'])
heightMult, spacer = float(tvInfo['height']), float(tvInfo['spacer'])
circleMult = float(tvInfo['circleRadius'])
centerX, centerY = float(tvInfo['centerx']), float(tvInfo['centery'])
rightXMult, leftXMult = float(tvInfo['rightx']), float(tvInfo['leftx'])
rightEdge, leftEdge = float(tvInfo['rightEdge']), float(tvInfo['leftEdge'])

def endExp():
    win.flip()
    proc.terminate()
    logging.flush()
    win.close()
    core.quit()

datadlg = gui.Dlg(title='Record Data?', pos=None, size=None, style=None,\
     labelButtonOK=' Yes ', labelButtonCancel=' No ', screen=-1)
ok_data = datadlg.show()
recordData = datadlg.OK

if recordData:
    date = time.strftime("%m_%d")
    expName = 'F1_Sentence_Eye_Tracking_SM'
    expInfo = {'Subject Name': ''}
    
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    if dlg.OK == False:
        core.quit()
    
    # Create folder for each experiment, will contain CSV data file and all eye tracking data files.
    # This folder will have the same name as the CSV file.
    OUTPATH = os.path.join(os.getcwd(), 'Data', \
        (expInfo['Subject Name'] + '_' + date + '_' + expName))
    if not os.path.isdir(OUTPATH):
        os.mkdir(OUTPATH)
    
    # Write experimental data to CSV file
    fileName = os.path.join(OUTPATH,\
        (expInfo['Subject Name'] + '_' + date + '_' + expName + '.csv'))
    fileName2 = os.path.join(OUTPATH,\
        (expInfo['Subject Name'] + '_' + 'CALIBRATION' + '_' + date + '_' + expName + '.csv'))
        
datadlg = gui.Dlg(title='Select cross position', screen=-1)
datadlg.addField('Position: ', choices = ["Center", "Right", "Left"])
ok_data2 = datadlg.show()
if ok_data2 is None:
    endExp()
elif ok_data2[0] == 'Left':
    centerX = -(leftEdge-3)
    dirExclusions = [2]
elif ok_data2[0] == 'Right':
    centerX = rightEdge-3
    dirExclusions = [0]
else:
    dirExclusions = []

    
headers = ['Sentence', 'Direction', 'Reading Time (s)', 'Eye Tracking Start Time (CPU Uptime)']
if not os.path.isfile(fileName):
    csvOutput(headers, fileName)
    
headers2 = ['X Position', 'Y Position', 'Eye Tracking Start Time (CPU Uptime)', 'Eye Tracking End Time (CPU Uptime)']
if not os.path.isfile(fileName2):
    csvOutput(headers2, fileName2)

mon = monitors.Monitor('TV') # Change this to the name of your display monitor
mon.setWidth(float(tvInfo['Width (cm)']))
win = visual.Window(
    size=(int(tvInfo['Width (px)']), int(tvInfo['Height (px)'])), fullscr=True, screen=int(tvInfo['Screen number']), 
    winType='pyglet', allowGUI=True, allowStencil=False,
    monitor= mon, color='grey', colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='cm')
    
def genDisplay(displayInfo):
    displayText = visual.TextStim(win=win,
    text= displayInfo['text'],
    font='Arial',
    pos=(displayInfo['xPos'], displayInfo['yPos']),
    height=displayInfo['heightCm'],
    wrapWidth=500,
    ori=0, 
    color=displayInfo['color'],
    colorSpace='rgb',
    opacity=1, 
    languageStyle='LTR',
    depth=0.0)
    return displayText
    
def displaceCalc(angle):
    angleRad = np.deg2rad(angle)
    xDisp = np.tan(angleRad)*distToScreen
    return xDisp
    

cross = visual.ShapeStim(
    win=win, name='Cross', vertices='cross',units='cm', 
    size=(1, 1),
    ori=0, pos=(centerX, centerY),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1, depth=-1.0, interpolate=True)
    
radius = displaceCalc(2)*circleMult
Circle = psychopy.visual.Circle(
    win=win,
    units="cm",
    size = radius
)    
Circle.contrast = 1
#grating = psychopy.visual.GratingStim(
#    win=win,
#    units="cm",
#    size = radius
#)    
#grating.sf = 5/radius
#grating.contrast = 1
#grating.mask = 'circle'

def instructions():
    genDisplay({'text': 'You will be presented with either a complete sentence',\
        'xPos': 0, 'yPos': centerY+4, 'heightCm': 1, 'color': 'white'}).draw()
    genDisplay({'text': 'or a series of words arranged to form a sentence.',\
        'xPos': 0, 'yPos': centerY+2, 'heightCm': 1, 'color': 'white'}).draw()
    genDisplay({'text': 'Read each sentence completely.',\
        'xPos': 0, 'yPos': centerY,'heightCm': 1, 'color': 'white'}).draw()
    genDisplay({'text': 'Press the spacebar after reading all sentences.',\
        'xPos': 0, 'yPos': centerY-2,'heightCm': 1, 'color': 'white'}).draw()
    genDisplay({'text': 'Press the spacebar to continue',\
        'xPos': 0, 'yPos': centerY-4,'heightCm': 1, 'color': 'white'}).draw()
    win.flip()
    keyy = event.waitKeys(keyList = ['space', 'escape']) 
    if keyy[0] == 'escape': 
        win.flip()
        logging.flush()
        win.close()
        core.quit()

def instructions2():
    genDisplay({'text': 'You will see a number of white dots around the screen.',\
        'xPos': 0, 'yPos': centerY+2, 'heightCm': 1, 'color': 'white'}).draw()
    genDisplay({'text': 'When they appear, look at them until they disappear.',\
        'xPos': 0, 'yPos': centerY, 'heightCm': 1, 'color': 'white'}).draw()
    genDisplay({'text': 'Press the space bar to begin.',\
        'xPos': 0, 'yPos': centerY-2,'heightCm': 1, 'color': 'white'}).draw()
    win.flip()
    keyy = event.waitKeys(keyList = ['space', 'escape']) 
    if keyy[0] == 'escape': 
        win.flip()
        logging.flush()
        win.close()
        core.quit()

def expBreak():
    dispInfo = {'text': 'Break', 'xPos': 0, 'yPos': centerY+4, 'heightCm': 3, 'color': 'white'}
    breakText = genDisplay(dispInfo)
    dispInfo = {'text': '', 'xPos': 0, 'yPos': centerY, 'heightCm': 3, 'color': 'white'}
    for i in range(20):
        breakText.draw()
        dispInfo['text'] = str(20-i) + ' seconds'
        genDisplay(dispInfo).draw()
        win.flip()
        time.sleep(1)
        
def inBounds(trialInfo):
    if trialInfo['dir'] in dirExclusions:
        return False
    if trialInfo['dir'] == 0:
        if (centerX + displaceCalc(trialInfo['angle'])) > rightEdge:
            return False
    elif trialInfo['dir'] == 2:
        if (centerX - displaceCalc(trialInfo['angle'])) < (-leftEdge):
            return False
    return True

def genPairs():
    pairs = list(range(0))
    for i in range(trials):
        for j in range(len(sentences)):
            pairs.append(j*10)
    shuffle(pairs)
    return pairs
    
def interpretPair(pair):
    angle = 0
    direction = directions[int(pair%10)]
    sentence = sentences[int(pair/10)]
    sentence1 = sentence[0]
    sentence2 = sentence[1]
    sentence3 = sentence[2]
    sentence4 = sentence[3]
    sentence5 = sentence[4]
    return {'angle': angle, 'dir': direction, 'sentence': sentence, 'sentence1': sentence1, 'sentence2': sentence2, 'sentence3': sentence3, 'sentence4': sentence4, 'sentence5': sentence5}
   

def calibPeriod(xCoord, yCoord, dotNum):
    if xCoord == -40:
        xPos = centerX + abs(displaceCalc(-40))*leftXMult
    elif xCoord ==40:
        xPos = centerX + displaceCalc(40)*rightXMult
    elif xCoord ==0:
        xPos = centerX
    if yCoord == -20:
        yPos = centerY - abs(displaceCalc(-20))
    elif yCoord ==20:
        yPos = centerY + displaceCalc(20)
    elif yCoord ==0:
        yPos = centerY
    genDisplay({'text': 'Dot' + str(dotNum),\
        'xPos': xPos, 'yPos': yPos+2, 'heightCm': 1.5*heightMult, 'color': 'white'}).draw()
    genDisplay({'text': 'press spacebar to continue.',\
        'xPos': xPos, 'yPos': yPos+2, 'heightCm': 1.5*heightMult, 'color': 'white'}).draw()
    win.flip()
    keys = event.waitKeys(keyList = ['space', 'escape'])
    key = keys[0]
    if key[0] == 'escape':
        win.flip()
        logging.flush()
        win.close()
        core.quit()
    Circle.color = 'white'
    Circle.pos = (xPos, yPos)
    Circle.draw()
    
    win.flip()
    startTime = upTime()
    
    time.sleep(5)
    endTime = upTime()
    output = (xCoord, yCoord, startTime, endTime)
    csvOutput(output, fileName2)

instructions2()

calibPeriod(0, 0, 1)

instructions()

pairs = genPairs()



#correct = 0
#incorrect = 1

run = 0
mistakes = 0

stimheight = displaceCalc(2)*heightMult

mistakedict = {}

for pair in pairs:
    win.flip()
    trialInfo = interpretPair(pair)
    if not inBounds(trialInfo):
        continue
    cross.draw()
    time.sleep(.1)
    win.flip()
    interstimulus = random.uniform(.3,.8)
    time.sleep(interstimulus)
    #grating.ori = trialInfo['orientation']
    displacement = 0
    if trialInfo['dir'] == 0:
        xPos = centerX + displacement*rightXMult
    elif trialInfo['dir'] ==2:
        xPos = centerX + displacement*leftXMult
    genDisplay({'text': trialInfo['sentence1'], 'xPos': xPos, 'yPos': centerY+10, 'heightCm': stimheight, 'color': 'white'}).draw()
    genDisplay({'text': trialInfo['sentence2'], 'xPos': xPos, 'yPos': centerY+5, 'heightCm': stimheight, 'color': 'white'}).draw()
    genDisplay({'text': trialInfo['sentence3'], 'xPos': xPos, 'yPos': centerY, 'heightCm': stimheight, 'color': 'white'}).draw()
    genDisplay({'text': trialInfo['sentence4'], 'xPos': xPos, 'yPos': centerY-5, 'heightCm': stimheight, 'color': 'white'}).draw()
    genDisplay({'text': trialInfo['sentence5'], 'xPos': xPos, 'yPos': centerY-10, 'heightCm': stimheight, 'color': 'white'}).draw()
    times = {'start': 0, 'end': 0}
    win.timeOnFlip(times, 'start')
    
    currentTime = upTime()
    win.flip()
    keys = event.waitKeys(timeStamped = True, keyList = ['space', 'escape'])
    key = keys[0]
    if key[0] == 'escape':
        endExp()
    times['end'] = key[1]
    readingTime = times['end'] - times['start']
    buffer = 10.0 - interstimulus - readingTime
    if buffer > 0:
        output = (trialInfo['sentence1']+' '+trialInfo['sentence2']+' '+trialInfo['sentence3']+' '+trialInfo['sentence4']+' '+trialInfo['sentence5'], trialInfo['dir'], readingTime, currentTime)
        csvOutput(output, fileName)
    else:
        mistakedict[mistakes] = trialInfo
        mistakes += 1
    run += 1
    win.flip()
    if run%52 == 0 and run != 208:
        expBreak()
    if buffer > 0:
        time.sleep(buffer)

run2 = 0
if mistakes > 0:
    genDisplay({'text': 'These trials are a make-up of your mistakes',\
        'xPos': 0, 'yPos': centerY+5, 'heightCm': 1, 'color': 'white'}).draw()
    genDisplay({'text': 'Please follow the same instructions',\
        'xPos': 0, 'yPos': centerY+3, 'heightCm': 1, 'color': 'white'}).draw()
    genDisplay({'text': 'and press Space to continue',\
        'xPos': 0, 'yPos': centerY+1, 'heightCm': 1, 'color': 'white'}).draw()
    win.flip()
    keyyy = event.waitKeys(keyList = ['space', 'escape'])
    if keyyy[0] == 'escape': 
        win.flip()
        logging.flush()
        win.close()
        core.quit()
    l = 0
    while l < mistakes:
        win.flip()
        trialInfo = mistakedict[l]
        if not inBounds(trialInfo):
            continue
        cross.draw()
        time.sleep(.1)
        win.flip()
        interstimulus2 = random.uniform(.3,.8)
        time.sleep(interstimulus2)
        displacement = 0
        if trialInfo['dir'] == 0:
            xPos = centerX + displacement*rightXMult
        elif trialInfo['dir'] ==2:
            xPos = centerX + displacement*leftXMult  
        genDisplay({'text': trialInfo['sentence1'], 'xPos': xPos, 'yPos': centerY+10, 'heightCm': stimheight, 'color': 'white'}).draw()
        genDisplay({'text': trialInfo['sentence2'], 'xPos': xPos, 'yPos': centerY+5, 'heightCm': stimheight, 'color': 'white'}).draw()
        genDisplay({'text': trialInfo['sentence3'], 'xPos': xPos, 'yPos': centerY, 'heightCm': stimheight, 'color': 'white'}).draw()
        genDisplay({'text': trialInfo['sentence4'], 'xPos': xPos, 'yPos': centerY-5, 'heightCm': stimheight, 'color': 'white'}).draw()
        genDisplay({'text': trialInfo['sentence5'], 'xPos': xPos, 'yPos': centerY-10, 'heightCm': stimheight, 'color': 'white'}).draw()
        times = {'start': 0, 'end': 0}
        win.timeOnFlip(times, 'start')
        
        currentTime = upTime()
        win.flip()
        keys = event.waitKeys(timeStamped = True, keyList = ['space', 'escape'])
        key2 = keys[0]
        if key2[0] == 'escape':
            endExp()
        times['end'] = key2[1]
        readingTime = times['end'] - times['start']
        buffer2 = 10.0 - interstimulus2 - readingTime
        if buffer2 > 0:
            output = (trialInfo['sentence1']+' '+trialInfo['sentence2']+' '+trialInfo['sentence3']+' '+trialInfo['sentence4']+' '+trialInfo['sentence5'], trialInfo['dir'], readingTime, currentTime)
            csvOutput(output, fileName)
        else:
            mistakedict[mistakes] = trialInfo
            mistakes += 1
        run2 += 1
        l += 1
        win.flip()
        if len (dirExclusions) == 0 and run2%52 == 0:
            expBreak()
        if buffer2 > 0:
            time.sleep(buffer2)
        
strmistakes = str(mistakes)
print(strmistakes + ' mistakes')
endExp()