#! -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import cross_validation
from sklearn.externals import joblib
import matplotlib.pyplot as plt
import random
plt.style.use('ggplot')


def main():
    file = open('/home/howie/code/python/frame/BJData.txt').read()
    raw_data = file.strip().split('\n')
    headers = raw_data[0].strip().split('\t')
    data = np.array([x.strip().split('\t') for x in raw_data[1:]])
    
    districtList = list(set(data[:, 0]))
    districtDict = {}
    for i, d in enumerate(districtList):
        districtDict[d] = i
    
    typeList = list(set(data[:, 1]))
    typeDict = {}
    for i, t in enumerate(typeList):
        typeDict[t] = i

    data[:, 0] = [districtDict[k] for k in data[:, 0]]
    data[:, 1] = [typeDict[k] for k in data[:, 1]]
        
    row, col = data.shape
    for j in xrange(col):
        if 'NULL' in data[:, j]:
            mean = np.mean([float(x) for x in data[:, j] if x != 'NULL'])
            for i in xrange(row):
                if data[i, j] == 'NULL':
                    data[i, j] = mean

    data = data.astype(float)
    #data = data[:, range(12) + range(14, col)]
    train = data[:800, :-1]
    labels = data[:800, -1]
    test = data[800:, :-1]
    testLabels = data[800:, -1]

    rf = RandomForestRegressor()
    rf.fit(train, labels)
    rf_predictions = rf.predict(test)
    rf_feature_importances = rf.feature_importances_
    rfscore = rf.score(test, testLabels)
    print 'Random Forest Score:', rfscore
    rf_featimpo = zip(rf_feature_importances, headers[:-1])

    gbm = GradientBoostingRegressor()
    gbm.fit(train, labels)
    gbm_predictions = gbm.predict(test)
    gbm_feature_importances = gbm.feature_importances_
    gbmscore = gbm.score(test, testLabels)
    print 'Gradient Boosting Machine Score:', gbmscore
    gbm_featimpo = zip(gbm_feature_importances, headers[:-1])

    #joblib.dump(rf, '/home/howie/code/python/frame/rf.model')
    #joblib.dump(gbm, '/home/howie/code/python/frame/gbm.model')
    
    #plotting('Random Forest', rf_predictions, testLabels, rf_featimpo)
    #plotting('Gradient Boosting Machine', gbm_predictions, testLabels, gbm_featimpo)

    ## simulating provided that we chose 30 frame ads position
    Nsim = 100
    rf_rank = [sum(sorted(rf_predictions, reverse=True)[:Nsim])] * Nsim
    gbm_rank = [sum(sorted(gbm_predictions, reverse=True)[:Nsim])] * Nsim

    random_pick = []
    for i in range(Nsim):
        random_pick.append(sum(random.sample(testLabels, Nsim)))

    plt.plot(range(Nsim), rf_rank, 'g', linewidth=2, label='Random Forest')
    plt.plot(range(Nsim), gbm_rank, 'b', linewidth=2, label='Gradient Boosting Machine')
    plt.plot(range(Nsim), random_pick, 'r', linewidth=2, label='Random Pick')
    plt.title('Simulation')
    plt.legend()
    plt.show()


def plotting(model, predictions, testLabels, featimpo):    
    featimpo.sort()

    ax1 = plt.subplot(2, 1, 1)
    ax1.plot(predictions, 'b', linewidth=2, label='Predicted data')
    ax1.plot(testLabels, 'g', linewidth=2, label='Actual data')
    ax1.set_xlabel('Frame Ads Positions')
    ax1.set_ylabel('Delta Users')
    ax1.set_title(model + ' Predicitons')
    ax1.legend(loc=4)

    ax2 = plt.subplot(2, 1, 2)
    ax2.barh(range(len(featimpo)), [x[0] for x in featimpo])
    ax2.set_title('Feature Importances')
    ax2.set_xlabel('Relative Importances')
    plt.yticks(range(len(featimpo)), [x[1] for x in featimpo])
    
    plt.show()


main()
