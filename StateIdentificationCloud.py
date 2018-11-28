import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg
import itertools
from matplotlib.patches import Ellipse
import matplotlib as mpl
from sklearn.mixture import GaussianMixture as GMM
from sklearn.decomposition import PCA
from sklearn.svm import LinearSVC

# df is the data file that is being manipulated

# Following function is from the scikit learn site on GaussianMixture model


def plot_results(X, Y_, means, covariances, title):  # add index between covariance and title if you want subplots.
    # splot = plt.subplot(2, 1, 1 + index)
    for i, (mean, covar, color) in enumerate(zip(
            means, covariances, color_iter)):
        v, w = linalg.eigh(covar)
        v = 2. * np.sqrt(2.) * np.sqrt(v)
        u = w[0] / linalg.norm(w[0])
        # as the DP will not use every component it has access to
        # unless it needs it, we shouldn't plot the redundant
        # components.
        if not np.any(Y_ == i):
            continue
        plt.scatter(X[Y_ == i, 0], X[Y_ == i, 1], .8, color=color)

        # Plot an ellipse to show the Gaussian component
        angle = np.arctan(u[1] / u[0])
        angle = 180. * angle / np.pi  # convert to degrees
        ell = mpl.patches.Ellipse(mean, v[0], v[1], 180. + angle, color=color)
        # ell.set_clip_box(splot.bbox)
        ell.set_alpha(0.5)
        # splot.add_artist(ell)

    plt.xlim(-9., 5.)
    plt.ylim(-3., 6.)
    plt.xticks(())
    plt.yticks(())
    plt.title(title)
    plt.axis('on')

# Pearson Correlation Coefficient Feature Selection Begins


df = pd.read_excel('Matthew_Data.xlsx')  # Import the initial data sheet from excel
R_raw = df  # Store the initial data sheet as a separate variable
corr_mat = R_raw.corr().abs()  # Makes a correlation matrix given the data sheet, converts to absolute values

# Plot the first correlation matrix
plt.figure(1)
plt.matshow(corr_mat, fignum=1)
plt.title("Correlation Matrix Before Feature Selection Using PCC")
plt.xlabel("Features")
plt.ylabel("Features")

AvgCorr = corr_mat.mean()  # Calculates the average
# Set the upper triangle and diagonal of correlation matrix to NaN, negating duplicate pairs
corr_mat.values[np.triu_indices_from(corr_mat, 0)] = np.nan
# Set any ppc value under or equal to 0.9 to Nan, leaving only pairs correlated above 0.9
corr_mat = corr_mat.where(corr_mat > 0.9)
# Turns python data frame into a series, stacks data and removes all NaN values
s = corr_mat.stack()
so = s.sort_values(kind="quicksort")  # Sorts the values in ascending order
drop_columns = set()  # Creates a set that will hold the names of the features to be dropped

for x, val in so.iteritems():  # Iterates through correlation pairs > 0.9
    # Features average correlations are compared; feature with higher average correlation is dropped
    if AvgCorr[x[0]] > AvgCorr[x[1]]:
        drop_columns.add(x[0])
    else:
        drop_columns.add(x[1])

df = df.drop(drop_columns, axis=1)
X = df
# Plots the new correlation matrix after feature selection has been performed
plt.figure(2)
plt.matshow(df.corr().abs(), fignum=2)
plt.title("Correlation Matrix After Feature Selection Using PCC")
plt.xlabel("Features")
plt.ylabel("Features")

plt.show()


# PCA Block Begins

pca = PCA(n_components=6, whiten=False, svd_solver='full')
pca.fit(df)       # fit the model with data
transform = pd.DataFrame(pca.fit_transform(df))  # apply the dimensionality reduction on data

components = pca.components_
##########################################################################

# Work in Progress:
slope = np.diff(pca.explained_variance_, n=1)
slopeOfSlope = np.diff(pca.explained_variance_, n=2)
cnt = 0
num_components = 1
while cnt < (len(slope) - 1):
    if (abs(slopeOfSlope[cnt - 1]) - abs(slopeOfSlope[cnt])) <= 0.0001:
        cnt = len(np.diff(pca.explained_variance_, n=2))
    num_components = cnt + 1
    cnt = cnt + 1

