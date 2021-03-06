import pandas as pd
import numpy as np
import os 
import pickle
import unicodedata

from scipy.stats import norm
from scipy import stats
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import seaborn as sns

#from DataSetEncoder import DataSetEncoder 

import operator

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
        self.merge_splittype  = None  #how ids dfall split back into train and test
        
        
        #Preprocess_EncodeCategoricalFeatures
        self.encodings = None #Dictionary with the mappings applied on the encoding phase
        
        #Preprocess_TransformNumericFeaturesr
        self.lmbdaDict = None #Dictionary with the lambdas applied on numerica box cox encoding
        
        #Preprocess_TransformPredictor
        self.predictor_shift = None # Shift correction to be applied to the prediction prior to the transformation
        
        self.one_hot_numeric_rounding = 2 #In case we want to deal with numeric variables as categories and encode them; This is the rounding factor

        
    def loadData(self, file_path, nrows=None):
        if file_path.endswith('.csv'):
            f = pd.read_csv(file_path,nrows=nrows)
        elif file_path.endswith('.json'):
            f = pd.read_json(open(file_path))
        else:
            raise Exception('File Extension not supported')
        return f
 
    
#specify columns and data types:       
# train = pd.read_csv(train_file,
#                    usecols=["date_time", "srch_ci", "srch_co", "site_name", "user_id", "is_booking", "user_location_country", 
#                             "user_location_region", "user_location_city", "hotel_market", "hotel_country", "orig_destination_distance", 
#                             "srch_destination_id", "srch_adults_cnt", "srch_children_cnt", "srch_rm_cnt", "srch_destination_type_id", "hotel_cluster"],
#                    dtype={'date_time':np.str_, "srch_ci":np.str_, "srch_co":np.str_, 'site_name':np.int8, 'user_id':np.int32, "is_booking":np.float64,  'user_location_country':np.int16
#                            ,'user_location_region':np.int16 , 'user_location_city':np.int32, "hotel_market":np.int32, "hotel_country":np.int32, "orig_destination_distance":np.float64, 
#					"srch_adults_cnt":np.int8, "srch_children_cnt":np.int8, "srch_rm_cnt":np.int8, "srch_destination_type_id":np.int8, 
#                             "hotel_cluster":np.int32
#                           }
#                     )

         
    
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
        
        
        cols = ['FieldName', 'DataType', 'NonNACount','DistinctCount','IsUnique','MostComon','MostComonCount','MostComonPc'
        , 'Min', 'Max', 'Avg', 'Std', 'Skewness']
        returndf = pd.DataFrame(columns=cols)
        
        for col in df.columns:
            data=df[col]
            
            d = {}
            
            d['FieldName'] = col 
            d['DataType'] = data.dtype
            d['NonNACount'] =  data.count()
            try:
                d['DistinctCount'] = data.nunique(dropna=False) 
                d['IsUnique']  = d['DistinctCount'] == d['NonNACount'] 
                
                value_counts = data.value_counts()
                d['MostComon'] = value_counts.index[0]
                d['MostComonCount'] = value_counts.iloc[0]
                d['MostComonPc'] = np.round(d['MostComonCount'] / np.float(d['NonNACount']),4)
            except:
                #in case we have TypeError: unhashable type: 'list'
                pass            
            
            if data.dtype in('int64','float64'):
                d['Min']      =  round(min(data),4)
                d['Max']      =  round(max(data),4)
                d['Avg']      =  round(np.mean(data),4)
                d['Std']      =  round(np.std(data),4)
                d['Skewness'] =  round(stats.skew(data),4)    
                
            
            
        
            returndf  = returndf.append(d, ignore_index=True)
        return returndf



    ##TO DO: check that predictor_type is either continuous or discrete
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
            
    #add features to plot in case is a new feature?
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
            elif train[f].dtype in('int32', 'int64', 'float32', 'float64'):
                
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
            #num_features = [x for x in self.all_features if x in features_to_plot]
            num_features = features_to_plot
        else:
            num_features =  list(self.num_features)  
        
        
        correlationMatrix = train[num_features].corr().abs()
        plt.subplots(figsize=(13, 9))
        sns.heatmap(correlationMatrix,annot=True)
        
        # Mask unimportant features
        sns.heatmap(correlationMatrix, mask=correlationMatrix < 1, cbar=False)
        plt.show()
        return correlationMatrix



    
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
            
    
    #Reports number of distinct counts across numericfeatures; rounding from
    #upper to lower decimal places
    def AnalyseNumericFeaturesRoundingCounts(self, dfall, upper=7, lower=-1):
        d ={}
        for i in range (upper, lower, -1):
            l = []
            for col in self.num_features:
                l.append (len(dfall[col].apply(lambda x:round(x,i)).value_counts()))
            d[i] = l
            
        df = pd.DataFrame(d, index=self.num_features)
        return df

            
    
    #On the train set, set values that dont exist on the test set to NIT - Not In Test
    def Preprocess_UpdateValuesNotOnTest(self, train, test, new_value='NIT'):

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

    
    #Set to Nan the categories that exist on train but not on test and vice versa;
    #On another words, to be non-nan, the cat needs to exist in both train and test sets    
    #It takes the dfall and both train and test as parameters; The last two are used to verify whether or not values
    #exist and dfall is where the updates will be applied
    def Preprocess_NanValuesNotOnBothDatasets(self, dfall, train, test):

        if self.cat_features is None:
            raise TypeError("Execute the SetUpTrainTest method to use this feature")
            return        
        
        for column in self.cat_features:
            if train[column].nunique() != test[column].nunique():
                set_train = set(train[column].unique())
                set_test = set(test[column].unique())
                remove_train = set_train - set_test
                remove_test = set_test - set_train
        
                remove = remove_train.union(remove_test)
                def filter_cat(x):
                    if x in remove:
                        return np.nan
                    return x
        
                dfall[column] = dfall[column].apply(lambda x: filter_cat(x), 1)
                print column, '->', len(dfall[column][pd.isnull(dfall[column])]),'occurences on these cats:' ,', '.join(remove)
                    
        return dfall
        
    #this works when train has a continuous set if IDs like 0 to 10 and then test has a continuous set of ids, 11 to 25 for example
    def Preprocess_MergeTrainTest(self, train, test, merge_splittype):        

        if self.predictor_name is None:
            raise TypeError("Execute the SetUpTrainTest method to use this feature")
            return
    
        if merge_splittype not in ('continuous', 'byindex'):
            raise Exception('Merge split type must be continuous or byindex')
        
        self.merge_splittype = merge_splittype
        
        self.train_ids = train[self.id_field_name]
        self.test_ids = test[self.id_field_name]
        self.target = train[self.predictor_name]        
        test[self.predictor_name] = '?' if self.predictor_type =='categorical' else 0
        
        if merge_splittype ==  'continuous':
            dfall = pd.concat((train, test)).reset_index(drop=True)
        elif merge_splittype ==  'byindex':
            dfall = pd.concat((train, test))
                
        self.len_train_before = len(train)
        self.len_test_before = len(test)
                

        #train = train.drop([self.id_field_name],axis=1)#deprecated    
        #test = test.drop([self.id_field_name],axis=1) deprecated                
        #do not ignore index; Most certenlly will end up with duplicated indexes but we need the original indexes when joining self.test_ids back to the test set
        #dfall = pd.concat((train, test), axis=0, ignore_index=False) # deprecated
                
        return dfall
        

    
    #threshold between "One Hot" Encoding (dummies) and "regular" encoding.
    #The threshold is applied to the distinct count values of the column, so for example, if the threshold is 5, a column with 2
    #   unique values will be "One Hot" Encoded (so each value becomes another column with flag 1 for the real one and 0 for the other
    #   and a column with 10 unique values will get one integer value for each one of its unique values
    #Use a very high value to "One Hot" all columns and  0 to regular encode all columns
    def Preprocess_EncodeCategoricalFeatures(self, dfall, encoding_threshold=5, extra_encode=[]):

        #to remeber the order
        ID = self.id_field_name
        dfall[ID]=pd.Categorical(dfall[ID], dfall[ID].values.tolist())
        
        new_names = []        
        self.encodings={}
        
        #dfall['cat1'].dtypes
        #encoder = DataSetEncoder() deprecated
        
        for col in dfall.columns:
            if ((dfall[col].dtypes == object or col in extra_encode)):

                #if we are passing anythin on the extra_encode, it may be a numeric so we need to count with the rounding
                if dfall[col].dtypes == object:
                    num_encode_values= len(dfall[col].value_counts()) 
                else:
                    num_encode_values = len( dfall[col].apply(lambda x:round(x,self.one_hot_numeric_rounding)).value_counts())

                
                if num_encode_values <= encoding_threshold:                    
                    print 'One Hot Encoding: ',col
                    new_name = 'is'+col
                    
                    #Normal only encode string features, but we can force to encode a numeric;
                    #If thats the case, we may want to round the feature first
                    if dfall[col].dtypes == object:
                        dfall_dummy = pd.get_dummies(dfall[col], prefix=new_name).astype(np.int8)
                    else:
                        print '     Encoding Numeric Feature with '+str(self.one_hot_numeric_rounding)+' decimal places'
                        dfall_dummy = pd.get_dummies(dfall[col].apply(lambda x:round(x,self.one_hot_numeric_rounding)), prefix=new_name).astype(np.int8)
                        
                    dfall = dfall.drop([col], axis=1)
                    dfall = pd.concat((dfall, dfall_dummy), axis=1)
                    new_names.extend(dfall_dummy.columns)
                else:
                    print 'Regular Encoding: ',col
                    r=pd.factorize(dfall[col], sort=True)
                    dfall[col] = r[0]
                    #wrong when there are -1s:
                    #self.encodings[col] = zip( np.unique(r[0]), r[1] )
                    
                    #this deals with -1 resulted of the Nans possibly produced by function Preprocess_NanValuesNotOnBothDatasets
                    #the idea is to remove the -1 from the mapping (otherwise it will be on the first possition and scramble the resul)
                    #and then add it manually in the end when appropriate
                    mappings = []
                    t = None
                    uniques = np.unique(r[0])
                    if -1 in uniques:
                        uniques  = np.delete(uniques,np.where(uniques ==-1))
                        t = (-1, 'Nan')
                        
                    mappings = zip(uniques, r[1])
                    if t is not None:
                        mappings.append(t)
                    self.encodings[col] = mappings
    
                        
                    #Second code deprecated:
                    #Get a list of unique values soted alphabetic
                    #sorting_list=np.unique(sorted(dfall[col],key=lambda x:(str.lower(x),x)))
                    #dfall[col]=pd.Categorical(dfall[col], sorting_list)
                    #
                    #dfall=dfall.sort_values(col)
                    #r=pd.factorize(dfall[col], sort=True)
                    #
                    #dfall[col] = r[0]
                    #self.encodings[col] = zip( np.unique(r[0]), r[1])

                    #deprecated
                    #dfall[col], self.encodings = encoder.encode(dfall[col].values,col,self.encodings) 
                    new_names.append(col)
            else:
                print 'Not touching: ',col
                new_names.append(col)
        
        #Reorder 
        dfall=dfall.sort_values(ID) 

        
        #rearange the data frame to the original position:
        dfall = dfall[new_names]

        dfall = dfall.drop([ID],axis=1)        
        return dfall
    
    
    def Preprocess_TransformPredictor(self, dfall, trans_type ='log', predictor_shift = 0):
        
        if self.predictor_name is None:
            raise TypeError("Execute the SetUpTrainTest method to use this feature")
            return            
            
        if trans_type == 'log':
            self.predictor_shift = predictor_shift            
            dfall[self.predictor_name]= np.log(dfall[self.predictor_name] + predictor_shift)
            
        
        return dfall
        
    
    def Preprocess_TransformNumericFeatures(self, dfall, trans_type ='boxcox', correction=0.00001):

        if self.num_features is None:
            raise TypeError("Execute the SetUpTrainTest method to use this feature")
            return           
        
        if trans_type not in ['boxcox']:
            raise TypeError("Transformation type not supported")
            return            

        self.lmbdaDict = {}
        for c in self.num_features:
            print 'Applying', trans_type + 'transformation on:', c
            if trans_type == 'boxcox':
                  b = stats.boxcox(dfall[c]+ correction)
                  dfall[c] = b[0]
                  self.lmbdaDict[c]=b[1]
        
        return dfall
        
        #possible idea to improve:
