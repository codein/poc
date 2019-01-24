Please submit a complete outline for chapter 1 of the course you have chosen from our wishlist.
Please provide
the title of each chapter,
the title of each lesson, and
a brief description of each lesson's contents including a learning objective for each lesson.

Please use the sample outline as a template to guide you in your submission.



----step 3 ----

Now, use the chapter outline you created in the previous section to help you list the practice exercises you will build to help learners practice the same materials they learned in the corresponding chapter.

Please make sure to:
1. Refer to the sample practice outline here for reference:  http://bit.ly/2RvmGei
2. Include 7 to 10 exercises covering the learning objectives in this chapter.
3. Only make exercises on the topics covered in the specified chapter, not on any other aspect (e.g. you can assume they understand all programming aspects not covered in the course).
4. Choose from the following 3 different types of exercises: MultipleChoiceChallenge, BlanksChallenge, and OutputChallenge (which allows selecting the code to match the output or select the output to match the code).
5. Make sure to have a good mix of different exercise types.
Submit an outline of the corresponding practice exercises you would create for your chapter using the guidelines above. Please refer to the sample practice outline here for guidance: http://bit.ly/2RvmGei *
Finally, create 3 sample exercises from your practice outline. You may include images and tables if you choose. Use this guide as a reference: http://bit.ly/2VtVFaj *
--- step 4 ----
Are the learning objectives concise?
Do you cover only the learning objectives relevant to this course?
Learning objectives of prerequisite courses should not be tackled in the Practice set of this course.
To understand what topics are covered in prerequisite courses, check the corresponding course page at datacamp.com.  You’ll find the course prerequisites on the dedicated course page, at the bottom of the right sidebar.
Are the learning objectives testable? Rather than writing "Student will understand X," a good learning objective should specify what the student will do to demonstrate what they know.
Are the learning objectives should be specific? If the objectives aren't clear to you, then they really won't be to the students.


#### notes ####

# Linear Classifiers in Python

Chapter outline rubric: see below

