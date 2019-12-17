
# Chap 3. 오라클 메모리
## 01 오라클 메모리 구조

종류|내용
:---:|---
SGA(System Global Area)|모든 사용자가 공유 가능
PGA(Program Global Area, Private Global Area)|사용자마다 공유하지 않고 개별적으로 사용

### 1) PGA(Program Global Area)의 개념
PGA란?

    데이터베이스에 접속하는 모든 유저에게 할당되는 각각의 서버 프로세스가 독자적으로 사용하는 오라클 메모리 영역

- User Process와 Server Process
  
항목|내용
:---:|---
User Process | DB에 접속하기 위한 프로세스로 서버 프로세스에 연결되면 모든 정보를 전달한다. SQL을 실행하면 SQL을 전달하고 응답이 올 때까지 대기한다.
Server Process | User Process로 부터 SQL과 기타 정보를 전달받아 요청받은 내용을 수행하기 위해 모든 작업을 수행한다. 이때 요청받은 내용과 정보를 PGA에 저장한다.

- 오라클은 Dedicated 서버 방식과 Shared 서버 방식이 존재한다.

종류|내용|장점|단점
:---:|---|---|---
Dedicated Server|User Process가 Server Process에 접속하면 새로운 Server Process를 만든다.<br> PGA = 변수 저장 공간(Stack Space) + UGA|Shared 보다 관리 용이|메모리 사용량이 크다
Shared Server|하나의 Server Process를 여러 User Process들이 공유.<br> PGA = 변수 저장 공간(Stack Space),<br> UGA = 기본적으로 Shared Pool, Large Pool에 저장하기도 한다.|메모리 사용량이 적다|Server Process가 죽으면 모든 User Process가 Rollback(관리가 힘들다)

구분|항목|내용
|:---:|---|---
|SQL Work Area|비트맵 생성 영역|<b>비트맵 인덱스</b> 생성 영역.
||비트맵 병합 영역|비트맵 인덱스를 통한 실행 분석 후 비트맵을 병합하는 경우에 사용하는 영역.<br> WHERE에서 OR 연산 시 2개 비트 값을 비교할 때 병합이 일어난다.
||정렬 공간|Order by, Group by 시에 정렬을 수행하기 위한 공간. 해당 공간에서 정렬이 일어나면 메모리 정렬이라한다.<br> 공간이 부족하면 DISK에 임시 테이블 스페이스를 이용.
||해쉬 공간|해쉬 조인의 해쉬 영역 생성 영역.
|UGA|세션 메모리|서버 프로세스에 의해 추출된 결과 값을 전달하기 위해 필요한 유저 프로세스의 세션 정보를 저장
|Private SQL Area|영구 영역|<b>바인드 변수</b> 값을 저장. 영구 영역은 SQL 문장이 완료될 때 해제됨. 
||런타임 영역|쿼리의 실행 상태 정보를 저장 DML 문장의 경우 SQL 문장이 완료될 때 해제됨.

비트맵 인덱스

    컴퓨터의 최소 단위인 비트를 이용하여 컬럼 값을 저장하고 이를 이용하여 ROWID를 자동으로 생성하는 인덱스의 한 방법.

바인드 변수 

    SQL에서 상수 값을 변수 처리한 부분을 의미한다. WHERE EMPNO := B1 에서 ::B1의 변수 값이 바인드 변수

### 2) PGA(Program Global Area)의 관리

항목|필수여부|설정값|내용
:---:|:---:|:---:|---
WORKAREA_SIZE_POLICY|X|AUTO(Default)|MANUAL과 AUTO로 설정 가능. MANUAL : SORT_AREA_SIZE 파라미터를 이용하여 정렬공간을 설정 AUTO : PGA_AGGREGATE_TARGET 파라미터를 이용 
PGA_AGGREGATE_TARGET|O|물리 메모리의 10~20%|모든 세션의 PGA 크기의 합으로 해당 크기까지 오라클이 자동으로 관리한다. 단순 지표임.
PGA_AGGREGATE_LIMIT|O|Default|실제 PGA 크기를 설정하는 파라미터.
_SMM_MAX_SIZE|X|Default|하나의 서버 프로세스가 사용 가능한 최대 SQL 작업 영역의 크기, 각각의 서버프로세스는 해당 값을 초과할 수 없다.
_SMM_PX_MAX_SIZE|X|Default|하나의 병렬 실행에 속한 SLAVE 프로세스들이 사용가능한 최대 SQL 작업 영역의 크기. 전체 총합을 의미
_PGA_MAX_SIZE|X|Default|하나의 서버 프로세스가 사용 가능한 최대 PGA 크기를 지정, 각각의 서버프로세스는 해당 값을 초과할 수 없다.

- _SMM_MAX_SIZE, _SMM_PX_MAX_SIZE, _PGA_MAX_SIZE는 PGA_AGGREGATE_TARGET 값에 영향을 받는다.

---

# 질문 
1. WORKAREA_SIZE_POLICY에서 AUTO와 MANUAL이 왜 서로 상반되는 기능이 아니라 PGA 크기를 결정 or 정렬 공간 설정 인지

    http://wiki.gurubee.net/pages/viewpage.action?pageId=6260127

    단순히 POLICY값을 AUTO로 지정하면, PGA_AGGREGATE_TARGET에 의해 정렬 및 해쉬 공간의 크기가 알아서 지정되니까 <br>
    정렬 및 해쉬 공간을 바꾸고 싶으면 POLICY값을 MANUAL로 하고 SORT_AREA_SIZE, HASH_AREA_SIZE를 지정하면 된다 로 이해하면 되는건가요?
