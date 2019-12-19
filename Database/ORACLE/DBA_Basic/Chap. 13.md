# Chap 13. 제약 조건
## 01 제약 조건의 개념
제약 조건이란?

    데이터 정합성을 유지하기 위해 테이블에 발생하는 DML을 검토하는 조건

<img src=https://t1.daumcdn.net/cfile/tistory/2627FC4854FA0F3408 />

제약 조건은 해당 테이블에 DML이 발생할 경우 제약 조건을 확인하여 Insert, Update 또는 Delete를 수행할지 여부를 결정한다.<br>
이처럼 데이터베이스 내의 데이터 변경을 감지하여 전체 데이터베이스내의 정합성을 유지해주는 역할을 수행한다.

목적|내용
:---:|---
데이터 정합성 유지|데이터의 특성 및 속성에 맞게 테이블에 데이터 저장

위의 그림과 같이 EMP 테이블에 EMPNO 컬럼에는 NULL을 허용하지 않는 제약 조건이 구성되어 있다고 가정하자. 이러한 제약 조건이 존재하는 상황에서 다음과 같은 Insert 문이 수행되었다고 하자

    SQL> INSERT INTO 사원 VALUES('', '장우형', '20');

위의 예제에서 EMP 테이블의 EMPNO 컬럼은 NOT NULL 제약 조건이 설정되어 있으므로 위의 SQL은 아래와 같은 에러가 발생하며 Insert 작업이 실패한다.

    SQL> INSERT INTO 사원 VALUES('', '장우형', '20');
    ERROR at line 1:
    ORA-01400: cannot inser NULL into ("사원번호", "사원이름", "부서번호")

## 02 제약 조건의 종류
<img src=https://t1.daumcdn.net/cfile/tistory/2627FB4854FA0F3508 />

제약 조건에는 5가지가 존재한다.

### 1) NOT NULL 제약 조건
<img src=https://t1.daumcdn.net/cfile/tistory/2227FE4854FA0F3508 />

- NOT NULL 제약 조건은 해당 컬럼에 NULL 값을 허용하지 않는 제약 조건이다.

### 2) UNIQUE 제약 조건
<img src=https://t1.daumcdn.net/cfile/tistory/242C6F4854FA0F3506 />

- UNIQUE 제약 조건은 해당 컬럼에 동일한 값의 존재 여부를 확인하는 제약 조건이다. 하지만 NULL 값의 중복에 대해서는 허용한다.

#### 복합 컬럼 UNIQUE 제약조건
- 위의 예제에서 사원 번호와 사원 이름 컬럼이 각각 UNIQUE 제약 조건을 만족할 필요는 없다. 
- 예를 들어 사원번호='0003' 사원이름='이가혜'가 존재한다 했을 때, 새로 Insert되는 데이터가 사원번호='0003' 사원이름='이가혜'라면 에러가 발생하지만 사원번호='0003' 사원이름='이가혜' 라면 Insert는 성공한다.

#### UNIQUE 제약 조건과 인덱스
- UNIQUE 제약 조건은 해당 컬럼에 UNIQUE 인덱스를 생성하여 UNIQUE 제약 조건을 유지한다.
- 해당 UNIQUE 제약 조건 컬럼에 UNIQUE 인덱스가 존재하지 않는다면, UNIQUE를 확인하기 위해 항상 테이블을 처음부터 끝까지 엑세스하여 중복 데이터를 확인하기 때문에 성능 저하가 발생한다. 인덱스를 생성하지 않으면 자동으로 오라클이 생성한다.

--- 
# 질문
### 질문 1. UNIQUE 제약 조건에 UNIQUE 인덱스라는 건, 우리가 일반적으로 PRIMARY KEY에서 이야기하는 인덱스와 동일한 구조의 인덱스 인가요?

### 질문 2. PRIMARY KEY와 동일한 인덱스라면 PRIMARY KEY에서 PRIMARY KEY의 위치를 인덱스를 통해 빠르게 찾는 역할을 UNIQUE 인덱스에서도 동일하게 하는건가요?  
---

### 3) PRIMARY KEY 제약 조건
<img src=https://t1.daumcdn.net/cfile/tistory/264C744854FA0F363C />

- PRIMARY KEY 제약 조건은 해당 컬럼에 대해 UNIQUE 제약 조건과 NOT NULL 제약 조건을 동시에 만족해야 되는 제약 조건이다.
- Insert되는 데이터가 UNIQUE 제약 조건 또는 NOT NULL 제약 조건 중 하나라도 위배되면 Insert는 실패한다. 

#### PRIMARY KEY 제약 조건과 인덱스
- PRIMARY KEY 제약 조건은 UNIQUE 제약 조건을 포함하므로 해당 제약 조건의 컬럼에 UNIQUE 인덱스가 자동으로 생성된다.

