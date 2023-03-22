The Forward-Forward Algorithm
=============

## abstract
기존 방식은 forward-backward 방식. 오류를 역전파(backpropagation) 함으로써 가중치들을 업데이트 함. 본 연구에선 Forward-Forward(FF) 
방식을 제안. 2 way forward pass(positive, negative dataset. 네트워크에서 생성됨) 로 forward-backward 효과를 낼 것임.  

각 네트워크 레이어는 목적함수를 가지고 있고 positive data에는 좋은 점수, negative data에는 낮은 점수를 그 목표로 함. 
positive way 와 negative way 가 분리될 수 있다면 negative way 는 오프라인으로 할 수 있고, 미분하느라(backpropagation) 
시간을 허비하지 않을 수 있음(backward 하느라 학습을 멈추지 않아도 됨) <br>

## 1. Backpropagation의 문제점
* Stochastic gradient descent는 딥러닝의 성공에 많은 영향을 끼침
* time sequence 방식이든, 이미지든 역전파는 실제 뉴런이 배우는 방식과는 다름(뉴런이 backward pass를 사용한다고 할 수 없음)
* top-down 방식(backpropagation)은 이후 레이어가 이전 레이어에 영향을 미치지만, 실제 인간의 지각능력은 실시간으로 작동함
* 역전파의 큰 문제점은 올바른 미분값을 구하기 위해선 forward pass에서의 계산 방법을 완벽히 알아야 한다는 점임.
  블랙 박스를 input으로 할 때 블랙 박스가 어떤식으로 forward pass 되는 지 모른다면 역전파도 할 수 없음.
* 완벽한 forward pass 모델이 존재하지 않기 때문에 강화학습시 매번 다른 모델이 선택됨(수많은 매개변수의 섭동 때문).
  하지만 이러한 상황을 average하기 위해선 learning rate 가 parameter 수에 반비례 해야 
  하는데(작은 learning rate) 이렇게 되면 학습 시 비용이 커짐. 이러한 이유로 거대한 모델에선 Backpropagation과 비교할 순 없음. 
* 이번 연구의 요점은 비선형성을 포함한 인공신경망 모델들이 이런 기법들에 의지하지 않아도 된다는 것. FF 방식은 Backpropagation보다 
  속도면에서는 비슷하지만 모델의 정확한 계산방식(e.g. RNN, CNN 이 forward시 계산 방식이 다름)을 몰라도 작동한다는 데에 있음.
* 논문에서 테스트한 바에 의하면 FF방식이 역전파보다 빠른 것이 아님. 매우 큰 데이터셋으로 학습된 매우 큰 모델들은 계속 역전파를 
  사용할 것으로 보임. 
* 하지만 FF방식은 두가지 측면에서 장점을 보일 것 같은데 model이 cortex상에서 학습되는 경우, low power hardware에서 학습되는 경우.

