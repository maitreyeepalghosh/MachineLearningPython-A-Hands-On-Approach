import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.metrics import confusion_matrix

filePath='D:\\Users\\703152439\\Desktop\\training data.csv'
def get_training_data(filePath):
    df = pd.read_csv(filePath)
    return df

training_df =get_training_data(filePath)
print training_df.head()
---------------------------------------

training_df.rename(columns={'Latitude (degree)':'Latitude','Longitude (degree)':'Longitude','Distance (km)':'Distance','Min Temp (°C)':'MinTemp','Max Temp (°C)':'MaxTemp','Wind (km/h)':'WindSpeed','Humidity (%)':'Humidity','Weather':'Weather','Target':'Target'},inplace=True)

training_df.columns


training_df.info()


training_df.describe()


values=training_df.values
values


#get the unique category of Weather

print training_df['Weather'].unique()

# get the count of each category of weather data

training_df['Weather'].value_counts()


#which city has max temperature
maxTempPlace = training_df.loc[((training_df['MaxTemp'].max() ),['CityName'])]


print maxTempPlace




#which all city has min humidity

minHumidPlace = training_df.loc[((training_df['Humidity'].min() ),['CityName'])]
print minHumidPlace


#How many citie's weather are sunny


sunnyPlaces_df = training_df.loc[((training_df['Weather'] =='Sunny')& (training_df['MinTemp'] < 15 ),['CityName','Weather'])]
print "List of nearby cool places::\n", sunnyPlaces_df.shape



%matplotlib inline
import pandas as pd
import numpy as np
import pylab as plt

#plot sunny and cloudy count

training_df['Weather'].value_counts().plot(kind='bar', 
                                         title='Sunny and Cloudy Counts')
										 
										 
										 
										 
										 
										 
coolPlaces_df =  training_df.loc[((training_df['MinTemp'] < 15 ) & (training_df['Distance'] < 500)) , ['CityName','Weather']]
print "List of nearby cool places::\n", coolPlaces



#find the weather in the nearby cool places 
coolPlaces['Weather'].value_counts().plot(kind='bar',                                       
                                         title='Sunny and Cloudy Counts')

coolPlaces['Weather'].value_counts()





import matplotlib.pyplot as plt

# Plot the data according to the Distance  


training_df["Distance"].plot(kind='bar',                                       
                                         title='Distance')
------------------------------------------------------------------


training_df["MaxTemp"].plot(kind='bar',title='MaxTemp')

--------------------------------------------
training_df["Humidity"].plot(kind='bar',title='Humidity')

----------------------------------------

from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
le = preprocessing.LabelEncoder()
var_mod = [u'CityName', u'Latitude', u'Longitude', u'Distance', u'MinTemp',
       u'MaxTemp', u'WindSpeed', u'Humidity', u'Weather']
le = LabelEncoder()
for i in var_mod:
    training_df[i] = le.fit_transform(training_df[i])
training_df.dtypes
training_df

---------------------------------------------


train,test=train_test_split(training_df,test_size=0.2)

------------------------------------------------

x_train=train[[u'CityName', u'Latitude', u'Longitude', u'Distance', u'MinTemp',
       u'MaxTemp', u'WindSpeed', u'Humidity', u'Weather']]
y_train=train[['Target']]
x_test=test[[u'CityName', u'Latitude', u'Longitude', u'Distance', u'MinTemp',
       u'MaxTemp', u'WindSpeed', u'Humidity', u'Weather']]
y_test=test['Target']  

-------------------------------------
len(x_train)
x_train
-----------------------
len(x_test)
x_test
----------------
len(y_train)
y_train
-----------------
len(y_test)
y_test
------------------
model=LogisticRegression(penalty='l2',C=1)
model.fit(x_test,y_test)
-------------------
predicted = model.predict(x_test)
--------------------

accuracy= (y_test == predicted).sum()/float(len(y_test))
print "Accuarcy::  ",accuracy

------------------
confusion_matrix(y_test,predicted)
---------------
dtModel = DecisionTreeClassifier(min_samples_split=20, random_state=99)
dtModel.fit(x_test,y_test)
predicted = dtModel.predict(x_test)
accuracy= (y_test == predicted).sum()/float(len(y_test))
print "Accuracy: ",accuracy
confusion_matrix(y_test,predicted)

--------------------------
