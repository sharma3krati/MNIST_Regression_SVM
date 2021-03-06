import numpy as np
from scipy.io import loadmat
from scipy.optimize import minimize
from sklearn import svm
import matplotlib.pyplot as plt


def preprocess():
    """ 
     Input:
     Although this function doesn't have any input, you are required to load
     the MNIST data set from file 'mnist_all.mat'.

     Output:
     train_data: matrix of training set. Each row of train_data contains 
       feature vector of a image
     train_label: vector of label corresponding to each image in the training
       set
     validation_data: matrix of training set. Each row of validation_data 
       contains feature vector of a image
     validation_label: vector of label corresponding to each image in the 
       training set
     test_data: matrix of training set. Each row of test_data contains 
       feature vector of a image
     test_label: vector of label corresponding to each image in the testing
       set
    """

    mat = loadmat('mnist_all.mat')  # loads the MAT object as a Dictionary

    n_feature = mat.get("train1").shape[1]
    n_sample = 0
    for i in range(10):
        n_sample = n_sample + mat.get("train" + str(i)).shape[0]
    n_validation = 1000
    n_train = n_sample - 10 * n_validation

    # Construct validation data
    validation_data = np.zeros((10 * n_validation, n_feature))
    for i in range(10):
        validation_data[i * n_validation:(i + 1) * n_validation, :] = mat.get("train" + str(i))[0:n_validation, :]

    # Construct validation label
    validation_label = np.ones((10 * n_validation, 1))
    for i in range(10):
        validation_label[i * n_validation:(i + 1) * n_validation, :] = i * np.ones((n_validation, 1))

    # Construct training data and label
    train_data = np.zeros((n_train, n_feature))
    train_label = np.zeros((n_train, 1))
    temp = 0
    for i in range(10):
        size_i = mat.get("train" + str(i)).shape[0]
        train_data[temp:temp + size_i - n_validation, :] = mat.get("train" + str(i))[n_validation:size_i, :]
        train_label[temp:temp + size_i - n_validation, :] = i * np.ones((size_i - n_validation, 1))
        temp = temp + size_i - n_validation

    # Construct test data and label
    n_test = 0
    for i in range(10):
        n_test = n_test + mat.get("test" + str(i)).shape[0]
    test_data = np.zeros((n_test, n_feature))
    test_label = np.zeros((n_test, 1))
    temp = 0
    for i in range(10):
        size_i = mat.get("test" + str(i)).shape[0]
        test_data[temp:temp + size_i, :] = mat.get("test" + str(i))
        test_label[temp:temp + size_i, :] = i * np.ones((size_i, 1))
        temp = temp + size_i

    # Delete features which don't provide any useful information for classifiers
    sigma = np.std(train_data, axis=0)
    index = np.array([])
    for i in range(n_feature):
        if (sigma[i] > 0.001):
            index = np.append(index, [i])
    train_data = train_data[:, index.astype(int)]
    validation_data = validation_data[:, index.astype(int)]
    test_data = test_data[:, index.astype(int)]

    # Scale data to 0 and 1
    train_data /= 255.0
    validation_data /= 255.0
    test_data /= 255.0

    return train_data, train_label, validation_data, validation_label, test_data, test_label


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def blrObjFunction(initialWeights, *args):
    """
    blrObjFunction computes 2-class Logistic Regression error function and
    its gradient.

    Input:
        initialWeights: the weight vector (w_k) of size (D + 1) x 1 
        train_data: the data matrix of size N x D
        labeli: the label vector (y_k) of size N x 1 where each entry can be either 0 or 1 representing the label of corresponding feature vector

    Output: 
        error: the scalar value of error function of 2-class logistic regression
        error_grad: the vector of size (D+1) x 1 representing the gradient of
                    error function
    """
    train_data, labeli = args

    n_data = train_data.shape[0]
    n_features = train_data.shape[1]
    error = 0
    error_grad = np.zeros((n_features + 1, 1))

    ##################
    # YOUR CODE HERE #
    ##################
    # HINT: Do not forget to add the bias term to your input data
    biases = np.full((n_data,1),1)
    X = np.concatenate((biases,train_data),axis=1)
    
    newRow = n_features + 1
    col = 1
    w = initialWeights.reshape(newRow,col)
    theta_value = sigmoid(np.dot(X,w))
    
    #Negative log likelihood
    first = labeli * np.log(theta_value)
    second = (1.0 - labeli) * np.log(1.0 - theta_value)
    
    error_func = first + second
    error = (- 1.0 * np.sum(error_func) ) / n_data
    #gradient of error function with respect to w
    #cross-entropy error function
    error_grad = np.sum((theta_value - labeli)*X, axis=0) / n_data
    
    return error, error_grad
    


