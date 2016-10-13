import pandas as pd
import numpy as np


from scipy.stats import norm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt



class Analyser:

    def __init__(self):
        print 'Class Initialized'
    
    
    ##TO DO: check that predictor_type is either continuous or discrite
    def SetUp(self, predictor_name, predictor_type, id_field_name='id'):        
        #Name and type of the field to be predicted:        
        self.predictor_name = predictor_name        
        self.predictor_type = predictor_type
        
        #Name of the unique identifyier on the dataset, not usefull for prediction
        self.id_field_name = id_field_name
        
        

        
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
        
        
        cols = ['FieldName', 'DataType', 'NonNACount','DistinctCount','IsUnique','MostComon','MostComonCount','MostComonPercentage' ]
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
        
            returndf  = returndf.append(d, ignore_index=True)
        return returndf







    def AnalyseDataSet(self, train):
        self.all_features = [x for x in train.columns if x not in [self.id_field_name, self.predictor_name]]
        self.cat_features = [x for x in train.select_dtypes(include=['object']).columns if x not in [self.id_field_name, self.predictor_name]]
        self.num_features = [x for x in train.select_dtypes(exclude=['object']).columns if x not in [self.id_field_name, self.predictor_name]]



    
    def AnalysePredictor(self, train, predictor_transformation='none'):
        
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
            print 'not implemented'
            
        
        
        

#from DataSetAnalyser.DataSetAnalyserMain import DataSetAnalyserMainClass