---

### 3) SGA(System Global AREA)의 개념

SGA란?

    - 오라클이 SQL을 수행하기 위해 데이터를 읽거나 변경할 때 사용하는 공용 메모리 영역
  
항목 | 내용 | 파라미터
:---:|---|---
Shared Pool | SQL의 빠른 파싱(Parsing) | SHARED_POOL_SIZE(동적 영역)
데이터 버퍼 캐시(Data Buffer Cache) | 데이터 블록의 빠른 엑세스(재사용 포함), 실제 데이터에 대한 캐시 역할 | DB_CACHE_SIZE(일반 영역), <br>DB_KEEP_CACHE_SIZE(고정 영역),<br> DB_RECYCLE_CACHE_SIZE(재활용영역)
리두 로그 버퍼(Redo Log Buffer) | 모든 변경 사항에 대한 로그를 기록하여 장애 발생 시 복구(Recovery) | LOG_BUFFER
Large Pool | UGA 영역 저장, RMAN(Recovery Manager) 정보 저장, 병렬 프로세스 정보 저장, I/O 슬레이브 프로세스 정보 저장 | LARGE_POOL_SIZE
자바(Java) Pool | 자바의 명령에 대해 파싱할 경우 사용하는 공간 | JAVA_POOL_SIZE
Streams Pool | 기존의 데이터 복제 및 Event를 원격의 다른 DB로 전송하는 Stream을 위한 공간.|STREAMS_POLL_SIZE 

### 4) SGA의 관리
- SGA 설정 값을 변경하고자할 경우 전체 SGA를 합한 값이 SGA_MAX_SIZE 파라미터에서 정한 값 이하까지 ALTER SYSTEM SET 명령을 이용하여 변경할 수 있다.
- SGA의 크기 확인은 다음과 같은 데이터 딕셔너리 뷰 조회 또는 SQL로 가능하다
  - V$SGA
  - V$PARAMETER
  - V$SPPARAMETER
  - V$SGA_DYNAMIC_COMPONENTS
  - show parameter 명렁어
  
## 02 Shared Pool

Shared Pool 이란?

    파라메터 정보, 실행된 SQL, SQL 분석/실행 정보 및 오라클 오브젝트 정보를 저장하는 메모리 영역으로 SQL 파싱을 위한 공간
- `SQL 파싱은 어떤 유저던지 파싱 정보를 공유해서 사용할 수 있어서 Shared Pool에서 진행되는 것 같다.`

파싱(Parsing)이란?

    유저 프로세스에서 요청한 SQL을 수행하기 전에 수행할 수 있는 SQL인지 아닌지를 검증하고 분석하는 단계
- 이와 같은 파싱은 소프트 파싱과 하드 파싱으로 구분된다.

항목|내용
:---:|---
소프트 파싱 | 기존에 동일한 SQL이 수행된 걸 확인하고 해당 SQL의 파싱 정보를 재사용
하드 파싱 | 기존에 동일한 SQL이 수행되었지만 메모리 부족으로 LRU 알고리즘에 의해 버려지거나 수행된 적이 없는 SQL로, 다시 파싱을 수행

Shared Pool의 목적 : 파싱을 효과적으로 수행, 이전에 수행된 SQL은 소프트 파싱 유도, 하드 파싱 시 자원 사용 최소화

|항목|구성 요소|구성 요소
|:---:|---|---
|고정영역||프로세스 목록/세션 목록/Enqueue 목록/트랜잭션 목록
|동적영역|라이브러리 캐시| 메타 정보 : 해쉬테이블<br> Subpool1 : LRU 리스트/Shared Pool Latch/Free 리스트<br> Subpool2 : LRU 리스트/Shared Pool Latch/Free 리스트 <br> - SQL을 수행하기 위한 모든 정보를 저장 <br> - Subpool 별로 LRU 리스트, Free 리스트 및 Shared Pool Latch 사용
||데이터 딕셔너리 캐시(로우 캐시)|시스템 테이블스페이스의 딕셔너리 정보 저장(테이블의 메타데이터)
|Reserved 영역||동적 메모리 할당을 위한 공간으로 공간을 많이 필요로 하는 SQL 파싱에 주로 사용
<br>

아키텍쳐 항목|목적
:---:|---
해쉬 테이블|메모리 크기 내에서 지금까지 수행된 모든 SQL을 저장
LRU(Least Recently Used) 리스트|최근에 가장 적게 사용된 SQL을 메모리에서 삭제하여 자주 사용될 SQL 정보를 유지하는 리스트

### 1) Shared Pool의 구성

항목|목적
:---:|---
고정 영역 | 오라클이 SGA를 관리하는 메커니즘 및 오라클 파라미터 정보를 저장
동적 영역 | 라이브러리 캐시와 데이터 딕셔너리 캐시로 구분
Reserved 영역 | 동적 메모리 할당을 위한 공간

- 동적 영역은 다음과 같이 두 가지로 구분된다

