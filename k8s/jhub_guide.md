Kubernetes jhub 설치
=====
*****
### 1. flannel 설치
네트워크 통신을 위해 설치함

### 2. helm 설치

```
# curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3
# chmod 700 get_helm.sh
# ./get_helm.sh
```

### 3. jupyterhub 설치
#### 3.1 storage class & PV 생성
jhub_sc.yaml 참조

#### 3.2 config.yaml 파일 생성
config.yaml 참조
```
# This file can update the JupyterHub Helm chart's default configuration values.
#
# For reference see the configuration reference and default values, but make
# sure to refer to the Helm chart version of interest to you!
#
# Introduction to YAML:     https://www.youtube.com/watch?v=cdLNKUoMc6c
# Chart config reference:   https://zero-to-jupyterhub.readthedocs.io/en/stable/resources/reference.html
# Chart default values:     https://github.com/jupyterhub/zero-to-jupyterhub-k8s/blob/HEAD/jupyterhub/values.yaml
# Available chart versions: https://jupyterhub.github.io/helm-chart/
#
```

#### 3.3 helm에 jupyterhub repo 등록

```
$ helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
$ helm repo update
```
성공 시 
```
Hang tight while we grab the latest from your chart repositories...
...Skip local chart repository
...Successfully got an update from the "stable" chart repository
...Successfully got an update from the "jupyterhub" chart repository
Update Complete. ⎈ Happy Helming!⎈
```  
라는 메세지가 화면에 표시됨

#### 3.4 helm 으로 jupyterhub 설치
생성한 config.yaml파일을 토대로 jupyterhub가 설치됨.    
config 파일이 존재하는 경로에서  
```
helm upgrade --cleanup-on-fail \
  --install <helm-release-name> jupyterhub/jupyterhub \
  --namespace <k8s-namespace> \
  --create-namespace \
  --version=<chart-version> \
  --values config.yaml
  --debug
```  
명령어 실행

