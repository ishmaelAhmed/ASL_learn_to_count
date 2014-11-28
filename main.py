import Leap, sys, thread, time, random
import matplotlib
import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Leap import *
from pylab import *
import matplotlib.image as mpimg
import random
from sklearn import datasets, neighbors
import numpy as np
import matplotlib.path as mpath
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle, Wedge, Polygon

# ##############IMPORT IMAGES#############################
leap_prompt = mpimg.imread('images/leap_low.png')
one_hand = mpimg.imread('images/one_hand.png')
two_hands = mpimg.imread('images/two_hands.png')
img_left = mpimg.imread('images/arrow_left_low.png')
img_right = mpimg.imread('images/arrow_right_low.png')
smiley_star = mpimg.imread('images/smiley_star.png')
try_again = mpimg.imread('images/try_again.png')
img_asl0 = mpimg.imread('images/asl_0.png')
img_asl1 = mpimg.imread('images/asl_1.png')
img_asl2 = mpimg.imread('images/asl_2.png')
img_asl3 = mpimg.imread('images/asl_3.png')
img_asl4 = mpimg.imread('images/asl_4.png')
img_asl5 = mpimg.imread('images/asl_5.png')
img_asl6 = mpimg.imread('images/asl_6.png')
img_asl7 = mpimg.imread('images/asl_7.png')
img_asl8 = mpimg.imread('images/asl_8.png')
img_asl9 = mpimg.imread('images/asl_9.png')
ph_asl0 = mpimg.imread('images/photo_0.png')
ph_asl1 = mpimg.imread('images/photo_1.png')
ph_asl2 = mpimg.imread('images/photo_2.png')
ph_asl3 = mpimg.imread('images/photo_3.png')
ph_asl4 = mpimg.imread('images/photo_4.png')
ph_asl5 = mpimg.imread('images/photo_5.png')
ph_asl6 = mpimg.imread('images/photo_6.png')
ph_asl7 = mpimg.imread('images/photo_7.png')
ph_asl8 = mpimg.imread('images/photo_8.png')
ph_asl9 = mpimg.imread('images/photo_9.png')
login1 = mpimg.imread('images/login_1.png')
login5 = mpimg.imread('images/login_5.png')
login10 = mpimg.imread('images/login_10.png')

###############INITIALIZE VARIABLES#############################
controller = Leap.Controller()

handcolor = '#e80c0c'
center_timer = 0
correct_timer = 0


###############INITIALIZE SESSION#############################
clf = pickle.load(open('userData/classifier.p', 'rb'))
testData = np.zeros((1, 30), dtype='f')
database = pickle.load(open('userData/database.p', 'rb'))
userName = raw_input('Please enter your name: ')

if userName in database:
    welcomeMessage = "Welcome back, " + userName + "!"
    database[userName]['logins'] += 1
    print welcomeMessage
    print database[userName]

else:
    userType = raw_input('Are you a kid or adult?')
    welcomeMessage = "Welcome, " + userName + "!"
    database[userName] = {'userType': userType, 'logins': 1, 'lesson': 1, 'digitsComplete': 0, 'sessionAccuracy': 0,
                          '0attempted': 0, '1attempted': 0, '2attempted': 0, '3attempted': 0, '4attempted': 0,
                          '5attempted': 0, '6attempted': 0, '7attempted': 0, '8attempted': 0, '9attempted': 0,
                          '0correct': 0, '1correct': 0, '2correct': 0, '3correct': 0, '4correct': 0, '5correct': 0,
                          '6correct': 0, '7correct': 0, '8correct': 0, '9correct': 0}
    print welcomeMessage
    print database[userName]

###############INITIALIZE THE GUI#############################
matplotlib.interactive(True)
fig1 = plt.figure(figsize=(10, 6))
fig1.patch.set_facecolor('white')
header_view = plt.subplot2grid((6, 10), (0, 0), colspan=10, rowspan=2)

hand_view = plt.subplot2grid((6, 10), (2, 5), colspan=5, rowspan=8, projection='3d')
main_view = plt.subplot2grid((6, 10), (2, 0), colspan=5, rowspan=8)

header_view.get_xaxis().set_visible(False)
header_view.get_yaxis().set_visible(False)
main_view.get_xaxis().set_visible(False)
main_view.get_yaxis().set_visible(False)
# hand_view.set_axis_off() #this gets rid of grid too

