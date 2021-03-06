# Chap 12. 언두 데이터
## 01 언두 데이터의 개념
<img src=https://t1.daumcdn.net/cfile/tistory/226E834454FA0E613B />

#### 위의 그림을 통해 언두 데이터에 대해 확인해보자.
- 언두 데이터: DML이 발생할 경우 변경되기 전의 데이터 값
- 언두 세그먼트: 언두 데이터를 저장하는 세그먼트
- 언두 테이블스페이스: 언두 세그먼트를 저장하는 테이블스페이스

위의 그림에서 '서울'이라는 위치 컬럼의 데이터가 언두 데이터이며, 해당 컬럼은 변경 작업에 의해 '분당'으로 변경되므로 변경되기 전인 '서울'값이 언두 데이터가 된다.<br>
해당 언두 데이터는 '서울'에서 '분당'으로 값을 변경하기 전에 언두 세그먼트에 저장되어 롤백(Rollback) 등의 작업 수행 시 사용한다.

## 02 언두 데이터의 목적
<img src=https://t1.daumcdn.net/cfile/tistory/246FFC4454FA0E613A />

#### 언두 데이터의 3가지 목적
목적|내용
:---:|---
작업 롤백|작업 수행 중이나 후에 커밋을 수행하지 않고 작업을 취소한 경우
읽기 일관성|변경 중인 데이터 또는 변경된 데이터에 대한 조회 시 정합성 보장
복구|시스템 장애 시 커밋(Commit)이 수행된 작업까지 복구

### 1) 작업 롤백
- 특정 작업을 수행한 후 커밋을 수행하지 않고 롤백을 수행하게 되면 작업 수행전의 데이터로 복구되는 기능이다.

#### 롤백 절차
<img src=https://t1.daumcdn.net/cfile/tistory/2148844454FA0E6106 />

1. 유저에 의해 (1) 변경 작업 수행
2. 변경 작업을 수행하기 전에 (2)와 같이 롤백을 위해 변경전 데이터인 '서울'을 언두 데이터로 생성하여 언두 세그먼트에 저장
3. 변경 작업을 통해 (3)과 같이 '서울'을 '분당'으로 변경 수행
4. 유저에 의해 (4)와 같이 롤백 수행
5. 언두 세그먼트에 존재하는 언두 데이터를 (5)와 같이 부서 테이블에 복구하여 '분당'인 값을 '서울'로 복구

#### 롤백
- 롤백은 변경전의 데이터로 복구한느 작업을 의미하며 해당 작업에 대해 커밋을 수행했다면 더 이상 롤백을 수행할 수 없다.<br>커밋은 롤백을 수행하지 않고 변경 작업을 확정하는 의미이기 때문

### 2) 읽기 일관성(Read Consistency)
- 조회하는 도중에 발생한 변경 데이터에 대해 어떤 데이터를 보여주는 것이 옳은가에 대한 개념

<img src=https://t1.daumcdn.net/cfile/tistory/214E164454FA0E6204 />

#### 위 작성 상황에 대한 가정
- 수행 시간이 많이 소요되는 조회 수행
- 조회 대상 데이터 중 조회가 이루어지지 않은 데이터에 대해 다른 유저에 의해 변경 작업 발생 및 커밋 완료
- 변경 작업이 수행된 후 해당 데이터에 대해 조회

조회가 이루어지는 상황에서 변경된 데이터에 대해 변경된 데이터를 추출하는가 아니면 변경되기 전의 데이터를 추출하는 가의 의미가 읽기 일관성이다.<br>
오라클에서는 조회가 먼저 수행되었다면 수행된 시점을 기준으로 조회 중 변경된 데이터는 조회 이후 시점이므로 변경 이전의 데이터(언두 데이터)를 결과로 추출하도록 설계되어있다.<br>
오라클에서는 이러한 읽기 일관성을 지원하기 위해 언두 데이터를 이용한다.

#### 읽기 일관성 수행 절차
<img src=https://t1.daumcdn.net/cfile/tistory/2652DC4454FA0E6202 />