항목 | 목적
:---:|---
라이브러리 캐시 | DB에 접속한 유져가 실행한 SQL, 오라클이 내부적으로 사용하는 SQL, SQL에 대한 분석 정보, 실행계획 등이 저장됨. 파싱이 수행되는 공간
데이터 딕셔너리 캐시<br>(로우 캐시)|테이블, 인덱스, 함수 및 트리거 등 오라클 오브젝트 정보 및 권한 외에도 시스템 테이블스페이스의 모든 딕셔너리 정보가 저장됨.

### 2) 라이브러리 캐시의 Subpool
Latch와 Enqueue란?

    Latch : 메모리에 대한 락(Lock) 메커니즘
    Enqueue : 테이블 등의 오브젝트에 대한 락(Lock) 메커니즘

    PGA의 경우 공유 자원이 아니므로 Latch 등으로 Lock을 구현하지 않지만, SGA는 공유 자원이므로 많은 Latch가 존재한다.

- SQL에 대한 하드 파싱을 수행하려면 라이브러리 캐시에서 메모리를 할당받아야하는데 이때 Subpool의 유무에 따라 할당 받는 과정이 달라진다.

- Subpool이 존재하지 않는 경우
  - 메모리 조각(Chunk)를 할당해주는 Shared Pool Latch가 하나이므로 모든 서버 프로세스는 하나의 Shared Pool Latch에게 요청한다.

- Subpool이 존재하는 경우
  - 라이브러리 캐시가 여러개의 Subpool로 구분되어 있고 각각의 Subpool에는 Latch가 존재하므로 모든 서버 프로세스는 할당받은 Subpool의 Shared Pool Latch에 요청한다.

- Subpool의 장점과 단점
  - 장점 : Shared Pool Latch 경합 감소, 1개라서 경합이 일어난다.
  - 단점 : 너무 많은 개수로 Subpool을 구성하면 프리 리스트에서 사용 가능한 메모리 조각을 찾지 못해 ORA-4031 에러가 발생

### 3) 라이브러리 캐시의 해쉬 테이블
- 기존의 SQL 검색 속도 향상을 위해 사용한다.

- 파싱 수행 과정
  
순번|항목|발생 주체 또는 발생 지점
:---:|---|---
1|문장 확인(Syntax Check) | Shared Pool의 라이브러리 캐시 및 데이터 딕셔너리 캐시
2|Semantic 확인(Database Resolution)|Shared Pool의 데이터 딕셔너리 캐시
3|검색(Search)|Shared Pool의 라이브러리 캐시, `해싱 할때는 SQL의 ASCII 값을 사용한다.`
4|Optimization|옵티마이저
5|TM 락|서버 프로세스, 파싱 트리(Parsing Tree)를 만드는동안 테이블이 수정되지 않도록 lock을 건다.

해싱을 쓰는 이유?

    데이터가 10000개라 가정하고, 100개의 Bucket에 균일하게 해싱되어있다 했을 때, 10000개의 데이터를 모두 살펴보는 것이 아니라 100개의 데이터(Object handle)만 확인한다.
    해싱할 때 대소문자가 서로 다른 ASCII 값을 가지고 있으므로 같은 SQL문이라도 대소문자가 다르면 다른 해싱 값을 갖는다. 띄어쓰기 및 오브젝트 소유자도 일치해야한다.

---
# 질문
1. Database Resolution이 뭔가요?, 참조 테이블 및 컬럼 그리고 권한을 확인하는 작업인가요?
---

### 4) Shared Pool의 공간 관리(해시 테이블 공간)
- Shared Pool의 크기는 제한되어 있으므로 SHARED_POOL_SIZE 파라미터에 지정된 크기 이상의 정보가 저장되어야 한다면, 과거에 저장되어 있던 정보를 제거하고 새로운 정보를 저장하게 된다. 
- 오라클은 `LRU(Least Recently Used) 알고리즘`을 통해 해시 테이블의 Object Handle을 제거하거나 유지한다.

- 사용할 수 있는 메모리 공간을 '사용가능 메모리 조각(Free Chunk)'이라고 하며 해당 조각들은 Shared Pool Latch에 의해 할당된다. 이러한 메모리 조각을 관리하는게 LRU 리스트이다.
- LRU 리스트의 양 끝을 MRU(Most Recently Used) End, LRU(Least Recently Used) End라고 한다
- 최근에 사용된 데이터는 MRU쪽에 가장 오래전에 사용된 데이터는 LRU쪽으로 이동한다.

<br>

- 메모리 조각을 할당받는 순서
  
순번|내용
:---:|---
1|Shared Pool Latch 획득 후 Free 리스트를 검색, 빈곳이 있는지 검색
2|라이브러리 캐쉬의 LRU 리스트를 검색
3|Reserved Free 리스트를 탐색
4|Spare Free 메모리 탐색

Reserved Free 리스트

    크기가 큰 객체 저장, 동적 메모리 할당 시 메모리 조각 부족으로 인한 SQL 실행 실패(ORA-4031) 방지
    Shared Pool 의 구성요소

Spare Free Memory(리스트)

    단편화 최소화를 위해 일정 크기를 고정 영역에 숨겨둠, 기동 후 처음 50% 정도는 Free List에 올리지 않고 숨겨둔다.
    메모리 할당이 꼭 필요한 경우 이 영역에서 할당 받는다.