hand_view.set_xlim(-200, 200)
hand_view.set_ylim(-200, 500)
hand_view.set_zlim(0, 200)
hand_view.view_init(azim=95)
for axis in hand_view.w_xaxis, hand_view.w_yaxis, hand_view.w_zaxis:
    for elt in axis.get_ticklines() + axis.get_ticklabels():
        elt.set_visible(False)

plt.draw()
print "drawing initial plot"
pause(.00001)

###############PROGRAM FUNCTIONS#############################
def CenterData(X):
    allXCoordinates = X[0, ::3]
    meanValue = allXCoordinates.mean()
    X[0, ::3] = allXCoordinates - meanValue
    allYCoordinates = X[0, 1::3]
    meanValue = allYCoordinates.mean()
    X[0, 1::3] = allYCoordinates - meanValue
    allZCoordinates = X[0, 2::3]
    meanValue = allZCoordinates.mean()
    X[0, 2::3] = allZCoordinates - meanValue
    return X


def handleBones(bone):
    boneBase = bone.prev_joint
    boneTip = bone.next_joint
    bones = {
        'plotx': [-(boneBase[0]), -(boneTip[0])],
        'ploty': [boneBase[1], boneTip[1]],
        'plotz': [-(boneBase[2]), -(boneTip[2])],
        'xTip': boneTip[0],
        'yTip': boneTip[1],
        'zTip': boneTip[2],
    }
    return bones


def plotHand(hand):
    k = 0
    for i in range(0, 5):
        finger = hand.fingers[i]
        bone = finger.bone(0)
        bones = handleBones(bone)
        lines.append(hand_view.plot(bones['plotx'], bones['ploty'], bones['plotz'], handcolor, linewidth=6))
        testData[0, k] = bones['xTip']
        testData[0, k + 1] = bones['yTip']
        testData[0, k + 2] = bones['zTip']
        k = k + 3
        for j in range(1, 4):
            bone = finger.bone(j)
            bones = handleBones(bone)
            lines.append(hand_view.plot(bones['plotx'], bones['ploty'], bones['plotz'], handcolor, linewidth=4))
            if ( (j == 0) | (j == 3) ):
                testData[0, k] = bones['xTip']
                testData[0, k + 1] = bones['yTip']
                testData[0, k + 2] = bones['zTip']
                k = k + 3
    return testData


def clear_hand_view(lines):
    while ( len(lines) > 0 ):
        ln = lines.pop()
        ln.pop(0).remove()
        del ln


def draw_view(lines):
    plt.draw()
    #print "drawing plot main loop"


def clear_view(lines):
    clear_hand_view(lines)
    header_view.cla()
    main_view.cla()


def saveUserData():
    pickle.dump(database, open('userData/database.p', 'wb'))


def checkLesson():
    lesson = database[userName]['lesson']
    header_view.text(.01, .76, "Level " + str(lesson), fontsize=30, fontweight='bold')
    return lesson


def checkHandPosition(hand):
    center_hand = hand.fingers[2].bone(0).next_joint[0]
    return center_hand


def welcomeView():
    header_view.text(.01, .76, welcomeMessage, fontsize=30, fontweight='bold')
    plt.draw
    print "drawing plot"
    if database[userName]['logins'] == 1:
        main_view.imshow(login1)
        plt.draw()
        print "drawing plot for welcome view"
        pause(2)
        header_view.text(.01, .52, "Use one hand to play.", fontsize=18, fontweight='bold')
        main_view.imshow(one_hand)
        plt.draw()
        print "drawing plot for welcome view"
        pause(3)
        header_view.text(.01, .32, "Use two hands to quit.", fontsize=18, fontweight='bold')
        main_view.imshow(two_hands)
        pause(3)
        main_view.cla()
        header_view.text(.01, .12, "Sign down toward the Leap Motion instead of forward.", fontsize=18,
                         fontweight='bold')
        main_view.imshow(ph_asl0)
        pause(6)
        main_view.cla()

    elif database[userName]['logins'] == 5:
        main_view.imshow(login5)
    elif database[userName]['logins'] == 10:
        main_view.imshow(login10)
    plt.draw()
    print "drawing plot for welcome view"
    pause(2)
    main_view.cla()
    header_view.cla()