### 4) FOREIGN KEY 제약 조건
- FOREIGN KEY 제약 조건은 다른 제약 조건과 달리 2개의 테이블에 의해서 구성되는 제약 조건이다. 
- PRIMARY KEY를 가지고 있는 테이블 1(부모 테이블)과, 테이블 1의 PRIMARY KEY를 참조하여 FOREIGN KEY를 생성한 테이블 2(자식 테이블)가 있다고 가정해보자. <br>테이블 2에 새로운 데이터가 Insert 될 때, 새로운 데이터의 FOREIGN KEY 컬럼 값이 테이블 1의 PRIMARY KEY 컬럼에 존재하지 않는다면 에러가 발생하며 Insert는 실패한다. 

#### FOREIGN KEY 제약 조건과 인덱스
- FOREIGN KEY 제약 조건은 부모 테이블의 참조되는 컬럼에는 PRIMARY KEY/UNIQUE 제약 조건이 존재해야 설멍이 가능하다. 자식 테이블에 데이터가 저장될 때마다 부모 테이블을 조회하며 부모 테이블에 PRIMARY KEY 제약 조건이 설정되므로 UNIQUE 인덱스가 존재해야 부모 테이블 조회에 대한 성능을 보장받을 수 있다.

### 5) CHECK 제약 조건
<img src=https://t1.daumcdn.net/cfile/tistory/2632944854FA0F3603 />

- CHECK 제약 조건은 특정 컬럼에 저장되어야 하는 데이터의 조건을 설정해 놓고 해당 조건을 만족해야만 데이터를 변경하거나 또는 신규로 저장할 수 있게 해주는 제약 조건이다.
- 예를 들어 CHECK 제약 조건이 급여>'200' 이라 설정되어 있다면, Insert 또는 Update 시 급여 컬럼의 값은 200 보다 커야 해당 DML이 가능하다.

## 03 제약 조건의 관리
<img src=https://t1.daumcdn.net/cfile/tistory/276C344D54FA0FC730 />

### 1) NOT NULL 제약 조건
    SQL> CREATE TABLE EMP(
         EMPNO      VARCHAR2(4) NOT NULL, # 로우 레벨 제약 조건 
         SAL        VARCHAR2(10),
         HIREDATE   DATE,
         ENAME      VARCHAR2(8)
         CONSTRAINT ENAME_NN NOT NULL(ENAME)); # 테이블 레벨 제약 조건

NOT NULL 제약 조건은 두 가지 형태로 생성할 수 있다. 첫 번째 NOT NULL 제약 조거은 로우 레벨로 제약 조건 이름을 설정하지 않은 제약 조건이며, 두 번쨰 NOT NULL 제약 조건은 테이블 레벨로 제약 조건의 이름을 설정한 경우이다.

#### 제약 조건 이름
- 위의 예제와 제약 조건에 이름을 정하지 않는 경우에는 SYS_Cn의 형태로 제약 조건의 이름이 생성된다.
- DBA_CONSTARINTS 데이터 딕셔너리 뷰를 조회하면 해당 제약 조건의 이름을 확인할 수 있다.

기존의 테이블 컬럼에 NOT NULL 제약 조건을 추가하는 SQL

    SQL> ALTER TABLE EMP MODIFY (EMPNO VARCHAR2(4) NOT NULL);

#### NOT NULL 제약 조건의 주의 사항
- 중복 데이터와 작업 시간
  - 해당 컬럼에 NOT NULL 제약 조건에 위배되는 데이터가 존재하지 않아야 함
  - 테이블의 크기가 대용량일 경우 과다한 시간 소요

NOT NULL 제약 조건을 제거하는 SQL

    SQL> ALTER TABLE EMP DROP CONSTRAING ENAME_nn;

제약 조건을 활성화시키거나, 비활성화시키는 SQL

    SQL> ALTER TABLE EMP DISABLE CONSTRAINT ENAME_nn; # 제약 조건 비활성화
    SQL> ALTER TABLE EMP ENABLE CONSTRAINT ENAME_nn;  # 제약 조건 활성화

### 2) UNIQUE 제약 조건
UNIQUE 제약 조건은 테이블 레벨로만 생성이 가능하다, 제약 조건의 이름을 지정해야 한다.

    SQL> CREATE TABLE EMP(
         EMPNO      VARCHAR2(4),
         SAL        VARCHAR2(10),
         HIREDATE   DATE,
         ENAME      VARCHAR2(8)
         CONSTRAINT EMP_EMPNO_UK UNIQUE(EMPNO));

해당 테이블에 UNIQUE 제약 조건을 추가하는 SQL

    SQL> ALTER TABLE EMP ADD CONSTRAINT EMPNO_UK UNIQUE(EMPNO)

#### UNIQUE 제약 조건 주의 사항
- 중복 데이터와 작업 시간
  - 해당 컬럼에 UNIQUE 제약 조건에 위배되는 데이터가 없어야 함
  - 테이블의 크기가 대용량일 경우 과다한 시간 소요

### 3) PRIMARY KEY 제약 조건
PRIMARY KEY 제약 조건이 정의된 컬럼의 데이터는 UNIQUE 조건과 NOT NULL 조건을 만족해야한다.

    SQL> CREATE TABLE EMP(
        EMPNO       VARCHAR2(4),
        SAL         VARCHAR2(10),
        HIREDATE    DATE,
        ENAME       VARCHAR2(8)
        CONSTRAINT EMP_EMPNO_PK PRIMARY KEY(EMPNO))