def blrPredict(W, data):
    """
     blrObjFunction predicts the label of data given the data and parameter W 
     of Logistic Regression
     
     Input:
         W: the matrix of weight of size (D + 1) x 10. Each column is the weight 
         vector of a Logistic Regression classifier.
         X: the data matrix of size N x D
         
     Output: 
         label: vector of size N x 1 representing the predicted label of 
         corresponding feature vector given in data matrix

    """
    label = np.zeros((data.shape[0], 1))

    ##################
    # YOUR CODE HERE #
    ##################
    # HINT: Do not forget to add the bias term to your input data
    N = data.shape[0]
    D = data.shape[1]
    
    # Adding biases
    biases = np.full((N,1),1)
    X = np.concatenate((biases,data),axis=1)
    
    prob = sigmoid(np.dot(X,W))
    
    l = np.argmax(prob,axis=1)
    
    label = l.reshape((N,1)) 
    return label

def mlrObjFunction(params, *args):
    """
    mlrObjFunction computes multi-class Logistic Regression error function and
    its gradient.

    Input:
        initialWeights_b: the weight vector of size (D + 1) x 10
        train_data: the data matrix of size N x D
        labeli: the label vector of size N x 1 where each entry can be either 0 or 1
                representing the label of corresponding feature vector

    Output:
        error: the scalar value of error function of multi-class logistic regression
        error_grad: the vector of size (D+1) x 10 representing the gradient of
                    error function
    """
    train_data, labeli = args
    n_data = train_data.shape[0]
    n_feature = train_data.shape[1]
    error = 0
    error_grad = np.zeros((n_feature + 1, n_class))

    ##################
    # YOUR CODE HERE #
    ##################
    # HINT: Do not forget to add the bias term to your input data

    biases = np.full((n_data,1),1)
    X = np.concatenate((biases,train_data), axis=1)
    W = params.reshape((n_feature + 1, n_class))
    
    #caclulating theta
    numerator = np.exp(np.dot(X,W))
        
    denom = np.sum(numerator,axis=1)
    denom = denom.reshape(denom.shape[0],1)
    
    theta_value = numerator/denom
   
    
    Sum = np.sum(Y*np.log(theta_value))
    #cross-entropy error function
    error = - (np.sum(Sum))
    error_grad = np.dot(X.T,(theta_value - labeli))
    error_grad = error_grad.ravel()
    return error, error_grad


def mlrPredict(W, data):
    """
     mlrObjFunction predicts the label of data given the data and parameter W
     of Logistic Regression

     Input:
         W: the matrix of weight of size (D + 1) x 10. Each column is the weight
         vector of a Logistic Regression classifier.
         X: the data matrix of size N x D

     Output:
         label: vector of size N x 1 representing the predicted label of
         corresponding feature vector given in data matrix

    """
    label = np.zeros((data.shape[0], 1))
    row = data.shape[0]
    ##################
    # YOUR CODE HERE #
    ##################
    # HINT: Do not forget to add the bias term to your input data
    biases = np.full((row,1),1)
    X = np.concatenate((biases,data), axis=1)

    t = np.sum(np.exp(np.dot(X,W)),axis=1)    
    t = t.reshape(t.shape[0],1)
    
    theta_value = np.exp(np.dot(X,W))/t
    
    label = np.argmax(theta_value,axis=1)
    label = label.reshape(row,1)
    return label


"""
Script for Logistic Regression
"""
train_data, train_label, validation_data, validation_label, test_data, test_label = preprocess()

# number of classes
n_class = 10

# number of training samples
n_train = train_data.shape[0]

# number of features
n_feature = train_data.shape[1]

Y = np.zeros((n_train, n_class))
for i in range(n_class):
    Y[:, i] = (train_label == i).astype(int).ravel()

# Logistic Regression with Gradient Descent
W = np.zeros((n_feature + 1, n_class))
initialWeights = np.zeros((n_feature + 1, 1))
opts = {'maxiter': 100}
for i in range(n_class):
    labeli = Y[:, i].reshape(n_train, 1)
    args = (train_data, labeli)
    nn_params = minimize(blrObjFunction, initialWeights, jac=True, args=args, method='CG', options=opts)
    W[:, i] = nn_params.x.reshape((n_feature + 1,))

# Find the accuracy on Training Dataset
predicted_label = blrPredict(W, train_data)
print('\n Training set Accuracy:' + str(100 * np.mean((predicted_label == train_label).astype(float))) + '%')

# Find the accuracy on Validation Dataset
predicted_label = blrPredict(W, validation_data)
print('\n Validation set Accuracy:' + str(100 * np.mean((predicted_label == validation_label).astype(float))) + '%')

# Find the accuracy on Testing Dataset
predicted_label = blrPredict(W, test_data)
print('\n Testing set Accuracy:' + str(100 * np.mean((predicted_label == test_label).astype(float))) + '%')

"""
Script for Support Vector Machine
"""

print('\n\n--------------SVM-------------------\n\n')
##################
# YOUR CODE HERE #
##################
#Random Selection of Samples
index = np.random.randint(50000, size = 10000)
svm_data = train_data[index,:]
svm_label = train_label[index,:]

