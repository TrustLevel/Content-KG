from snet.sdk import SnetSDK
import config
import trustlevel_pb2
import trustlevel_pb2_grpc

def invoke_service():
   snet_config = {"private_key": config.PRIVATE_KEY, "eth_rpc_endpoint": config.ETH_RPC_ENDPOINT}
   sdk = SnetSDK(config=snet_config)
   service_client = sdk.create_service_client(
      org_id=config.ORG_ID,
      service_id=config.SERVICE_ID,
      service_stub= trustlevel_pb2_grpc.service_stub # replace service_stub
   )
   request = trustlevel_pb2.input_method(arguments) # replace input_method and arguments
   response = service_client.service.service_method(request) # replace service_method
   print(f"service invoked successfully :: response :: {response}")


invoke_service() # call invoke service method