해당 테이블에 PRIMARY KEY 제약 조건을 추가하는 SQL

    SQL> ALTER TABLE EMP ADD PRIMARY KEY (EMPNO);

### 4) FOREIGN KEY 제약 조건
FOREIGN KEY 에는 두 가지 요소가 존재한다. 부모 테이블과 자식 테이블이 있다.

    SQL> CREATE TABLE EMP(
        EMPNO       VARCHAR2(4),
        SAL         VARCHAT2(10),
        HIREDATE    DATE,
        ENAME       VARCHAR2(8)
        CONSTRAINT 사원_부서번호_FK FOREIGN KEY(사원번호) REFERENCES 부서(부서번호));

FOREIGN KEY 제약 조건에는 부모 테이블 참조 컬럼의 값만 저장되게 된다.

### 5) CHECK 제약 조건
생성된 CHECK 제약 조건에 의해 해당 컬럼에 저장되는 값이 제약 조건을 만족하지 못하면 값을 입력할 수 없다.

    SQL> CREATE TABLE EMP(
        EMPNO       VARCHAR2(4),
        SAL         VARCHAR2(10),
        HIREDATE    DATE,
        ENAME       VARCHAR2(8)
        CONSTRAINT EMP_SAL_CK CHECK (SAL > 0));

해당 테이블에 CHECK 제약 조건을 추가하는 SQL

    SQL> ALTER TABLE EMP ADD CONSTRAINT EMP_SAL_CK CHECK (SAL > 0);

### 6) 제약 조건 확인
제약 조건의 정보를 확인하는 SQL

    SQL> SELECT CONTRAINT_NAME, CONSTRAINT_TYPE, SEARCH_CONDITON
           FROM DBA_CONSTRAINTS
          WHERE TABLE_NAME = 'EMP';
    
    CONSTRAINT_NAME CONTRAINT_TYPE SEARCH_CONDITION
    -----------------------------------------------
    SYS_C0010738    C              EMPNO IS NOT NULL
    SYS_C0010738    C              DEPTNO IS NOT NULL
    SYS_C0010741    P

CONSTRAINT_TYPE 컬럼의 값 종류
CONSTRAINT_TYPE 컬럼 값|내용
:---:|---
C|CHECK 제약 조건
P|PRIMARY KEY 제약 조건
U|UNIQUE 제약 조건

제약 조건에 사용된 컬럼을 확인하는 SQL

    SQL> SELECT CONSTRAINT_NAME, COLUMN_NAME
           FROM DBA_CONS_COLUMNS
          WHERE TABLE_NAME = 'EMP';

    CONSTRAINT_NAME COLUMN_NAME
    ---------------------------
    SYS_C0010738    EMP_NO
    SYS_C0010738    DEPTNO
    SYS_C0010741    EMNO

#### 제약 조건과 컬럼 삭제
제약 조건이 설정되어 있는 컬럼을 제거한느 순간 오류가 발생한다. 이를 해결하기 위해 사용되는 옵션이 CASCADE 옵션이다.

    SQL> ALTER TABLE EMP DROP COLUMN EMPNO CASCADE CONTRAINTS;

## 04 제약 조건과 실무
<img src=https://t1.daumcdn.net/cfile/tistory/226D9E4D54FA0FC72E />

실제 데이터베이스를 운영하다 보면 몇 가지 제약 조건은 많이 사용되지 않게 된다. <br>
특히 FOREIGN KEY 제약 조건은 더욱 사용하지 않게 된다. 잘 사용하지 않는 제약 조건은 아래와 같다.
- FOREIGN KEY 제약 조건
- CHECK 제약 조건

### 1) FOREIGN KEY 제약 조건
FOREIGN KEY 제약 조건의 단점
- FOREIGN KEY 제약 조건의 단점
  - 자식 테이블의 제약 조건 컬럼에 인덱스 필요
    - 공간 낭비 및 성능 저하 발생
  - 관리의 어려움
      - 자식 테이블에 값이 입력 될 때 마다 매번 부토 테이블을 조회하여 값의 존재 유무를 체크해야하므로 성능 저하가 발생할 수 있다. 
      - 또한, 데이터 입력시 항상 부모 테이블 -> 자식 테이블 순서로 생성되야 하므로 여러 대용량 테이블의 배치 작업 시에 테이블 입력 순서를 조절해야하는 번거로움이 있다.

### 2) CHECK 제약 조건
- NOT NULL 조건도 CHECK 제약 조건이다. NOT NULL 제약 조건을 제외하고 나머지 CHECK 제약 조건은 거의 사용하지 않게 되며 대부분 어플리케이션에서 데이터를 제어한다. 
- 이러한 방법이 좀 더 관리하기 쉽고 유연성이 강하기 때문에 다양한 경우를 구현할 수 있다.