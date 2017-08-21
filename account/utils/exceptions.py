from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import status, exceptions
from rest_framework.validators import (
    ValidationError
)

# 自定义异常处理

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.

    response = exception_handler(exc, context)
    if isinstance(exc, exceptions.APIException):
        if response is not None and 'detail' in response.data:
            response.data['ret'] = 1
            if  isinstance(response.data['detail'],(list,tuple)):
                response.data['msg'] = response.data['detail'][0]
            else:
                response.data['msg'] = response.data['detail']
            del  response.data['detail']

        return response

    elif isinstance(exc, ValidationError):
        if response is not None and 'detail' in response.data:
            response.data['ret'] = 1
            if isinstance(response.data['detail'],(list,tuple)):
                response.data['msg'] = response.data['detail'][0]
            else:
                response.data['msg'] = response.data['detail']
            del  response.data['detail']
        return response

    # # Now add the HTTP status code to the response.
    # if response is not None:
    #     response.data['ret'] = 1
    #     response.data['msg'] = response.data['detail']
    #     del response.data['detail']

    return None


from django.utils.translation import ugettext as _


class ServiceException(Exception):

    def __init__(self, err_code=None, status=None, error_msg=None):
        if err_code == None:
            self.err_code = 1
        else:
            self.err_code = err_code
        if status == None:
            self.status = status.HTTP_400_BAD_REQUEST
        else:
            self.status = status
        if error_msg == None:
            self.error_msg = _('服务端异常')
        else:
            self.error_msg = error_msg

    def response(self, headers=None):
        data = {
            'ret': self.err_code,
            'msg': self.error_msg,
        }

        return Response(data, self.status, headers=headers)

    # def render_500(request):
    #     if request.is_ajax():
    #         err = {
    #             'error_code': errors.SYSTEM_ERROR,
    #             'error': 'Internal Server Error',
    #             'message': 'Internal Server Error',
    #         }
    #         return JsonResponse(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #     return redirect('/error/?c=500')