### 5) Shared Pool의 Reseved 공간
- 메모리 조각 부족으로 인해 발생하는 SQL 수행 실패(ORA-4031)를 방지하기 위한 미리 예약해둔 공간
- SHARED_POOL_RESERVED_SIZE 파라미터의 특징
  - 따로 설정하지 않으면 기본 공간은 Shared Pool 크기의 5%
  - 최대 Reserved 공간은 Shared Pool 크기의 50%
- 단점 : 4,400 Byte 이하의 SQL은 Reserved 공간을 사용하지 않으므로 Reserved 공간을 크게 잡으면 메모리 낭비가 발생할 수 있다.
- Shared Pool의 5 ~ 10% 정도가 적당하다.

## 03 데이터 버퍼 캐시(Data Buffer Cache)
데이터 버퍼 캐시란?

    오라클이 데이터를 읽고 수정하기 위해 디스크에 존재하는 데이터를 읽어 저장하는 공간

`디스크에서 데이터를 읽어오는 것(Physical Read) 보다 메모리에서 데이터를 읽는 것(Logical Read)가 훨씬 빨라서 사용하는 캐시, CPU 명령어 캐시랑 똑같은 역할`

- 데이터 버퍼 캐시도 Shared Pool의 라이브러리 캐시처럼 LRU 알고리즘으로 새로 적재하고 제거한다.

### 1) 데이터 버퍼 캐시 활용
- 데이터 버퍼 캐시를 사용하는 프로세스들의 역할

항목|내용
:---:|---
서버 프로세스|디스크로부터 필요한 데이터 블록을 엑세스하여 데이터 버퍼 캐시에 저장하는 역할
DBWR(Database Witer)<br>백그라운드 프로세스|데이터 버퍼 캐시에 저장되어 있는 블록 중 수정된 블록의 내용을 디스크로 쓰는 역할

- DB_FILE_MULTIBLOCK_READ_COUNT 파라미터에 지정된 수만큼 데이터 블록을 데이터 버퍼 캐시로 한 번에 읽는다.
- `오라클의 I/O 단위는 데이터 블록이다.` 그래서 데이터 하나만 읽으려고 해도 해당 데이터가 포함된 데이터 블록을 읽어온다.

### 2) 다중 데이터 블록 크기 지정
- DB_BLOCK_SIZE 파라미터로 데이터 블록의 크기를 지정할 수 있다. 
- 9i 부터는 여러 개의 데이터 블록을 지정할 수 있게 되었음. 변경하려면 init\<SID>.ora를 변경하면 된다. 여기서\<SID> 는 전역 데이터베이스 이름.

### 3) 데이터 블록 크기와 데이터 버퍼 캐시
- 데이터 블록을 크게 했을 경우

항목|내용
:---:|---
장점|- 메모리에서 데이터 블록 사용율이 높음 (하나의 블록이 많은 데이터를 담고 있어서 자주 사용됨)<br> - 한 번의 디스크 I/O로 많은 데이터 추출 가능
단점|데이터 블록에 대한 경합 발생 가능성 증가 (하나의 블록이 많은 데이터를 담고 있어서 유저가 경쟁)

- 데이터 블록을 작게 했을 경우

항목|내용
:---:|---
장점|데이터 블록에 대한 경합 발생 가능성 감소 (하나의 블록이 적은 데이터를 담고 있어서 유저의 경쟁이 줄어듦)
단점|- 메모리에서 데이터 블록 사용율이 낮음 (하나의 블록이 적은 데이터를 담고 있어서 덜 사용됨)<br> - 한 번의 디스크 I/O로 적은 데이터 추출 가능
- 데이터 블록 크기는 대부분 8K로 설정하여 사용하면 큰 문제는 없다.

### 4) 다중 데이터 버퍼 캐시 설정
- 데이터 버퍼 캐시를 어무 성격에 따라 분리하는 것

종류|내용|크기
:---:|---|---
기본(Default)|일반 데이터 버퍼 캐시 DB_CACHE_SIZE 파라미터로 설정. 일반적인 테이블이나 인덱스 적재|중간
고정(Keep)|재사용률이 높다고 판단하여 가능하면 삭제하지 않으려고 하는 데이터 버퍼 캐시 DB_KEEP_CACHE_SIZE 파라미터로 설정. 자주 사용되고 성능을 좌우할 수 있는 테이블이나 인덱스를 적재|가장 큼
재활용(Recycle)|재사용이 거의 안된다고 판단하여 해당 메모리 블록들은 빠른 시간 안에 제거되게 된다. DB_RECYCLE_CACHE_SIZE 파라미터로 설정. 자주 사용되지 않는 테이블을 적재|가장 작음

- `고정, 재활용이라는 말은 캐시 공간을 고정하고, 자주 재활용 한다 라는 의미` 
  
## 04 리두 로그 버퍼(Redo Log Buffer)
### 1) 리두 로그 버퍼의 개념 및 목적
리두 로그 버퍼란?

    개념 : 오브젝트 및 데이터 변경 시 생성되는 로그를 저장하는 SGA 메모리 공간
    목적 : 데이터베이스내의 모든 변경 작업에 대한 복구(Recovery)를 지원

