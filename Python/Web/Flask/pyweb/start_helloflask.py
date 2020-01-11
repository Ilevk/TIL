from helloflask import app
# helloflask 모듈 안에 __init__.py가 있기 때문에
# 해당 모듈은 __init__.py에 의해서 대표된다. 그렇기 때문에 
# 모듈에서 app을 부르면 __init__.py에 있는 app이 불러와진다.


app.run(host='0.0.0.0') # 127.0.0.1 == localhost(나 자신)

# 이제 이 파일을 실행하면 플라스크 프로세스가 뜬다. 
# 특징으로는 Lazy loading인데, 처음부터 모든걸 다 올리는게 아니라 필요한만큼 올리겠다.
# Environment는 product랑 develop 2개가 있는데, 
# develop은 당연히 개발모드(디버그 모드 가능), product는 실제 서비스 모드(디버그 오프 모드)
# 개발하지말라고 경고가 뜬다. 디벨롭 모드로 바꿔야함.
# WSGI가 포트를 리스닝 하고 있다.