import pandas as pd
import numpy as np


from scipy.stats import norm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt



class Analyser:

    def __init__(self):
        print 'Class Initialized'
        
        #More infor about tese fields on the SetUpTrainTest method
        self.predictor_name = None
        self.predictor_type = None
        self.id_field_name = None
        self.all_features = None
        self.cat_features = None
        self.num_features = None
        
    
        
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



    def AnalyseFeatures_plot(self, train, test=None, features_to_plot= None, normed = 0):
        #Are we comparing the train set with a test set?        
        if self.all_features is not None:
            all_features = self.all_features
        else: 
            all_features = [x for x in train.columns]
        
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
                
                if test is not None:         
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
                    plt.title('aaa')
                
                plt.grid(True)
                

                   
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
                    plt.title('aaa')
                
                plt.grid(True)
                
                    
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
            
        
        
        

#from DataSetAnalyser.DataSetAnalyserMain import DataSetAnalyserMainClass
