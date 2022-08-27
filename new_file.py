

import pickle
import pymongo
import pandas as pd

def most_common(lst):
    '''Returns the most common element in a list'''
    return max(set(lst), key=lst.count)


def euclidean(point, data):
    '''Euclidean distance between a point  & data'''
    return np.sqrt(np.sum((point - data)**2, axis=1))


class KNeighborsClassifier_IdoShiraz():
    def __init__(self, k=5, dist_metric=euclidean):
        self.k = k
        self.dist_metric = dist_metric
    def fit(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train
    def predict(self, X_test):
        neighbors = []
        for x in X_test:
            distances = self.dist_metric(x, self.X_train)
            y_sorted = [y for _, y in sorted(zip(distances, self.y_train))]
            neighbors.append(y_sorted[:self.k])
        return list(map(most_common, neighbors))
    def evaluate(self, X_test, y_test):
        y_pred = self.predict(X_test)
        accuracy = sum(y_pred == y_test) / len(y_test)
        return accuracy


def save_model_to_mongo(model):
    knn_model = pickle.dumps(model)
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client[""]
    collection = db["models"]
    collection.insert_one({"knn model":knn_model})


def load_model_from_mongo(client, database, collection):
    myclient = pymongo.MongoClient(client)
    mydb = myclient[database]
    mycol = mydb[collection]
    model = mycol.find()[0]["knn model"]
    return model



# # saving the scaler
import pymongo
import pickle
data=pickle.dumps(scaler)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Diabetes"]
collection = db["scaler"]
collection.insert_one({"data":data})