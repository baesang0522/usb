Kubernetes 설치
=====
K8S 사용하면서 에러 혹은 중요한 사항 정리용
-----
*****
## 1. 클러스터 구성
!['cluster_settings'](./assets/cluster_setting.png)  
### 1.1 서버명 변경 및 k8s 관리 유저 생성
한 눈에 역할을 알아보기 쉽도록 마스터 노드는 k8s-master, 워커 노드는 k8s-node1(36), k8s_node2(37)로 서버명 변경 및 k8s 관리를 위한 유저 생성
유저명은 '`kube`' 로 통일하였음
  
root 계정으로 visudo 입력 후 아래 이미지처럼 생성한 유저 추가(생성한 유저에 root권한 부여)  
!['sudo_auth'](./assets/sudo_auth.png)  
쿠버네티스 관리를 편리하게 하기 위함.

완료되면 커맨드창이 아래와 같은 형태로 변함.  
!['after_work'](./assets/after_work.png)  

### 1.2 쿠버네티스 설치 준비
(모두 root 계정으로 실행)
#### docker 설치 및 활성화

```
# curl -s https://get.docker.com | sudo sh

# systemctl enable --now docker
```

#### SELINUX 비활성화

```
# setenforce 0

# sed -i 's/^SELINUX=enforcing$/SELINUX=disabled/' /etc/selinux/config
```

#### SWAP 비활성화

```
# swapoff -a

# sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
```

#### 방화벽 끄기

```
# systemctl disable firewalld

# systemctl stop firewalld
```

#### IPTABLES 설정

```
# cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
> br_netfilter
> EOF
```
```
# cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
> net.bridge.bridge-nf-call-ip6tables = 1
> net.bridge.bridge-nf-call-iptables = 1
> EOF
```
```
sysctl --system
```

#### host(/etc/hosts)파일 편집

```
# cat <<EOF >> /etc/hosts
> {ip} k8s-master
> {ip} k8s-node1
> {ip} k8s-node2
> EOF
```

### 쿠버네티스 설치
#### kubernetes.repo 등록
```
$ cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
> [kubernetes]
> name=Kubernetes
> baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-\$basearch
> enabled=1
> gpgcheck=1
> repo_gpgcheck=1
> gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
> exclude=kubelet kubeadm kubectl
> EOF
```

#### kuber