Course: [Linear Classifiers in Python](https://www.datacamp.com/courses/linear-classifiers-in-python)

Prerequisites to course:
* Python, at the level of Intermediate Python for Data Science
* scikit-learn, at the level of Supervised Learning with scikit-learn
* supervised learning, at the level of Supervised Learning with scikit-learn

## Chapter 1: Applying logistic regression and SVM
In this chapter you will learn the basics of applying logistic regression and support vector machines (SVMs) to classification problems. You'll use the syntax from  a popular machine learning library for Python called scikit-learn to fit classification models to real data.

### Lesson 1: scikit-learn refresher
---
This lesson reviews the syntax for scikit-learn to achieve various supervised learning steps, ranging from loading data to model evaluation. It also emphasizes the approach required to avoid over-fitting.

#### Learning objectives
* The learner will be able to perform steps of supervised learning with KNN classifier, along with tunning it's hyper-parameter.
* The learner will have an understanding why just training error alone is a poor metric for the models ability to classify unseen data.
* The learner will be able to compare models by their individual testing accuracies.


### Lesson 2: Applying logistic regression and SVM
---
Firstly, this lesson will guide you to apply logistic regression and SVC classifiers on scikit-learn's built in datasets. Secondly it cautions us on the over-fitting risk we take when using a complex classifier.

#### Learning objectives
* The learner will be able to apply LogisticRegression and SVC with default hyper-parameters
* The learner will be able to identify when a model is under-fitting or over-fitting.

### Lesson 3: Linear classifiers
---
This lesson discuses what it means when a classifier is linear. It also reviews few key vocabulary that will be used in following chapters.

#### Learning objectives
* The learner will able to differentiate if a decision boundary is linear or non-linear.
* The learner will be able to visualize decision boundaries for 2 dimensional datasets.
* The learner will be refresher on few key vocabulary classification, decision boundary, linear classifier and linearly separable.



# Exercise Outline
MultipleChoiceChallenge,
BlanksChallenge
OutputChallenge (which allows selecting the code to match the output or select the output to match the code).

## Lesson 1: scikit-learn refresher
---
### 1.1 Is the learner able to apply KNN classifier given the desired code output?
* BlanksChallenge
* Solution: KNeighborsClassifier() function

### 1.1 Is the user able to perform steps of supervised learning with KNN classifier?
* BlanksChallenge
* Solution: pipeline = .fit(X_train,y_train) then .score(X_train, y_train) then .score(X_test, y_test)

### 1.1 Is the learner able to combine the fit and predict functions to obtain predicted class labels when applying KNN classifier?
* BlanksChallenge
* Solution: .fit() and then .predict()

### 1.1 Is the learner able to apply KNN classifier with a specified number of neighbors?
* BlanksChallenge
* Solution: n_neighbors argument

### 1.1 Is the learner understands the need to reserve some data for testing in order to ensure that the model is not over-fitting?
* OutputChallenge
* Solution: .fit(X_train, y_train) instead of .fit(X,y)

### 1.1 Is the learner able to obtain testing accuracies for two KNN with different n_neighbors.
* OutputChallenge
* Solution: .score(X_test, y_test)

### 1.1 Is the learner able to calculate training accuracy for a KNN model?
* BlanksChallenge
* Solution: .score(X_test, y_test)

### Lesson 2: Applying logistic regression and SVM
---

### 2.1 Is the learner able to avoid using a complex classifier given two models LogisticRegression and SVC, which are fitted on same dataset? Additionally SVC model has inferior testing accuracy, but has higher training accuracy.
* OutputChallenge
* Solution: preferred_model = linear_svc

### 2.2 Is the learner able to discriminate between a model under-fitting or over-fitting?
* MultipleChoiceChallenge
* Solution: under-fitting models have low training accuracy and over-fitting models have a low testing accuracy

### 2.3 Is the learner able to combine the fit and predict_proba functions to obtain confidence score when applying LogisticRegression?
* BlanksChallenge
* Solution: .fit() and then .predict_proba()


### 2.4 Is the learner able to pick an ideal model given following options
|              | A |   B |  C|
---------------
training error | 20% | 30% | 10%|
testing error  | 15% | 10% |  20%|

* MultipleChoiceChallenge
* Solution: B

### Lesson 3: Linear classifiers
---

### 3.1 Is learner will able to differentiate if a decision boundary is linear or non-linear given decision boundary visualizations.
* MultipleChoiceChallenge
* Solution: identify liner boundary

### 3.2 Does the learner know the definition of key vocabulary?
* MultipleChoiceChallenge
* Solution:
    * classification: learning to predict categories
    * decision boundary: the surface separating different predicted classes
    * linear classifier: a classifier that learns linear decision boundaries
    * linearly separable: a data set can be perfectly explained by a linear classifier


https://www.researchgate.net/figure/Overfitting-and-underfitting-effect-on-error_fig4_325999203

# Exercise

## Ex #1 [MultipleChoiceChallenge]
### Question:

Refer to the attached image for question. Which option correctly describes the model's behavior?
![Overfitting-and-underfitting-effect-on-error](Overfitting-and-underfitting-effect-on-error.jpeg)


### Possible answers:
* A. Overfitting
* B. Underfitting

### The correct answer is:
A

### This exercise tests:
Is the learner able to discriminate between a model under-fitting or over-fitting?

[Image Reference](https://www.researchgate.net/figure/Overfitting-and-underfitting-effect-on-error_fig4_325999203)
Al-Behadili, Hayder & Ku-Mahamud, Ku & Sagban, Rafid. (2018). Rule pruning techniques in the ant-miner classification algorithm and its variants: A review. 10.1109/ISCAIE.2018.8405448.


## Ex #2 [OutputChallenge]
### Question:

In this exercise, you'll apply LinearSVC and SVC on wine dataset.
The dataset is divided into three sections `train`,`test` and `unseen`.

Complete the code to achieve better score on `unseen` dataset.
```

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


preferred_model = _ _ _ _

print(preferred_model.score(X_unseen, y_unseen))

```

### The correct answer is:
```
preferred_model = linear_svc
```

### This exercise tests:
Is the learner able to avoid using a complex classifier given two models LogisticRegression and SVC, which are fitted on same dataset.

Additionally SVC model has inferior testing accuracy, but has higher training accuracy.


## Ex #3 [BlanksChallenge]
### Question:
Fill in the correct function from scikit-learn to calculate Training accuracy
```
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
digits = datasets.load_digits()
Xtrain, Xtest, ytrain, ytest = train_test_split(digits.data, digits.target)

knn = KNeighborsClassifier()
knn.fit(Xtrain,ytrain)

training_accuracy = knn._ _ _ _

print("Training accuracy = {0}".format(training_accuracy))
```

### The correct answer is:
`score(X_test, y_test)`

### This exercise tests:
Is the learner able to calculate training accuracy for a KNN model?