1. (1)과 같이 부서 테이블에 대한 조회를 수행한다. 
2. [10, DM팀, 서울]인 데이터를 읽기 전에 다른 변경 프로세스에 의해 (2)와 같이 위치 컬럼의 값을 '분당'으로 변경을 수행한다.
3. 변경을 수행하기 위해 이전 데이터인 '서울'을 (3)과 같이 언두 데이터로 생성하여 언두 세그먼트에 저장한다.
4. (4)와 같이 (1)에서의 조회 프로세스가 변경된 데이터에 접근한다.
5. (2)에서의 변경 프로세스가 변경된 데이터에 대해 (5)와 같이 커밋을 수행했는지 안 했는지에 따라 결과가 다르게 추출될 수 있다.
6. 커밋을 수행했더라도 해당 변경 프로세스는 조회 프로세스보다 뒤에 수행되었으므로 이전 값을 추출 해야한다. 그렇기 때문에 언두 세그먼트로 이동해서 해당 데이터에 대한 언두 데이터를 검색한다. 언두 데이터가 존재하지 않는다면 ORA-1555(Snapshot Too Old) 에러를 발생시키고, 조회 프로세스는 비정상 종료된다.
7. 커밋을 수행하지 않았다면 6단계와 마찬가지로 이전 데이터를 언두 세그먼트로 이동해서 찾는다. 이 경우에는 언두 데이터가 반드시 존재하므로 ORA-1555 에러가 발생하지 않는다.<br>하지만 커밋된 데이터의 경우에는 언두 세그먼트에서 삭제될 수 있으므로 해당 에러가 발생할 수 있다.


#### 언두 데이터를 호출하는 기준
커밋 수행 여부가아니라 작업 수행한 시점으로 언두 데이터를 호출하므로 이를 확인할 수 있는 어떤 값이 존재해야 한다.
구분|내용
:---:|---
커밋이 수행되지<br>않은 경우|커밋이 수행되지 않았다면 해당 로우에 락(Lock)이 수행되고 데이터 블록 헤더의 트랙잭션 테이블에 트랜잭션 중이라고 기록한다.<br>이러한 경우 현재 DML 중이라는 의미이며 해당 데이터는 반드시 언두 데이터에 존재하게 된다.
커밋이 수행된<br>경우|커밋이 수행되었다며 해당 로우에는 락 정보가 해제된다. 그렇기 때문에 락 정보로 언두 데이터를 호출할 수는 없게된다. <br>이 경우에는 오라클의 SCN을 확인하여 조회 프로세스의 SCN이 변경 프로세스의 SCN보다 낮은 경우(조회를 먼저 수행) 언두 세그먼트를 호출한다.

Block Cleanout이란?

    커밋을 수행하면 해당 블록의 트랜잭션 테이블과 락 Byte를 정리하는 작업을 의미한다. 

Delayed Block Cleanout이란?

     해당 데이터 블록이 버퍼 캐시가 아닌 디스크에 존재하는 경우 커밋 시 바로 Block Cleanout을 수행하지 않고 추후 조회 시 수행하는 것을 의미한다.

### 3) 복구
복구를 수행하면 언두 세그먼트의 언두 데이터를 이용하여 복구를 수행한다.
구분|내용
:---:|---
인스턴스 복구|언두 데이터를 이용
미디어 복구| 언두 데이터 일부 이용
<br>

<img src=https://t1.daumcdn.net/cfile/tistory/21704D4454FA0E6239 />

#### 위 작성 상황에 대한 가정
- 시스템 비정상 종료
- 시스템 비정상 종료로 인한 오라클 비정상 종료
- 시스탬 장애 해결 후 오라클 재기동

비정상 종료 전 수행되던 DML에 대해 커밋된 데이터는 데이터 파일에 기록하고 커밋되지 않은 데이터는 롤백을 수행한다.

#### 복구 수행 절차
1. (1)과 같이 장애 발생 시점 이후의 리두 로그 파일을 적용한다. 리두 로그 파일 내부에는 커밋된 데이터와 커밋되지 않은 데이터가 함께 존재하므로, 해당 리두 로그 파일을 적용한 후에 데이터베이스에는 장애전 커밋된 데이터뿐만 아니라 커밋되지 않은 데이터도 함께 존재한다. 
2. (1)번 단계에서 리두 로그의 SQL을 실제 수행하므로 (2)와 같이 언두 세그먼트를 재생성한다.
3. (1)번 단계를 수행한 후 커밋된 데이터만을 오라클에 저장하기 위해 (3)과 같이 재생성된 언두 세그먼트의 언두 데이터를 이용하여 커밋되지 않은 데이터를 롤백한다.
4. 언두 세그먼트 적용 후에는 (3)과 같이 오라클에는 커밋된 데이터만 존재한다.

