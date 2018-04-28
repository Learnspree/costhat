from costhat import *

''' Functions used in test script '''
def truncate(f):
    return float('%.3f'%(f))

# Overall costs listed based on "per million requests"
def test_aws_spf_coldstart():

    test_netcore = LambdaEndpoint('test_netcore')
    test_netcore_service = LambdaService('test_netcore_service', [test_netcore])
    test_netcore_costs = {'capi' : 0, 'cio' : 0, 'ccmp' : 5.62, "coth" : 0}
    test_netcore.configure_endpoint(test_netcore_costs)

    aws_logger = LambdaEndpoint('aws_logger')
    aws_logger_service = LambdaService('aws_logger_service', [aws_logger])
    aws_logger_costs = {'capi' : 0, 'cio' : 0, 'ccmp' : 22.7, "coth" : 0}
    aws_logger.configure_endpoint(aws_logger_costs)

    # API Calls $3.50 per million requests + data transfer out ($0.09/GB for first 10TB)
    # Traffic is within 1GB _ so $0.09 total for transfer and $3.50 for the API calls
    common_metrics = LambdaEndpoint('common_metrics')
    common_metrics_service = LambdaService('common_metrics_service', [common_metrics])
    common_metrics_costs = {'capi' : 3.59, 'cio' : 0.47, 'ccmp' : 20.83, "coth" : 0}
    common_metrics.configure_endpoint(common_metrics_costs)
    
   # IO costs based on DynamoDB cost @ $0.47 per month for 1 WCU _ enough for 1 write per second or 2.5m per month
    # This is the minimum and is enough to cover the 1 million requests being priced
    # https://aws.amazon.com/dynamodb/pricing/    
    common_cost_metrics = LambdaEndpoint('common_cost_metrics')
    common_cost_metrics_service = LambdaService('common_cost_metrics_service', [common_cost_metrics])
    common_cost_metrics_costs = {'capi' : 0, 'cio' : 0.47, 'ccmp' : 2.49, "coth" : 0}
    common_cost_metrics.configure_endpoint(common_cost_metrics_costs)

    test_netcore_cg = [(aws_logger_service, aws_logger, 1)]
    test_netcore.set_callgraph(test_netcore_cg)

    aws_logger_cg = [(common_metrics_service, common_metrics, 1)]
    aws_logger.set_callgraph(aws_logger_cg)

    common_metrics_cg = [(common_cost_metrics_service, common_cost_metrics, 1)]
    common_metrics.set_callgraph(common_metrics_cg)

    model = CosthatModel([test_netcore_service, aws_logger_service, common_metrics_service, common_cost_metrics_service])

    # test cold start 1000000 (1 million) calls
    coldstart1m = {test_netcore_service : { test_netcore : 1 }}
    costs = truncate(model.calculate_costs(coldstart1m))
    expected = 56.17
    print("Single Test Function: Hoping for %f, and received %f" % (expected, costs))
    assert costs == expected