#    # compute skew and do Box-Cox transformation
#    skewed_feats = X_train[da.num_features].apply(lambda x: skew(x.dropna()))
#    print("\nSkew in numeric features:")
#    print(skewed_feats)
#    # transform features with skew > 0.25 (this can be varied to find optimal value)
#    skewed_feats = skewed_feats[skewed_feats > 0.25]
#    skewed_feats = skewed_feats.index
#    for feats in skewed_feats:
#        X_train_test[feats] = X_train_test[feats] + 1
#        X_train_test[feats], lam = boxcox(X_train_test[feats])
#
#    X_train_test[numeric_feats].apply(lambda x: skew(x.dropna()))        


        
        
    def Preprocess_SplitBackIntoTrainAndTest(self, dfall):

        if self.predictor_name is None:
            raise TypeError("Execute the SetUpTrainTest method to use this feature")
            return     
        
        if self.merge_splittype == 'continuous':
            train = dfall[:self.len_train_before]
            test = dfall[self.len_train_before:]
        elif self.merge_splittype == 'byindex':
            train = dfall[dfall.index.isin(self.train_ids)]
            test = dfall[dfall.index.isin(self.test_ids)]  
        else:
            raise Exception('Merge split type must be continuous or byindex')      
        test = test.drop([self.predictor_name],axis=1)
        
        #Check the Lenght is still the same
        assert(self.len_train_before == len(train))
        assert(self.len_test_before == len(test))
    
        return train, test

    def Utils_SaveObjects(self, save_path, train, test, da
                                   , save_file_train = 'train.pkl'
                                   , save_file_test = 'test.pkl'
                                   , DataSetAnalyserObj = 'daObject.pkl'):  
        

        pickle.dump(train, open(os.path.join(save_path, save_file_train), 'wb'))
        pickle.dump(test , open(os.path.join(save_path, save_file_test), 'wb'))
        pickle.dump(da   , open(os.path.join(save_path, DataSetAnalyserObj), 'wb'))
        
    def Utils_LoadObjects(self, save_path, save_file_train = 'train.pkl'
                                   , save_file_test = 'test.pkl'
                                   , DataSetAnalyserObj = 'daObject.pkl'):    
                
        train_path = os.path.join(save_path, save_file_train)
        print 'Loading training pickle from:',train_path
        train = pickle.load(open(train_path , 'rb'))
        
        test_path = os.path.join(save_path, save_file_test)
        print 'Loading testing  pickle from:',test_path
        test  = pickle.load(open(test_path, 'rb'))
        
        da  = pickle.load(open(os.path.join(save_path, DataSetAnalyserObj), 'rb'))
        
        return train, test, da
        
    def Utils_strip_accents(self,s):
       if isinstance(s, str):
           return s
       else:
           return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


    def Utils_XGBFeatureImportance(self, features, model, save_path, save_fig_name='feature_importance_xgb'):
        save_fig_name = save_path + save_fig_name
        outfile = open(save_fig_name+'.fmap', 'w')
        i = 0
        for feat in features:
            outfile.write('{0}\t{1}\tq\n'.format(i, feat))
            i = i + 1
    
        outfile.close()
            
        importance = model.get_fscore(fmap=save_fig_name+'.fmap')
        importance = sorted(importance.items(), key=operator.itemgetter(1))
        
        
        df = pd.DataFrame(importance, columns=['feature', 'fscore'])
        df['fscore'] = df['fscore'] / df['fscore'].sum()
        
        
        plt.figure()
        df.plot()
        df.plot(kind='barh', x='feature', y='fscore', legend=False, figsize=(12, 30))
        plt.title('XGBoost Feature Importance')
        plt.xlabel('relative importance')
        plt.gcf().savefig(save_fig_name+'.png')
        
        return df
