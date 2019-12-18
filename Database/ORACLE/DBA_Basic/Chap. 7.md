# Chap 7. 오라클 시작과 종료
## 01 오라클 시작 및 종료 개념

<img src=https://t1.daumcdn.net/cfile/tistory/2778993B54FA04B730 />

단계|내용
:---:|---
종료(SHUTDOWN)|데이터베이스에 대한 엑세스를 수행할 수 없는 상태
노마운트(NOMOUNT)|파라미터 파일 읽기, SGA 할당, alertSID.log 파일과 Trace 파일 시작 및 필요 백그라운드 프로세스 기동
마운트(MOUNT)|컨트롤 파일을 읽은 후 데이터 파일 및 리두 로그 파일을 인지
오픈(OPEN)|온라인 데이터 파일과 온라인 리두 로그 파일의 존재 및 정합성 확인 후<br> 해당 파일들을 엑세스하여 실제 데이터베이스를 사용할 수 있는 상태

- 데이터베이스를 사용하기 위해서는 해당 단계를 수행해야하며, 종료시키기 위해서도 마찬가지의 단계를 역순으로 수행해야 한다.

## 02 오라클 시작 및 종료 단계별 세부 사항
### 1) 종료 단계
- 데이터베이스를 이용하여 어떠한 작업도 수행할 수 없는 단계.

### 2) 노마운트(NOMOUNT) 단계
<img src=https://t1.daumcdn.net/cfile/tistory/25592E3454FA045F02 />

- 노마운트 단계를 인스턴스 단계라고도 한다. 이는 메모리와 백그라운드 프로세스를 구성하는 단계이기 때문이다.

인스턴스란?

    오라클 메모리와 백그라운드 프로세스를 의미

- 노마운트 단계에서 수행하는 작업
  - Alert Log 파일과 Trace 파일 시작
  - 파라미터 파일 엑세스
  - SGA 할당
  - 백그라운드 프로세스 기동

- 노마운트 단계 작업 순서
  1. Trace 파일 및 alertSID.log 파일을 열고 이 후 시작 과정 및 모든 에러가 alertSID.log 파일에 기록
  2. 파라미터 파일 확인
  3. 파라미터 파일 확인시 spfileSID.ora 파일을 확인하며 존재 하지 않는다면, spfile.ora 파일 확인
  4. 2단계의 파일이 존재하지 않는다면 정적 파라미터 파일인 initSID.ora 파일을 확인, 해당 파일도 존재하지 않는다면 에러 발생
  5. 파라미터 파일을 확인한 후 설정한 값에 따라 오라클 메모리 영역인 SGA를 할당
  6. 5단계의 작업이 종료하게 되면 오라클 백그라운드 프로세스를 시작


#### 아직 컨트롤 파일을 엑세스하지 않은 단계이기 때문에 컨트롤 파일 재생성이 가능하며, SGA는 기동이 되었으므로 재구성이 불가능하다.

- 노마운트 단계에서 가능한 업무
  - 컨트롤 파일 재생성

### 3) 마운트(MOUNT) 단계

<img src=https://t1.daumcdn.net/cfile/tistory/2553F43454FA045F05 />

- 마운트 단계에서 수행하는 작업
  - 컨트롤 파일 확인
  - 컨트롤 파일내의 데이터 파일 정보 및 리두 로그 파일 정보만 인지

#### 마운트 단계에서는 컨트롤 파일에 기록되어 있는 파일들의 위치와 상태 내용만 확인할 뿐 실제 파일이 존재하는지와 정상인지는 확인하지 않는다.<br>그렇기 때문에 실제 파일에 이상이 있어도 마운트 단계까지는 작업이 가능하다.<br>이러한 이유로 데이터베이스 복구는 보통 마운트 단계에서 수행하며, 특히 시스템 테이블스페이스에 장애가 발생한 경우 마운트 단계에서만 복구가 가능하다.

- 마운트 단계에서 가능한 업무
  - 데이터 파일 이름/위치 변경(오라클 12c에서는 온라인 작업 가능)
  - 데이터베이스 복구
  - 아카이브 모드 적용 및 해제

### 4) 오픈(OPEN) 단계

<img src=https://t1.daumcdn.net/cfile/tistory/23014D3454FA046039 />

- 오픈단계에서 수행하는 작업
  - 온라인 데이터 파일 확인(오프라인 데이터 파일은 생략)
  - 온라인 리두 로그 파일 확인
  - 언두 세그먼트를 온라인 상태로 변경

- 오픈 단계 작업 순서
  1.  컨트롤 파일 내용만으로 확인한 데이터 파일과 리두 로그 파일의 상태 및 위치 정보를 확인하여 데이터 파일과 리두 로그 파일을 엑세스할 수 있도록 구성
  2.  1단계에서 파일들 간의 정합성이 맞지 않거나 또는 파일이 컨트롤 파일에 명시된 위치에 존재하지 않는다면 에러가 발생하면서 데이터베이스 오픈 불가
  3.  파일들을 정상적으로 확인했다면, 언두 세그먼트를 온라인 상태로 변경. 이때 필요하다면 SMON 백그라운드 프로세스가 인스턴스 복구를 수행

- 오픈 단계에서 가능한 업무
  - 데이터베이스 엑세스가 가능하므로 노마운트/마운트 단계에서의 작업을 제외한 모든 작업 가능

