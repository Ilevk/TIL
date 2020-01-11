from flask import Flask, g


app = Flask(__name__) # 실행되면 main이 된다. , 여기 아래에다가 하나하나 설정을 추가할 예정이다.
app.debug = True # use only debug


@app.before_request # 리퀘스트를 처리하기 전에 이걸 실행해 줘.
def before_request():
    print('Before_request!!!')
    # g는 글로벌이라는 의미,
    # Application Context는 모든 유저들이 공유하는 영역, 
    # Session Context는 나만의 영역 그래서 내정보는 암호화해서 Session Context에 담아야한다.
    g.str = '한글' # g는 Application Context에 있다. , g도 import 해야한다.
    # g에는 2개의 서버가 있을 때, 현재 로드를 어떤 서버로 보낼지에 대한 주소 값을 담을 수도 있다.(모든 유저를 제어하는 용도)

@app.route('/gg')
def helloworld():
    return 'Hello World!' + getattr(g, 'str', '111') # '111'은 디폴트 값

# URI를 정의하는걸 Route 라고한다. 리퀘스트가 왔을 떄 어떤걸 시켜야할지 판단한다.
@app.route("/")   # 아무것도 안준걸 / 라고 부른다.
def helloworld(): # 해당 문자열을 띄울꺼다.
    return 'Hello Flask World!'

# 이제 띄울 곳을 만들어보자.
# ../start_helloflask.py
from helloflask import app