{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "ee52153e",
   "metadata": {},
   "outputs": [
    {
     "ename": "FileNotFoundError",
     "evalue": "[Errno 2] No such file or directory: 'sample.pickle'",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mFileNotFoundError\u001b[0m                         Traceback (most recent call last)",
      "\u001b[1;32m<ipython-input-1-97b24290b801>\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[0;32m    216\u001b[0m     \u001b[0mX\u001b[0m\u001b[1;33m,\u001b[0m\u001b[0my\u001b[0m\u001b[1;33m,\u001b[0m\u001b[0mXtest\u001b[0m\u001b[1;33m,\u001b[0m\u001b[0mytest\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mpickle\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mload\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mopen\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;34m'sample.pickle'\u001b[0m\u001b[1;33m,\u001b[0m\u001b[1;34m'rb'\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    217\u001b[0m \u001b[1;32melse\u001b[0m\u001b[1;33m:\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m--> 218\u001b[1;33m     \u001b[0mX\u001b[0m\u001b[1;33m,\u001b[0m\u001b[0my\u001b[0m\u001b[1;33m,\u001b[0m\u001b[0mXtest\u001b[0m\u001b[1;33m,\u001b[0m\u001b[0mytest\u001b[0m \u001b[1;33m=\u001b[0m \u001b[0mpickle\u001b[0m\u001b[1;33m.\u001b[0m\u001b[0mload\u001b[0m\u001b[1;33m(\u001b[0m\u001b[0mopen\u001b[0m\u001b[1;33m(\u001b[0m\u001b[1;34m'sample.pickle'\u001b[0m\u001b[1;33m,\u001b[0m\u001b[1;34m'rb'\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m,\u001b[0m\u001b[0mencoding\u001b[0m \u001b[1;33m=\u001b[0m \u001b[1;34m'latin1'\u001b[0m\u001b[1;33m)\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m    219\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m    220\u001b[0m \u001b[1;31m# LDA\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;31mFileNotFoundError\u001b[0m: [Errno 2] No such file or directory: 'sample.pickle'"
     ]
    }
   ],
   "source": [
    "import numpy as np\n",
    "from scipy.optimize import minimize\n",
    "from scipy.io import loadmat\n",
    "from numpy.linalg import det, inv\n",
    "from math import sqrt, pi\n",
    "import scipy.io\n",
    "import matplotlib.pyplot as plt\n",
    "import pickle\n",
    "import sys\n",
    "\n",
    "#Pinaz\n",
    "def ldaLearn(X,y):\n",
    "    # Inputs\n",
    "    # X - a N x d matrix with each row corresponding to a training example\n",
    "    # y - a N x 1 column vector indicating the labels for each training example  \n",
    "    # Outputs\n",
    "    # means - A d x k matrix containing learnt means for each of the k classes\n",
    "    # covmat - A single d x d learnt covariance matrix \n",
    "    \n",
    "    # IMPLEMENT THIS METHOD \n",
    "    unique_label = np.unique(y)\n",
    "    means = np.zeros((len(unique_label), len(X[0])))\n",
    "    for i in unique_label:\n",
    "        x1 = X[np.where(y == i)[0]]\n",
    "        means[int(i)-1] = x1.mean(axis=0)\n",
    "    covmat = np.cov(X.T)\n",
    "    return means, covmat\n",
    "\n",
    "def qdaLearn(X,y):\n",
    "    # Inputs\n",
    "    # X - a N x d matrix with each row corresponding to a training example\n",
    "    # y - a N x 1 column vector indicating the labels for each training example\n",
    "    #\n",
    "    # Outputs\n",
    "    # means - A d x k matrix containing learnt means for each of the k classes\n",
    "    # covmats - A list of k d x d learnt covariance matrices for each of the k classes\n",
    "    \n",
    "    # IMPLEMENT THIS METHOD\n",
    "    covmats = []\n",
    "    labels = np.unique(y)\n",
    "    means = np.zeros([len(labels),len(X[1])])\n",
    "\n",
    "    for i in range(len(labels)):\n",
    "        m = np.mean(X[np.where(y == labels[i])[0],],axis=0)\n",
    "        means[i,] = m\n",
    "        covmats.append(np.cov(np.transpose(X[np.where(y == labels[i])[0],])))\n",
    "    \n",
    "    return means, covmats\n",
    "\n",
    "def ldaTest(means,covmat,Xtest,ytest):\n",
    "    # Inputs\n",
    "    # means, covmat - parameters of the LDA model\n",
    "    # Xtest - a N x d matrix with each row corresponding to a test example\n",
    "    # ytest - a N x 1 column vector indicating the labels for each test example\n",
    "    # Outputs\n",
    "    # acc - A scalar accuracy value\n",
    "    \n",
    "    # ypred - N x 1 column vector indicating the predicted labels\n",
    "\n",
    "    # IMPLEMENT THIS METHOD\n",
    "    g = 1 / np.sqrt((2*np.pi**len(means)*det(covmat)))\n",
    "    ll = np.zeros((len(Xtest), len(means)))\n",
    "    for i in range(len(Xtest)):\n",
    "        for h in range(len(means)):\n",
    "            b = Xtest[i, :] - means[int(h) - 1]\n",
    "            t = (-1/2)*np.dot(np.dot(b.T, inv(covmat)), b)\n",
    "            ll[i,int(h)-1] = g * np.e**t \n",
    "            \n",
    "    ypred = []\n",
    "    for row in ll:\n",
    "        ypred.append(list(row).index(max(list(row)))+1)\n",
    "    \n",
    "    \n",
    "    acc = 0\n",
    "    for k in range(len(ypred)):\n",
    "        if ypred[k] == ytest[k]:\n",
    "            acc += 1\n",
    "    acc = acc / len(ypred)\n",
    "    ytest=ytest.flatten()\n",
    "    return acc, np.array(ypred)\n",
    "    \n",
    "\n",
    "def qdaTest(means,covmats,Xtest,ytest):\n",
    "    # Inputs\n",
    "    # means, covmats - parameters of the QDA model\n",
    "    # Xtest - a N x d matrix with each row corresponding to a test example\n",
    "    # ytest - a N x 1 column vector indicating the labels for each test example\n",
    "    # Outputs\n",
    "    # acc - A scalar accuracy value\n",
    "    # ypred - N x 1 column vector indicating the predicted labels\n",
    "\n",
    "    # IMPLEMENT THIS METHOD\n",
    "    a = np.unique(ytest)\n",
    "    ll = np.zeros((len(Xtest), len(means)))\n",
    "    for i in range(len(Xtest)):\n",
    "        for h in range(len(means)):\n",
    "            index = int(h)-1\n",
    "            b = Xtest[i, :] - means[index]\n",
    "            t = (-1/2)*np.dot(np.dot(b.T, inv(covmats[index])), b)\n",
    "            g = 1 / np.sqrt((2*np.pi**len(means))*det(covmats[index]))\n",
    "            ll[i,index] = g * np.e**t \n",
    "            \n",
    "    ypred = []\n",
    "    for row in ll:\n",
    "        ypred.append(list(row).index(max(list(row)))+1)\n",
    "    \n",
    "    \n",
    "    acc = 0\n",
    "    for k in range(len(ypred)):\n",
    "        if ypred[k] == ytest[k]:\n",
    "            acc += 1\n",
    "    acc = acc / len(ypred)\n",
    "    ytest=ytest.flatten()\n",
    "    return acc, np.array(ypred)\n",
    "    return acc,ypred\n",
    "\n",
    "\n",
    "#Janhavi\n",
    "def learnOLERegression(X,y):\n",
    "    # Inputs:\n",
    "    # X = N x d\n",
    "    # y = N x 1\n",
    "    # Output:\n",
    "    # w = d x 1\n",
    "\n",
    "    # IMPLEMENT THIS METHOD\n",
    "    # converting from 2nd j(w)formula given\n",
    "    x_transed = np.transpose(X)                       \n",
    "                                                      \n",
    "    dot_x = np.dot(x_transed , X)                     \n",
    "    dot_y = np.dot(x_transed , y)                     \n",
    "    inverse = np.linalg.inv(dot_x)                    #inverse of the dot_x\n",
    "    w = np.dot(inverse, dot_y)                        #calculating the weight\n",
    "    return w\n",
    "\n",
    "\n",
    "#Krati\n",
    "def testOLERegression(w,Xtest,ytest):\n",
    "    # Inputs:\n",
    "    # w = d x 1\n",
    "    # Xtest = N x d\n",
    "    # ytest = X x 1\n",
    "    # Output:\n",
    "    # mse\n",
    "\n",
    "    # IMPLEMENT THIS METHOD\n",
    "    #literal converstion from the formula given\n",
    "    p = np.dot(Xtest,w)\n",
    "    s = np.subtract(ytest,p)\n",
    "    diff = np.square(s)                                #subtracts the dot product of the w and the x from $\n",
    "    rmse = np.sum(diff)                                #performs a summation\n",
    "    N = Xtest.shape[0]                                 #gets the sphape of xtest so that we can get N\n",
    "    mse = np.divide(rmse,N)\n",
    "    return mse\n",
    "\n",
    "\n",
    "def learnRidgeRegression(X,y,lambd):\n",
    "    # Inputs:\n",
    "    # X = N x d                                                               \n",
    "    # y = N x 1 \n",
    "    # lambd = ridge parameter (scalar)\n",
    "    # Output:                                                                  \n",
    "    # w = d x 1                                                                \n",
    "\n",
    "    # IMPLEMENT THIS METHOD   \n",
    "    \n",
    "    N, d = np.shape(X)\n",
    "    \n",
    "    XT_dot_X = np.dot(X.T,X)\n",
    "    lam_val = lambd*np.eye(d)\n",
    "    sum_X_I_inv = np.linalg.inv( XT_dot_X + lam_val )\n",
    "    XT_dot_y = np.dot(X.T, y)\n",
    "    w = np.dot(sum_X_I_inv, XT_dot_y)\n",
    "    return w\n",
    "\n",
    "def regressionObjVal(w, X, y, lambd):\n",
    "    \n",
    "    # compute squared error (scalar) and gradient of squared error with respect\n",
    "    # to w (vector) for the given data X and y and the regularization parameter\n",
    "    # lambda\n",
    "    \n",
    "    # IMPLEMENT THIS METHOD\n",
    "    \n",
    "    N = X.shape[0]\n",
    "    w = np.mat(w).T\n",
    "    y_Xdw = y - np.dot(X, w) \n",
    "\n",
    "    error = 0.001  * ( np.dot(y_Xdw.T, y_Xdw) + (lambd * np.dot(w.T, w)) )\n",
    "    learning_rate =  0.0005\n",
    "    error_grad =  X.T.dot(X.dot(w) - y) * learning_rate\n",
    "    error_grad = np.ndarray.flatten(np.array(error_grad))\n",
    "    #print(error)\n",
    "    #print(error_grad)\n",
    "    return error, error_grad\n",
    "\n",
    "#Pinaz\n",
    "def mapNonLinear(x,p):\n",
    "    # Inputs:                                                                  \n",
    "    # x - a single column vector (N x 1)                                       \n",
    "    # p - integer (>= 0)                                                       \n",
    "    # Outputs:                                                                 \n",
    "    # Xp - (N x (p+1)) \n",
    "    # IMPLEMENT THIS METHOD\n",
    "    N = x.shape[0]\n",
    "    Xp = np.ones((N, p+1))\n",
    "    for i in range(1, p+1):\n",
    "        Xp[:, i] = np.power(x,i)\n",
    "    return Xp\n",
    "\n",
    "#Janhavi\n",
    "# Main script\n",
    "\n",
    "# Problem 1\n",
    "# load the sample data                                                                 \n",
    "if sys.version_info.major == 2:\n",
    "    X,y,Xtest,ytest = pickle.load(open('sample.pickle','rb'))\n",
    "else:\n",
    "    X,y,Xtest,ytest = pickle.load(open('sample.pickle','rb'),encoding = 'latin1')\n",
    "\n",
    "# LDA\n",
    "means,covmat = ldaLearn(X,y)\n",
    "ldaacc,ldares = ldaTest(means,covmat,Xtest,ytest)\n",
    "print('LDA Accuracy = '+str(ldaacc))\n",
    "# QDA\n",
    "means,covmats = qdaLearn(X,y)\n",
    "qdaacc,qdares = qdaTest(means,covmats,Xtest,ytest)\n",
    "print('QDA Accuracy = '+str(qdaacc))\n",
    "\n",
    "# plotting boundaries\n",
    "x1 = np.linspace(-5,20,100)\n",
    "x2 = np.linspace(-5,20,100)\n",
    "xx1,xx2 = np.meshgrid(x1,x2)\n",
    "xx = np.zeros((x1.shape[0]*x2.shape[0],2))\n",
    "xx[:,0] = xx1.ravel()\n",
    "xx[:,1] = xx2.ravel()\n",
    "\n",
    "fig = plt.figure(figsize=[12,6])\n",
    "plt.subplot(1, 2, 1)\n",
    "\n",
    "zacc,zldares = ldaTest(means,covmat,xx,np.zeros((xx.shape[0],1)))\n",
    "plt.contourf(x1,x2,zldares.reshape((x1.shape[0],x2.shape[0])),alpha=0.3)\n",
    "plt.scatter(Xtest[:,0],Xtest[:,1],c=ytest.ravel())\n",
    "plt.title('LDA')\n",
    "\n",
    "plt.subplot(1, 2, 2)\n",
    "\n",
    "zacc,zqdares = qdaTest(means,covmats,xx,np.zeros((xx.shape[0],1)))\n",
    "plt.contourf(x1,x2,zqdares.reshape((x1.shape[0],x2.shape[0])),alpha=0.3)\n",
    "plt.scatter(Xtest[:,0],Xtest[:,1],c=ytest.ravel())\n",
    "plt.title('QDA')\n",
    "\n",
    "plt.show()\n",
    "# Problem 2\n",
    "if sys.version_info.major == 2:\n",
    "    X,y,Xtest,ytest = pickle.load(open('diabetes.pickle','rb'))\n",
    "else:\n",
    "    X,y,Xtest,ytest = pickle.load(open('diabetes.pickle','rb'),encoding = 'latin1')\n",
    "\n",
    "# add intercept\n",
    "X_i = np.concatenate((np.ones((X.shape[0],1)), X), axis=1)\n",
    "Xtest_i = np.concatenate((np.ones((Xtest.shape[0],1)), Xtest), axis=1)\n",
    "\n",
    "w = learnOLERegression(X,y)\n",
    "mle = testOLERegression(w,Xtest,ytest)\n",
    "\n",
    "w_i = learnOLERegression(X_i,y)\n",
    "mle_i = testOLERegression(w_i,Xtest_i,ytest)\n",
    "\n",
    "print('MSE without intercept '+str(mle))\n",
    "print('MSE with intercept '+str(mle_i))\n",
    "\n",
    "# Problem 3\n",
    "k = 101\n",
    "lambdas = np.linspace(0, 1, num=k)\n",
    "i = 0\n",
    "mses3_train = np.zeros((k,1))\n",
    "mses3 = np.zeros((k,1))\n",
    "for lambd in lambdas:\n",
    "    w_l = learnRidgeRegression(X_i,y,lambd)\n",
    "    mses3_train[i] = testOLERegression(w_l,X_i,y)\n",
    "    mses3[i] = testOLERegression(w_l,Xtest_i,ytest)\n",
    "    i = i + 1\n",
    "fig = plt.figure(figsize=[12,6])\n",
    "plt.subplot(1, 2, 1)\n",
    "plt.plot(lambdas,mses3_train)\n",
    "plt.title('MSE for Train Data')\n",
    "plt.subplot(1, 2, 2)\n",
    "plt.plot(lambdas,mses3)\n",
    "plt.title('MSE for Test Data')\n",
    "\n",
    "plt.show()\n",
    "# Problem 4\n",
    "k = 101\n",
    "lambdas = np.linspace(0, 1, num=k)\n",
    "i = 0\n",
    "mses4_train = np.zeros((k,1))\n",
    "mses4 = np.zeros((k,1))\n",
    "opts = {'maxiter' : 20}    # Preferred value.                                                \n",
    "w_init = np.ones((X_i.shape[1],1))\n",
    "for lambd in lambdas:\n",
    "    args = (X_i, y, lambd)\n",
    "    w_l = minimize(regressionObjVal, w_init, jac=True, args=args,method='CG', options=opts)\n",
    "    w_l = np.transpose(np.array(w_l.x))\n",
    "    w_l = np.reshape(w_l,[len(w_l),1])\n",
    "    mses4_train[i] = testOLERegression(w_l,X_i,y)\n",
    "    mses4[i] = testOLERegression(w_l,Xtest_i,ytest)\n",
    "    i = i + 1\n",
    "fig = plt.figure(figsize=[12,6])\n",
    "plt.subplot(1, 2, 1)\n",
    "plt.plot(lambdas,mses4_train)\n",
    "plt.plot(lambdas,mses3_train)\n",
    "plt.title('MSE for Train Data')\n",
    "plt.legend(['Using scipy.minimize','Direct minimization'])\n",
    "\n",
    "plt.subplot(1, 2, 2)\n",
    "plt.plot(lambdas,mses4)\n",
    "plt.plot(lambdas,mses3)\n",
    "plt.title('MSE for Test Data')\n",
    "plt.legend(['Using scipy.minimize','Direct minimization'])\n",
    "plt.show()\n",
    "\n",
    "\n",
    "# Problem 5\n",
    "pmax = 7\n",
    "lambda_opt = lambdas[np.argmin(mses3)] # REPLACE THIS WITH lambda_opt estimated from Problem 3\n",
    "mses5_train = np.zeros((pmax,2))\n",
    "mses5 = np.zeros((pmax,2))\n",
    "for p in range(pmax):\n",
    "    Xd = mapNonLinear(X[:,2],p)\n",
    "    Xdtest = mapNonLinear(Xtest[:,2],p)\n",
    "    w_d1 = learnRidgeRegression(Xd,y,0)\n",
    "    mses5_train[p,0] = testOLERegression(w_d1,Xd,y)\n",
    "    mses5[p,0] = testOLERegression(w_d1,Xdtest,ytest)\n",
    "    w_d2 = learnRidgeRegression(Xd,y,lambda_opt)\n",
    "    mses5_train[p,1] = testOLERegression(w_d2,Xd,y)\n",
    "    mses5[p,1] = testOLERegression(w_d2,Xdtest,ytest)\n",
    "\n",
    "print(\"Test MSE - Lambda 0.06\")\n",
    "print(mses5) #Test\n",
    "\n",
    "fig = plt.figure(figsize=[12,6])\n",
    "plt.subplot(1, 2, 1)\n",
    "plt.plot(range(pmax),mses5_train)\n",
    "plt.title('MSE for Train Data')\n",
    "plt.legend(('No Regularization','Regularization'))\n",
    "plt.subplot(1, 2, 2)\n",
    "plt.plot(range(pmax),mses5)\n",
    "plt.title('MSE for Test Data')\n",
    "plt.legend(('No Regularization','Regularization'))\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "99383f3c",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
