from xgboost.sklearn import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.svm import SVC
import numpy as np
#事先准备三个模型，xgb和rf模型都已经通过cross_validation找出了较好的参数
clf1 = XGBClassifier(learning_rate =0.1, n_estimators=140, max_depth=1,min_child_weight=2, gamma=0, subsample=0.7, colsample_bytree=0.6,objective= 'binary:logistic', nthread=4, scale_pos_weight=1)
clf2 = RandomForestClassifier(n_estimators=50,max_depth=1,min_samples_split=4,min_samples_leaf=54,oob_score=True)
clf3 = SVC(C=0.1,probability=True)

from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import cross_val_score
eclf = VotingClassifier(estimators=[('xgb', clf1), ('rf', clf2), ('svc', clf3)], voting='hard')
for clf, label in zip([clf1, clf2, clf3, eclf], ['XGBBoosting', 'Random Forest', 'SVM', 'Ensemble']):
    scores = cross_val_score(clf, x, y, cv=5, scoring='accuracy')
    print("Accuracy: %0.2f (+/- %0.2f) [%s]" % (scores.mean(), scores.std(), label))


# Accuracy: 0.93 (+/- 0.00) [XGBBoosting]
# Accuracy: 0.93 (+/- 0.00) [Random Forest]
# Accuracy: 0.93 (+/- 0.00) [SVM]
# Accuracy: 0.93 (+/- 0.00) [Ensemble]
# 懵比，这三个怎么一样啊…
# 回到hard vote 的原理，在这种少数服从多数的硬投票中，投出的结果，表明大多数模型认同的结果。
# 比如，如果三个分类器对一个给定的样本的预测是这样的：
# 硬投票不能计算概率

# PLAN2 Weighted Average Probabilities (Soft Voting)
# 软投票和硬投票不同之处在于，它返回的结果是一组概率的加权平均数。可是这个权重是随便赋予的吗？
# 貌似是的，看谁顺眼，给谁高点（未解之谜，待我再查查）
eclf = VotingClassifier(estimators=[('xgb', clf1), ('rf', clf2), ('svc', clf3)], voting='soft',weights=[2,1,1])
clf1.fit(x,y)
XGBClassifier(base_score=0.5, colsample_bylevel=1, colsample_bytree=0.6,
       gamma=0, learning_rate=0.1, max_delta_step=0, max_depth=1,
       min_child_weight=2, missing=None, n_estimators=140, nthread=4,
       objective='binary:logistic', reg_alpha=0, reg_lambda=1,
       scale_pos_weight=1, seed=0, silent=True, subsample=0.7)
clf2.fit(x,y)
RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
            max_depth=1, max_features='auto', max_leaf_nodes=None,
            min_impurity_split=1e-07, min_samples_leaf=54,
            min_samples_split=4, min_weight_fraction_leaf=0.0,
            n_estimators=50, n_jobs=1, oob_score=True, random_state=None,
            verbose=0, warm_start=False)
clf3.fit(x,y)
SVC(C=0.1, cache_size=200, class_weight=None, coef0=0.0,
  decision_function_shape=None, degree=3, gamma='auto', kernel='rbf',
  max_iter=-1, probability=True, random_state=None, shrinking=True,
  tol=0.001, verbose=False)
eclf.fit(x,y)
VotingClassifier(estimators=[('xgb', XGBClassifier(base_score=0.5, colsample_bylevel=1, colsample_bytree=0.6,
       gamma=0, learning_rate=0.1, max_delta_step=0, max_depth=1,
       min_child_weight=2, missing=None, n_estimators=140, nthread=4,
       objective='binary:logistic', reg_alpha=0, reg_lambda=1,
  max_iter=-1, probability=True, random_state=None, shrinking=True,
  tol=0.001, verbose=False))],
         n_jobs=1, voting='soft', weights=[2, 1, 1])
pre = eclf.predict_proba(test[predictors_test])
np.savetxt("D:\Python\\1\\result_vote_xgb_rf_svm.csv", pre, delimiter=',')