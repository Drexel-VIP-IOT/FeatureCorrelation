import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

xlsx = pd.ExcelFile('adib_data.xlsx')
data = pd.read_excel(xlsx, 'AE_Data')  # reads the named excel spreadsheet

pca = PCA(n_components=6, whiten=False, svd_solver='full')
pca.fit(data)       # fit the model with data
transform = pd.DataFrame(pca.fit_transform(data)) # apply the dimensionality reduction on data



components = pca.components_
##########################################################################
#Work in Progress:
slope = np.diff(pca.explained_variance_, n=1)
slopeOfSlope = np.diff(pca.explained_variance_, n=2)
cnt = 0;
num_components = 1
while cnt < (len(slope) - 1):
    if (abs(slopeOfSlope[cnt - 1]) - abs(slopeOfSlope[cnt])) <= 0.0001:
        cnt = len(np.diff(pca.explained_variance_, n=2))
    num_components = cnt + 1
    cnt = cnt + 1

###########################################################################

invTran = pd.DataFrame(pca.inverse_transform(transform))

fig = plt.figure(num=None, figsize=(26, 12), dpi=80, facecolor='w', edgecolor='k')
fig.suptitle('PCA Component Scatter Plots', fontsize=16)

plt.subplot(2, 2, 1)
plt.scatter(data.iloc[1:, 0], data.iloc[1:, 1], c='blue', alpha=0.2)  # scatter plot: first two components in data file
plt.scatter(invTran.iloc[:, 0], invTran.iloc[:, 1], c='red', alpha=0.8)  # scatter plot: component 1 and 2 after PCA
plt.axis('equal')
plt.xlabel("Decomposed Feature1")
plt.ylabel("Decomposed Feature2")

plt.subplot(2, 2, 2)
plt.scatter(data.iloc[1:, 0], data.iloc[1:, 1], c='red', alpha=0.2)  # line 62-75 scatter plot:
plt.scatter(data.iloc[1:, 2], data.iloc[1:, 3], c='red', alpha=0.2)  # all 26 components in data file
plt.scatter(data.iloc[1:, 4], data.iloc[1:, 5], c='red', alpha=0.2)
plt.scatter(data.iloc[1:, 6], data.iloc[1:, 7], c='red', alpha=0.2)
plt.scatter(data.iloc[1:, 8], data.iloc[1:, 9], c='red', alpha=0.2)
plt.scatter(data.iloc[1:, 10], data.iloc[1:, 11], c='red', alpha=0.2)
plt.scatter(data.iloc[1:, 12], data.iloc[1:, 13], c='red', alpha=0.2)
plt.scatter(data.iloc[1:, 14], data.iloc[1:, 15], c='red', alpha=0.2)
plt.scatter(data.iloc[1:, 16], data.iloc[1:, 17], c='red', alpha=0.2)
plt.scatter(data.iloc[1:, 18], data.iloc[1:, 19], c='red', alpha=0.2)
plt.scatter(data.iloc[1:, 20], data.iloc[1:, 21], c='red', alpha=0.2)
plt.scatter(data.iloc[1:, 22], data.iloc[1:, 23], c='red', alpha=0.2)
plt.scatter(data.iloc[1:, 24], data.iloc[1:, 25], c='red', alpha=0.2)
plt.scatter(invTran.iloc[:, 2], invTran.iloc[:, 3], c='blue', alpha=0.5)  # scatter plot: component 1 and 2 after PCA
plt.axis('equal')
plt.xlabel("Decomposed Feature3")
plt.ylabel("Decomposed Feature4")

plt.subplot(2, 2, 3)
plt.scatter(data.iloc[1:, 0], data.iloc[1:, 1], c='cyan', alpha=0.2)  # scatter plot: first two components in data file
plt.scatter(invTran.iloc[:, 4], invTran.iloc[:, 5], c='red', alpha=0.8)  # scatter plot: component 1 and 2 after PCA
plt.axis('equal')
plt.xlabel("Decomposed Feature5")
plt.ylabel("Decomposed Feature6")

plt.show()