#Linear Kernel
linear_model = svm.SVC(kernel='linear')
linear_model.fit(svm_data, svm_label)

print('\n---------Linear Kernel---------\n')
print('\n Training Accuracy =' + str(linear_model.score(train_data, train_label)*100) + '%')
print('\n Validation Accuracy =' + str(linear_model.score(validation_data, validation_label)*100) + '%')
print('\n Testing Accuracy =' + str(linear_model.score(test_data, test_label)*100) + '%')

# RBF with Gamma set to 1

rbf_model0 = svm.SVC(kernel='rbf', gamma = 1.0)
rbf_model0.fit(svm_data, svm_label)

print('\n---------RBF Kernel with Gamma = 1---------\n')
print('\n Training Accuracy =' + str(rbf_model0.score(svm_data, svm_label)*100) + '%')
print('\n Validation Accuracy =' + str(rbf_model0.score(validation_data, validation_label)*100) + '%')
print('\n Testing Accuracy =' + str(rbf_model0.score(test_data, test_label)*100) + '%')

# RBF with gamma set to default = scale

rbf_model1 = svm.SVC(kernel='rbf', gamma = 'scale')
rbf_model1.fit(svm_data, svm_label)

print('\n---------RBF Kernel with Gamma = default---------\n')
print('\n Training Accuracy =' + str(rbf_model1.score(train_data, train_label)*100) + '%')
print('\n Validation Accuracy =' + str(rbf_model1.score(validation_data, validation_label)*100) + '%')
print('\n Testing Accuracy =' + str(rbf_model1.score(test_data, test_label)*100) + '%')

# RBF with gamma = scale and varying C 

accuracy = np.zeros((11,3), float)
C_values = np.array([1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
i = 0

# Varying C
for c in C_values:
  #  print("C=", c)
    rbf_model2 = svm.SVC(kernel = 'rbf', C = c, gamma='scale')
    rbf_model2.fit(svm_data, svm_label.ravel())
    if i <= 10: 
        accuracy[i][0] = rbf_model2.score(train_data, train_label) * 100
        accuracy[i][1] = rbf_model2.score(validation_data, validation_label) *100
        accuracy[i][2] = rbf_model2.score(test_data, test_label) *100
        
        print('\n---------RBF Kernel with Gamma = default(scale) and C = '+ str(c) +'---------\n')
        print('\n Training Accuracy =' + str(accuracy[i][0]) + '%')
        print('\n Validation Accuracy =' + str(accuracy[i][1]) + '%')
        print('\n Testing Accuracy =' + str(accuracy[i][2]) + '%')
        
    i = i + 1


plt.title('Accuracy vs C',pad=10,fontsize=20,fontweight = 'bold')

plt.xlabel('C Value', labelpad=20, weight='bold', size=15)
plt.ylabel('Accuracy', labelpad=20, weight='bold', size=15)

plt.xticks( C_values, fontsize=18)
plt.yticks( np.arange(85,100, step=0.5),  fontsize=18)


plt.plot(C_values, accuracy[:,0], color='r')
plt.plot(C_values, accuracy[:,1], color='b')
plt.plot(C_values, accuracy[:,2], color='g')

plt.legend(['Training_Data','Validation_Data','Test_Data'])

rbf_final = svm.SVC(kernel = 'rbf', gamma = 'auto', C = 20)
rbf_final.fit(train_data, train_label.ravel())

print('---RBF with best C---')
print('\nTraining Accuracy =' + str( rbf_final.score(train_data, train_label)* 100 ) + '%')
print('\nValidation Accuracy = ' + str( rbf_final.score(validation_data, validation_label)* 100) + '%')
print('\nTesting Accuracy =' + str( rbf_final.score(test_data, test_label)* 100) + '%')
 
"""
Script for Extra Credit Part
"""
# FOR EXTRA CREDIT ONLY
print('\n----------Multi-class Logistic Regression-----------')
W_b = np.zeros((n_feature + 1, n_class))
initialWeights_b = np.zeros((n_feature + 1, n_class))
opts_b = {'maxiter': 100}

args_b = (train_data, Y)
nn_params = minimize(mlrObjFunction, initialWeights_b, jac=True, args=args_b, method='CG', options=opts_b)
W_b = nn_params.x.reshape((n_feature + 1, n_class))

# Find the accuracy on Training Dataset
predicted_label_b = mlrPredict(W_b, train_data)
print('\n Training set Accuracy:' + str(100 * np.mean((predicted_label_b == train_label).astype(float))) + '%')

# Find the accuracy on Validation Dataset
predicted_label_b = mlrPredict(W_b, validation_data)
print('\n Validation set Accuracy:' + str(100 * np.mean((predicted_label_b == validation_label).astype(float))) + '%')

# Find the accuracy on Testing Dataset
predicted_label_b = mlrPredict(W_b, test_data)
print('\n Testing set Accuracy:' + str(100 * np.mean((predicted_label_b == test_label).astype(float))) + '%')
