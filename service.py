import grpc
from trustlevel_pb2_grpc import TrustLevelBiasServiceStub
from trustlevel_pb2 import BiasRequest

def get_bias_score(text):
    with grpc.insecure_channel('your-grpc-endpoint') as channel:
        stub = TrustLevelBiasServiceStub(channel)
        request = BiasRequest(text=text)
        response = stub.AnalyzeBias(request)
        return response.bias_score