#### 인스턴스 복구와 미디어 복구
구분|내용
:---:|---
인스턴스 복구|시스템 또는 오라클이 비정상 종료한 후 재기동 시 발생하는 복구 방식, 앞의 예와 같은 절차를 수행하여 데이터 정합성을 보장
미디어 복구|실제 디스크 데이터 파일 등에 장애가 발생하여 기존 백업본을 이용하여 복구를 수행하는 경우

## 03 언두 세그먼트의 개념
### 1) 언두 세그먼트의 특징
<img src=https://t1.daumcdn.net/cfile/tistory/266E1C3D54FA0EAE14 />

#### 언두 세그먼트의 특징
항목|내용
:---:|---
일반 세그먼트와 동일한 구조|테이블은 익스텐트로 구성되며 익스텐트는 데이터 블록으로 구성된다. 언두 세그먼트 또한 익스텐트로 구성되며 해당 익스텐트들은 언두 블록으로 구성된다. 언두 블록과 데이터 블록은 동일하다. 따라서 물리적으로 일반 세그먼트와 언두 세그먼트는 동일한 구조를 가진다.
하나의 작업은 하나의 언두 세그먼트를 사용|언두 테이블스페이스에는 여러 개의 언두 세그먼트가 생성될 수 있다. 그러나 아무리 많은 언두 세그먼트가 존재하더라도 하나의 작업은 하나의 언두 세그먼트만을 사용한다.
언두 블록 단위로 사용|언두 세그먼트의 사용은 언두 블록 단위로 사용한다. 하나의 언두 세그먼트는 여러 개의 작업에 의해 동시에 사용될 수 있다. 하지만 내부의 개별 언두 블록은 하나의 작업에 의해서만 사용 가능하다.

### 2) 언두 세그먼트의 확장
언두 세그먼트는 일반 세그먼트와 동일하게 확장할 수 있다.

<img src=https://t1.daumcdn.net/cfile/tistory/2774B83D54FA0EAF0F />

#### 언두 세그먼트 확장 절차
1. (1)과 같이 어떤 언두 세그먼트에 4개의 익스텐트가 할당되어 있으며 그 중 2개의 익스텐트인 EX1과 EX2는 사용 중에 있다.
2. 사용 중인 2개의 익스텐트가 부족하다면 사용중이 아닌 익스텐트를 확인하게 되며 (2)와 같이 사용중이 아닌 EX3 익스텐트를 사용하여 해당 작업에 대한 이전 이미지를 저장한다.
3. EX3 익스텐트가 모두 사용되면 또 다른 사용 중이 아닌 익스텐트를 찾게 된다. 위 그림에서는 EX4가 사용되고 있지 않으므로 선택되어 다른 작업에 의해 이전 이미지를 저장한다.
4. 해당 언두 세그먼트에 할당된 4개의 익스텐트를 모두 사용한 후 또 다른 작업에 의해 추가적인 언두 세그먼트의 공간이 필요하다면, 이러한 경우 첫 번째 익스텐트를 확인하고 비어있으면 사용 비어있지 않다면 EX5라는 새로운 익스텐트를 할당하여 저장한다.

- 이와 같은 경우에서 익스텐트 1은 사용 중이지만 익스텐트 2는 사용 중이 아니더라도 언두 세그먼트는 확장이 된다. 그 이유는 순서대로 재사용하기 때문이다.

- 언두 세그먼트를 동그랗게 표현하는 이유는 환형 큐처럼 빙글빙글 돌면서 재사용하기 때문

### 3) 언두 세그먼트의 축소

일반 세그먼트는 크기를 감소시키기 위해 Truncate 또는 할당 해제를 수행해야 하지만 언두 세그먼트의 축소는 다르다

<img src=https://t1.daumcdn.net/cfile/tistory/266A073D54FA0EAF16 />

- 언두 세그먼트를 Truncate 절단 했을 경우
- 언두 세그먼트에 Shrink를 수행 했을 경우
- 언두 세그먼트에 Optimal 크기를 할당 했을 경우

종류|내용
:---:|---
Truncate 절단 | 그냥 익스텐트를 절단하여 해제
Optimal 크기 할당|언두 세그먼트가 자동으로 축소될 수 있게 설정, 12시간마다 현재 사용하지 않은 언두 세그먼트의 익스텐트를 반납한다. 최소 4MB까지 축소
Shrink|Optimal과 다르게 수동으로 언두 세그먼트를 축소

