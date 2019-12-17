# Chap 6. 오라클 필수 파일
## 01 오라클 파일 종류
- 오라클 파일에는 4가지가 존재한다.
    1. 패스워드 파일
    2. Trace 파일
    3. 컨트롤 파일
    4. 파라미터 파일

- 각각의 파일의 종류 및 특징 확인

항목|내용
:---:|---
파라미터 파일|오라클 기동 시 필요하면 SGA 및 기타 환경을 구성하기 위한 정보가 기록된 파일
컨트롤 파일|데이터베이스의 현재 상태에 대한 정보 및 정합성을 확인하는 바이너리 파일로 `매우 중요`
백그라운드 Trace파일|백그라운드 프로세스에서 발생하는 이벤트 및 오류 로그를 저장하는 파일
Alert 로그 파일|데이터베이스의 전체적인 이벤트 및 로그를 저장하는 파일
유저 Trace 파일|유저의 오류나 추적 활성화에 의해 발생하는 내용을 저장하는 파일
Core Trace 파일|운영 체제의 문제를 오라클 프로세스가 감지하거나 오라클 버그에 의해 생성되는 파일
패스워드 파일|오라클 접속 시 인증을 위한 파일

## 02 파라미터 파일의 개념 및 종류
### 1) 파라미터 파일의 개념
파라미터 파일이란?

    오라클의 환경을 설정하는 파일로 정적 파라미터 파일과 오라클 9i부터 새로 소개된 동적 파라미터 파일이 존재한다.
    
- 파라미터 파일의 위치
  - 유닉스 또는 리눅스: $ORACLE_HOME/dbs
  - Windows 플랫폼: $ORACLE_HOME/database

### 2) 파라미터 파일의 종류

<img src=https://t1.daumcdn.net/cfile/tistory/266F2A3754FA029B24 />

구분|정적 파라미터 파일|동적 파라미터 파일
:---:|:---:|:---:
파일 형식|텍스트 형식|바이너리 형식
관리|사용자가 관리|오라클이 관리
파일 수정|텍스트 편집기로 수정|일반 편집기로 수정하면 사용할 수 없음<br>(정적 파라미터 파일로 변경 후 수정 또는 SQL 명령어로 수정)
관련 뷰|V$PARAMETER|V$SPPARAMETER
파일명|init\<SID>.ora|spfile\<SID>.ora
동적 파라미터 종류|적음|많음

- 동적 파라미터의 특징

항목|내용
|:---:|---
|동적 파라미터|데이터베이스 재기동 없이 ALTER SYSTEM SET 명령어로 변경 사항을 적용할 수 있는 파라미터
||ALTER SYSTEM SET 명령어로 변경한 후 해당 파라미터 파일을 변경해야만 다음 데이터베이스 재기동 시 적용

---
# 질문
1. ALTER SYSTEM SET 명령어로 변경하면 동적 파라미터 파일이 알아서 변경되는게 아니고<br>
SCOPE 옵션에 따라서 파일에만, 현재 메모리에만, 둘다 적용하는건지

    SQL> ALTER SYSTEM SET <파라미터 이름>=<변경값> SCOPE=[SPFILE|MEMORY|BOTH];
---

## 03 파라미터 파일의 관리
- 파라미터 파일에 대한 생성, 변경 및 확인하는 방법을 알아보자
  