# Overall costs listed based on "per million requests"
def test_aws_spf_fictional_30k_TPS():

    # Define the controller functions
    main_controller = LambdaEndpoint('main_controller')
    main_controller_service = LambdaService('main_controller_service', [main_controller])
    main_controller_costs = {'capi' : 0, 'cio' : 0, 'ccmp' : 0.41, "coth" : 0}
    main_controller.configure_endpoint(main_controller_costs)

    aws_controller = LambdaEndpoint('aws_controller')
    aws_controller_service = LambdaService('aws_controller_service', [aws_controller])
    aws_controller_costs = {'capi' : 0, 'cio' : 0, 'ccmp' : 0.41, "coth" : 0}
    aws_controller.configure_endpoint(aws_controller_costs)

    az_controller = LambdaEndpoint('az_controller')
    az_controller_service = LambdaService('az_controller_service', [az_controller])
    az_controller_costs = {'capi' : 0, 'cio' : 0, 'ccmp' : 0.40, "coth" : 0}
    az_controller.configure_endpoint(az_controller_costs)


    # Define the 5 AWS Test Functions
    test_netcore = LambdaEndpoint('test_netcore')
    test_netcore_service = LambdaService('test_netcore_service', [test_netcore])
    test_netcore_costs = {'capi' : 0, 'cio' : 0, 'ccmp' : 5.62, "coth" : 0}
    test_netcore.configure_endpoint(test_netcore_costs)

    test_java = LambdaEndpoint('test_java')
    test_java_service = LambdaService('test_java_service', [test_java])
    test_java_costs = {'capi' : 0, 'cio' : 0, 'ccmp' : 1.03, "coth" : 0}
    test_java.configure_endpoint(test_java_costs)

    test_go = LambdaEndpoint('test_go')
    test_go_service = LambdaService('test_go_service', [test_go])
    test_go_costs = {'capi' : 0, 'cio' : 0, 'ccmp' : 0.41, "coth" : 0}
    test_go.configure_endpoint(test_go_costs)

    test_py = LambdaEndpoint('test_py')
    test_py_service = LambdaService('test_py_service', [test_py])
    test_py_costs = {'capi' : 0, 'cio' : 0, 'ccmp' : 0.41, "coth" : 0}
    test_py.configure_endpoint(test_py_costs)

    test_js = LambdaEndpoint('test_js')
    test_js_service = LambdaService('test_js_service', [test_js])
    test_js_costs = {'capi' : 0, 'cio' : 0, 'ccmp' : 0.41, "coth" : 0}
    test_js.configure_endpoint(test_js_costs)

    # Define the 2 Azure Test Functions    
    test_az_cs = LambdaEndpoint('test_az_cs')
    test_az_cs_service = LambdaService('test_az_cs_service', [test_az_cs])
    test_az_cs_costs = {'capi' : 0, 'cio' : 0, 'ccmp' : 0.40, "coth" : 0}
    test_az_cs.configure_endpoint(test_az_cs_costs)

    test_az_js = LambdaEndpoint('test_az_js')
    test_az_js_service = LambdaService('test_az_js_service', [test_az_js])
    test_az_js_costs = {'capi' : 0, 'cio' : 0, 'ccmp' : 0.80, "coth" : 0}
    test_az_js.configure_endpoint(test_az_js_costs)

    # Define the Common Functions for SPF
    aws_logger = LambdaEndpoint('aws_logger')
    aws_logger_service = LambdaService('aws_logger_service', [aws_logger])
    aws_logger_costs = {'capi' : 0, 'cio' : 0, 'ccmp' : 22.7, "coth" : 0}
    aws_logger.configure_endpoint(aws_logger_costs)

    azure_logger = LambdaEndpoint('azure_logger')
    azure_logger_service = LambdaService('azure_logger_service', [azure_logger])
    azure_logger_costs = {'capi' : 0, 'cio' : 0, 'ccmp' : 22.7, "coth" : 0}
    azure_logger.configure_endpoint(azure_logger_costs)

    # API Calls $3.50 per million requests + data transfer out ($0.09/GB for first 10TB)
    # Traffic is within 1GB _ so $0.09 total for transfer and $3.50 for the API calls
    common_metrics = LambdaEndpoint('common_metrics')
    common_metrics_service = LambdaService('common_metrics_service', [common_metrics])
    common_metrics_costs = {'capi' : 3.59, 'cio' : 0.47, 'ccmp' : 20.83, "coth" : 0}
    common_metrics.configure_endpoint(common_metrics_costs)
    
   # IO costs based on DynamoDB cost @ $0.47 per month for 1 WCU _ enough for 1 write per second or 2.5m per month
    # This is the minimum and is enough to cover the 1 million requests being priced
    # https://aws.amazon.com/dynamodb/pricing/    
    common_cost_metrics = LambdaEndpoint('common_cost_metrics')
    common_cost_metrics_service = LambdaService('common_cost_metrics_service', [common_cost_metrics])
    common_cost_metrics_costs = {'capi' : 0, 'cio' : 0.47, 'ccmp' : 2.49, "coth" : 0}
    common_cost_metrics.configure_endpoint(common_cost_metrics_costs)

    # Set call graphs for all 7 test functions which are all the same
    test_aws_cg = [(aws_logger_service, aws_logger, 1)]
    test_java.set_callgraph(test_aws_cg)
    test_go.set_callgraph(test_aws_cg)
    test_py.set_callgraph(test_aws_cg)
    test_js.set_callgraph(test_aws_cg)
    test_netcore.set_callgraph(test_aws_cg)

    test_az_cg = [(azure_logger_service, azure_logger, 1)]
    test_az_cs.set_callgraph(test_az_cg)
    test_az_js.set_callgraph(test_az_cg)

    logger_cg = [(common_metrics_service, common_metrics, 1)]
    aws_logger.set_callgraph(logger_cg)
    azure_logger.set_callgraph(logger_cg)

    common_metrics_cg = [(common_cost_metrics_service, common_cost_metrics, 1)]
    common_metrics.set_callgraph(common_metrics_cg)

    main_ctrl_cg = [(aws_controller_service, aws_controller, 1), (az_controller_service, az_controller, 1)]
    main_controller.set_callgraph(main_ctrl_cg)

    aws_ctrl_cg = [(test_java_service, test_java, 1), (test_go_service, test_go, 1), (test_py_service, test_py, 1), (test_js_service, test_js, 1), (test_netcore_service, test_netcore, 1)]
    aws_controller.set_callgraph(aws_ctrl_cg)

    az_ctrl_cg = [(test_az_cs_service, test_az_cs, 1), (test_az_js_service, test_az_js, 1)]
    az_controller.set_callgraph(az_ctrl_cg)    

    model = CosthatModel([main_controller_service, aws_controller_service, az_controller_service, test_netcore_service, test_go_service, test_py_service, test_js_service, test_java_service, aws_logger_service, test_az_cs_service, test_az_js_service, azure_logger_service, common_metrics_service, common_cost_metrics_service])

    # test main test controller function at a rate of 1,000 TPS = 86.4 million calls per day
    test_hightps = {main_controller_service : { main_controller : 86.4 }}
    costs = truncate(model.calculate_costs(test_hightps))
    expected = 31462.56 
    print("Full TPS: Hoping for %f, and received %f" % (expected, costs))
    assert costs == expected
    
    
''' Start main test script '''
#test_aws_spf_coldstart()
test_aws_spf_fictional_30k_TPS()