import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn import metrics
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score

#This function is desined to remove duplicate columns with the same name.
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
#This function converts each yes no into binary.
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

#This function recategorizes each reason fo why a customer left.
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


# This function creates percentages of a column provided.

def percentage_col(df,column,string=False, churn= False):
    """
    This function takes in a dataframe, column and returns the percentage of each row respective to its churn value.
    If the column's percentage is not based on its churned value it will just calculate the percent per column.
    If the column is based on its churn value it will calculate the percentage per churn value. This will also turn
    the column from binary to Yes or No.
    """
    if churn== True:
        values=[]
        for i in df.index:
            if df.churn_value[i]==1:

                summ=df[df.churn_value==1][column].sum()
                values.append(round((df[column][i] * 100)/summ,2))

            else:

                summ=df[df.churn_value==0][column].sum()
                values.append(round((df[column][i] * 100)/summ,2))
    else:
        values=[]
        for i in df.index:
            summ=df[column].sum()
            values.append(round((df[column][i] * 100)/summ,2))      

                
    if string== True:        
        for i in df.index:  
            if df.churn_value[i]==1:
                df.churn_value[i]= "Yes"
            else:
                df.churn_value[i]= "No"
    return values





#this function was created to visualize scores and create a dataframe with each score.
def scoring(preds ,model, xtrain,y_train,y_test,model_name: str,cv):
    from sklearn.model_selection import cross_val_score
    """
    The function statrts by returning the training scores of the model then, it takes in predictions of the
    model, model, model name, and times that model will be cross validated and returns the Accuracy, 
    Recall, F1 score and the CV Min, Max, Mean and Range scores based on accuracy.
    
    The function also creates a DF that saves all the infomation into a dataframe, making changes globaly. 
    """
    model.verbose=False
    def warn(*args, **kwargs):
        pass
    import warnings
    warnings.warn = warn
    
    if "scores_df" not in globals():
        global scores_df 
        scores_df = pd.DataFrame(columns=["Name","Accuracy","Recall","F1","CV Min","CV Max","CV Mean","CV Range"])
        
    if "scores_df" in globals():
        
        if "Grid"in(model_name).split():
            
            model.verbose=False
            print ("Training Accuracy: {}".format(metrics.accuracy_score(y_train, model.best_estimator_.predict(xtrain))))
            print ("Training Recall: {}".format(metrics.recall_score(y_train, model.best_estimator_.predict(xtrain))))
            print ("Training F1: {}".format(metrics.f1_score(y_train, model.best_estimator_.predict(xtrain))))

            vars()[model_name+"_recc"]=metrics.recall_score(y_test, preds)
            vars()[model_name+"_acc"]=metrics.accuracy_score(y_test, preds)
            vars()[model_name+"_f1"]=metrics.f1_score(y_test,preds)

            print("\n"+model_name+" Accuracy: {}".format(vars()[model_name+"_acc"]))
            print(model_name+" Recall: {}".format(vars()[model_name+"_recc"]))
            print(model_name+" F1: {}".format(vars()[model_name+"_f1"]))
            def warn(*args, **kwargs):
                pass
                
            import warnings
            warnings.warn = warn


            scores = cross_val_score(model.best_estimator_, xtrain, y_train, cv=cv)

            print("\nCross-Validation ({} times) Accuracy Scores:".format(cv))    
            print('Min: ', round(scores.min(), 6),'  Max: ', round(scores.max(), 6),'  Mean: ', round(scores.mean(), 6), '  Range: ', round(scores.max() - scores.min(), 6))

        else:
            
            model.verbose=False
            print ("Training Accuracy: {}".format(metrics.accuracy_score(y_train, model.predict(xtrain))))
            print ("Training Recall: {}".format(metrics.recall_score(y_train, model.predict(xtrain))))
            print ("Training F1: {}".format(metrics.f1_score(y_train, model.predict(xtrain))))

            vars()[model_name+"_recc"]=metrics.recall_score(y_test, preds)
            vars()[model_name+"_acc"]=metrics.accuracy_score(y_test, preds)
            vars()[model_name+"_f1"]=metrics.f1_score(y_test,preds)

            print("\n"+model_name+" Accuracy: {}".format(vars()[model_name+"_acc"]))
            print(model_name+" Recall: {}".format(vars()[model_name+"_recc"]))
            print(model_name+" F1: {}".format(vars()[model_name+"_f1"]))

            def warn(*args, **kwargs):
                pass
                
            import warnings
            warnings.warn = warn

            scores = cross_val_score(model,xtrain , y_train, cv=cv, verbose=False)

            print("\nCross-Validation ({} times) Accuracy Scores:".format(cv))    
            print('Min: ', round(scores.min(), 6),'  Max: ', round(scores.max(), 6),'  Mean: ', round(scores.mean(), 6), '  Range: ', round(scores.max() - scores.min(), 6))


        if model_name not in list(scores_df.Name):
            
            scores_df=scores_df.append({'Name':model_name, "Accuracy":vars()[model_name+"_acc"] , "Recall": vars()[model_name+"_recc"],"F1":vars()[model_name+"_f1"],"CV Min":scores.min() ,"CV Max":scores.max(),"CV Mean":scores.mean(), "CV Range": (scores.max() - scores.min())}, ignore_index=True)
    
        else:
            i=list(scores_df[scores_df.Name==model_name].index)
            scores_df.drop(scores_df.index[i], inplace=True) 
            scores_df=scores_df.append({'Name':model_name, "Accuracy":vars()[model_name+"_acc"] , "Recall": vars()[model_name+"_recc"],"F1":vars()[model_name+"_f1"],"CV Min":scores.min() ,"CV Max":scores.max(),"CV Mean":scores.mean(), "CV Range": (scores.max() - scores.min())}, ignore_index=True)



