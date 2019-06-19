# Model criticism

Model criticism is necessary to validate that the model solves the task quite accurately and has the properties and functionality that were incorporated in it at the time of the development of the architecture. In the process of criticism, both the architecture of the model itself and cases of incorrect work are investigated and analyzed to find ways to further improvement.

Below are the stages of model criticism, for each of which there is a list of problems that can be detected on it:

## 1. Analysis of the architecture and training procedures

* **The presence of "dead" neurons**

When using the ReLU activation function, it is possible that a group of neurons ceases to be activated for all objects in the sample. This means that unnecessary calculations are made that do not affect the final result.

* **Missing model functionality**

There are architectures that, in addition to the predicted value, provide additional information about the model's behavior by adding some complications, such as the attention block modules. In some cases, this information does not allow for a better interpretation of the model, while it becomes more complicated, which negatively affects the time of training and inference.


## 2. Analysis of the model quality assessment procedure

* [**Invalid metric selection**](class_imbalance.ipynb)
In some cases, the selected metric does not reflect the real quality of the model, for example accuracy in the case of a strong imbalance of classes.

* **The instability of the metric value with repeated training of the model**

Randomness in the learning procedure can have a non-negligible impact on the value of the selected metric, so a single training of the model is not enough to determine the quality of the model, since the obtained value of the metric can be an outlier.


## 3. Analysis of  the incorrect predictions

* [**Not enough data augmentation**](data_augmentation.ipynb)<br>
The model may not be invariant to some transformations of the input data that may appear in the test set.

* [**Unnoticed class imbalance**](class_imbalance.ipynb)<br>
Due to a high class imbalance model can overfit and predict only majority classes while on some metrics this will be reflected slightly.

