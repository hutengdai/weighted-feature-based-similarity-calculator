import re
import sys
import numpy as np
import pandas as pd
import pprint
pp = pprint.PrettyPrinter(indent=4)
pprint.sorted = lambda x, key=None: x


def segsFeats(featfilepath):
    '''
    input argument: path to feats.txt.
    output 1: segsFeats, a dictionary of segs along with all the feat values (+cont, 0str, etc.)
    output 2: segsnozero, a dictionary of segs with only the non-zero feat values (+cont but not 0str)
    output 3: feats, a list of feat names

    the feats.txt file needs to be in the standard 2009 UCLAPL GUI format, i.e., tab separated, no 'word_boundary' seg defined in the list of segs, and the first line starts with an empty tab and then feat names.
    '''
    with open(featfilepath, 'r', encoding='utf-8') as featfile:
        feat_file = featfile.readlines()
    feats = feat_file.pop(0).lstrip("\t").rstrip("\n").split("\t")

    segsFeats = {}
    for line in feat_file:
        line = line.rstrip("\n").split("\t")
        seg = line[0]
        segsFeats[seg] = []
        for feat in feats:
            i = feats.index(feat)
            segsFeats[seg].append(str(line[i+1])+str(feat))
            # tuple(segsFeats[seg])
    segsFeatsnozero = {}
    for line in feat_file:
        line = line.rstrip("\n").split("\t")
        seg = line[0]
        segsFeatsnozero[seg] = []
        for feat in feats:
            i = feats.index(feat)
            if line[i+1] != '0':
                segsFeatsnozero[seg].append(str(line[i+1])+str(feat))
    if 'wb' not in feats:
        feats.append('word_boundary')
    return(segsFeats)

def sumW(unshared_final):
    sumW = 0
    for unsharedfeat in unshared_final:
        try:
            sumW += dlist[unsharedfeat]
        except KeyError:
            sumW += 0
    return sumW

def distance(seg1, seg2, dlist):
    '''
    Phonetic distance is the summed Ws of non-shared feats
    '''
    m = 0
    n = 0
    shared_feats = []

    for feat_a in seg1:
        for feat_b in seg2:
            if feat_a == feat_b:
                m+=1
                shared_feats.append(feat_a)
            else:
                n+=1

    unshared_feat_value_a = np.setdiff1d(seg1,shared_feats).tolist()
    unshared_feat_value_b = np.setdiff1d(seg2,shared_feats).tolist()

    unshared_raw = []
    unshared_final = []

    for feat_value_a in unshared_feat_value_a:
        for feat_value_b in unshared_feat_value_b:
            unshared_raw.append(feat_value_a[1:])
            unshared_raw.append(feat_value_b[1:])
            # unshared_raw repeats all unshared feats again and again :(
            # unshared_final singles out unshared feats to a list :)
            for x in unshared_raw:
                if x not in unshared_final:
                    unshared_final.append(x)

    # print(unshared_final)
    distance = sumW(unshared_final)
    return distance

def similarity(seg1, seg2, dlist, filepath):
    with open(filepath, 'r', encoding='utf-8') as featfile:
        feat_file = featfile.readlines()
        feats = feat_file.pop(0).lstrip("\t").rstrip("\n").split("\t")
        segs2Feats = segsFeats(filepath)  
    seg1 = segs2Feats.get(seg1)
    seg2 = segs2Feats.get(seg2)

    d = distance(seg1, seg2, dlist) 
    similarity = 1 - d/sumW(feats)
 
    return similarity

def writedataframe(dlist, filepath):
    sim_etc = {}
    segs2Feats = segsFeats(filepath)  
    inventory = list(segs2Feats.keys())
    df = pd.DataFrame(index=inventory, columns=inventory)
    df = df.fillna(0)

    for x in inventory:
        for y in inventory:
            sim_etc[y] = round(similarity(x, y, dlist, filepath),2)
        
        df.loc[x]= pd.Series(sim_etc)
        df.to_csv(r'similarity-matrix.csv')
    pp.pprint(df)
    return df                

                
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + " [-v] yourfeatfile.txt")
        quit()  

    verbose = False
    i = 1
    if sys.argv[1] == '-v':
        verbose = True
        i += 1
            
    filepath = sys.argv[i]


    dlist = {'cg' : 0.2, 
            'voice' : 0.4,
            'sg' : 0.4,
            'sonorant' : 1,
            "consonant" : 1,
            "nasal": 1,
            "coronal": 0.1,
            "labial": 0.1,
            "labiodental": 0.1,
            "dorsal": 0.1
             }    
    pp.pprint(writedataframe(dlist, filepath))


    # consoant = [p,t,k,q,ʔ,b,d,ɡ,t͡s,t͡ʃ,f,s,ʃ,x,χ,h,z,ʒ,ʁ,m,n,r,j,l,w,i,y,u,e,ӕ,a,pʰ,pʼ,tʼ,tʰ,tʰʷ,tʷʼ,tʷ,t͡sʰ,t͡sʼ,t͡sʰʷ,t͡sʷʼ,t͡sʷ,sʷ,zʷ,t͡ʃʼ,t͡ʃʰ,kʰ,kʼ,kʷ,kʷʼ,kʰʷ,ɡʷ,χʷ,qʼ,qʰ,qʷ,qʷʼ,qʰʷ,ʁʷ]
    # c:/Users/huten/Desktop/Writing/Lezgian-GSC/modified-phoneme-distance-calculator/lezgian.txt

    # df = writedataframe(consonant,28,dlist)
    # print(df)
    # print(distance('p',"pʼ", dlist)) #0.1
    # print(distance('p',"b", dlist)) #0.2
    # print(distance('p',"pʰ", dlist)) #0.3
    # print(distance('qʼ',"t͡sʼ", dlist)) 
    # print(similarity('tʰʷ',"ʁ", dlist, filepath)) 

    
    # print(distance('q',"t͡sʼ", dlist)) 
    # print(similarity('q',"t͡sʼ", dlist, filepath)) 

    # print(distance('q',"t͡sʰ", dlist)) 
    # print(similarity('q',"t͡sʰ", dlist, filepath))

    # print(distance('q',"t͡s", dlist))
 

    # print(distance('q',"z", dlist)) 
    # print(distance("t͡s","ɡ", dlist)) #0.3
    # print(distance("t͡s","k", dlist)) #0.3
    # print(distance("t͡s","kʼ", dlist)) #0.3
    # print(distance("k","m", dlist)) #0.3