## 04 언두 세그먼트의 종류 및 관리 방식
### 1) 언두 세그먼트 종류
<img src=https://t1.daumcdn.net/cfile/tistory/2263BB3D54FA0EB018 />

종류|내용
:---:|---
시스템<br>언두 세그먼트|시스템 테이블 스페이스에 존재하는 오브젝트가 변경될 경우 사용하는 언두 세그먼트, 데이터베이스 생성 시 시스템 테이블스페이스에 자동 생성
비시스템<br>언두 세그먼트|일반 유저의 DML 작업 시 언두 데이터를 저장하기 위해 사용
지연<br>언두 세그먼트|특정 테이블스페이스가 오프라인, 임시 또는 For Recovery로 상태가 변경 될 경우 진행 중인 작업에 대해 복구를 수행하기 위해 해당 테이블스페이스에 대한 언두 세그먼트에 언두 데이터를 보관.

### 2) 언두 세그먼트 관리 방식
자동 언두 관리와 수동 언두 관리가 있다.

<img src=https://t1.daumcdn.net/cfile/tistory/226AE43D54FA0EB015 />

항목|자동 언두 관리|수동 언두 관리
:---:|:---:|:---:
관리 주체|오라클 커널|데이터베이스 관리자
언두 세그먼트|자동 관리|수동 관리
Snapshot 에러|언두 테이블스페이스 증가 및<br> UNDO_RETENSION 파라미터 조정으로 에러 감소|언두 테이블스페이스 증가 및 언두 세그먼트 크기와 개수 조절 필요

- 자동 언두 관리
  - 오라클 커널에 의해 언두 세그먼트가 관리되고 조절된다. 
  - 데이터베이스 관리자가 수행해야할 부분은 필요시 언두 테이블스페이스를 증가시키는 것
  - 9i 버전부터 가능한 관리 방식, 오라클 12c부터는 기본적으로 이 방식을 사용 
  - UNDO_MENAGEMENT 파라미터를 'AUTO'로 설정하고 UNDO_TABLESPACE 파라미터에 사용하고자 하는 언두 테이블스페이스 이름을 설정
- 수동 언두 관리
  - 데이터베이스 관리자에 의해 언두 세그먼트가 관리되고 조절된다.
  - 데이터베이스 관리자에 의한 지속적인 언두 세그먼트 모니터링 및 관리가 필요하다.
  - 9i 버전 이전에 사용하던 방식, 지금은 잘 사용하지 않는다.
  - UNDO_MANAGEMENT 파라미터를 'MANUAL'로 설정

#### UNDO_RETENSION 파라미터
- 언두 세그먼트가 변경 전 데이터를 저장하고 있는 시간을 지정해주는 파라미터로 초단위로 설정 가능
- 기본 값은 900초이며 이 경우 언두 세그먼트 축소가 발생하더라도 데이터 변경 발생 후 15분 이전 데이터가 저장된 언두 세그먼트의 데이터 블록은 재사용되지 않게 된다.
- 언두 테이블스페이스 공간을 모두 사용하였으나 언두 세그먼트 확장이 필요한 경우 파라미터에 지정된 값은 무시되어 사용하지 않는 언두 세그먼트의 익스텐트는 축소될 수 있다. 이러한 경우에는 파라미터에 지정된 시간을 지키지 못하게된다.
  
---
# 질문
#### 질문 1. 언두 테이블스페이스 공간을 모두 사용해서 세그먼트를 추가로 할당할 수 없을 경우 사용하지 않는 언두 세그먼트의 익스텐트를 축소했다가 다시 추가 한다는 의미인가요?

#### 질문 2. 언두 세그먼트 축소는 책에서 따로 다루지 않아서 인터넷에서 추가 했는데, 이유가 있을까요?
---

## 05 언두 테이블스페이스 관리
<img src=https://t1.daumcdn.net/cfile/tistory/2773B13D54FA0EB011 />

### 1) 언두 테이블스페이스 생성
- 언두 테이블스페이스를 생성하는 2가지 방법
  1. 데이터베이스 생성 시 언두 테이블스페이스 생성
  2. 데이터베이스 생성 후 언두 테이블스페이스 생성