#Returns names of columns 
def names():
    names=['Senior Citizen',
 'Partner',
 'Dependents',
 'Tenure Months',
 'Phone Services',
 'Device Protection',
 'Tech Support',
 'Paperless Billing',
 'Monthly Charges',
 'CLTV',
 'Satisfaction Score',
 'Refer a Friend',
 'Num. of Referrals',
 'Tenure in Months',
 'AVG MON LD Charges',
 'AVG MON GB Download',
 'Device Protection Plan',
 'Premium Tech Support',
 'Music Streaming',
 'Unlimited Data',
 'Total Refunds',
 'Tot. Extra Data Charges',
 'Tot. LD Charges',
 'Total Revenue',
 'Age Under 30',
 'Num. of Dependents',
 'Internet Services',
 'Online Security',
 'Online Backup',
 'Multiple Tel. Lines',
 'TV Sreaming',
 'Total Charges Tel.',
 'Movie Streaming',
 'Cit Adelanto',
 'Cit Anaheim',
 'Cit Apple Valley',
 'Cit Bakersfield',
 'Cit Brea',
 'Cit Cerritos',
 'Cit Chula Vista',
 'Cit Concord',
 'Cit Crescent Mills',
 'Cit El Monte',
 'Cit Elk Grove',
 'Cit Fremont',
 'Cit Fresno',
 'Cit Glendale',
 'Cit Hayward',
 'Cit Huntington Beach',
 'Cit Inglewood',
 'Cit Irvine',
 'Cit Lakewood',
 'Cit Lancaster',
 'Cit Lompoc',
 'Cit Long Beach',
 'Cit Los Angeles',
 'Cit Modesto',
 'Cit Mountain View',
 'Cit Oakland',
 'Cit Pasadena',
 'Cit Riverside',
 'Cit Sacramento',
 'Cit San Bernardino',
 'Cit San Diego',
 'Cit San Dimas',
 'Cit San Francisco',
 'Cit San Jose',
 'Cit Santa Barbara',
 'Cit Santa Monica',
 'Cit Santa Rosa',
 'Cit Smith River',
 'Cit Stockton',
 'Cit Sun City',
 'Cit Temecula',
 'Cit Whittier',
 'Zip 90623',
 'Zip 91010',
 'Zip 91206',
 'zip 91762',
 'Zip 93245',
 'Zip 93702',
 'Zip 93711',
 'Zip 94027',
 'Zip 94520',
 'Latitude_33.8681',
 'Latitude_34.162515',
 'Latitude_36.739385',
 'Longitude_-121.55325',
 'Longitude_-120.653519',
 'Longitude_-119.82947',
 'Longitude_-118.24902',
 'Longitude_-118.203869',
 'Longitude_-117.815532',
 'Male',
 'Offer A',
 'Offer B',
 'Offer C',
 'Offer D',
 'Offer E',
 'DSL',
 'Fiber Optic',
 'No Internet Type',
 'Age 20',
 'Age 30',
 'Age 40',
 'Age 50',
 'Age 60',
 'Age 70',
 'Credit Card Payment',
 'Check in Mail Payment',
 'One Year Contract',
 'Two Year Contract']
    return names



