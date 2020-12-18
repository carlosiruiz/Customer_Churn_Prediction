import pandas as pd
import numpy as np

def remove_dups(lists, df):
    """
    list: list of duplicate columns to delete.
    
    Takes in a list of duplicated columns with the same name and removes the duplicated column and creates a
    new column with a new name and values assigned.
    Once that is complete it drops column from dataframe.
    """
    for i in range(len(lists)):
        df["tel_"+lists[i]]=df[lists[i]].iloc[:,1:2]
        df.drop(lists[i],axis=1,inplace=True)

def to_binary(column, df):
    """
    Takes in a column and turns its value from a Yes or No to a binary. 
    """
    conditions=[
        (df[column].str.lower()=='yes'),            
        (df[column].str.lower()=='no'),
    ]
    choises=[
        1,
        0,

    ]
    df[column]=np.select(conditions,choises,default=0)


def reason_cleanup(column, df):
    """
    Takes in the tel_churn_reason column and creates its own main categories as to why a customer churned. 
    
    """    
    
    reasons={
        "Competition Offers":["Competitor had better devices","Competitor made better offer","Competitor offered more data","Competitor offered higher download speeds"],
        "Customer Satisfaction":["Attitude of support person","Attitude of service provider","Poor expertise of online support","Poor expertise of phone support"],
        "Pricing":["Price too high","Lack of affordable download/upload speed"],
        "Charges and Fees":["Long distance charges","Extra data charges"],
        "Product and Services":["Product dissatisfaction","Network reliability","Service dissatisfaction","Limited range of services","Lack of self-service on Website"],
        "External Factors":["Moved","Deceased"],
        "Unkown":["Don't know"],
        "Did Not Churn":["No reason given"]
    }
    reason=[]
    for i in df[column].index:
        for key in reasons.keys():
            if df[column][i]in reasons[key]:
                reason.append(key)
    return reason
