#TA評分 8/10
'''架構完整，註解勉強尚可，然而程式仍有些許不正確，例如視角規格並非簡報裡所指定，---(line 67 附近已有指定unit為degree?)
反應時間應為 probe 階段的 2 秒內，超過 2 秒即不再收集反應按鍵。---(已修正)
建議 trials 數的變數應用更有彈性的寫法，例如使用 len 函數。---(是為了測試方便，line 163 已加註解)'''

from psychopy import visual,event,core,monitors,tools, gui
import numpy as np
import pandas as pd
import random
#-------some functions written for this mid-term project--------#

def en_pr(win, record, current_t_index, pORe):
#"record"---> A 9*40 array. See the function "add" in line 78.#"pORe"--->A string to assign to do encoding or probe. See line 37.
#In the client code, "record" is initiated in line 153.

    text_cross=visual.TextStim(win=win,pos=[0,0],color=[-1,-1,-1],text="+",units="norm")
    num_check=5# 5*5 squares
    check_size=[0.65,0.65]
    location=[0,0]
    loc=np.array(location)+np.array(check_size)//2
    xys=[]# positions of the 25 squares in the coordiate
    colors=np.zeros((num_check**2,3))
    all_co=[#the colors provoded by TA in the handout.
        [0,0,0],
        [1,0,0],
        [0,0,1],
        [0.93,0.009,0.93],
        [0,1,0],
        [1,1,0],
        [-1,-1,-1],
        [1,1,1],
        [0,0,0]
    ]
    loc1=[18,19,23,24]#the numbers of the 25 squares as shown in the handout.
    loc2=[15,16,20,21]
    loc3=[0,1,5,6]
    loc4=[3,4,8,9]
    loc_four=[loc1,loc2, loc3, loc4]#four quadrants

    r = current_t_index

    if(pORe == 'en'):
        loc_co= [record[0][r], record[1][r], record[2][r], record[3][r]]
    else:
        loc_co= [record[4][r], record[5][r], record[6][r], record[7][r]]

    #assign the 4 colors to the random locations in the 4 quadrants.
    for i in range(4):                
        colors[loc_four[i][record[9][r][i]]] = all_co[loc_co[i]]        
        i+=1

    low,high = num_check//-2, num_check//2#TA's code for adjust the center
    if abs(low)!=high:
        low+=1
        high+=1

    for y in range(low,high):#positions in the coordinate
        i=0
        for x in range(low,high):
            i+=1
            if i%2==0:
                y_delta=-check_size[0]/2
            else:
                y_delta=0
            xys.append(((check_size[0]+2)*x,(check_size[1]+2)*y+y_delta))

    stim=visual.ElementArrayStim(win,
                                xys=xys,
                                fieldPos=loc,
                                colors=colors,
                                nElements=num_check**2,
                                elementMask=None,
                                elementTex=None,
                                units="deg",
                                sizes=(check_size[0],
                                    check_size[1]))

    stim.size=(check_size[0]+10*num_check,
                check_size[1]*num_check+check_size[0]/2)
    stim.draw()
    text_cross.draw()
    win.flip()

def add(record, set_data, t_index, loc_random):#"loc_random"--->See line 165, the for loop randomly generate 'loc_r', the location in each quadrant, and 'trial_r', the index of the chosen trial in the stimulation file.
    record[0].append(set_data[('encoding_first')][t_index])
    record[1].append(set_data[('encoding_second')][t_index])
    record[2].append(set_data[('encoding_third')][t_index])
    record[3].append(set_data[('encoding_fourth')][t_index])
    record[4].append(set_data[('probe_first')][t_index])
    record[5].append(set_data[('probe_second')][t_index])
    record[6].append(set_data[('probe_third')][t_index])
    record[7].append(set_data[('probe_fourth')][t_index])
    record[8].append(set_data[('ans')][t_index])
    record[9].append(loc_random)

def save(subID, record, response_key, response_time, correct):
    output={
        'encoding_first':record[0],
        'encoding_second':record[1],
        'encoding_third':record[2],
        'encoding_fourth':record[3],
        'probe_first':record[4],
        'probe_second':record[5],
        'probe_third':record[6],
        'probe_fourth':record[7],
        'ans': record[8],
        'response_key':response_key,
        'response_time':response_time,
        'correct':correct
    }
    df=pd.DataFrame(output)
    df.to_csv(str(subID)+'.csv',index=False)


#---------client code-----------#

myDlg = gui.Dlg(title="Psychopy Dialog")
myDlg.addField('Subject: ')
myDlg.addField('Condition:', '(1 or 2)')#a input hint
ok_data = myDlg.show()  # show dialog and wait for OK or Cancel
if myDlg.OK:  # or if ok_data is not None
    subID = ok_data[0]
    cond = ok_data[1]