def isReady(hand):
    global handcolor
    global center_timer
    global correct_timer
    hand_center = checkHandPosition(hand)
    #print hand_center
    if hand_center > 50:
        #main_view.imshow(img_left)
        center_timer = 0
        correct_timer = 0
        handcolor = '#e80c0c'
    elif hand_center < -50:
        #main_view.imshow(img_right)
        center_timer = 0
        correct_timer = 0
        handcolor = '#e80c0c'
    elif -50 < hand_center < 50 and handcolor is not '#B3B2B1':
        center_timer = center_timer + 1
        #print center_timer
    if center_timer == 4:
        handcolor = '#ff6f00'

    elif center_timer == 12:
        handcolor = '#ffaf1a'

    elif center_timer == 20:
        return True
    else:
        return False


def lesson1():
    num2sign = 0
    main_view.text(.08, .18, "Sign 0", fontsize=24, fontweight='bold')
    main_view.imshow(ph_asl0)


def getAssignment(lesson):
    global handcolor
    handcolor = '#309419'
    print "get digit to sign"
    if lesson == 1:
        lesson1()
    return num2sign


###############PROGRAM CLASSES#############################
class Assignment(object):
    def __init__(self, digit, timelimit, imgtype):

        self.digit = digit
        self.timelimit = timelimit
        self.isCorrectTimer = 0
        self.timer = 0
        self.assign_text = 'Sign ' + str(digit)
        self.image = eval('img_asl' + str(digit))
        self.incorrectImg = 'try_again'
        self.correctImg = 'smiley_star'
        self.imgType = imgtype

    def getImage(self):
        if self.imgType is 'photo':
            self.image = eval('ph_asl' + str(self.digit))
        return self.image

    def isCorrect(self, testData):

        self.timer = self.timer + 1

        CenterData(testData)
        predictedClass = clf.predict(testData)

        if self.digit is predictedClass:
            self.isCorrectTimer = self.isCorrectTimer + 1

        if self.isCorrectTimer is 20:
            return True

        if self.timer is self.timelimit:
            return False

        return 'running'


class Lesson(object):
    def __init__(self, config):
        self.hasAssignment = False

        self.digits = config['digits']

        self.presentation_mode = config['presentation_mode']

        self.level = config['level']

    def get_assignment(self):
        return Assignment(self.get_digit(), self.get_time_limit(), self.get_imgtype())

    def get_time_limit(self):
        return 100

    def get_imgtype(self):
        return 'photo'

    def getNextLesson(lesson):
        return lesson

    def isComplete(lesson):
        #how do we check it
        return False

    def get_digit(self):
        return 0


###############MAIN PROGRAM LOOP#############################
welcomeView()

while (True):
    print 'one loop'
    frame = controller.frame()
    #array to hold hand data
    lines = []

    level = checkLesson()

    try:
        current_lesson
    except NameError:
        config = {
            'digits': [0],
            'presentation_mode': 'img',
            'level': 1
        }
        current_lesson = Lesson(config)

    else:
        if current_lesson.level != level:
            current_lesson = Lesson()

    if len(frame.hands) < 1:
        main_view.imshow(leap_prompt)
        draw_view(lines)
        clear_view(lines)
    elif len(frame.hands) == 1:
        #print "1 hand"
        hand = frame.hands[0]
        testData = plotHand(hand)
        #when user is ready, give assign a digit to sign
        if isReady(hand):
            print "Ready to sign"
            #current_assignment = Assignment(5,100,'photo')

            if current_lesson.hasAssignment is False:
                current_assignment = current_lesson.get_assignment()
                current_lesson.hasAssignment = True

            if current_assignment.isCorrect(testData) is 'running':
                print "timer"
                print current_assignment.timer
                handcolor = "#309419"
                main_view.text(.08, .18, current_assignment.assign_text, fontsize=24, fontweight='bold')
                main_view.imshow(current_assignment.getImage())
            elif current_assignment.isCorrect(testData):
                current_lesson.hasAssignment = False
                main_view.text(.08, .18, 'Good job!', fontsize=24, fontweight='bold')
                main_view.imshow(smiley_star)
            else:
                current_lesson.hasAssignment = False
                main_view.text(.08, .18, 'Out of time.', fontsize=24, fontweight='bold')
                main_view.imshow(try_again)

            print current_assignment


        #testData = CenterData(testData)
        #predictedClass = clf.predict(testData)
        draw_view(lines)
        clear_view(lines)
        saveUserData()

    #quit the program when 2 hands are over the controller
    elif (len(frame.hands) == 2):
        #check which digit was assigned last -- (assign as first digit of next lesson?)
        saveUserData()
        print "goodbye"
        quit()
