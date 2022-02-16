Kubernetes 정리
=====
K8S 사용하면서 에러 혹은 중요한 사항 정리용
-----
*****
### 서비스 정의
쿠버네티스의 서비스는 pod와 비슷한 REST 오브젝트. 모든 REST오브젝트와 마찬가지로,
서비스 정의를 API서버에 POST하여 인스턴스를 생성할 수 있음.  

예를 들어, 각각 TCP포트 9376에서 수신하고 `app=MyApp` 레이블을 가지고 있는 pod세트가 있다고 가정  
```
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
```
이 yaml파일은 "my-service"라는 새로운 서비스 오브젝트를 생성하고, `app=MyApp` 레이블을 가진 pod의 TCP9376 포트를 대상으로 함
쿠버네티스는 이 서비스에 서비스 프록시가 사용하는 IP 주소("cluster IP"라고 불리는 것)를 할당.  
서비스의 기본 프로토콜은 TCP. 다른 프로토콜을 사용할 수도 있음.

####지원 프로토콜
> **TCP**: 모든 종류의 서비스에 TCP 사용가능. 기본 네트워크 프로토콜    
> **HTTP**: 클라우드 공급자가 이를 지원하는 경우, LoadBalancer 모드의 서비스를 사용하여 서비스의 엔드포인트로 전달하는 외부 HTTP/HTTPS
> 리버스 프록시 설정 가능.  
> **PROXY 프로토콜**: 클라우드 공급자가 지원하는 경우에, LoadBalancer 모드의 서비스를 사용, 쿠버 자체 외부에 로드 밸런서를 구성할 수 있으며, 
> 이때 접두사가 PROXY 프로토콜인 연결을 전달하게 됨  
> 
> 이 외에도 지원되는 프로토콜이 더 있음. 우선 중요해 보이는 것만 정리.

많은 서비스가 하나 이상의 포트를 노출해야 하기 때문에, 쿠버는 서비스 오브젝트에서 다중 포트 정의를 지원. 각 포트는 동일 혹은 다른 프로토콜로 정의될 수 있음.  

### 서비스 찾기
쿠버네티스는 서비스를 찾는 두 가지 기본 모드를 지원. 환경 변수와 DNS
#### 환경 변수
파드가 노드에서 실행될 때, kubelet은 각 활성화된 서비스에 대해 환경 변수 세트를 추가한다. 도커 링크 호환 변수와 보다 간단한 
`{SVCNAME}_SERVICE_HOST` 및 `{SVCNAME}_SERVICE_PORT` 변수를 지원하고, 이때 서비스 이름은 대문자이고 대시는 밑줄로 변환된다.

예를 들어, TCP 포트 6379를 개방하고 클러스터 IP 주소 10.0.0.11이 할당된 서비스 `redis-master`는, 다음 환경 변수를 생성한다.
```
REDIS_MASTER_SERVICE_HOST=10.0.0.11
REDIS_MASTER_SERVICE_PORT=6379
REDIS_MASTER_PORT=tcp://10.0.0.11:6379
REDIS_MASTER_PORT_6379_TCP=tcp://10.0.0.11:6379
REDIS_MASTER_PORT_6379_TCP_PROTO=tcp
REDIS_MASTER_PORT_6379_TCP_PORT=6379
REDIS_MASTER_PORT_6379_TCP_ADDR=10.0.0.11
```
> **참고:**  
> 서비스에 접근이 필요한 pod가 있고, 환경 변수를 사용해 포트 및 클러스터 IP를 클라이언트 pod에 부여하는 경우, 클라이언트 파드가 
> 생성되기 **_전에_** 서비스를 만들어야 한다. 그렇지 않으면, 해당 클라이언트 pod는 환경 변수를 생성할 수 없다.






