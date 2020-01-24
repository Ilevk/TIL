from googleapiclient import discovery
import os

key_file = '../disco-abacus-265000-41c9458ac705.json'

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_file

# AI Platform 에서 보여지는 모델의 이름
model_name= "Mnist_Keras"
# 해당 모델의 버전
version= "V1_Mnist"
# 해당 모델의 가중치 파일이 저장되어있는 Google Storage 주소
gs_location= "gs://mnist_ml_serving_test/simple_keras_mnist_model"

service = discovery.build('ml', 'v1')
# 사용하고 있는 프로젝트 id
project_id = 'projects/{}'.format('disco-abacus-265000')

''' 
AI Platform에 먼저 빈 모델을 만들어야한다.
disco-abacus-265000 프로젝트의 models에 해당 모델의 이름으로 모델을 생성함.
여기에서 models는 AI Platform 콘솔의 맨 마지막 탭인 모델을 지칭함.
'''
name = 'projects/disco-abacus-265000/models/{}'.format(model_name)
try:
    '''
    해당 코드는 위의 model_name을 가진 모델이 있는지 확인하는 코드.
    해당 모델이 존재하지 않는다면 except 절에서 새로 모델을 생성한다.
    '''
    response = service.projects().models().get(
        name=name
    ).execute()
except:
    '''
    생성할 모델의 내용
    이름, 해당 모델이 생성될 지역 등을 포함하여 요청을 날린다.
    '''
    body = {
        'name': model_name,
        'regions': ['asia-northeast1'],
        'onlinePredictionLogging': True,
        'onlinePredictionConsoleLogging':True
    }
    response = service.projects().models().create(
        parent='projects/disco-abacus-265000',
        body=body
    ).execute()

'''
모델을 생성한 이후에는 해당 모델 안에 버전으로 관리되는 모델을 넣을 수 있게 된다.
이하 모델 정보와 함께 AI Platform의 'Mnist_Keras'라는 모델에 'V1_Mnist' 버전이 생성된다.
'''
models = 'projects/disco-abacus-265000/models/{}'.format(model_name)
request_dict = {'name': version,
                'deploymentUri': gs_location,
                'runtimeVersion': '1.14',
                'framework': 'tensorflow',
                'pythonVersion': '3.5'}
response = service.projects().models().versions().create(parent=models,
                                              body=request_dict).execute()