항목|내용
:---:|---
정적 파라미터 파일 생성|$ORACLE_HOME/dbs/init\<SID>.ora 파일을 참고해서 텍스트 편집기로 생성 후 저장<br><br>SQL><br> CREATE PFILE PFILE ='pfile_name'<br>FROM SPFILE='spfile_name';
동적 파라미터 파일 생성|SQL> <br>CREATE SPFILE[='spfile_name]<br>FROM PFILE[='pfile_name'];
파라미터 값 변경|SQL><br>ALTER SYSTEM SET parameter_name=parameter_value<br>[COMMENT='text']<br>[SCOPE=MEMORY\|SPFILE\|BOTH] <br> [SID='sid'\|c*];
파라미터 값 확인|SQL> SELECT * FROM V\$PARAMETER;<br>SQL> SELECT * FROM V\$SPPARAMETER;<br>SQL> SHOW PARAMETER parameter_name

### 1) 파라미터 파일 생성
1. 수동 정적 파라미터 파일 생성
    - $ORACLE_HOME/dbs/init.ora 파일을 init\<SID>.ora 파일로 복사
    - init\<SID>.ora 파일을 편집기로 열고 원하는 파라미터를 수정

2. 동적 파라미터 파일을 정적 파라미터 파일로 변경
    - 동적 파라미터 파일에 기록되어 있는 파라미터 설정 값이 정적 파라미터 파일로 복사된다.
    - SQL> CREATE PFILE = 'pfile_name' FROM SPFILE = 'spfile_name';

변수 이름|내용
:---:|---
pfile_name|생성될 정적 파라미터 파일이며 이름만 설정하면 기본 위치에 저장된다.
spfile_name|정적 파라미터 파일 생성에 참조할 동적 파라미터 파일 이름을 설정

- SQL> CREATE PFILE FROM SPFILE

3. 동적 파라미터 파일 생성
   - 정적 파라미터 파일을 기준으로 생성할 수 있다.
   - SQL> CREATE SPFILE = 'spfile_name' FROM PFILE = 'pfile_name';

- 다음은 기본위치에 존재하는 정적 파라미터 파일을 이요해 동적 파라미터 파일을 생성하는 예제이다.
 
    SQL> CREATE SPFILE = '/data1/spfileORCL.ora'
    FROM PFILE = '\$ORACLE_HOME/dbs/initORCL.ora'

### 2) 파라미터 파일의 값 변경
데이터베이스 오픈 상태에서 파라미터 값을 변경하는 방법

    SQL> ALTER SYSTEM SET parameter_name=parameter_value
         [COMMENT='text]
         [SCOPE=MEMORY | SPFILE | BOTH]
         [SID= 'sid' | '*' ];

옵션 종류 | 내용
:---:|---
COMMENT|동적 파라미터 파일의 설정 값을 해당 명령어로 변경 시 주석을 추가할 수 있는 옵션
SCOPE|파라미터 설정 값 변경 시 변경 범위를 지정, 정적 파라미터 파일을 사용할 경우에는 MEMORY 옵션만 사용가능<br>동적 파라미터 파일을 사용하는 경우에는 MEMORY, SPFILE, BOTH 옵션을 사용할 수 있다.
SID|오라클 RAC(Real Application Cluster)를 사용할 경우 변경된 파라미터 값이 적용될 노드를 선택하는 옵션

SCOPE 옵션

    MEMORY: 메모리 범위에서만 적용, 재시작 시 변경된 설정 값이 적용되지 않음.
    SPFILE: 변경된 설정 값을 동적 파라미터 파일에만 적용, 재시작 시 변경된 설정 값이 적용 됨
    BOTH: 변고이던 설정 값을 메모리와 동적 파라미터 파일 모두에 적용

오라클 RAC(Real Application Cluster)란?

    오라클 RAC는 하나의 데이터베이스에 여러 개의 인스턴스(SGA+백그라운드 프로세스)를 구성하는 아키텍쳐

파라미터 값 변경 예제

    SQL> ALTER SYSTEM SET db_cache_size = 1G
         COMMENT = '2017.10.15 작업자 김재형'
         SCOPE = BOTH
         SID = '*';

파라미터 설정 값은 다음과 같은 SQL을 사용해 접속한 세션 단위로도 바꿀 수 있다.

    SQL> ALTER SESSION SET sort_area_size = 52428800;

### 3) 파라미터 값 조회
항목|내용
:---:|---
V$PARAMETER|정적 파라미터 파일을 사용하는 경우 조회
V$SPPARAMETER|동적 파라미터 파일을 사용하는 경우 조회

첫 번째로 V\$PARAMETER 동적 성능 뷰를 조회하는 경우를 확인해보자.

    SQL> SELECT NAME, TYPE, VALUE, ISDEFAULT, ISSES_MODIFIABLE, ISSYS_MODIFIABLE
         FROM V$PARAMETER;

각 컬럼의 항목
항목|목적
:---:|---
NAME|파라미터 이름
TYPE|파라미터를 설정하는 타입
VALUE|파라미터 값
ISDEFAULT|파라미터 기본 값 사용 유무
ISSES_MODIFIABLE|ALTER SESSION 명령으로 파라미터 설정 값을 변경할 수 있는지 유무
ISSYS_MODIFIABLE|ALTER SSYSTEM 명령으로 파라미터 설정 값을 변경할 수 있는지 유무

TYPE 컬럼이 가질 수 있는 값
TYPE 컬럼 값|사용 가능 설정 값| 파라미터 예제
:---:|---|:---:
1|TRUE/FALSE 중 하나를 의미 |TIMED_STATISTICS
2|문자 값을 의미|CONTROL_FILES
3|작은 숫자 값을 의미|SESSION
4|파일을 의미|IFILE
5|지정된 값 없음|-
6|큰 숫자 값 의미|SHARED_POOL_SIZE

두 번째로 V\$SPPARAMETER 동적 성능 뷰를 확인해보자

    SQL> SELECT * FROM V$SPPARAMETER;

항목|목적
:---:|---
SID|인스턴스 번호
NAME|파라미터 이름
VALUE|파라미터 값
DISPLAY_VALUE|정적 파라미터 파일에 명시된 값
ISSPECIFIED|동적 파라미터 파일에 해당 파라미터가 설정되어 있는지 유무
ORDINAL|파라미터 설정 값의 순서
UPDATE_COMMENT|가장 최근의 파라미터 설정 값 변경 시 주석의 내용

동적 성능 뷰를 조회하지 않고 간단히 파라미터 설정 값을 확인할 수 있음

    SQL> show parameter SORT

- SHOW PARAMETER 명령은 SYS와 SYSTEM 유저만이 사용 가능하다. 
  - 일반유저가 쓰기 위해서는 다음 조건을 만족해야한다.

항목|조건1|조건2
:---:|:---:|:---:
O7_DICTIONARY_ACCESSIBILITY 파라미터|TRUE|TRUE/FALSE
SELECT ANY TABLE 권한|O|
SELECT ANY DICTIONARY 권한||O

## 04 컨트롤 파일의 개념 및 내용
컨트롤 파일이란?

    데이터 베이스의 현재 상태 정보를 저장하는 바이너리 파일이며 오라클 데이터베이스 운영에 필요한 필수 파일

<img src=https://t1.daumcdn.net/cfile/tistory/246EF23754FA029C24 />

### 1) 컨트롤 파일의 내용
- 데이터베이스 이름
- 데이터베이스 생성 시 타임스탬프
- Current 리두 로그 파일 번호
- 체크포인트 정보
- 테이블스페이스 정보
- 데이터 파일과 리두 로그 파일 정보
- 데이터베이스 생성 시 생성되는 데이터베이스 구분자
- 아카이브 로그 위치와 상태 정보
- RMAN(Recovery Manager) 사용 시 백업 위치와 백업 파일 상태
  
컨트롤 파일 위치는 V$CONTROLEFILE을 조회하거나 show parameter 명령으로 확인할 수 있다. 

## 05 컨트롤 파일의 관리
### 1) 컨트롤 파일 다중화 개념
컨트롤 파일 다중화란?

    컨트롤 파일을 하나가 아닌 여러 개의 컨트롤 파일로 해당 데이터베이스를 운영하겠다는 뜻

<img src=https://t1.daumcdn.net/cfile/tistory/226F1C3754FA029D24 />

- 컨트롤 파일 다중화의 필요 이유
  - 컨트롤 파일이 손상되면 오라클은 데이터베이스 정합성을 확인하지 못하게 되므로 비정상 종료된다.
  - 또한 비정상 종료후 복구를 수행해야 하며 복구 방식은 매우 복잡하게 수행되고 현시점까지 복구는 어렵다.
  - 이러한 장애를 최소화 하기 위해 여러 개의 컨트롤 파일로 운영하는 것이 필요함
- 컨트롤 파일이 손상되는 이유
  - 디스크 장애로 저장되어 있던 컨트롤 파일 손상
  - 사용자 실수로 삭제

#### 컨트롤 파일 사용 시 주의사항
항목 | 내용
:---:|---
컨트롤 파일 다중화 장점|- 데이터베이스 변경 시 모든 컨트롤 파일에 기록한다.<br>- 다중화된 컨트롤 파일 중 하나라도 정상적이라면 재시작 시 복잡한 복구 단계를 수행할 필요가 없다.
컨트롤 파일 다중화 주의 사항|디스크 장애에 대비하여 반드시 각각의 컨트롤 파일은 서로 다른 디스크에 위치시켜야 한다. 같은 디스크에 저장한 경우 디스크 장애가 발생한다면 모두 손실되어 컨트롤 파일 다중화의 의미가 없어진다. 

<br>

<img src=https://t1.daumcdn.net/cfile/tistory/266EFA3754FA029D24 />

- 위와 같은 경우 운영 중에 데이터베이스는 비정상 종료되지만 추후 데이터베이스 재시작 시에는 데이터베이스가 종료된 상태에서 컨트롤 파일2를 컨트롤 파일1로 복사하면 정상적으로 데이터베이스를 운영할 수 있게된다.

#### 컨트롤 파일의 개수와 성능
- 데이터베이스 변경시마다 컨트롤 파일에 변경 내용을 기록하므로 너무 많은 컨트롤 파일로 다중화를 구성하면 디스크 I/O 경합이 발생하여 성능이 저하될 수 있다.

### 2) 컨트롤 파일 다중화 방법
항목|목적
:---:|---
정적 파라미터 사용|1. 데이터베이스 종료<br>2. 편집기로 CONTROL_FILES 파라미터 수정<br>3. 운영체제 명령으로 CONTROL_FILES 파라미터 수정한 것에 맞게 컨트롤 파일 복사<br>4. 데이터베이스 시작
동적 파라미터 사용|1. 명령어로 CONTROL_FILS 파라미터 수정<br>2. 데이터베이스 종료<br>3. 운영체제 명령으로 CONTROL_FILES 파라미터 수정한 것에 맞게 컨트롤 파일 복사<br>4. 데이터베이스 시작

#### 컨트롤 파일 다중화 예제
정적 파라미터 파일 사용 시
   
    1. 데이터베이스르 종료시킨다
    SQL> SHUTDOWN

    2. 텍스트 편집기로 CONTROL_FILES 파라미터를 수정한다.
    > grep CONTROL_FILES $ORACLE_HOME/dbs/initORCL.ora
    CONTROL_FILES = '/data1/control1.ctl'

    > vi $ORACLE_HOME/dbs/initORCL.ora
    # CONTROL_S 파라미터에 /data2/control2.dtl 추가

    > grep CONTROL_FILES $ORACLE_HOME/dbs/initORCL.ora
    CONTROL_FILES = '/data1/control1.ctl', '/data2/control2.ctl'

    3. 운영 체제 명령으로 원래 존재하던 컨트롤 파일을 CONTROLE_FILES 파라미터 수정한 것에 맞게 이중화할 위치에 복사한다.
    > cp /data1/control1.ctl /data2/control2.ctl

    4. 데이터베이스를 기동시킨다.
    SQL> STARTUP

동적 파라미터 파일 사용 시
   
    1. ALTER SYSTEM SET 명령으로 CONTROLE_FILES 파라미터를 수정한다.
    SQL> ALTER SYSTEM SET
         control_files = '/data1/control1.ctl', '/data2/control2.ctl' SCOPE=spfile;

    2. 데이터베이스르 종료시킨다
    SQL> SHUTDOWN

    3. 운영 체제 명령으로 원래 존재하던 컨트롤 파일을 CONTROLE_FILES 파라미터 수정한 것에 맞게 이중화할 위치에 복사한다.
    > cp /data1/control1.ctl /data2/control2.ctl

    4. 데이터베이스를 기동시킨다.
    SQL> STARTUP

## 06 패스워드 파일의 개념
패스워드 파일이란?

    데이터베이스에서 직접 SYSDBA와 SYSOPER 권한을 관리하기 위해 사용하는 파일

### 1) 운영체제 인증 방식
운영체제 인증이란?

    SYSDBA와 SYSOPER 권한을 특정 운영체제 그룹에 할당하여 해당 운영체제 그룹에 포함되는 운영체제 유저만이 
    해당 권한을 소유하는 인증 방식

- 운영체제 그룹에 속한 운영체제 유저로 시스템에 접근한 경우에만 SYSDBA와 SYSOPER 권한으로 데이터베이스에 접근할 수 있게 된다. SYSDBA와 SYSOPER 권한은 데이터베이스에서 최고의 권한이다.

<img src=https://t1.daumcdn.net/cfile/tistory/236F7D3754FA029E24 />

- 위 그림과 같이 오라클을 설치할 때 dba 운영체제 그룹에 SYSDBA와 SYSOPER 권한을 할당하고 해당 그룹에 oracle과 dbadmin 유저를 생성하여 해당 운영체제 그룹으로 할당한다.

항목|내용
:---:|---
oracle과 dbadmin 유저|데이터베이스 기동 및 종료 등의 작업을 수행 가능
wasadmin 유저|dba 운영체제 그룹이 아니므로 SYSDBA와 SYSOPER 권한을 사용할 수 없으므로 기동 및 종료 등의 작업 수행 불가

### 2) 패스워드 파일 인증 방식
패스워드 파일 인증이란?

    SYSDBA 또는 SYSOPER 권한을 운영체제 인증없이 데이터베이스 유저에 의해 인증하는 방식

<img src=https://t1.daumcdn.net/cfile/tistory/256F4A3754FA029F24 />

- 위 그림과 같이 패스워드 파일을 사용하여 인증을 받게 되면 앞에서 언급한 운영체제 인증은 기본적으로 사용하게 되며 패스워드 파일에 등록된 데이터베이스 유저 또한 SYSDBA 또는 SYSOPER 권한을 사용할 수 있게 된다.

#### 패스워드 파일과 파라미터
- 인증 방식에 관련된 파라미터는 REMOTE_LOGIN_PASSWORDFILE 파라미터
- 운영체제 인증일 경우 기본 값인 NONE을 설정
- 패스워드 파일 인증일 경우 EXCLUSIVE로 설정

## 07 패스워드 파일의 관리
항목|내용
:---:|---
패스워드 파일 생성|orapwd file=file_name password=password entries=max_users
패스워드 파일 삭제|rm과 같은 운영체제 명령어를 사용하여 파일을 삭제
패스워드 파일 수정|1. 데이터베이스 종료<br>2. 패스워드 파일 삭제 후 재생성<br>3. 데이터베이스 시작

- 패스워드 파일 생성 시 옵션
  
옵션|내용
:---:|---
file|패스워드 파일 이름이며 orapwdSID로 생성
password|SYSDBA와 SYSOPER의 비밀번호
entries|SYSDBA 및 SYSOPER로 접속할 수 있는 최대 오라클 유저 수

## 08 Trace 파일의 개념
Trace 파일이란?

    오라클은 운영 중 특정 이벤트가 발생하면 이벤트가 발생한 원인에 따라 여러 종류의 Trace 파일을 생성한다.
    Trace 파일을 확인하여 발생한 이벤트의 원인을 분석할 수 있다.

<img src=https://t1.daumcdn.net/cfile/tistory/266F9E3754FA029F23 />

- Trace 파일의 종류

종류|내용
:---:|---
코아(Core) Trace|운영체제 및 오라클 엔진 이상 등이 발생하면 생성
유저 Trace|유저 작업에 의해 생성
백그라운드 Trace|백그라운드 프로세스의 문제 발생 시 생성
Alert 로그|경고 로그 파일로 데이터베이스 전반적인 로그 생성

### 1) 유저 Trace 파일

<img src=https://t1.daumcdn.net/cfile/tistory/216F733754FA029F24 />

- Trace 파일은 유저 덤프와 동일하다. 유저 Trace 파일의 발생 원인은 다음과 같다.
  - 유저의 오류에 의해 발생
  - 임의로 유저 추적 활성화에 의해 발생

- 유저 Trace 파일은 발생된 오류에 대한 분석 외에 유저가 수행한 SQL 튜닝을 위해서 자주 사용된다.
- 수행중인 SQL에 대해 유저 Trace를 세션 단위로 활성화 및 비활성화시킬 수 있다. 
  - SQL> ALTER SESSION SET SQL_TRACE = TRUE ;   유저 Trace 활성화
  - SQL> ALTER SESSION SET SQL_TRACE = FALSE;  유저 Trace 비활성화

#### TKPROF
- 생성된 유저 Trace 파일은 TKPROF 오라클 유틸리티를 사용하여 해당 유저가 수행한 SQL의 실행 계획 및 통계치를 보다 수월하게 분석할 수 있게 된다. 

예제

    > tkprof tracefile outputfile sys=no explain=sys/oracle

옵션|내용
:---:|---
tracefile|유저 추적으로 생성된 유저 Trace 파일 이름
outputfile|TKPROF 수행 후 추출되는 파일 이름
sys|대상 SQL을 수행하기 위해 오라클이 내부적으로 수행하는 SQL에 대한 정보 추출 여부
explain|대상 SQL에 대한 실행계획 추출 옵션

다른 유저의 Trace를 활성화 시키기 위한 오라클 프로시져 사용법

    SQL> EXEC DBMS_SYSTEM.SET_SQL_TRACE_IN_SESSION(sid, serical#, boolean);

- 위의 명령어에서 SID와 serial#의 값은 V\$SESSION을 조회해서 확인할 수 있다. 
- 유저 Trace 파일은 SID_ora_PID.ora 형식으로 저장되며 SID는 인스턴스 이름, PID는 이벤트를 발생시킨 유저의 서버 프로세스 이름

### 2) 백그라운드 Trace 파일
<img src=https://t1.daumcdn.net/cfile/tistory/2325243954FA02A003 />

- 백그라운드 Trace 파일은 DIAGNOSTIC_DEST 파라미터에서 지정한 위치 아래에 trace 디렉토리에 저장되며 2가지 Trace 파일이 존재한다.
  - SID_process_PID.trc: 백그라운드 프로세스에 의해 문제가 감지될 경우 생성
  - alertSID.log: 데이터베이스의 전체적인 로그 기록
    - SID는 인스턴스 이름
    - PID는 운영체제에서의 프로세스 이름

- alertSID.log 파일에는 다음과 같은 정보가 저장된다.
  - 데이터베이스 시작, 종료 단계 및 시간
  - 파라미터 파일에 명시된 파라미터 설정 값
  - 로그 시퀀스 번호 및 로그 스위치 번호
  - 테이블스페이스 및 언두 세그먼트 생성 정보
  - 오류 감지 및 생성된 Trace 파일의 이름과 위치

- alertSID.log 파일은 오랫동안 서비스 하게되면 크기가 매우 커진다. 해당 파일은 삭제하거나 참조를 위해 다른곳으로 이동시키면 자동으로 다시 생성되어 데이터베이스의 모든 변경을 새로 기록한다.


### 3) 코어 Trace 파일

<img src=https://t1.daumcdn.net/cfile/tistory/2152BF3954FA02A036 />

- 백그라운드 Trace 파일은 DIAGNOSTIC_DEST 파라미터에서 지정한 위치 아래에 cdump 디렉토리에 생성된다.
- 코어 Trace 파일은 운영체제의 문제를 오라클 프로세스가 감지한 경우 및 오라클 버그 등에 의해 생성되며 치명적일 가능성이 높다.

## 09 자동 진단 저장소(Automatic Diagnotic Repository)
- 오라클 11g버전부터 Trace 파일 및 로그 파일들을 한곳에서 관리하기 위해 자동 진단 저장소(ADR)라는 개념을 도입하였다. 
- 해당 저장소의 위치는 DIAGNOTIC_DEST 파라미터로 지정하며, 지정된 위치 아래에 각각의 파일을 저장하기 위한 디렉토리가 자동 생성된다.

ADR_HOME 경로|하위 디렉토리명|내용
|:---:|:---:|---
|DIAGNOTIC_DEST<br>/diag<br>/rdbms<br>/<database_name><br>/\<SID>|alert|Alert 로그 파일(XML 포맷) 저장
||trace|백그라운드 Trace 파일 저장<br>유저 Trace 파일 저장<br>경고 로그 파일 (TEXT 포맷) 저장
||cdump|코아 Trace 파일 저장
||incident|특정 시점에 발생한 Trace 파일을 시점별 디렉토리로 저장

해당 디렉토리 위치는 V$DIAG_INFO 동적 성능뷰를 통해 확인 가능

    SQL> SELECT * FROM V$DIAG_INFO;