- 해당 로그 들은 서버 프로세스에 의해 리두 로그 버퍼에 기록된 후 백그라운드 프로세스인 LGWR(Log Writer) 프로세스에 의해 파일에 저장된다.

- 복구(Recovery)와 롤백(Rollback)

항목|개념|주체
:---:|---|---
복구|장애에 대한 데이터베이스 복구|리두 로그 파일 + 언두 데이터
롤백|작업에 대한 작업 전 데이터로 복구|언두 데이터

### 2) 리두 로그 버퍼의 아키텍쳐

#### (1) Physiological 로깅
- 데이터베이스 로깅에는 아래와 같이 3가지가 존재한다.

종류|내용
:---:|---
Logical 로깅 | 작업에 대한 전후 이미지가 아닌 작업의 명세를 기록
Physigal 로깅 | 변경된 블록에 대한 전후 이미지를 모두 저장
Physiological 로깅 | 변경된 데이터에 대해서는 전후 이미지를 저장, 작업의 명세를 기록

#### (2) Write-Ahead 로깅
- 로그를 기록하는 작업을 먼저 수행, 실제 데이터에 대해 DML을 수행하기 전에 변경에 대한 내용을 리두 로그 버퍼에 기록

종류|내용
:---:|---
Logical 버퍼 Ahead|실제 블록 변경 전 리두 로그를 로그 버퍼에 먼저 기록
로그 파일 Ahead|DBWR이 블록을 데이터 파일에 기록하기 전에 LGWR이 리두 로그 버퍼의 리두 로그를 로그 파일에 기록

#### (3) 로그 Force At Commit
- 작업에 대한 Commit 발생시 해당 작업에 의해 발생한 데이터 버퍼 캐시에 존재하는 데이터 버퍼를 데이터 파일에 기록하는 것이 아니라 해당 작업의 리두 로그 버퍼의 내용을 로그 파일에 기록한다. 
- 따라서 Commit된 데이터는 반드시 리두 로그 파일에 로그를 기록하게 된다.


#### 리두 로그의 생성 과정
1. DML이 발생하는 대상 데이터 블록 변경 제한: 데이터 블록에 락 걸기
2. 리두 로그 생성 
3. 리두 로그에 대한 통계정보를 수집
4. 리두 Copy Latch 획득: 리두 로그를 기록하기 위해 먼저 값을 복사할 수 있는 권한 Latch를 얻는다.
5. 리두 Allocation Latch: 리두 로그를 기록할 데이터 공간을 할당받기 위한 Latch를 얻는다.
6. SCN(System Change Number) 할당: 트랜잭션이 커밋될 때 마다 순차적으로 증가하는 숫자 할당. 리두 레코드의 헤더 파일에 저장하기 위해 SCN을 할당받는다.
7. 리두 로그 버퍼 공간 확인: Copy&Allocation Latch 획득 후 로그를 저장할 공간을 찾는다. 공간이 있으면 8단계 없으면 9,10 단계를 수행한다.
8. 리두 로그 기록: 공간이 존재하면 로그를 버퍼에 기록한다.
9. 리두 Writing Latch 획득: 버퍼에 공간이 없으면, 리두 로그 버퍼의 내용을 디스크로 쓰기위한 Writing Latch(LGWR를 기동시킬 수 있는 하나만 존재하는 Latch)를 획득한다.
10. LGWR 기동: Writing Latch를 획득한 프로세스는 LGWR 프로세스를 기동시켜 버퍼의 내용을 디스크에 쓰고 공간을 확보하여 8단계를 수행한다.

- Latch와 Enqueue: 자원의 정합성을 유지하기 위한 락개념

항목|Latch|Enqueue
:---:|:---:|:---:
대상 자원|메모리|오브젝트
락 모드|대부분 Exclusive 모드|Exclusive/Share 모드
자동 여부|자동으로 수행|인위적으로 수행
락 시간|짧은 시간|짧은 시간/긴 시간

- 리두 로그 버퍼 관련 Latch
  - 리두 로그 버퍼는 메모리 영역이므로 해당 공간에서 락이 필요하게 되면 Latch를 사용하게 된다.
  
항목|개수|내용
:---:|:---:|---
리두 Allocation Latch|1개 존재|리두 로그 버퍼에서 사용할 공간 할당
리두 Copy Latch|N개 존재|리두 로그 버퍼에서 리두 로그를 기록
리두 Writing Latch|1개 존재|LGWR를 기동시켜 버퍼의 내용을 디스크 로그 파일에 기록

#### 3) 리두 로그의 성능
- 리두 로그 버퍼는 기본 값만으로도 최적화 되어 있지만, 과다하게 트랜잭션을 수행하여 로그를 많이 생성한다면 성능 저하가 발생할 수 있다. 다음과 같은 방법으로 리두를 적게 사용할 수 있다.

항목|사용방법|내용
:---:|:---:|---
SQL 로더의 직접 로딩<br>(Direct Loading)|Unrecoverable 옵션 사용|OS의 일반적인 읽을 수 있는 파일을 테이블로 로딩하는 경우 사용
Insert에서의 직접 로딩<br>(Direct Loading)|Append 힌트 이용<br>/Nologging 옵션 이용|Select 후 Insert하는 대용량 Insert에서 사용 가능
인덱스 Rebuild|Nologging 옵션 이용|많은 DML로 인덱스의 균형이 어긋나는 경우 주기적으로 수행
인덱스 생성|Nologging 옵션 이용|조회 속도 향상을 위한 인덱스 생성 작업
Create Table as Select<br>(CTAS)|Nologging 옵션 이용|기존 테이블을 복사하는 경우 사용