else:
    print('user cancelled')
    exit()

#(input in the console if the gui doesn't work)
# print("Psychopy Dialog")
# subID = input("Subject: ")
# cond = input("Condition(1 or 2): ")

set2_data = pd.read_csv('set2.csv')
set4_data = pd.read_csv('set4.csv')
#assign the stimulation data of each session accroding to the input
if(cond == '1'):
    data_s1 = set2_data
    data_s2 = set4_data
elif(cond == '2'):
    data_s1 = set4_data
    data_s2 = set2_data
else:
    #avoid wrong input, and provide error messages
    print('Condition(1 or 2): wrong input')
    exit()
data = [data_s1, data_s2]

mon=monitors.Monitor(name='myMac',width=37,distance=60)
mon.setSizePix((800,600))
win=visual.Window(size=[800,600],units='pix',monitor=mon)
clock_key=core.Clock()
text=visual.TextStim(win=win,pos=[0,0],color=[-1,-1,-1])
text_cross=visual.TextStim(win=win,pos=[0,0],color=[-1,-1,-1],text="+",units="norm")

rkey =[]
rt = []
crt = []
record = [[], [], [], [], [],
         [], [], [], [], []]
#record 4 encoding colors, 4 probe colors, 1 ans, 1 loc_r(random number for location in each quadrant)

blocks_num=2
trials_num_per_block=3 # 3 for test, there're 40 stim set in each csv file; try to use len(data_frame) for flexibility, eg: len(data_s1)
pre_duration=0.2
stimuli_duration_e=0.1
stimuli_interval=0.9
stimuli_duration_p=2.0
trial_interval=random.uniform(0.65,0.95)

for b in range(blocks_num):
    for t in range(trials_num_per_block):
        #random location in each quadrant
        loc_r = [random.randint(0,3), random.randint(0,3), 
        random.randint(0,3), random.randint(0,3)]
        #random trial index. From 0~39 in each stimulation file. 
        trial_r = random.randint(0,39)
        add(record, data[b], trial_r, loc_r)

text.text = 'Your task is to determine whether the two sets of colors are identical.\n\nOnce the second color set shows up, react as accurately and quickly as possible.\n\nPress any key to continue.' 
text.draw()
win.flip()
event.waitKeys()

text.text = 'Session 1\n\nPress the key \'M\' for identical sets, and the key \'C\' for different sets.\n\nPress any key to start.' 
text.draw()
win.flip()
event.waitKeys()

#Interesting story:
#   Here we initially used the while-loop structure in the gabor practice,
#   but found it would be quite a burden for some old laptops.
#   Therefore, we change it into core.wait() for the same purpose of duration control,
#   and it seemed to turn out better. 
#   Just a little curious about the pros and cons of the two arrangements respectively.
for b in range(blocks_num):
    for t in range(trials_num_per_block):
        current_t_index=trials_num_per_block*b+t
        text_cross.draw()
        win.flip()
        core.wait(pre_duration)

        en_pr(win, record, current_t_index, 'en')
        core.wait(stimuli_duration_e)

        text_cross.draw()
        win.flip()
        core.wait(stimuli_interval)

        current_key='HAHA'
        current_rt=5487
        current_crt=5555
        event.clearEvents()
        clock_key.reset()
        while clock_key.getTime()<stimuli_duration_p:
            en_pr(win, record, current_t_index, 'pr')
            key_info=event.getKeys(keyList=['m','c'],timeStamped=clock_key)
            if key_info:
                key_details=key_info[0]
                current_key=key_details[0]
                current_rt=key_details[1]
                break
        #check the correctness
        if(current_key == 'm'):
            if (record[8][current_t_index] == 1):
                current_crt = 1
            else:
                current_crt = 0
        elif(current_key == 'c'):
            if (record[8][current_t_index] == 0):
                current_crt = 1
            else:
                current_crt = 0

        rkey.append(current_key)
        rt.append(current_rt)
        crt.append(current_crt)
        win.flip()
        core.wait(trial_interval)

        if ((current_t_index+1)%trials_num_per_block==0)and((current_t_index+1)%(trials_num_per_block*blocks_num)!=0):
            text.text = 'Session 2\n\nPress the key \'M\' for identical sets, and the key \'C\' for different sets.\n\nPress any key to start.' 
            text.draw()
            win.flip()
            event.waitKeys()

text.text = 'The experiment is done,\nPlease notify the experimenter.\nPress any key to exit.'
text.draw()
win.flip()
event.waitKeys()

save(subID, record, rkey, rt, crt)

win.close()
core.quit()

#Ref:

#random.randint:
#https://docs.python.org/3/library/random.html

#wxpython
#https://www.wxpython.org/pages/downloads/

#psychopy.gui
#https://www.psychopy.org/api/gui.html
