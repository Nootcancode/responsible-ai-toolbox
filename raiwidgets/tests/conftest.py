# Copyright (c) Microsoft Corporation
# Licensed under the MIT License.

import pytest
import shap
import sklearn
from sklearn.model_selection import train_test_split

from responsibleai import RAIInsights


@pytest.fixture(scope='session')
def create_rai_insights_object():
    X, y = shap.datasets.adult()
    y = [1 if r else 0 for r in y]

    X, y = sklearn.utils.resample(
        X, y, n_samples=1000, random_state=7, stratify=y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.01, random_state=7, stratify=y)

    knn = sklearn.neighbors.KNeighborsClassifier()
    knn.fit(X_train, y_train)

    X['Income'] = y
    X_test['Income'] = y_test

    ri = RAIInsights(knn, X, X_test, 'Income', 'classification',
                     categorical_features=['Workclass', 'Education-Num',
                                           'Marital Status',
                                           'Occupation', 'Relationship',
                                           'Race',
                                           'Sex', 'Country'])
    ri.explainer.add()
    ri.counterfactual.add(10, desired_class='opposite')
    ri.error_analysis.add()
    ri.causal.add(treatment_features=['Hours per week', 'Occupation'],
                  heterogeneity_features=None,
                  upper_bound_on_cat_expansion=42,
                  skip_cat_limit_checks=True)
    ri.compute()
    return ri
