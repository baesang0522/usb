Graph Neural Network
=============

Graph Neural Network(GNN)은 크게 세가지 부분으로 나눌 수 있음
1. Input layer
2. GNN layer
3. Multilayer Perceptron prediction layer(이 부분은 다른 형태의 네트워크로 대체 가능한 듯)


Input layer 는 GNN layer로 들어가는 graph data 의 초기 형태를 정의함. 
GNN layer 는 해당 정보를 받아 node 와 edge 의 정보를 업데이트 함.
Mlp prediction layer 는 특정 태스크를 수행함. node classification, link prediction 등 GNN layer 의 
output 을 이용하여 태스크 수행.

### 1. Input layer
앞서 언급했듯이 input layer 의 목적은 초기 네트워크 형태의 표현을 정의하는데에 있음.
```python
# one-hot vector 로 구성된 5개의 node 를 가지고 있는 graph 정의
import numpy as np

X = np.eye(5, 5)
n = X.shape[0]

np.random.shuffle(X)
print(X)

# output:
[[0., 0., 1., 0., 0.]  # Node 1
 [0., 0., 0., 1., 0.]  # Node 2
 [1., 0., 0., 0., 0.]  # ..
 [0., 0., 0., 0., 1.]  # ..
 [0., 1., 0., 0., 0.]] # Node 5
```
각 행은 graph 상의 node 정보를 의미. input layer 는 각 node 정보를 linear transform 함. 
```markdown
Y = WX + b
```
one hot vector 에선 bias value 를 사용하지 않으므로(Dwivedi et al., 2020) 선형 변환에서 고려하지 않음.
```python
# Dimension of the node features (embedding)
emb = 3

# Weight matrix (initialized according to Glorot & Bengio (2010))

W = np.random.uniform(-np.sqrt(1./emb), np.sqrt(1./emb), (n, emb))

# print(W)
[[-0.34857891, -0.5419972,   0.43603217]
 [ 0.26261991,  0.04720523, -0.42555547]
 [-0.09968833,  0.3218483,   0.09688095]
 [-0.36646565,  0.37652735, -0.45564272]
 [-0.24990413, -0.50164433, -0.51217414]]
L_0 = X.dot(W)
# print(L_0)
[[-0.09968833,  0.3218483,   0.09688095]
 [-0.36646565,  0.37652735, -0.45564272]
 [-0.34857891, -0.5419972,   0.43603217]
 [-0.24990413, -0.50164433, -0.51217414]
 [ 0.26261991,  0.04720523, -0.42555547]]
```
5차원 vector(one hot form) -> 3차원 feature vector(after linear projection)
> Paraphrasing Dwivedi et al.:
>    > The goal of the input layer is to embed the input features of nodes (and edges) 
       to a d-dimensional vector of hidden features. This new representation is obtained via
       a simple linear transformation (also known as projection).

현재 샘플들은 random 하게 생성된 샘플이기 때문에 별 의미가 없는 상태지만 two step 으로 업데이트 되게 됨.
* GNN layer 는 neighbor node 의 feature 들을 aggregation 함
* MLP layer 로 특정 task 에 대한 학습을 진행

이렇게 2단계 프로세스를 지나면 특정 task 에 적합하게 embedding 된 node 들의 특징들을 얻을 수 있음.

### 2. GNN layer
GNN layer 의 목적은 input layer 에서 얻은 D-dimensional representation 을 업데이트 하는 것.  
"recursive neighborhood diffusion(이웃 노드의 재귀적 확산?)" 으로 수행됨. 각 node 의 feature 들은
이웃 node feature 들을 이용하여 업데이트 됨. node 끼리 message 가 왔다갔다 하며 업데이트 한다고 생각하면
편함. adjacency matrix 를 이용하여 수행할 것.

```python
# Randomly generated adjacency matrix
A = np.random.randint(2, size=(n, n))
np.fill_diagonal(A, 1) # Include the self loop

# The following lines are a trivial ack to crate a symmetric
# Adj matrix that defines the edges of an undirected
# graph of 5 nodes
A = (A + A.T)
A[A>1] = 1
print(A)

# output:
[[1, 1, 1, 0, 1] # Connections to Node 1
 [1, 1, 1, 1, 1]
 [1, 1, 1, 1, 0]
 [0, 1, 1, 1, 0]
 [1, 1, 0, 0, 1]]
```
adjacency matrix 와 input layer 의 output(node vector 의 linear transform) 을 곱하면,

```python
# adjacency matrix
[[1, 1, 1, 0, 1] # Connections to Node 1
 [1, 1, 1, 1, 1]
 [1, 1, 1, 1, 0]
 [0, 1, 1, 1, 0]
 [1, 1, 0, 0, 1]]

# L_0: output from the input layer
[[-0.09968833,  0.3218483,   0.09688095]
 [-0.36646565,  0.37652735, -0.45564272]
 [-0.34857891, -0.5419972,   0.43603217]
 [-0.24990413, -0.50164433, -0.51217414]
 [ 0.26261991,  0.04720523, -0.42555547]]

L_1 = A.dot(L_0)

# print(L_1)
[[-0.55211298,  0.20358368, -0.34828506]
 [-0.8020171,  -0.29806065, -0.86045919]
 [-1.06463701, -0.34526588, -0.43490372]
 [-0.96494868, -0.66711419, -0.53178468]
 [-0.20353407,  0.74558089, -0.78431723]]

# print(L_0[0, :] + L_0[1, :] + L_0[2, :] + L_0[4, :])
[-0.55211298,  0.20358368, -0.34828506]

# print(L_1[0,:])
[-0.55211298,  0.20358368, -0.34828506] # node 1's aggregation
```
각 node 의 embedding 값과 adjacency matrix 를 행렬곱 하면 각 node 별 aggregation 값(neighbor 들의 값들이 
aggregation)이 나옴. 즉, local structure of graph 를 나타냄.  
  
key idea:  
만약 neural network 를 구성할 때 L 개의 layer 를 쌓는다고 가정. target node 의 값은 L-hop 에 있는
node 들의 특징을 aggregate 한 값이 됨. -> 정보 보존 이라고 생각하면 될 듯
> Dwivedi et al.
>    > Stacking L GNN layers allows the network to build node representation from L-hop 
       neighborhood of each node

GNN layer 는 다양한 알고리즘이 적용 가능함. CNN 같은 isotropic 한 알고리즘이나 Attention 같은 anisotropic
알고리즘 등.
