# from sklearn import datasets

# digits = datasets.load_digits()

# print(digits.keys())

# print(digits['target_names'])

# print(digits['target'])

# for i in (digits['target']):
#     print(i)

# for i in (digits['data']):
#     print(i)



import pickle
import pymongo
import pandas as pd


def save_x_test_to_mongo(test_to_mongo):
    import pickle
    data=pickle.dumps(test_to_mongo)
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Diabetes"]
    collection = db["test_to_mongo"]
    collection.insert_one({"data":data})

# # # saving the scaler
# import pymongo
# import pickle
# data=pickle.dumps(scaler)
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client["Diabetes"]
# collection = db["scaler"]
# collection.insert_one({"data":data})









# saving the best model
def save_model_to_db(model, client, db, dbconnection, model_name,accuracy,parameters,f1_score,mapk):
    pickled_model = pickle.dumps(model)
    myclient = pymongo.MongoClient(client)
    mydb = myclient[db]
    mycon = mydb[dbconnection]
    # check if model already exists 
    if mycon.count_documents({'model_name':model_name}) == 0:
        # base estimator pickeling if is talked about model with best estimators in the parameters 
        if 'base_estimator'  in parameters:
            base_estimator=pickle.dumps(parameters['base_estimator'])
            parameters.pop('base_estimator')
            parameters['base_estimator']=base_estimator
        elif  'base_estimator__base_estimator' in parameters:
                base_estimator=pickle.dumps(parameters['base_estimator__base_estimator'])
                parameters.pop('base_estimator__base_estimator')
                parameters['base_estimator__base_estimator']=base_estimator
        elif 'estimators' in parameters:
            for param in parameters:
                if 'estimators' in param:
                    for i in range(len(parameters[param])):
                        estimator=pickle.dumps(parameters[param][i])
                        parameters[param][i]=estimator
        mycon.insert_one({'model':pickled_model,"accuracy":accuracy,"parameters":parameters,'mapk':mapk,'f1_score':f1_score,'model_name':model_name,"dbconnection":dbconnection,'model':pickled_model})
    else:
        # check if the model has better accuracy and if so replace it with the new one
        if mycon.find_one({'model_name':model_name})['accuracy'] < accuracy:
            if 'base_estimator'  in parameters:
                base_estimator=pickle.dumps(parameters['base_estimator'])
                parameters.pop('base_estimator')
                parameters['base_estimator']=base_estimator
                mycon.insert_one({'model':pickled_model,"accuracy":accuracy,"parameters":parameters,'mapk':mapk,'f1_score':f1_score,'model_name':model_name,"dbconnection":dbconnection,'model':pickled_model})
                # and delete the old one
                mycon.delete_one({'model_name':model_name})
            elif  'base_estimator__base_estimator' in parameters:
                base_estimator=pickle.dumps(parameters['base_estimator__base_estimator'])
                parameters.pop('base_estimator__base_estimator')
                parameters['base_estimator__base_estimator']=base_estimator
                mycon.insert_one({'model':pickled_model,"accuracy":accuracy,"parameters":parameters,'mapk':mapk,'f1_score':f1_score,'model_name':model_name,"dbconnection":dbconnection,'model':pickled_model})
                # and delete the old one
                mycon.delete_one({'model_name':model_name})   
            elif 'estimators' in parameters:
                for param in parameters:
                    if 'estimators' in param:
                        for i in range(len(parameters[param])):
                            estimator=pickle.dumps(parameters[param][i])
                            parameters[param][i]=estimator
    print("saved",model_name,accuracy)
    





def load_data_from_db(client, db, dbconnection):
    myclient = pymongo.MongoClient(client)
    mydb = myclient[db]
    mycol = mydb[dbconnection]
    records=mycol.find()
    list_cr=list(records)
    for i in list_cr:
        for j in i['parameters']:
            i[j]=i['parameters'][j]
        del i['parameters']
    df=pd.DataFrame(list_cr)
    df['model']=df['model'].apply(lambda x: pickle.loads(x))
    return df