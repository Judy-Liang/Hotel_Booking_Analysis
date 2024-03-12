from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,  confusion_matrix, classification_report

def RFC_metrics(X_train, X_test, y_train, y_test):
    RFC = RandomForestClassifier()
    RFC.fit(X_train, y_train)

    y_pred = RFC.predict(X_test)

    acc_train = RFC.score(X_train, y_train)
    acc_test = accuracy_score(y_test, y_pred)
    conf = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    return acc_train, acc_test, conf, report