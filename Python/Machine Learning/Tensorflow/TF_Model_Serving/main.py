from werkzeug.exceptions import BadRequest
def auto_deploy(request):
    parameters = [
        'model_name',
        'version',
        'input_size',
        'model_type',
        'input_function',
        'epochs',
        'train_mse',
        'eval_mse',
        'gs_location',
        'framework',
        'normalization',
        'predict_size',
    ]

    if not request.get_json():
        raise BadRequest('invalid request body: body should be json')

    json_request = request.get_json()
    for parameter in parameters:
        if not json_request.get(parameter) is None:
            continue
        raise BadRequest('invalid request parameterL: %s' % parameter)