언두 테이블 스페이스 생성 명령어

    # 데이터베이스 생성 시 생성
    SQL> CREATE DATABASE
         ....
         UNDO TABLESPACE undo_tbs DATAFILE '/oradata/test/undo01.dbf' SIZE 1000M;

    # 데이터베이스 생성 후 생성
    SQL> CREATE UNDO TABLESPACE undo_tbs DATAFILE '/oradata/test/undo01.dbf' SIZE 1000M;

### 2) 언두 테이블스페이스 변경
데이터 파일 추가

    SQL> ALTER TABLESPACE undo_tbs ADD DATAFILE '/oradata/test/undo02.dbf' SIZE 1000M;

데이터 파일 이름 변경

    SQL> ALTER TABLESPACE undo_tbs
         RENAME DATAFILE '/oradata/test/undo02.dbf' TO '/oradata/test/undo_tbs02.dbf';

언두 테이블스페이스 오프라인 변경

    SQL> ALTER TABLESPACE undo_tbs OFFLINE;

테이블스페이스 백업

    SQL> ALTER TABLESPACE undo_tbs BEGIN BACKUP;

### 3) 언두 테이블스페이스 제거
#### UNDO_TABLESPACE 파라미터에 지정되어 있는 언두 테이블 스페이스는 제거 불가
    SQL> DROP TABLESPACE undo_tbs;

### 4) 언두 테이블스페이스 교체
    SQL> ALTER SYSTEM SET UNDO_TABLESPACE=undo_tbs_test;

### 5) 언두 세그먼트 확인
관련 뷰|내용
:---:|---
DBA_ROLLBACK_SEGS|현재 데이터베이스에 존재하는 모든 언두 세그먼트에 대한 내용 조회
V$ROLLSTAT|현재 데이터베이스에 존재하는 언두 세그먼트 중 온라인 상태인 언두 세그먼트 조회
V$ROLLNAME|모든 언두 세그먼트의 이름 조회
V$UNDOSTAT|언두 세그먼트에 대한 모니터링 및 튜닝을 위한 정보 조회

    SQL> SELECT SEGMENT_NAME, OWNER, TABLESPACE_NAME, STATUS
           FROM DBA_ROLLBACK_SEGS;
    
    SEGMENTS_NAME  OWNER  TABLESPACE_NAME  STATUS
    ---------------------------------------------
    SYSTEM         SYS    SYSTEM           ONLINE
    _SYSSMU1$      PUBLIC UNDO_TBS         ONLINE
    _SYSSMU2$      PUBLIC UNDO_TBS         ONLINE
    _SYSSMU2$      PUBLIC UNDO_TBS         ONLINE

위의 예제는 DBA_ROLLBACK_SEGS 데이터 딕셔너리 뷰를 조회한 것이며 OWNER 컬럼을 확인해보자.

- SYS: 시스템용 언두 세그먼트
- PUBLIC: 유저용 언두 세그먼트

해당 DBA_ROLLBACK_SEGS 데이터 딕셔너리 뷰는 데이터베이스에 존재하는 모든 언두 세그먼트를 조회할 수 있다.

    SQL> SELECT NAME.NAME, STAT.EXTENTS, STAT.RSSIZE, STATS.XACTS
           FROM V$ROLLSTAT STAT, V$ROLLNAME NAME
          WHERE STAT.USN = NAME.USN;

    NAME       EXTENTS  RSSIZE  XACT
    --------------------------------
    SYSTEM     7        444000     1
    _SYSSMU1$  10       5550000    2
    _SYSSMU2$  20       33330000   3
    _SYSSMU2$  30       22220000   0


V\$ROLLSTAT 동적 성능 뷰와 V$ROLLNAME 동적 성능 뷰를 조인하여 조회한 결과
컬럼 이름|내용
:---:|---
NAME|언두 세그먼트 이름
EXTENTS|해당 언두 세그먼트에 할당된 익스텐트 개수
RSSIZE|언두 세그먼트 크기
XACTS|현재 해당 언두 세그먼트를 사용 중인 트랜잭션 개수

    SQL> SELECT SES.USERNAME, TRAN.XIDUSN, TRAN.USED_UBLK
           FROM V$SESSION SES, V$TRANACTION TRAN
          WHERE SES.SADDR = TRAN.SES_ADDR;

    USERNAME XIDUSN USED_UBLK
    -------------------------
    SCOTT    2      1

컬럼 이름|내용
:---:|---
USERNAME|언두 세그먼트 사용자 이름
XIDUSN|언두 세그먼트 번호
USED_UBLK|사용 중이 언두 세그먼트 블록 개수