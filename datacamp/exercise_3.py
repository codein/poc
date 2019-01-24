from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
digits = datasets.load_digits()
Xtrain, Xtest, ytrain, ytest = train_test_split(digits.data, digits.target)

knn = KNeighborsClassifier()
knn.fit(Xtrain,ytrain)


training_accuracy = knn.score(Xtest,ytest)

print("Training accuracy = {0}".format(training_accuracy))