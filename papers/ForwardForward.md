The Forward-Forward Algorithm
=============

## abstract
기존 방식은 forward-backward 방식. 오류를 역전파(backpropagation) 함으로써 가중치들을 업데이트 함. 본 연구에선 Forward-Forward(FF) 
방식을 제안. 2 way forward pass(positive, negative dataset. 네트워크에서 생성됨) 로 forward-backward 효과를 낼 것임.  

각 네트워크 레이어는 목적함수를 가지고 있고 positive data에는 좋은 점수, negative data에는 낮은 점수를 그 목표로 함. 
positive way 와 negative way 가 분리될 수 있다면 negative way 는 오프라인으로 할 수 있고, 미분하느라(backpropagation) 
시간을 허비하지 않을 수 있음(빠름) <br>

<br>

##1. Backpropagation의 문제점
* Stochastic gradient descent는 딥러닝의 성공에 많은 영향을 끼침
* time sequence 방식이든, 이미지든 역전파는 실제 뉴런이 배우는 방식과는 다름(뉴런이 backward pass를 사용한다고 할 수 없음)
* top-down 방식(backpropagation)은 이후 레이어가 이전 레이어에 영향을 미치지만, 실제 인간의 지각능력은 실시간으로 작동함
* 역전파의 큰 문제점은 올바른 미분값을 구하기 위해선 forward pass에서의 계산 방법을 완벽히 알아야 한다는 점임.
  블랙 박스를 input으로 할 때 블랙 박스가 어떤식으로 forward pass 되는 지 모른다면 역전파도 할 수 없음.
* 완벽한 forward pass 모델이 존재하지 않기 때문에 강화학습(reinforcement learning 이라고 나왔지만 딥러닝 기법 중 '강화 학습' 
  을 의미하는 것은 아닌듯. 다음 문단을 읽어보면 '계산방식을 알고 있는' 다양한 딥러닝 기법을 의미하는 듯)시 매번 다른 모델이 
  선택됨(수많은 매개변수의 섭동 때문).하지만 이러한 상황을 average하기 위해선 learning rate 가 parameter 수에 반비례 해야 
  하는데(작은 learning rate) 이렇게 되면 학습 시 비용이 커짐. 이러한 이유로 거대한 모델에선 Backpropagation과 비교할 순 없음. 
* 이번 연구의 요점은 비선형성을 포함한 인공신경망 모델들이 이런 기법들에 의지하지 않아도 된다는 것. FF 방식은 Backpropagation보다 
  속도면에서는 비슷하지만 모델의 정확한 계산방식(e.g. RNN, CNN 이 forward시 계산 방식이 다름)을 몰라도 작동한다는 데에 있음.
* 논문에서 테스트한 바에 의하면 FF방식이 역전파보다 항상 빠른 것이 아님. 매우 큰 데이터셋으로 학습된 매우 큰 모델들은 계속 역전파를 
  사용할 것으로 보임. 
* 하지만 FF방식은 두가지 측면에서 장점을 보일 것 같은데 model이 cortex상에서 학습되는 경우, low power hardware에서 학습되는 경우.

##2. Forward-Forward 알고리즘
FF 알고리즘은 [볼츠만 머신](https://idplab-konkuk.tistory.com/14) 에 영감을 받아 탄생한 탐욕적 멀티 레이어 절차(greedy multi-layer procedure). 
forward-backward 방식을 대체하기 위해 제안되었으며 두 개의 forward(positive, negative pass)는 같은 방향으로, 다른 데이터를 가지고, 
다른 목적을 위해 forward pass 됨.
positive 는 real data 를 이용하여 각 레이어의 weight 를 모델 성능(goodness)을 올리기 위해 pass 되고 negative 는 "negative data"를 
이용하여 각 히든 레이어의 성능을 
낮추기 위해 pass 됨. 본 논문에선 두가지 성능측정 방법을 살펴봄.   
```
1. sum of squared neural activities
2. negative sum of squared neural activities.
```
logistic function 이 적용된 input vector 가 positive 일 떄, 이 값이 positive 인지 negative 인지 잘 분류하는 것이 목적임. 