## 2. Forward-Forward 알고리즘
FF 알고리즘은 [볼츠만 머신](https://idplab-konkuk.tistory.com/14) 과 [Noise Contrastive Estimation](https://nuguziii.github.io/survey/S-006/) 
에 영감을 받아 탄생한 탐욕적 멀티 레이어 절차(greedy multi-layer procedure). 
forward-backward 방식을 대체하기 위해 제안되었으며 두 개의 forward(positive, negative pass)는 같은 방향으로, 다른 데이터를 가지고, 
다른 목적을 위해 forward pass 됨.
positive 는 real data 를 이용하여 각 레이어의 weight 를 모델 성능(goodness)을 올리기 위해 pass 되고 negative 는 "negative data"를 
이용하여 각 히든 레이어의 성능을 낮추기 위해(과적합 방지?) pass 됨. 본 논문에선 두가지 성능측정 방법을 살펴봄.   
```
1. sum of squared neural activities
2. negative sum of squared neural activities.
```
logistic function 이 적용된 input vector 가 positive 일 떄, 이 값이 positive 인지 negative 인지 잘 분류하는 것이 목적임.   
![p(positive)](Forward_Forward/FF_images/p(positive).png)  
싱글 hidden layer 에서 해당식의 결과가 높으면 positive, 낮으면 negative 하게 함. hidden layer 가 두개 이상일 때, 두번째 히든레이어에 
들어가는 input 이 단순 첫번째 hidden layer 의 아웃풋(length of activity vector in first hidden layer)일 경우 두번째 
히든 레이어의 작업은 의미가 없음(같은 행동(같은 벡터, 같은 활성화 함수)을 하는 것이기 때문이라고 생각. 같은 정보 사용). 
이를 해결하기 인풋 벡터들을 다 normalize 해줌 (Ba et al., 2016b; Carandini and Heeger, 2013) . 
이 행동은 first hidden layer에서 goodness 정보를 얻기 위한 작업에서 사용된 information 들과는 다른 정보들을 이용, goodness를 판단하는 역할을 할 듯.
다시 말하면, 첫번째 first hidden layer 에선 activity vector 의 길이와 방향이 goodness 를 판단하는데 사용되고 다음 레이어 부턴
방향만이 그 역할을 함

## 3. FF 알고리즘을 이용한 몇가지 시험
상대적으로 작은 네트워크(몇백만 정도의 연결)에서 유용하다는 것을 보일 것임. 큰 네트워크에서의 실험은 후속 논문에서.

### 3.1 베이스라인(Backpropagation)
Backpropagation 사용시 MNIST 는 약 1.4% 의 테스트 에러를 가진다고 설정.  

### 3.2 simple unsupervised example of FF 
FF 알고리즘이 해결해야 하는 두가지 질문이 있음.  
1. 좋은 negative data 가 있다면 모델이 특징을 잘 잡아 낼까?
2. negative data 는 어디서 오는가? 어디서 구할까?  
  
지도학습에서 [contrastive learning](https://daebaq27.tistory.com/97) 을 사용하는 방법은 첫째, input vector 를 라벨이나 기타 
정보 없이 representation vector 로 선형 변환하는 법을 학습함. 이렇게 변형된 vector 들을 이용해 logit vector 화 하는 방법을 학습함.
이 logit vector 는 softmax 를 이용, 라벨 별 확률 분포를 계산할 때 사용
이렇게 linear transformation 부터 logit 까지 학습하는 부분은 supervised 지만 hidden layer 를 사용하지 않고 따라서 backpropagation 도 
사용하지 않음. FF 알고리즘은 이러한 학습 방법을 이용, real data vector 를 positive example 에서, corrupted data vectors 를 negative example
에서 학습함. data를 오염(corrupt)시키기 위한 방안은 다양함.  
FF 알고리즘이 (특성화 된)이미지 상의 longer range correlation 에 집중하게 하기 위해서는 very different long range correlation 을 가지고
similar short range correlation 을 가진 이미지를 만들어야 함(corrupt image data).  
![figure1](Forward_Forward/FF_images/figure1.png)  

  
fully connected 에선 test error 1.37%, local receptive fields( without weight-sharing) 에선 1.16% 달성.  
  
### 3.3 A simple supervised example of FF
라벨 정보 없이 숨겨진 정보를 학습하는 것은 다양한 task 를 수행하는 큰 모델에서 합리적임. 비지도학습으로 잡다한 feature 들을 선발하고 
다양한 task 에서 유용한 정보들을 모델에서 선별해서 사용할 수 있기 때문(3.2 unsupervised). 하지만 하나의 task 를 수행하는 모집단의 분포를 모르는
작은 모델에선 지도학습을 사용하는 것이 합리적임.  
  
input 에 라벨을 포함(positive-correct, negative-incorrect)시켜서 학습시키는 방법으로 이를 달성할 수 있음. 라벨 분류에 필요없는 정보는 
모델이 무시하게 될 것임.  
  
60 epochs 에서 test error 1.36%(FF), backpropagation 은 20 epochs 에서 비슷한 성능 달성. Learning rate 를 2배로 높였을 땐 
60 epochs 에서 test error 1.46%.
  
각 이미지의 처음 10 픽셀에는 라벨 정보(MNIST 므로 10개. 각 0.1)가 들어감.  
![figure2](Forward_Forward/FF_images/figure2.png)

첫번째 히든 레이어를 제외한 나머지 히든 레이어에는 훈련시 학습된 softmax 에 입력값들이 들어감. 예측이 빠르지만 차선책. 첫번째 히든 레이어를 제외한
나머지 계층에서 나온 goodness 를 축적하여 판별하는 것이 베스트. 라벨별로 이 학습 방법을 사용하고(MNIST 이므로 X 10번) 중립라벨이 hard negative label 
을 pick 하는 방식으로 하면 epoch 수가 33% 가량 높아짐(학습이 더 어렵다는 의미인듯).
  
data augmentation 사용 500 epochs 학습 시 0.64% test error 발생. CNN(using backpropagation)과 성능 비슷  

### 3.4 Using FF to model top-down effects in perception
FF 알고리즘의 경우 한번에 하나의 레이어에서 탐욕적으로 학습하기 때문에 뒤쪽 레이어에서 학습된 것이 앞쪽 레이어에 영향을 줄 수 없음.  

이러한 문제점을 해결하기 위해 Multi layer RNN 처럼 네트워크를 구성하기로 함(input 되는 image 를 video 처럼 생각하여).  
![figure3](Forward_Forward/FF_images/figure3.png)  
8번 iteration 을 돌리고, 3~5 번의 iteration 에서 가장 높은 goodness 를 보이는 label 을 선택하는 방식으로 1.31% 의 테스트 에러를 얻음. 
Negative data 는 single forward pass 후 incorrect classes 확률을 보고 생성하는 방식으로 결정 됨. 이 방식은 학습을 효율적이게 함.

### 3.5 Using predictions from the spatial context as a teacher
top-down 입력은 이미지의 더 넓은 부분을 보고 판단하는 것. bottom-up 방식은 이미지의 좁은 부분을 보고 판단. 따라서 top-down 방식은 
bottom-up 방식의 contextual prediction 이라고 볼 수 있음(figure3 에서 내려오는 빨간 화살표, 올라가는 파란 화살표). 따라서 top-down 은
bottom-up 에서 올라오는 input 에서 특징 예측하는 것을 배울 것이고, 목적함수가 low squared 로 바뀐다면(positive 예측 못하게) top-down 은
bottom-up 에서 올라오는 input 을 무시하는 것을 배울 것. layer normalization 은 다음 레이어로 전달되는 정보량이 많아지게 함. 
노이즈에 강해짐.

### 4. Experiments with CIFAR-10  
CIFAR-10 데이터셋을 이용한 테스트. 32*32*3 형태.  
![table1](Forward_Forward/FF_images/table1.png)  
기본 DNN + weight decay. test 시 single forward pass(학습된 softmax 사용, table1 상의 one-pass softmax)는 빠르지만 
반복-평균(goodness 평균)보단 test loss 가 높았다. 또한 backpropagation 은 training loss 가 FF 보다 빠르게 감소(학습이 빨랐다?)했다.

### 5. Sleep
biological model 로서의 FF 알고리즘에 대한 해결점. positive pass 와 negative pass 를 분리하면 어떤 효과가 날지 등.

### 6. How FF relates to other contrastive learning techniques
### 6.1 Relationship to Boltzmann Machines
[볼츠만 머신 설명](https://helpingstar.github.io/dl/other_network/)  

large network 에서 균형 상태에 도달하기 어려운 등의 단점에도 불구하고 볼츠만 머신에선 forward-backward 프로세스를 iteration 으로 대체
한다는 것에 의의가 있음.  
FF 알고리즘은 볼츠만 머신의 Contrastive learning 기법과 local goodness 함수(볼츠만 머신의 energy 계산보다 다루기 쉬운)를 결합함


### 6.2 Relationship to Generative Adversarial Networks
Generative Adversarial Network(GAN)은 생성모델과 식별모델이 구분된 생성모델. 두 개체가 경쟁하며 진짜같은 데이터를 생성해냄. 
multilayer backpropagation 사용. 학습이 까다로움.  
FF 알고리즘은 모든 히든 레이어에서 탐욕적 선택을 하는(positive 인지 negative 인지 판단하는) GAN 의 특이케이스라고 볼 수 있는데 
이런 기능을 함으로서 역전파를 이용, 식별모델을 따로 학습할 필요가 없어짐. 생성모델도 역전파를 이용하여 학습할 필요가 없는데 생성을 위한 
특징(representative)을 자체 학습하는 것 보다 식별모델에서 학습된 특징을 가져다가 학습하면 그만이기 때문. 생성모델이 학습해야 
하는 부분은 "이 특징에서 어떻게 데이터를 만들어낼 수 있는가" 임. 만들어 냈다면 softmax 의 logit 을 계산하기 위한 linear transform 에서는
역전파가 필요가 없음(학습할 필요가 없음). FF 알고리즘은 두 모델에서 같은 특징을 이용하기 때문에 
한 모델이 다른 모델에 비해 빨리 학습하는 GAN 의 문제점을 해결할 수 있음.

### 6.3 Relationship to contrastive methods that compare representations of two different image crops
현재 contrastive method 를 사용한 image crop 알고리즘 중 하나인 SimCLR 과 FF 와의 비교. FF 가 비교 우위에 있다는 내용. 
이 부분은 관심이 없어 pass 함

### 6.4 A problem with stacked contrastive learning
Restricted Boltzmann machines(RBM), stacked autoencoder 등 first layer 에서 특징을 잡아내고 이 특징이 그대로 다음 레이어 input으로
들어가는 알고리즘등이 있음. random noise 를 포함한 이미지를 random weight matrix 에 통과시킬 때, output 벡터들은 실 데이터 보단
weight matrix 와 상관이 더 큼. 비지도 학습이 학습 데이터 상에서 어떤 구조를 발견했다 하더라도 이게 실 세계에서도 나타나는 특징이라곤 
할 수 없음 -> fatal flaw.  
  
positive, negative data 의 확률분포를 비교(contrastive)하는 일반 Boltzmann machines 에선 이런 문제점을 dealing 할 수 있었음.

### 7. Learning fast and slow
FF 알고리즘에서 weight 업데이트는 layer normalized output 을 변경시키지 않음. 이는 동시다발적인 weight 업데이트가 가능하게 하는데
earlier layer 의 값의 변경이 later layer 의 output 값에 영향을 미치지 않기 때문.  
Backpropagation 기법과 다르게 FF 알고리즘을 이용한다면 레이어들 중간에 기존 FF 알고리즘으로 학습된 layer(black box)들을 넣을 수 있다는 점.
이 방법을 쓰면 black box 레이어가 일정하다는 가정하에 "outer loop" FF 알고리즘은 새로운 데이터에 빠르게 적응을 할 것이라고 함. longer
timescale 에서도 성능이 향상될 것이라고 예상.

### 8. The relevance of FF to analog hardware
기존 forward - backward 방식에선 빠른 계산 A-to-D converter 가 필요했음. Forward - Forward 방식에선 필요 없음.

### 9. Mortal Computation
기존 컴퓨터 사이언스에선 프로그램과 하드웨어를 분리해서 생각하였음. 같은 프로그램, 같은 weights 는 다른 디바이스에서 돌아가야함.
이는 병행 프로그래밍 등 많은 장점이 있었음. 이러한 사고방식(program immortality)을 벗어난다면 하드웨어 구성에 드는 에너지들을 줄일 
수 있음(모든 것을 좋은 하드웨어로 구성할필요 없다는 의미인듯). 각각의 하드웨어에서 각각의 특징을 잡아 낼 테고 각각의 특징은 고유함(mortal).  
  
image 분류에서 사실 우리가 진짜로 궁금한건 픽셀간의 function 의 구조이지, 그 안의 parameter 가 아닌 것처럼. function 을 전달하면
다른 하드웨어에서 같은 오류(e.g. MNIST 에서 5를 6이라고 하는 경우, 하드웨어만 다를 시)도 발생시키지 않을 것임. 이 프로세스는 older model
이 new model 에게 어떻게 생각하는지 전달하는 것과 같음(teaching).  
  
### 10. Future work
FF 알고리즘은 지금 막 시작된 개념임. 다음과 같은 의문사항이 남았음
* 과연 FF 가 비지도 생성모델에서 필요한 충분히 좋은 negative data 를 잘 만들어 낼까?
* best goodness function 이 뭘까? 최근에 했던 실험에서는 그냥 minimizing unsquared for positive data 가 더 좋았음(and maximizing 
  squared for negative data).
* best 활성화 함수는 뭘까? 본 연구에서는 ReLU 만 사용해봄
* (image)부분데이터에서 각 영역에 맞는 많은 goodness function 을 사용 가능할까? 이게 가능하다면 훈련이 매우 빨라질 것
등등..
  

