- 리두 Less 작업의 장단점

항목|내용
:---:|---
리두 Less 작업의 장점|디스크 I/O 감소로 인해 작업 속도의 향상
리두 Less 작업의 단점|장애 발생시 해당 테이블 또는 백업본이 없는 경우 복구 불가

## 05 Large Pool
### 1) Large Pool 개념
- Large Pool을 지정하게 되면 Shared Pool의 부하를 감소시키게 된다.

항목|내용
:---:|---
UGA 영역 저장|UGA는 세션별로 메모리가 할당되지만 DB가 공유 서버 환경으로 설정되어 있다면, `Shared Pool을 사용하게 된다. 이런 경우 파싱을 수행하는 중요한 Shared Pool 영역이 공간이 감소하게 되는데`, 이를 방지하기 위해 Large Pool을 설정하게 되면 공유 서버 환경에서도 UGA 영역이 Large Pool을 사용한다.
RMAN(Recovery Manager)의 정보 저장|BACKUP_DISK_IO=n과 BACKUP_TAPE_IO_SLAVE=TRUE로 파라미터를 설정하면 I/O 슬레이브 프로세스는 LArge Pool을 사용한다.
병렬 프로세스의 정보를 저장|`Large Pool이 설정되어 있지 않다면 병렬 프로세스 메시지(PX MSG)가 Shared Pool을 사용`하게 되어 이를 방지하기 위해 Large Pool을 사용하도록 설정한다.
I/O 슬레이브 프로세스의 정보 저장|DBWR 프로세스는 해당 프로세스 아래에 슬레이브 프로세스를 기동시켜 더 빠른 디스크 I/O 작업을 수행한다. 이 `슬레이브 프로세스들 사이에서도 통신을 수행하는 과정에서 사용되는 메시지가 Large Pool을 사용`하게 하기위해 Large Pool 설정을 한다.

RMAN(Recovery Manager) 란?

    오라클은 백업과 복구를 위해 RMAN이라는 유틸리티를 제공하고 있다. 
    * 해당 유틸리티를 사용하게 되면 여러 개의 I/O 슬레이브 프로세스를 기동한다.

- 병렬 프로세싱을 수행한다면 반드시 Large Pool을 설정해야 효과를 얻을 수 있다. 병렬 프로세스 간에 주고받는 메시지의 크기가 매우 커질 수 있기 때문이다. -> Large Pool을 설정하지 않으면 Shared Pool을 사용하게 되니까!

### 2) Large Pool 설정

항목|내용
:---:|---
파라미터 파일 변경 후 <br>데이터베이스 재기동|정적 파라미터 파일인 경우 해당 파일에서 LARGE_POOL_SIZE 파라미터를 설정한 후 DB를 재기동
변경 수행|ALTER SYSTEM SET 명령어로 동적으로 전체 시스템에 적용 가능 하지만, 파라미터 파일에 기록해야 다음 재기동시 변경된 값이 적용됨

변경 수행 명령문
  
    SQL> ALTER SYSTEM SET LARGE_POOL_SIZE = 500M;

## 06 자바(Java) Pool 및 Streams Pool
### 1) 자바 Pool
- Large Pool과 마찬가지로 필요에 따라 지정해서 사용하는 SGA영역
- 자바 명령에 대해 파싱할 경우 사용하는 메모리공간이므로 자바를 설치하고 사용할 경우 지정해주어야 한다.
- JAVA_POOL_SIZE 파라미터로 지정이 가능

### 2) Streams Pool
- Stream은 기존의 데이터 복제 및 Event를 원격의 다른 데이터베이스로 전송할 수 있는데, 이와 같은 Stream을 위한 공간
- 오라클 DB 뿐만아니라 다른 DB로도 복제 및 Event 전송이 가능하다.

- Stream의 3가지 단계

항목|내용
:---:|---
Capture|- DB내에 원하는 오브젝트에 대한 변경된 데이터를 리두 로그로부터 엑세스하는 역할을 수행<br>- 엑세스한 DB 변경을 LCR(Logical Change Record)이라는 Event로 변환
Staging|- Event에 대한 전달이나 사용의 Stage로 큐(Queue)를 사용한다. <br>- 다른 DB로 전달(Propagation)하거나 사용자가 De-Queue할 때까지의 저장소로 큐(Queue)를 사용한다.
Apply|- Destination 큐 에서 LCR을 엑세스 하여 Target 오브젝트에 적용하는 프로세스

---
# 질문 

## 제가 이해한 내용
1. Capture 단계에서는 복제 또는 전달하려는 데이터를 LCR이라는 Event 로 만들(어서 큐에 대기시킨다.)
2. Staging 단계에서는 Capture 단계에서 만든 LRC을 큐에 저장한다.
3. Apply   단계에서는 Staging 단계에서 큐에 넣어둔 LCR들을 엑세스해서 사용자에게 주거나, 다른 DB로 전달한다. (Destination Queue에서 LCR을 읽어내어, Target Object에 적용하는 프로세스)

