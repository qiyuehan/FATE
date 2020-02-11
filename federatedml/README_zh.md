## 联邦机器学习

Federatedml模块包括许多常见机器学习算法的实现，以及必要的实用工具。 所有模块均采用去耦的模块化方法开发，以增强模块的可扩展性。 具体来说，我们提供：

1. 联邦学习算法：提供数据输入/输出，数据预处理，特征工程和建模的联邦学习算法。 下面列出了更多详细信息。

2. 实用性工具：提供用于支持联邦学习的工具，例如加密工具，统计模块，参数定义和传递变量的自动生成器等。

3. 框架：用于开发新算法模块的工具包和基本模型。 框架提供了可重用的函数，以使各模块标准化，并让模块之间更加紧凑。

4. 安全协议：提供了多种安全协议，以进行更安全的多方交互计算。

![federatedml_structure](/Users/jsy/Downloads/federatedml_structure.png)

<center>Figure 1： Federated Machine Learning Framework</center>
## 算法清单

1. **DataIO**

该组件通常是建模任务的第一个组件。 它将用户上传的数据转换为Instance对象，该对象可用于以下组件。

+ 对应模块名称：DataIO
+ 数据输入：DTable，值为原始数据
+ 数据输出：转换后的数据表，值为在`federatedml/feature/instance.py`中定义的Data Instance的实例

2. **Intersect**

计算两方的相交数据集，而不会泄漏任何差异数据集的信息。 主要用于纵向任务。

+ 对应模块名称：Intersection
+ 数据输入：DTable
+ 数据输出：两方DTable中相交的部分

3. **Federated Sampling**

对数据进行联邦采样，使得数据分布在各方之间变得平衡。这一模块同时支持单机和集群版本。

+ 对应模块名称：FederatedSample
+ 数据输入：DTable
+ 数据输出：采样后的数据，同时支持随机采样和分层采样

4. **Feature Scale**

特征归一化和标准化。

+ 对应模块名称：FeatureScale
+ 数据输入：DTable，其值为instance
+ 数据输出：转换后的DTable
+ 模型输出：变换系数，例如最小值/最大值，平均值/标准差

5. **Hetero Feature Binning**

使用分箱的输入数据，计算每个列的iv和woe，并根据合并后的信息转换数据。

+ 对应模块名称：Hetero Feature Binning
+ 数据输入：DTable，在guest中有标签y，在host中没有标签y
+ 数据输出：转换后的DTable
+ 模型输出：每列的iv/woe，分裂点，事件计数，非事件计数等

6. **OneHot Encoder**

将一列转换为One-Hot格式。

+ 对应模块名称：OneHotEncoder
+ 数据输入：DTable
+ 数据输出：转换了带有新列名的DTable
+ 模型输出：原始列名和特征值到新列名的映射

7. **Hetero Feature Selection**

提供多种类型的filter。每个filter都可以根据用户配置选择列。

+ 对应模块名称：HeteroFeatureSelection
+ 数据输入：DTable
+ 模型输入：如果使用iv filters，则需要hetero_binning模型
+ 数据输出：转换的DTable具有新的header和已过滤的数据实例
+ 模型输出：每列是否留下

8. **Union**

将多个数据表合并成一个。

+ 对应模块名称：Union
+ 数据输入：DTables
+ 数据输出：多个Dtables合并后的Dtable

9. **Hetero-LR**

通过多方构建纵向逻辑回归模块。

+ 对应模块名称：HeteroLR
+ 数据输入：DTable
+ 模型输出：Logistic回归模型

10. **Local Baseline**

使用本地数据运行sklearn Logistic回归模型。

+ 对应模块名称：LocalBaseline
+ 数据输入：DTable
+ 模型输出：Logistic回归

11. **Hetero-LinR**

通过多方建立纵向线性回归模块。

+ 对应模块名称：HeteroLinR
+ 数据输入：DTable
+ 模型输出：线性回归模型

12. **Hetero-Poisson**

通过多方构建纵向泊松回归模块。

+ 对应模块名称：HeteroPoisson
+ 数据输入：DTable
+ 模型输出：泊松回归模型

13. **Homo-LR**

通过多方构建横向逻辑回归模块。

+ 对应模块名称：HomoLR
+ 数据输入：DTable
+ 模型输出：Logistic回归模型

14. **Homo-NN**

通过多方构建横向神经网络模块。

+ 对应模块名称：HomoNN

+ 数据输入：DTable
+ 模型输出：神经网络模型

15. **Hetero Secure Boosting**

通过多方构建纵向Secure Boost模块。

+ 对应模块名称：HeteroSecureBoost
+ 数据输入：DTable，其值为instance
+ 模型输出：SecureBoost模型，由模型本身和模型参数组成

16. **Evaluation**

为用户输出模型评估指标。

+ 对应模块名称：Evaluation

17. **Hetero Pearson**

计算来自不同方的特征的纵向关联。

+ 对应模块名称：HeteroPearson

18. **Hetero-NN**

构建纵向神经网络模块。

+ 对应模块名称：HeteroNN

+ 数据输入：DTable
+ 模型输出：纵向神经网络模型