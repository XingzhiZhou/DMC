# DMC: Deep Multidimensional Clustering

This repository aims to provides items about deep multimensional clustering(DMC), such as datasets, typical training processes, evaluation protocol etc. 

[toc]

## What is DMC?

Deep multimensional clustering targets at multiple non-redundant partitions of unlabeled images with power of deep architectures that model non-linear similarity between images along different axes. For instance, we can group the figures based on the object meaning, environment, shape, color, material etc. 

## Why DMC?

DMC can extract more visual information than a single clustering that cares only about semantic meaning. With the use of  DMC, many applications are benefited, such as image search, video search, video recommendation, etc. 

## How DMC?  

19NeurIPSWorkshop Disentangling to Cluster Gaussian Mixture Variational Ladder Autoencoders

19 ICLR: LTVAE Learning Latent Superstructures in Variational Autoencoders for Deep Multidimensional Clustering

21 NeurIPS: MFCVAE Multi-Facet Clustering Variational Autoencoders



## Related Multidimension clustering  Literature

18 KDD: Discovering Non-Redundant K-means Clusterings in Optimal

19 AAAI: Multiple Independent Subspace Clusterings

19 IEEE: TRANSACTIONS ON CYBERNETICS: Discovering_Multiple_Co-Clusterings_With_Matrix_Factorization

20 AAAI: Multi-view multiple clusterings using deep matrix factorization

20 AAAI: Deep Embedded Non-Redundant Clustering

20 ICDM: Deep Incomplete Multi-view Multiple Clusterings

20 TKDD: Non-Redundant Subspace Clusterings with Nr-Kmeans

21 IJIS: Multipartition clustering of mixed data with Bayesian networks

21 MachineLearning: Multiple Clusterings Of Heterogenous information Netiworks

## DMC Datasets

There are some existing datasets for DMC, such as 

- [3DShapes](https://github.com/deepmind/3d-shapes) : 480000 Images with 6 labels for each single image.
- [Microsoft COCO](https://cocodataset.org/#home) : 330K images (>200K labeled), 5 captions per image

Here, we propose a new approach of image stitching to produce the datasets for multidimension clustering. CIFAR-100 is chosen as a base dataset. To forge a new figure, we randomly select four pictures in the base dataset and combine them as a $2\times2$ large picture. These four pictures are randomly choosen from 4 random categories. This approach can be repeated to get pictures with multiple captions such that be suitable for DMC. The corresponding code is on generate_grid_img.py

Through the approach above, we create the datasets at [baidu cloud link](https://pan.baidu.com/s/1oy9-h19yqF-OBAeIhCpCog?pwd=kybm). Following are some examples in the datasets

![image](https://github.com/XingzhiZhou/DMC/blob/master/imgs/grid0.jpg) 

![image](https://github.com/XingzhiZhou/DMC/blob/master/imgs/grid1.jpg)

![image](https://github.com/XingzhiZhou/DMC/blob/master/imgs/grid2.jpg)

![image](https://github.com/XingzhiZhou/DMC/blob/master/imgs/grid3.jpg)



## DMC Evaluation Protocols

NMI: normalized mutual information. 

ACC: Accuracy of clustering results after optimal matching through NMI.