### 질문 1.
- Staging 단계에서 사용하는 큐는 어떤 큐인가요? Source? Destination?
### 질문 2.
- Source Queue의 소유자는 처음 데이터를 가지고 있는 DB이고 Destination Queue가 목적지가 되는 DB의 소유인가요?
### 질문 3.
- Staging 단계에서 Propagation이 일어나면 Source Queue -> Destination Queue로 이동하는건가요?
### 질문 4.
- 위의 질문에 따라 추가 질문일 수도 있는 질문, Apply 단계에서 Destination Queue에서 LCR을 읽어낸다고 했는데, Source와 Destination 이 같은 DB 소유라면 그냥 단순히 목적에 의해 나누어둔 것 뿐인가요?
### 질문 5. 
- Streams Pool은 필수 메모리 영역이 아닌가요?
---

- Streams Pool을 사용하는 프로그램
  - Oracle Streams(DBMS_STREAMS package)
  - Advanced Queuing(DBMS_AQADM package)
  - Datapump export/import
  - OGG(Oracle Golden Gate) Integrated Mode

오라클 10g 이상에서는 STREAM_POOL_SIZE로 Maual하게 지정하거나 변경할 수 있음.
  
    SQL> ALTER SYSTEM SET streams_pool_size=100 K|M|G;

## 07 오라클 메모리 관리
### 1) 공유 메모리 자동 관리 개념
- 공유 메모리 자동 관리를 사용하게되면 MMAN(Memory Manager)프로세스가 주기적으로 업무 부하에 따른 SGA 사용량을 파악한다.
- 파악한 정보로 SGA_TARGET 파라미터가 지정한 범위 내에서 SGA 구성 요소의 크기를 동적으로 지정한다.
- 각 메모리 영역의 크기가 너무 크거나 작은 경우에 메모리 낭비 또는 성능 저하를 일으키므로 업무 부하를 판단하여 각 메모리의 크기를 자동으로 조정하는 공유 메모리 자동관리(Automatic Shared Memory Managemenrt, ASMM)기능을 사용해야한다.

### 2) 공유 메모리 자동 관리 특징
항목|내용
:---:|---
SGA 관리 요소 감소|데이터베이스 관리자가 수행하던 SGA 구성요소 크기 조정을 오라클이 자동 조정
메모리 사용 효율 증가|업무 부하에 따라 SGA 구성 요소의 크기가 동적으로 조정되어 메모리 효율 증가
메모리 부족으로 인한 에러 감소|업무 부하에 따라 SGA 구성 요소의 크기가 동적으로 조정되어 메모리 부족현상 감소

- 공유 메모리 자동 관리 기능은 파라미터 파일의 종류에 따라 달라진다.

항목|내용
:---:|---
동적 파라미터 파일(SPFILE)|- 공유 메모리 자동 관리 기능에 의해 동적으로 변하는 SGA 구성 요소의 크기가 파라미터 파일에 자동으로 반영됨. DB 재시작 시 이전 최적화된 메모리 값이 적용됨.<br>- ALTER SYSTEM 명령을 통해 운영 중에도 파라미터를 수정할 수 있고, 서버를 재시작 하지 않아도 반영, 바이너리 파일
정적 파라미터 파일(PFILE)|- 파라미터 파일에 정적으로 반영되지 않으므로 DB를 재시작할 때마다 SGA 최적화를 수행해야함. 공유 메모리 자동 관리 기능 사용 시 동적 파라미터 파일 사용 권장<br>- 오라클을 시작하는데 필수적인 파라미터들이 정의되어 있음. 기본 설정 파일, 서버를 재시작 해야 반영, 텍스트 파일

- 공유 메모리 자동 관리 기능을 사용하기 위해서는 다음과 같은 설정이 필요하다

설정 값|내용
:---:|---
STATISTIC_LEVEL|TYPICAL 또는 ALL
SGA_TARGET|SGA_MAX 값 이하까지 운영 중 동적으로 적용 가능, 0이 아닌 값으로 설정

- STATISTIC 파라미터 

설정 값| 내용
:---:|---
BASIC|통계를 수집하지 않으며 AWR, ADDM, 공유 메모리 자동 관리, 자동 옵티마이저 통계 수집 기능 사용불가
TYPICAL|기본 값으로 데이터베이스 통계 수집
ALL|TYPICAL 수집 데이터 이외에 운영 체제 통계와 SQL 실행계획 통계를 추가로 수집

- 공유 메모리 자동 관리의 단점
  - 일반적으로 공유 메모리 자동 관리는 추천하지 않음, 기존의 수동 관리가 더 유리한 경우가 많다.
<br>1) 관리 항목 증가 : MMAN 프로세스가 비정상 종료시 장애 발생
<br>2) 성능 저하 가능 : MMAN 프로세스의 주기적인 모니터링에 의한 자원 사용
<br>3) 정확한 메모리 관리가 어려움 : Literal SQL 등이 많은 경우에는 Shared Pool이 비정상적으로 커지는 현상 발생, 메모리 자동 관리 어려움