### 5) 오라클 STARTUP 전체 단계 요약
단계|수행 작업|가능한 작업
:---:|---|---
노마운트|- 파라미터 파일 읽기<br>- SGA 할당<br>- Alert Log 파일과 Trace 파일 시작<br>- 백그라운드 프로세스 기동|- 컨트롤 파일 재생성
마운트|- 컨트롤 파일 확인<br>- 컨트롤 파일 내의 데이터 파일 및 리두 로그 파일 인지|- 데이터 파일 이름/위치 변경<br>(오라클 12c에서는 온라인 작업 가능)<br>- 데이터베이스 복구<br>- 아카이브 모드 적용 및 해제
오픈|- 온라인 데이터 파일 확인<br>(오프라인 데이터 파일은 생략)<br>- 온라인 리두 로그 파일 확인<br> -언두 세그먼트를 온라인 상태로 변경|- 데이터베이스 엑세스<br>- 노마운트/마운트 단계에서의 작업을 제외한 모든 작업

## 03 오라클 시작 관리
- 오라클 시작 명령은 3가지로 구분된다.
  - 일반 시작
  - 제한된 모드로 시작
  - 읽기 전용으로 시작

### 1) 일반 시작
일반 시작

    SQL> STARTUP

특정 파라미터 파일을 이용한 일반 시작

    SQL> STARTUP pfile=/data1/pfile/initORCL.ora;

필요에 의해 종료 상태에서 노마운트 단계 또는 마운트 단계로 기동

    SQL> STARTUP NOMOUNT -> 노마운트 단계까지만 기동
    SQL> STARTUP MOUNT   -> 마운트 단계까지만 기동

노마운트 또는 마운트 단계에서 데이터베이스를 오픈 단계로 기동

    SQL> ALTER DATABASE OPEN;

- RESETLOGS
  - 데이터베이스 장애 발생으로 마운트 단계에서 불완전 복구 후 오픈을 수행할 떄에는 위의 명령어에 RESETLOGS 옵션을 추가하여 오픈시킨다.
  - 불완전 복구를 수행하게 되면 컨트롤 파일에 저장되어 있는 정합성 정보와 데이터 파일의 저합성 정보가 다르기 떄문에 강제로 정합성을 맞춰야만 오라클을 오픈할 수 있다. 이런 경우에 사용하는 옵션이 RESETLOGS 이다.

- 시작과 종료
  - 하위의 시작 단계에서 상위의 어느 시작 단계로등 이행 가능하나 역순으로는 불가능하다.

### 2) 제한된 모드로 시작
- 제한된 모드로 데이터베이스를 시작하면 RESTRICTED SESSION 권한을 가진 유저만 데이터베이스에 접속 가능
- 권한이 없는 다른 유저의 접속을 제한하고 데이터베이스 관리자만이 작업을 수행하기 위해서 사용

명령어|내용
:---:|---
SQL> STARTUP RESTRICT|종료 상태에서 제한된 모드로 데이터베이스를 오픈하는 명령어
SQL> ALTER SYSTEM ENABLE<br>RESTRICTED SESSION|오픈 상태에서 제한된 모드로 설정하는 명령어<br>RESTRICTED SESSION 권한을 가진 유저만이 데이터베이스에 접속 가능하다. 그러나 이미 접속해 있던 유저는 계속 사용이 가능
SQL> ALTER SYSTEM DISABLE<br>RESTRICTED SESSION|오픈 상태에서 제한된 모드를 해제하는 명령어<br>해당 명령을 수행한 후부터는 모든 유저가 접속이 가능

### 3) 읽기 전용으로 시작
- 읽기 전용으로 데이터베이스를 시작하면 DML, DDL 명령이 불가능하며, 조회를 수행하기 위한 SELECT 명령만 가능하다. 
- 종료 상태에서 바로 읽기 전용으로 구동할 수 없으며, 마운트 상태에서 ALTER DATABASE 명령으로 상태를 변경해야한다.

SQL> STARTUP MOUNT
SQL> ALTER DATABASE OPEN READ ONLY;

## 04 오라클 종료 관리
- 오라클 종료의 종류로는 2가지가 존재한다.
  - 정상 종료: NORMAL, TRANACTIONAL 및 IMMEDIATE
  - 비정상 종료: ABORT

<img src=https://t1.daumcdn.net/cfile/tistory/2354D43454FA046004 />

### 1) 오라클 종료의 종류 
명령어|내용
:---:|---
NORMAL|데이터베이스에 접속한 유저가 존재하면 해당 유저가 접속을 종료할 때까지 기다렸다가 종료
TRANSACTIONAL|종료 명령을 수행한 시점에 처리되던 SQL이 종료할 때까지 기다렸다가 종료
IMMEDIATE|종료 명령을 수행한 시점에 처리되던 SQL을 취소하고 해당 SQL에 대한 롤백이 완료되면 종료
ABORT|종료 명령을 수행한 시점에 처리되던 SQL을 취소하고 롤백을 수행하지 않고 종료

- 각 종료의 특성

종료 종류| 추가 접속 시도| 접속중인 세션| 수행중인 작업| 취소된 작업 롤백 여부|체크 포인트 수행|SHUTDOWN 소요시간
:---:|---|---|---|---|---|---
NORMAL|허용 안함|종료까지 대기|수행|-|수행|오래 소요
TRANSACTIONAL|허용 안함|작업중인 세션은<br>종료까지 대기|수행|-|수행|오래 소요
IMMEDIATE|허용 안함|강제 종료|강제 종료|수행|수행|짧음
ABORT|허용 안함|강제 종료|강제 종료|수행안함|수행안함|매우 짧음

- 빠른 종료
  - 보통의 경우 데이터베이스를 종료하기 위해서는 SHUTDOWN IMMEDATE를 수행하게 된다. IMMEDIATE는 수행 중인 작업에 대해 강제 종료를 하며 롤백을 수행하게 된다.<br>이를 좀 더 빠르게 수행하고자 한다면, 명령어를 수행하기 전에 운영체제에 존재하는 서버 프로세스를 강제 종료하여 빠르게 롤백을 수행하게 한다면 좀 더 빠른 종료를 수행할 수 있다.