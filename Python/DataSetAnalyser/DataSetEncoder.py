class DataSetEncoder:

    labelencoder={}

    def encode(self, d, col, labelencoder={}):
        if col not in labelencoder:
            labelencoder[col] = {}
        result = []
        for i in d:
            if i not in labelencoder[col]:
                labelencoder[col][i] = len(labelencoder[col])+1
                result.append(labelencoder[col][i])
            else:
                result.append(labelencoder[col][i])
        return result,labelencoder