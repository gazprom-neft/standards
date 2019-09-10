import os

import re
import glob
import dill

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error


plt.style.use('ggplot')


def show_samples(image_rows, p_true=None, p_pred=None, labels=None, figsize=None,
                 show_grid=False, row_titles=None):
    """Show images and masks."""
    if isinstance(image_rows, (list, tuple)):
        nrows = len(image_rows)
        ncols = len(image_rows[0])
    else:
        nrows = 1
        ncols = len(image_rows)
        image_rows = (image_rows,)
    if figsize is None:
        figsize = (3 * ncols, 3 * nrows)

    fig, big_axes = plt.subplots(nrows, 1, sharey=True, figsize=figsize)
    if nrows == 1:
        big_axes = (big_axes, )
    for row, big_ax in enumerate(big_axes, start=1):
        if row_titles is not None:
            big_ax.set_title(row_titles[row - 1], fontsize=16)
        big_ax.tick_params(labelcolor=(1, 1, 1, 0),
                           top='off', bottom='off', left='off', right='off')
        big_ax._frameon = False

    for i in range(nrows):
        for k in range(ncols):
            ax = fig.add_subplot(nrows, ncols, 1 + i * ncols + k)
            ax.imshow(image_rows[i][k])
            ax.grid(show_grid)
            if p_true is not None:
                ax.scatter(*p_true[k][::-1], color="green")
            if p_pred is not None:
                ax.scatter(*p_pred[k][::-1], color="red")
            if labels is not None:
                ax.set_title(labels[k])
    plt.tight_layout()
    plt.show()


def show_loss(loss, skip=0, figsize=None):
    """Show loss function."""
    if figsize is None:
        fogsize = (5, 3)
    plt.figure(figsize=figsize)
    x = np.arange(skip, len(loss))
    plt.plot(x, loss[skip:])
    plt.ylabel("Loss Function")
    plt.xlabel("Iteration")
    plt.show()


def show_histogram(arr, bins=10, figsize=None):
    """Show historgam."""
    if figsize is None:
        fogsize = (5, 3)
    plt.figure(figsize=figsize)
    plt.hist(arr, bins=bins)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.show()


def class_histogram(train, test):
    """Show distribution of classes in train and test."""
    train_labels, train_counts = np.unique(train.labels, return_counts=True)
    test_labels, test_counts = np.unique(test.labels, return_counts=True)
    plt.bar(train_labels, test_counts, label="Test")
    plt.bar(test_labels, train_counts, bottom=test_counts, label="Train")
    plt.xlabel("Category")
    plt.ylabel("Frequency")
    plt.legend()
    plt.show()


def class_precision(confusion_matrix):
    """Show class precision given by confusion matrix."""
    cfm = confusion_matrix
    plt.bar(np.arange(len(cfm)), cfm.diagonal() / (cfm.diagonal() + np.triu(cfm, 1).sum(axis=1)))
    plt.xticks(np.arange(len(cfm)))
    plt.xlabel("Category")
    plt.ylabel("Precision")
    plt.show()


def show_research(df, layout=None, average_repetitions=False, log_scale=False, rolling_window=None):
    """Show plots given by research dataframe."""
    if layout is None:
        layout = []
        for nlabel, ndf in df.groupby("name"):
            ndf = ndf.drop(['config', 'name', 'iteration', 'repetition'], axis=1).dropna(axis=1)
            for attr in ndf.columns.values:
                layout.append('/'.join([str(nlabel), str(attr)]))
    if type(log_scale) is bool:
        log_scale = [log_scale] * len(layout)
    if (type(rolling_window) is int) or (rolling_window is None):
        rolling_window = [rolling_window] * len(layout)
    rolling_window = [x if x is not None else 1 for x in rolling_window]

    fig, ax = plt.subplots(1, len(layout), figsize=(9 * len(layout), 7))
    if len(layout) == 1:
        ax = (ax, )

    for i, (title, log, rw) in enumerate(list(zip(*[layout, log_scale, rolling_window]))):
        name, attr = title.split('/')
        ndf = df[df['name'] == name]
        for clabel, cdf in ndf.groupby("config"):
            cdf = cdf.drop(['config', 'name'], axis=1).dropna(axis=1).astype('float')
            if average_repetitions:
                idf = cdf.groupby('iteration').mean().drop('repetition', axis=1)
                y_values = idf[attr].rolling(rw).mean().values
                if log:
                    y_values = np.log(y_values)
                ax[i].plot(idf.index.values, y_values, label=str(clabel))
            else:
                for r, rdf in cdf.groupby('repetition'):
                    rdf = rdf.drop('repetition', axis=1)
                    y_values = rdf[attr].rolling(rw).mean().values
                    if log:
                        y_values = np.log(y_values)
                    ax[i].plot(rdf['iteration'].values, y_values,
                               label='/'.join([str(r), str(clabel)]))
        ax[i].set_xlabel('iteration')
        ax[i].set_title(title)
        ax[i].legend()
    plt.show()