##########################################################################

invTran = pd.DataFrame(pca.inverse_transform(transform))

fig = plt.figure(num=None, figsize=(26, 12), dpi=80, facecolor='w', edgecolor='k')
fig.suptitle('PCA Component Scatter Plots', fontsize=16)

plt.subplot(2, 2, 1)
plt.scatter(df.iloc[1:, 0], df.iloc[1:, 1], c='blue', alpha=0.2)  # scatter plot: first two components in data file
plt.scatter(invTran.iloc[:, 0], invTran.iloc[:, 1], c='red', alpha=0.8)  # scatter plot: component 1 and 2 after PCA
plt.axis('equal')
plt.xlabel("Decomposed Feature1")
plt.ylabel("Decomposed Feature2")

plt.subplot(2, 2, 2)
plt.scatter(df.iloc[1:, 0], df.iloc[1:, 1], c='red', alpha=0.2)  # line 62-75 scatter plot:
plt.scatter(df.iloc[1:, 2], df.iloc[1:, 3], c='red', alpha=0.2)  # all 26 components in data file
plt.scatter(df.iloc[1:, 4], df.iloc[1:, 5], c='red', alpha=0.2)
plt.scatter(df.iloc[1:, 6], df.iloc[1:, 7], c='red', alpha=0.2)
plt.scatter(df.iloc[1:, 8], df.iloc[1:, 9], c='red', alpha=0.2)
plt.scatter(df.iloc[1:, 10], df.iloc[1:, 11], c='red', alpha=0.2)
plt.scatter(df.iloc[1:, 12], df.iloc[1:, 13], c='red', alpha=0.2)
plt.scatter(df.iloc[1:, 14], df.iloc[1:, 15], c='red', alpha=0.2)
plt.scatter(df.iloc[1:, 16], df.iloc[1:, 17], c='red', alpha=0.2)
plt.scatter(df.iloc[1:, 18], df.iloc[1:, 19], c='red', alpha=0.2)
plt.scatter(df.iloc[1:, 20], df.iloc[1:, 21], c='red', alpha=0.2)
plt.scatter(df.iloc[1:, 22], df.iloc[1:, 23], c='red', alpha=0.2)
plt.scatter(df.iloc[1:, 24], df.iloc[1:, 25], c='red', alpha=0.2)
plt.scatter(invTran.iloc[:, 2], invTran.iloc[:, 3], c='blue', alpha=0.5)  # scatter plot: component 1 and 2 after PCA
plt.axis('equal')
plt.xlabel("Decomposed Feature3")
plt.ylabel("Decomposed Feature4")

plt.subplot(2, 2, 3)
plt.scatter(df.iloc[1:, 0], df.iloc[1:, 1], c='cyan', alpha=0.2)  # scatter plot: first two components in data file
plt.scatter(invTran.iloc[:, 4], invTran.iloc[:, 5], c='red', alpha=0.8)  # scatter plot: component 1 and 2 after PCA
plt.axis('equal')
plt.xlabel("Decomposed Feature5")
plt.ylabel("Decomposed Feature6")

plt.show()


# The following code fits a GaussianMixture model on the cleaned data and graphs it.
GaussianMix = GMM(n_components=2,covariance_type='full',max_iter=800,init_params='random').fit(df)
color_iter = itertools.cycle(['navy', 'c'])
# plot_results(np.array(df), GaussianMix.predict(df), GaussianMix.means, GaussianMix.covariances_,"Gaussian Mixture")
# plt.show()


# Support Vector Machine Code
y = GaussianMix.predict(df)
clf = LinearSVC()
clf.fit(X, y)

Y = clf.predict(X)
num = 0
for index in range(0, len(Y)):
    if Y[index] == y[index]:
        num += 1

print(num/len(Y) * 100)
