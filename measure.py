import pandas as pd

# Precision, Recall, and F1-measure for an annotated and enriched dataset.
# Requires columns of annotation and result in a dataframe for comparison
def tptnfpfn(df):
    total = 0
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    types = []
    for idx,row in df.iterrows():
        total += 1
        annotation = row["annotation"]
        result = row["result"]
        if   len(annotation) and len(result) and annotation == result:
            #Classification found and matches annotation (correct), True Positive
            types.append('tp')
            tp += 1
        elif len(annotation) and len(result) and annotation != result:
            #Classification found but does not match annotation (incorrect), False Positive
            types.append('fp')
            fp += 1
        elif len(annotation) and not len(result):
            #Classification missing and there should be one (incorrect), False Negative
            types.append('fn')
            fn += 1
        elif not len(annotation) and len(result):
            #Classification found but there should not be one (incorrect), False Positive
            types.append('fp')
            fp += 1
        elif not len(annotation) and not len(result):
            #Classification missing and there should not be one (correct), True Negative
            types.append('tn')
            tn += 1
    df['type'] = types
    return total,tp,tn,fp,fn,df

def precision(df):
    total,tp,tn,fp,fn,df = tptnfpfn(df)
    P = tp / (tp + fp)
    return P,df

def recall(df):
    total,tp,tn,fp,fn,df = tptnfpfn(df)
    R = tp / (tp + fn)
    return R,df

def f1(df):
    total,tp,tn,fp,fn,df = tptnfpfn(df)
    P = tp / (tp + fp)
    R = tp / (tp + fn)
    F = 2 * ((P * R) / (P + R))
    return F,P,R,df