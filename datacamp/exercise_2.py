import sklearn.datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.svm import SVC

wine = sklearn.datasets.load_wine()
X_train, X_unseen, y_train, y_unseen = train_test_split(wine.data, wine.target)
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train)


linear_svc = LinearSVC()
svc = SVC() # default hyperparameters

linear_svc.fit(X_train, y_train)
print(linear_svc.score(X_train, y_train))
print(linear_svc.score(X_test, y_test))

svc.fit(X_train, y_train)
print(svc.score(X_train, y_train))
print(svc.score(X_test, y_test))

preferred_model = linear_svc

print(preferred_model.score(X_unseen, y_unseen))

preferred_model = svc

print(preferred_model.score(X_unseen, y_unseen))