import re
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


def simiarity(segment1, segment2,total_feature,dlist):
    m = 0
    n = 0
    shared_features = []
    unshared_features_a = []
    unshared_features_b = []
    a = segsFeats.get(segment1)
    b = segsFeats.get(segment2)
    # print("There are "+str(len(a))+" features in a")
    for feature_a in a:
        for feature_b in b:
            if feature_a == feature_b:
                m+=1
                shared_features.append(feature_a)
            else:

                n+=1
    # print(len(shared_features))
    unshared_features_a = np.setdiff1d(a,shared_features)
    unshared_features_b = np.setdiff1d(b,shared_features)
    #pair each feature class with a weight
    # print("shared features include "+str(shared_features))
    # print("unshared features in first segment include "+ str(unshared_features_a))
    # print("unshared features in second segment include "+ str(unshared_features_b))
    # for unshared_f in unshared_features_a:
    
    similarity = m/total_feature 
    return similarity, unshared_features_a, unshared_features_b
                
                
if __name__ == '__main__':
    with open("lezgian.txt", 'r', encoding='utf-8') as featurefile:
        feat_file = featurefile.readlines()
        features = feat_file.pop(0).lstrip("\t").rstrip("\n").split("\t")
        segsFeats = segsFeats("lezgian.txt")  
    # print(len(features))
    # dlist = {'+cg': 0.4,
    #          '-cg': 0.3,
    #          '0cg': 0.2,
    #          '+sg': 0.2,
    #          '-sg': 0.1,
    #          '0sg': 0.2,
    #          }       
    dlist = {'+cg': 0.4,
             '-voice': 0.3,
             '+sg': 0.2,
             '+voice': 0.1
             }    
    # consoant = [p,t,k,q,ʔ,b,d,ɡ,t͡s,t͡ʃ,f,s,ʃ,x,χ,h,z,ʒ,ʁ,m,n,r,j,l,w,i,y,u,e,ӕ,a,pʰ,pʼ,tʼ,tʰ,tʰʷ,tʷʼ,tʷ,t͡sʰ,t͡sʼ,t͡sʰʷ,t͡sʷʼ,t͡sʷ,sʷ,zʷ,t͡ʃʼ,t͡ʃʰ,kʰ,kʼ,kʷ,kʷʼ,kʰʷ,ɡʷ,χʷ,qʼ,qʰ,qʷ,qʷʼ,qʰʷ,ʁʷ]
    consonant = list(segsFeats.keys())
    similarity_etc = {}
    
    df = pd.DataFrame(index=consonant, columns=consonant)
    df = df.fillna(0)
    for x in consonant:
        for y in consonant:
            m_tuple = simiarity(x,y,28,dlist)
            similarity_etc[y] = m_tuple[0]
        df.loc[x]= pd.Series(similarity_etc)
    print(df)
    df.to_csv(r'similarity-matrix.csv')

    
    # print(simiarity('p','p',28,dlist))
    # print(similarity_etc)
    # unshared_features_a=similarity_etc[1]
    # unshared_features_b=similarity_etc[2]
    
    # for f_a in unshared_features_a:
    #     for f_b in unshared_features_b:
    #         try:
    #             print(dlist[f_a]-dlist[f_b])    
    #         except:
    #             pass