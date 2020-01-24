from werkzeug.exceptions import BadRequest
from googleapiclient import discovery
from googleapiclient import errors

'''
Request를 받아서 정상이면 GCP AI Platform에 배포하는 함수.
배포하고, 기존 모델이랑 비교해서 성능이 더 좋으면 바꿔치기
일단은 배포하는 기능부터 구현.
'''

def auto_deploy(request):
    parameters = [
        "model_name",
        "version",
        "gs_location",
    ]

    if not request.get_json():
        raise BadRequest('invalid request body: body should be json')

    json_request = request.get_json()
    for parameter in parameters:
        if not json_request.get(parameter) is None:
            continue
        raise BadRequest('invalid request parameterL: %s' % parameter)

    service = discovery.build('ml', 'v1')
    # 사용하고 있는 프로젝트 id
    project_id = 'projects/{}'.format('disco-abacus-265000')

    ''' 
    AI Platform에 먼저 빈 모델을 만들어야한다.
    disco-abacus-265000 프로젝트의 models에 해당 모델의 이름으로 모델을 생성함.
    여기에서 models는 AI Platform 콘솔의 맨 마지막 탭인 모델을 지칭함.
    '''
    name = 'projects/disco-abacus-265000/models/{}'.format(json_request['model_name'])
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
            'name': json_request['model_name'],
            'regions': ['asia-northeast1'],
            'onlinePredictionLogging': True,
            'onlinePredictionConsoleLogging': True
        }
        response = service.projects().models().create(
            parent='projects/disco-abacus-265000',
            body=body
        ).execute()

    '''
    모델을 생성한 이후에는 해당 모델 안에 버전으로 관리되는 모델을 넣을 수 있게 된다.
    이하 모델 정보와 함께 AI Platform의 'Mnist_Keras'라는 모델에 'V1_Mnist' 버전이 생성된다.
    '''
    models = 'projects/disco-abacus-265000/models/{}'.format(json_request['model_name'])
    request_dict = {'name': json_request['version'],
                    'deploymentUri': json_request['gs_location'],
                    'runtimeVersion': '1.14',
                    'framework': 'tensorflow',
                    'pythonVersion': '3.5'}
    response = service.projects().models().versions().create(parent=models,
                                                             body=request_dict).execute()
    if 'error' in response:
        res = {'code':400, 'message':'Error', 'data':response['error']}
    # 예외 처리
    try:
        response = request.execute()
        print(response)
    except errors.HttpError as err:
        # Something went wrong, print out some information.
        print('모델 생성 도중 오류가 발생하였습니다.')
        print(err._get_reason())

    res = {'code':200, 'message':'Sucess', 'data':None}

    return res