import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from warnings import filterwarnings
import datetime as dt
filterwarnings('ignore')

__all__=["missing_percentage","missing_percentage","dropnull_col","dropnull_rows","drop_missing",
         "test_methods","impute_numeric"]

def missing_summary(dataset):
    """
    Print the missing summary 
    of dataset
    """
    summary = dataset.isnull().sum()
    return summary

def missing_percentage(dataset):
    """
    Print the missing summary 
    in percentage 
    """
    percentage=round(dataset.isnull().mean()*100,2)
    return percentage

def dropnull_col(dataset):
    """
    Drop column of dataset with 
    null percentage greater than 70%
    """
    dataset1=dataset.copy()
    drop=[]
    s=round(dataset1.isnull().mean()*100,2)
    lst=list(zip(dataset1.columns,s))
    for ele in lst:
        if ele[1]>70:
            drop.append(ele[0])
    dataset1.drop(drop,axis=1,inplace=True)
    return dataset1

def dropnull_rows(dataset):
    """
    Drop rows of dataset with null
    percentage lies between 0 and 2 
    """
    dataset1=dataset.copy()
    drop=[]
    s=round(dataset1.isnull().mean()*100,2)
    lst=list(zip(dataset1.columns,s))
    for ele in lst:
        if ele[1]>0 and ele[1]<=2:
            drop.append(ele[0])
    dataset1.dropna(subset=drop,inplace=True)
    dataset1.reset_index(drop=True)
    return dataset1


def drop_missing(df, axis=0, thresh=None):
    """
    drop rows/columns according to axis
    with given thresh
    
    :param df: Dataset
    :param axis:0=rows/1=columns
    :param thresh: thresh
    """
    return df.dropna(axis=axis, thresh=thresh)

def test_methods(*,dataset,column):
    """
    check different methods for
    null column with comparison 
    by kdeplot
    
    :param dataset: Dataset
    :param column: Column 
    """
    try:
        if type(dataset[column])!="str":        
            dataset1=dataset.copy()
            dataset1["Mean"]=dataset1[column]
            dataset1["Median"]=dataset1[column]
            dataset1["Bfill"]=dataset1[column]
            dataset1["Ffill"]=dataset1[column]
            dataset1["Mean"].fillna(value=dataset1[column].mean(),inplace=True)
            dataset1["Median"].fillna(value=dataset1[column].median(),inplace=True)
            dataset1["Bfill"].fillna(method="bfill",inplace=True)
            dataset1["Ffill"].fillna(method="ffill",inplace=True)
            sns.kdeplot(dataset1[column])
            columns=["Mean","Median","Bfill","Ffill"]
            for col in columns:
                sns.kdeplot(dataset1[column],color="b")
                sns.kdeplot(dataset1[col],color="g")
                plt.title(f"Comparison graph of {column} and {col}") 
                plt.show()
    except:
        raise Exception("Column type should be int or float")
    
def impute_numeric(dataset,*,col=dict):
    """
    Imputes numeric columns with defined method
    
    :param dataset: Dataset
    :param col: Column with method 
    e.g{"Column1":"Mean","Column2":"Median"}
    """
    dataset1=dataset.copy()
    try:
        for column,method in col.items():
            if method.lower()=="mean":
                dataset1[column].fillna(value=dataset1[column].mean(),inplace=True)
            elif method.lower()=="median":
                dataset1[column].fillna(value=dataset1[column].median(),inplace=True)
            elif method.lower()=="bfill" or method.lower()=="backfill":
                dataset1[column].fillna(method="bfill",inplace=True)
            elif method.lower()=="ffill":
                dataset1[column].fillna(method="ffill",inplace=True)
            else:
                raise Exception
    except:
        raise Exception ("No method found")
    return dataset1



