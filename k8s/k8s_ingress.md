Kubernetes 정리 2
=====
K8S 사용하면서 에러 혹은 중요한 사항 정리용
-----
*****
## Ingress(인그레스)

네트워크 트래픽은 Ingress와 egress로 구분. egress는 외부로 나가는 것, Ingress는 외부에서 내부로 들어오는 네트워크 트래픽.  
  
쿠버네티스에도 `Ingress`라고 하는 오브젝트가 존재. 쿠버네티스의 Ingress는 외부에서 쿠버 클러스터 내부로 들어오는 네트워크 요청:
즉, Ingress 트래픽을 어떻게 처리할 지 정의함. 쿠버에서 실행중인 deployment나 service에 접근하기 위한 관문 같은 역할을 담당.

서비스를 외부로 노출시켜 제공해야 한다면 Ingress를 사용하는 것이 바람직함. Ingress 요청을 처리하기 위한 service는 일반적으로 
클라우드 플랫폼에서 제공되는 `LoadBalancer` 타입의 service를 사용함. private cloud환경에서 운영하는 서버에 ingress를 직접 구축한다면
service의 type을 `NodePort`, 또는 `ExternalIP`, `MetalLB`등을 대신 사용할 수 있음.

### 전제 조건들
인그레스 컨트롤러가 있어야 인그레스 설정 가능. 인그레스 리소스만 생성한다면 효과가 없다. `ingress-nginx`와 같은 인그레스 컨트롤러를 
배포해야 할 수도 있다.

### 인그레스 컨트롤러
인그레스 리소스가 작동하려면, 클러스터는 실행 중인 인그레스 컨트롤러가 반드시 필요. `kube-controller-manager` 바이너리 일부로 실행되는
컨트롤러의 다른 타입과 달리 인그레스 컨트롤러는 클러스터와 함께 자동으로 실행 X. 클러스터에 가장 적합한 인그레스 컨트롤러를 선택해야 함
하나의 클러스터 내에 여러 개의 인그레스 컨트롤러를 배포할 수 있다. 인그레스를 생성할 때, 클러스터 내에 둘 이상의 인그레스 컨트롤러가 존재하는 경우
어떤 인그레스 컨트롤러를 사용해야 하는지 명시해 주어야 함. `ingress.class` 어노테이션을 각각의 인그레스에 추가해야 함.  
만약 클래스를 정의하지 않으면, 클라우드 제공자는 기본 인그레스 컨트롤러를 사용할 수 있다.
https://kubernetes.io/ko/docs/concepts/services-networking/ingress-controllers/ 참조

### 인그레스
