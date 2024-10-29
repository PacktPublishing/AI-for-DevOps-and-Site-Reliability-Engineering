import numpy as np
from sklearn.metrics import confusion_matrix

# counts the number of true positives (y_true = 1, Y_pred = 1)
def find_TP(y_true, y_pred):
   return sum((y_true == 1) & (y_pred == 1))
# counts the number of false negatives (y_true = 1, Y_pred = 0) Type-II error
def find_FN(y_true, y_pred):
   return sum((y_true == 1) & (y_pred == 0))
# counts the number of false positives (y_true = 0, Y_pred = 1) Type-I error
def find_FP(y_true, y_pred):
   return sum((y_true == 0) & (y_pred == 1))
# counts the number of true negatives (y_true = 0, Y_pred = 0)
def find_TN(y_true, y_pred):
   return sum((y_true == 0) & (y_pred == 0))

def calculate_confusion_matrix(y_true, y_pred, labels=None):
    """
    Calculate the confusion matrix for a set of true labels and predicted labels.

    Parameters:
    y_true (list or np.array): True labels
    y_pred (list or np.array): Predicted labels
    labels (list): List of labels to index the matrix. This may be used to reorder or select a subset of labels.

    Returns:
    np.array: Confusion matrix
    """
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    return cm

def print_confusion_matrix(cm, labels):
    """
    Print the confusion matrix in a readable format.

    Parameters:
    cm (np.array): Confusion matrix
    labels (list): List of labels
    """
    print("Confusion Matrix:")
    print("Labels: ", labels)
    print(cm)

if __name__ == "__main__":
    # 0 - not anomaly
    # 1 - anomaly
    y_true = np.array([0, 1, 1, 1, 0, 1, 1, 1, 0, 1])
    y_pred = np.array([0, 1, 1, 1, 0, 0, 1, 1, 0, 1])
    labels = [0, 1 ]
    tp = find_TP(y_true, y_pred)
    tn = find_TN(y_true, y_pred)
    fn = find_FN(y_true, y_pred)
    fp = find_FP(y_true, y_pred)
    cm = calculate_confusion_matrix(y_true, y_pred, labels)
    print_confusion_matrix(cm, labels)
    print("TP: ", tp)
    print("TN: ", tn)
    print("FN: ", fn)
    print("FP: ", fp)
    print(f"Accuracy: {((tp + tn) / (tp + tn + fp + fn)):.2%}")
    print(f"Precision: {(tp / (tp + fp)):.2%}")
    print(f"Recall: {(tp / (tp + fn)):.2%}")
    print(f"F1-Score: {((2 * tp) / (2 * tp + fp + fn)):.2f}")