- Literal SQL : 동일한 SQL이지만 바인드 변수 처리를 하지 않아 SQL을 공유할 수 없어 하드 파싱을 일으키는 형태의 SQL

### 3) 공유 메모리 자동 관리 사용 시 고려 사항

고려 사항|내용
:---:|---
관리 영역 구분|MMAN 백그라운드 프로세스가 관리하지 않는 SGA 구성 요소와 관리하는 구성 요소에 대한 정확한 이해 필요
관리 대상에 대한 특정 값 설정|MMAN 백그라운드 프로세스에 의해 관리되는 메모리 영역의 값을 설정했을 경우

- MMAN 프로세스가 관리하지 않는 구성 요소, 고려 사항 1
  
항목|내용
:---:|---
고정 영역|Shared Pool에 저장된 고정 영역
다중 블록 데이터 버퍼 캐시|기본 데이터 버퍼 캐시를 제외한 DB_2K_CACHE_SIZE 같은 파라미터로 지정되는 다중 블록 데이터 버퍼 캐시
고정 또는 재활용 데이터 버퍼 캐시|DB_KEEP_CACHE_SIZE 또는 DB_RECYCLE_CACHE_SIZE로 지정되는 고정 또는 재활용 데이터 버퍼 캐시
리두 로그 버퍼|LOG_BUFFER로 설정하는 리두 로그 버퍼
- 따라서 상기 4개 영역의 메모리가 1GB이고, SGA_TARGET 값이 5GB라면, Shared Pool, 기본 데이터 버퍼 캐시, Large Pool, Java Pool은 MMAN 백그라운드 프로세스에 의해 4GB에서 자동 분배된다.

- MMAN 프로세스가 관리하는 메모리 영역의 값을 모두 설정했을 경우, 고려 사항 2
  
항목|내용
:---:|---
'0'으로 설정 | MMAN 프로세스가 각 SGA의 구성 요소 크기를 자유롭게 증가시키고 감소시킬 수 있다. But SGA 그래뉼 단위 이상의 값이어야 하므로 최소 크기는 4MB
'0'이 아닌 다른 값으로 설정 | SGA 구성 요소의 크기가 자동으로 변경되지만 사용자가 지정한 값 이하로 감소하지는 않는다. 지정한 값보다 큰 범위에서 조정된다.
- 값을 설정하는 이유는 각 구성요소의 크기 하한선을 정하기 위해서이다. 
- DBA가 경험상 데이터 버퍼 캐시가 1GB 이하로 감소되면 성능이 저하될 수 있다는걸 인지하고 있는 경우 DB_CACHE_SIZE를 1GB로 설정해 하한 값을 지정할 수 있다.

그래뉼 단위
    
    - Granule (명사) : 미립, 고운알, 과립, 작은공
    - SGA의 할당 단위로써, 9i 이하 버전에서는 SGA크기가 128MB보다 크면 16MB단위로 작으면 4MB 단위로 할당된다.
    - 10g에서는 기준이 바뀌어서, SGA 크기가 1GB보다 크면 16MB 단위로 작으면 4MB 단위로 할당된다.

### 4) 공유 메모리 자동 관리 확인
공유 메모리 자동 관리 모드에서 자동으로 설정한 SGA의 크기를 검색하기 위한 SQL

    SQL> SELECT * FROM V$SGA_DYNAMIC_COMPONENTS;
    
- 추출되는 컬럼들의 의미

컬럼명|내용
:---:|---
COMPONENT|SGA 구성 요소
CURRENT_SIZE|현재 SGA 구성 요소의 크기
MIN_SIZE|데이터베이스 시작 후 할당되었던 가장 작은 크기
MAX_SIZE|데이터베이스 시작 후 할당되었던 가장 큰 크기
USER_SPECIFIED_SIZE|사용자가 직접 설정한 SGA 구성 요소 크기(SGA 하한 값)
OPER_COUNT|데이터베이스 시작 후 조정되었던 횟수
LAST_OPER_TYPE|가장 마지막으로 조정된 타입
LAST_OPER_MODE|가장 마지막으로 조정된 방법
LAST_OPER_TIME|가장 마지막으로 변경된 시간
GRAULE_SIZE|SGA 그래뉼 단위

- LAST_OPER_TYPE 컬럼을 통해 어떻게 변경되었는지를 확인할 수 있으며, 다음과 같은 값이 저장될 수 있다.

가능 값 | 내용
:---:|---
STATIC|데이터베이스 시작 후 변동 없음
INITIALIZING|초기화
GLOW|크기 증가
SHRINK|크기 축소
SHRINK_CANCLE|크기 축소 중 취소

- LAST_OPER_MODE 컬럼을 통해 가장 마지막으로 조정된 방법을 확인할 수 있으며, 다음과 같은 값이 저장될 수 있다.

가능 값 | 내용
:---:|---
MANUAL|사용자가 직접 수정
DEFERRED|수정 값이 지연되어서 적용
IMMEDIATE|수정 값이 바로 적용

공유 메모리 자동 관리의 실무 적용 시 주의 사항

    SGA 구성 요소의 값을 설정하지 않으면 공유메모리 자동 관리에 의해 메모리 구조가 완전히 변경될 수 있으므로 최소 값을 설정해두는 것, 어떤 하나의 항목의 크기가 너무 작게 설정되는 것을 방지할 수 있다.