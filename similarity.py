import re
import sys
import numpy as np
import pandas as pd

def segsFeats(featfilepath):
    '''
    input argument: path to Features.txt.
    output 1: segsFeats, a dictionary of segments along with all the feature values (+cont, 0str, etc.)
    output 2: segsnozero, a dictionary of segments with only the non-zero feature values (+cont but not 0str)
    output 3: features, a list of feature names

    the Features.txt file needs to be in the standard 2009 UCLAPL GUI format, i.e., tab separated, no 'word_boundary' segment defined in the list of segments, and the first line starts with an empty tab and then feature names.
    '''
    with open(featfilepath, 'r', encoding='utf-8') as featurefile:
        feat_file = featurefile.readlines()
    features = feat_file.pop(0).lstrip("\t").rstrip("\n").split("\t")

    segsFeats = {}
    for line in feat_file:
        line = line.rstrip("\n").split("\t")
        seg = line[0]
        segsFeats[seg] = []
        for feature in features:
            i = features.index(feature)
            segsFeats[seg].append(str(line[i+1])+str(feature))
            # tuple(segsFeats[seg])
    segsFeatsnozero = {}
    for line in feat_file:
        line = line.rstrip("\n").split("\t")
        seg = line[0]
        segsFeatsnozero[seg] = []
        for feature in features:
            i = features.index(feature)
            if line[i+1] != '0':
                segsFeatsnozero[seg].append(str(line[i+1])+str(feature))
    if 'wb' not in features:
        features.append('word_boundary')
    return(segsFeats)


def wlist2feature(word, segsFeats):
    '''
        input argument: each line in a wlist and features (segsFeats)
    output: res, a list of the lists of feature bundles;
    '''

    res = []
    for segment in word:
        a = [segsFeats.get(segment)]
        for val in a:
            if val != None:
                res.append(val)
            else:
                pass
    return res


def simiarity(segment1, segment2,dlist):
    m = 0
    n = 0
    shared_features = []
    a = segsFeats.get(segment1)
    b = segsFeats.get(segment2)
    # print("There are "+str(len(b))+" features in b")
    for feature_a in a:
        for feature_b in b:
            if feature_a == feature_b:
                m+=1
                shared_features.append(feature_a)
            else:
                n+=1

    unshared_feature_value_a = np.setdiff1d(a,shared_features).tolist()
    unshared_feature_value_b = np.setdiff1d(b,shared_features).tolist()

    unshared_features_raw = []
    unshared_features_final = []

    for feature_value_a in unshared_feature_value_a:
        for feature_value_b in unshared_feature_value_b:
            unshared_features_raw.append(feature_value_a[1:])
            unshared_features_raw.append(feature_value_b[1:])
            # unshared_features_raw repeats all unshared features again and again :(
            # unshared_features_final singles out unshared features to a list :)
            for x in unshared_features_raw:
                if x not in unshared_features_final:
                    unshared_features_final.append(x)

    def weight(unshared_features_final):
        weight = 0
        for unsharedFeature in unshared_features_final:
            try:
                weight += dlist[unsharedFeature]
            except:
                weight += 0.1
        return weight


    # similarity = m/total_feature - activation(unshared_features_final)
    
    similarity = weight(unshared_features_final)
    return similarity

def writedataframe(consonant,total_feature,dlist):
    similarity_etc = {}
    df = pd.DataFrame(index=consonant, columns=consonant)
    df = df.fillna(0)
    for x in consonant:
        for y in consonant:
            similarity_etc[y] = simiarity(x,y,total_feature,dlist)
        df.loc[x]= pd.Series(similarity_etc)
        df.to_csv(r'similarity-matrix.csv')
    return df                
                
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + " [-v] yourfeaturefile.txt")
        quit()  

    verbose = False
    i = 1
    if sys.argv[1] == '-v':
        verbose = True
        i += 1
            
    filepath = sys.argv[i]

    # with open("Features.txt", 'r', encoding='utf-8') as featurefile:
    with open(filepath, 'r', encoding='utf-8') as featurefile:
        feat_file = featurefile.readlines()
        features = feat_file.pop(0).lstrip("\t").rstrip("\n").split("\t")
        segsFeats = segsFeats(filepath)  

    dlist = {'cg' : 0.1, 
            'voice' : 0.2,
            'sg' : 0.3,
             }    
    # consoant = [p,t,k,q,ʔ,b,d,ɡ,t͡s,t͡ʃ,f,s,ʃ,x,χ,h,z,ʒ,ʁ,m,n,r,j,l,w,i,y,u,e,ӕ,a,pʰ,pʼ,tʼ,tʰ,tʰʷ,tʷʼ,tʷ,t͡sʰ,t͡sʼ,t͡sʰʷ,t͡sʷʼ,t͡sʷ,sʷ,zʷ,t͡ʃʼ,t͡ʃʰ,kʰ,kʼ,kʷ,kʷʼ,kʰʷ,ɡʷ,χʷ,qʼ,qʰ,qʷ,qʷʼ,qʰʷ,ʁʷ]
    consonant = list(segsFeats.keys())

    # df = writedataframe(consonant,28,dlist)
    # print(df)
    # print(simiarity('p',"pʼ", dlist)) #0.1
    # print(simiarity('p',"b", dlist)) #0.2
    # print(simiarity('p',"pʰ", dlist)) #0.3
    print(simiarity('qʼ',"t͡sʼ", dlist)) 
    print(simiarity('q',"t͡sʼ", dlist)) 
    print(simiarity('q',"t͡sʰ", dlist)) 
    print(simiarity('q',"t͡s", dlist)) 

    # print(simiarity('q',"z", dlist)) 
    # print(simiarity("t͡s","ɡ", dlist)) #0.3
    # print(simiarity("t͡s","k", dlist)) #0.3
    # print(simiarity("t͡s","kʼ", dlist)) #0.3
    # print(simiarity("k","m", dlist)) #0.3




    # print(similarity_etc)

    
    # for f_a in unshared_features_a:
    #     for f_b in unshared_features_b:
    #         try:
    #             print(dlist[f_a]-dlist[f_b])    
    #         except:
    #             pass
    #   When there is a three-way laryngeal contrasts on [voice], 
    #   [cg], [sg], the contrasts between positive and negative values of these features are different.  