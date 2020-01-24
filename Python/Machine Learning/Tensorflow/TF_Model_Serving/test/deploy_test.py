import main
from unittest.mock import Mock


def deploy_test():
    data = {
        "model_name": "Mnist_Keras",
        "version": "V2_Mnist",
        "gs_location": "gs://mnist_ml_serving_test/simple_keras_mnist_model"
    }
    req = Mock(get_json=Mock(return_value=data), args=data)

    # Call tested function
    response = main.auto_deploy(req)
    print(response)

    assert response == {'code':200, 'message':'Sucess', 'data':None}

# if __name__ == '__main__':
#     deploy_test()