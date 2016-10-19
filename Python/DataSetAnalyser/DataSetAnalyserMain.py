import pandas as pd
import numpy as np
import os 
import pickle


from scipy.stats import norm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import seaborn as sns

from DataSetEncoder import DataSetEncoder 



class Analyser:

    def __init__(self):
        print 'Class Initialized'        
        #More infor about the fields bellow on the correspondent methods
        
        #SetUpTrainTest method:
        self.predictor_name = None #Name of the predictor; Used also as a test to check if SetUpTrainTest has been called
        self.predictor_type = None
        self.id_field_name  = None
        self.all_features   = None
        self.cat_features   = None
        self.num_features   = None
        
        #Preprocess_MergeTrainTest method:
        self.train_ids        = None  #Ids of the train set.
        self.target           = None  #Predictor
        self.test_ids         = None  #Ids of the test set. 
        self.len_train_before = None  #To assert the len is the same before\after merge\split
        self.len_test_before  = None  #To assert the len is the same before\after merge\split
        
        
        #Preprocess_EncodeCategoricalFeatures
        self.encodings = None #Dictionary with the mappings applied on the encoding phase
    

        
    def readCSV(self, file_path):
        f = pd.read_csv(file_path)
        return f
        
           
    
    def getBasicInfo(self, df):
        columns = ['Property', 'Value']
                
        d = {}
        d['Number of rows'] = df.shape[0]
        d['Number of columns'] = df.shape[1]
        d['Used Memory (Mb)']  = int(df.memory_usage().sum() / (1024 * 1024)) 
        dfBasic = pd.DataFrame(d.items(), columns=columns)
         
        d2 = {}
        for i in df.dtypes.value_counts().iteritems():
            d2[i[0]] = i[1]
            
        dfColDataTypeCount = pd.DataFrame(d2.items(), columns=['Data Type', 'Number of Columns'])
        
        return dfBasic, dfColDataTypeCount


    def getBasicInfoByFeature(self, df):
        #all_features = [x for x in train.columns if x not in ['id','loss']]
        
        
        cols = ['FieldName', 'DataType', 'NonNACount','DistinctCount','IsUnique','MostComon','MostComonCount','MostComonPercentage'
        , 'Min', 'Max', 'Avg', 'Std']
        returndf = pd.DataFrame(columns=cols)
        
        for col in df.columns:
            data=df[col]
            
            d = {}
            
            d['FieldName'] = col 
            d['DataType'] = data.dtype
            d['NonNACount'] =  data.count() 
            d['DistinctCount'] = data.nunique(dropna=False) 
            d['IsUnique']  = d['DistinctCount'] == d['NonNACount'] 
            
            value_counts = data.value_counts()
            d['MostComon'] = value_counts.index[0]
            d['MostComonCount'] = value_counts.iloc[0]
            d['MostComonPercentage'] = np.round(d['MostComonCount'] / np.float(d['NonNACount']),4)
            
            
            if data.dtype in('int64','float64'):
                d['Min'] =  round(min(data),4)
                d['Max'] =  round(max(data),4)
                d['Avg'] =  round(np.mean(data),4)
                d['Std'] =  round(np.std(data),4)            
            
            
        
            returndf  = returndf.append(d, ignore_index=True)
        return returndf



    ##TO DO: check that predictor_type is either continuous or discrite
    def SetUpTrainTest(self, train, predictor_name, predictor_type, id_field_name='id'):        
        #Name and type of the field to be predicted:        
        self.predictor_name = predictor_name        
        self.predictor_type = predictor_type
        
        #Name of the unique identifyier on the dataset, not usefull for prediction
        self.id_field_name = id_field_name


        self.all_features = [x for x in train.columns if x not in [self.id_field_name, self.predictor_name]]
        self.cat_features = [x for x in train.select_dtypes(include=['object']).columns if x not in [self.id_field_name, self.predictor_name]]
        #dates?
        self.num_features = [x for x in train.select_dtypes(exclude=['object']).columns if x not in [self.id_field_name, self.predictor_name]]

            
        
    def AnalyseFeatures_PlotBasic(self, train, test=None, features_to_plot= None, normed = 0):

        if test is not None and self.predictor_name is None:
            raise TypeError("To compare to a test set, you need to execute the SetUpTrainTest method")
            return        
            
        #Are we comparing the train set with a test set?        
        if self.all_features is not None:
            all_features = self.all_features
            predictor = self.predictor_name # to avoid comparing with the test set where it doesnt exist
        else: 
            all_features = [x for x in train.columns]
            predictor = 'not important'
        
        
        #Are we requesting specific features?
        if features_to_plot is not None:
            if type(features_to_plot) is not list:
                raise TypeError("features_to_plot has to be a list")
                
            all_features = [x for x in all_features if x in features_to_plot]
        
        
        #remobe the loss because there is no loss on test
        #Loop and plot:
        for f in all_features:           
            
            plt.figure(figsize=(10,4))
            plt.suptitle("Feature: "+f, fontsize=16)            
           
           
            if train[f].dtype == 'object':
                train_counts = train[f].value_counts()
                
                if test is not None:            
                    test_counts = test[f].value_counts()
                    ylim = max(train_counts[0], test_counts [0])
                else:
                    ylim = train_counts[0]
                
                ylim += ylim *.1
            
                ax1 = plt.subplot(1, 2, 1) #1 row, 2columns, 1st plot
                ax1.set_ylim([0,ylim])
                train_counts.plot(kind='bar', title='Train', color='b')
                
                if test is not None and f!=predictor:
                    ax2 = plt.subplot(1, 2, 2)
                    ax2.set_ylim([0,ylim])
                    test_counts.plot(kind='bar', title='Test', color='green')
                    
                plt.show()   
            elif train[f].dtype in('int64','float64'):
                
                ax1 = plt.subplot(1, 2, 1) #1 row, 2columns, 1st plot
                values = train[f]
                
                
                n, bins, patches = plt.hist(values, 60, normed=normed, facecolor='blue', alpha=0.75)
                if normed == 1:
                    (mu, sigma) = norm.fit(values)
                    y = mlab.normpdf( bins, mu, sigma)
                    l = plt.plot(bins, y, 'r--', linewidth=2)
                    plt.ylabel('Probability')
                    plt.title(r'$\mathrm{Train:}\ \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
                else:
                    plt.ylabel('Count')    
                    plt.title('Train')
                
                plt.grid(True)
                

                if test is not None and f!=predictor:                   
                    ax2 = plt.subplot(1, 2, 2)
                    values = test[f]
                    
                    n, bins, patches = plt.hist(values, 60, normed=normed, facecolor='green', alpha=0.75)
                    if normed == 1:
                        (mu, sigma) = norm.fit(values)
                        y = mlab.normpdf( bins, mu, sigma)
                        l = plt.plot(bins, y, 'r--', linewidth=2)
                        plt.ylabel('Probability')
                        plt.title(r'$\mathrm{Test:}\ \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
                    else:
                        plt.ylabel('Count')
                        plt.title('Test')
                
                    plt.grid(True)
                
                    
                plt.show()        
            

         
    def _checkFeaturesToPlotIsList(self,features_to_plot):

        if self.predictor_name is None:
            raise TypeError("To use this method, you need to execute the SetUpTrainTest method")
            
        #Are we requesting specific features?
        if features_to_plot is not None:
            if type(features_to_plot) is not list:
                raise TypeError("features_to_plot has to be a list")
                
        return True
        


    def AnalyseFeatures_TrainBoxPLot(self, train, features_to_plot= None):
        
        if features_to_plot is not None and self._checkFeaturesToPlotIsList(features_to_plot):               
            num_features = [x for x in self.all_features if x in features_to_plot]
        else:
            num_features =  list(self.num_features)
            
        plt.figure(figsize=(13,9))
        sns.boxplot(train[num_features])
        
        
        

    def AnalyseFeatures_TrainHeatMap (self, train, features_to_plot= None):
        
        if features_to_plot is not None and self._checkFeaturesToPlotIsList(features_to_plot):               
            num_features = [x for x in self.all_features if x in features_to_plot]
        else:
            num_features =  list(self.num_features)  
        

        num_features.append('loss')
        
        
        correlationMatrix = train[num_features].corr().abs()
        plt.subplots(figsize=(13, 9))
        sns.heatmap(correlationMatrix,annot=True)
        
        # Mask unimportant features
        sns.heatmap(correlationMatrix, mask=correlationMatrix < 1, cbar=False)
        plt.show()



    
    def AnalysePredictor(self, train, predictor_transformation='none'):
        if self.predictor_name is None:
            raise TypeError("Execute the SetUpTrainTest method to use this feature")
            return
            
        #http://matplotlib.org/users/pyplot_tutorial.html
        if self.predictor_type == 'continuous':
            values = train[self.predictor_name]
            
            if predictor_transformation == 'log':
                values = np.log(values)
            else:
                predictor_transformation = 'none' #in case not supported transformation
            
            # fit the normal distribution on ln(loss)
            (mu, sigma) = norm.fit(values)
            
            # the histogram of the ln(loss)
            n, bins, patches = plt.hist(values, 60, normed=1, facecolor='green', alpha=0.75)
            
            # add the fitted line
            y = mlab.normpdf( bins, mu, sigma)
            l = plt.plot(bins, y, 'r--', linewidth=2)
            
            #plot
            plt.xlabel('Predictor: ' + self.predictor_name + ' - Transformation: ' +predictor_transformation)
            plt.ylabel('Probability')
            plt.title(r'$\mathrm{Histogram\ of\ Ln(Loss):}\ \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
            plt.grid(True)
            
            plt.show()
        else:
            print 'predictor_type not implemented'
            
        
    def Preprocess_UpdateValuesNotOnTest(self, train, test, new_value='NIT'):# Not In Test

        for c in self.cat_features:
            test_indexes = test[c].value_counts().index.values
            if len(train.loc[~train[c].isin(test_indexes)]) >0:
                train.loc[~train[c].isin(test_indexes), c] = 'NIT' 
                print 'Field:', c, len(train[train[c] == 'NIT']), 'updates'
        
        return train
        #debug        
        #import pandasql as pdsql
        #pysql = lambda q: pdsql.sqldf(q, globals())
        #df1 = pysql("select distinct TR.cat116  from train TR left join (select distinct cat116  as cat116 from test ) TE on TR.cat116 = TE.cat116 where TE.cat116 is null")
        
        #c = 'cat1'
        #test_indexes = test[c].value_counts().index.values
        #if len(train.loc[~train[c].isin(test_indexes)]) >0:
            #train.loc[~train[c].isin(test_indexes), c] = 'NIT' # Not In Test
            #print 'Field:', c, len(train[train[c] == 'NIT'])        



    def Preprocess_MergeTrainTest(self, train, test):

        if self.predictor_name is None:
            raise TypeError("Execute the SetUpTrainTest method to use this feature")
            return        

        self.train_ids = train[self.id_field_name]
        train = train.drop([self.id_field_name],axis=1)
        
        
        self.target = train[self.predictor_name]        
        test[self.predictor_name] = 0
        
        
        self.test_ids = test[self.id_field_name]
        test = test.drop([self.id_field_name],axis=1)
        
        
        
        self.len_train_before = len(train)
        self.len_test_before = len(test)
                
        #do not ignore index; MOst certenlly will end up with duplicated indexes but we need the original indexes
        #when joining self.test_ids back to the test set
        dfall = pd.concat((train, test), axis=0, ignore_index=False)
        return dfall
    
    
    #threshold between "One Hot" Encoding (dummies) and "regular" encoding.
    #The threshold is applied to the distinct count values of the column, so for example, if the threshold is 5, a column with 2
    #   unique values will be "One Hot" Encoded (so each value becomes another column with flag 1 for the real one and 0 for the other
    #   and a column with 10 unique values will get one integer value for each one of its unique values
    #Use a very high value to "One Hot" all columns and  0 to regular encode all columns
    def Preprocess_EncodeCategoricalFeatures(self, dfall, encoding_threshold=5, extra_encode=[]):
        
        new_names = []
        
        self.encodings={}
        encoder = DataSetEncoder()
        
        for col in dfall.columns:
            if ((dfall[col].dtypes == object or col in extra_encode)):
                if len(dfall[col].value_counts()) <= encoding_threshold:
                    print 'One Hot Encoding: ',col
                    new_name = 'is'+col
            
                    dfall_dummy = pd.get_dummies(dfall[col], prefix=new_name).astype(np.int8)
                    dfall = dfall.drop([col], axis=1)
                    dfall = pd.concat((dfall, dfall_dummy), axis=1)
                    new_names.extend(dfall_dummy.columns)
                else:
                    print 'Regular Encoding: ',col
                    dfall[col], self.encodings = encoder.encode(dfall[col].values,col,self.encodings)                
                    new_names.append(col)
            else:
                print 'Not touching: ',col
                new_names.append(col)
        
        #rearange the data frame to the original position:
        dfall = dfall[new_names]
        return dfall
                
        
    def Preprocess_SplitBackIntoTrainAndTest(self, dfall):

        if self.predictor_name is None:
            raise TypeError("Execute the SetUpTrainTest method to use this feature")
            return     
        
        train = dfall[:self.len_train_before]
        test = dfall[self.len_train_before:]
        
        test = test.drop([self.predictor_name],axis=1)
        
        #Check the Lenght is still the same
        assert(self.len_train_before == len(train))
        assert(self.len_test_before == len(test))
        
        return train, test
    


 

    def Utils_SaveObjects(self, save_path, train, test, da
                                   , save_file_train = 'train.pkl'
                                   , save_file_test = 'test.pkl'
                                   , DataSetAnalyserObj = 'daObject.pkl'):  
        

        pickle.dump(train, open(save_path + save_file_train, 'wb'))
        pickle.dump(test , open(save_path + save_file_test, 'wb'))
        pickle.dump(da , open(save_path + DataSetAnalyserObj, 'wb'))
        
  
      
    def Utils_LoadObjects(self, save_path, save_file_train = 'train.pkl'
                                   , save_file_test = 'test.pkl'
                                   , DataSetAnalyserObj = 'daObject.pkl'):    
                
        train_path = save_path+save_file_train
        print 'Loading training pickle from:',train_path
        train = pickle.load(open(train_path , 'rb'))
        
        test_path = save_path+save_file_test
        print 'Loading testing  pickle from:',test_path
        test  = pickle.load(open(test_path, 'rb'))
        
        da  = pickle.load(open(save_path+DataSetAnalyserObj, 'rb'))
        
        return train, test, da
        















