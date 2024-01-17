from http import HTTPStatus

from flask_restx import Namespace, fields, Resource

from api.llm.service import query_to_llm

llm_api = Namespace('llm', description='메시지 API')

query_message_request = llm_api.model('query_message_request', {
    'message': fields.String(required=True, title='질문'),
})

query_message_response = llm_api.model('query_message_response', {
    'result': fields.String(required=True, title='답변'),
})


@llm_api.route("/query")
class QueryCls(Resource):
    @llm_api.expect(query_message_request)
    @llm_api.marshal_with(query_message_response, envelope='data')
    def post(self):
        return {'result': query_to_llm(llm_api.payload['message'])}


@llm_api.route('/health-check', strict_slashes=False)
class HealthCheck(Resource):
    @llm_api.doc(security=None, description='헬스 체크 API')
    @llm_api.response(code=HTTPStatus.OK.value, description='서버가 정상적으로 구동 되고 있음')
    def get(self) -> HTTPStatus:
        return HTTPStatus.OK