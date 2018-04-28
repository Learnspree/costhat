from costhat import *

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

    # # test cold start 100 calls
    # coldstart100 = {test_netcore_service : { test_netcore : 100 }}
    # costs = truncate(model.calculate_costs(coldstart100))
    # expected = 5617
    # print("Hoping for %d, and received %d" % (expected, costs))
    # assert costs == expected

    # test cold start 1000000 (1 million) calls
    coldstart1m = {test_netcore_service : { test_netcore : 1000000 }}
    costs = truncate(model.calculate_costs(coldstart1m))
    expected = 56170000
    print("Hoping for %d, and received %d" % (expected, costs))
    assert costs == expected
    

def test_basic_lambda_service():

    sae = LambdaEndpoint('ea')
    sa = LambdaService('a', [sae])
    sae_cf = {'capi' : 1, 'cio' : 0, 'ccmp' : 2, "coth" : 5}
    sae.configure_endpoint(sae_cf)

    sbe = LambdaEndpoint('eb')
    sb = LambdaService('b', [sbe])
    sbe_cf = {'capi' : 0, 'cio' : 0, 'ccmp' : 1, "coth" : 10}
    sbe.configure_endpoint(sbe_cf)

    sce = LambdaEndpoint('ec')
    sc = LambdaService('c', [sce])
    sce_cf = {'capi' : 1, 'cio' : 1, 'ccmp' : 1, "coth" : 0}
    sce.configure_endpoint(sce_cf)

    sae_cg = [(sb, sbe, 1), (sc, sce, 4)]
    sae.set_callgraph(sae_cg)

    sbe_cg = [(sc, sce, 0.1)]
    sbe.set_callgraph(sbe_cg)

    model = CosthatModel([sa, sb, sc])

    # test 1
    inward1 = {sa : { sae : 10 }}
    costs = truncate(model.calculate_costs(inward1))
    expected = 178.000
    print("Hoping for %d, and received %d" % (expected, costs))
    assert costs == expected

    # test 2
    inward2 = {sa : { sae : 5 }, sb : { sbe : 1 }}
    costs = truncate(model.calculate_costs(inward2))
    expected = 97.800
    print("Hoping for %d, and received %d" % (expected, costs))
    assert costs == expected

''' Start main test script! '''

# test_basic_lambda_service()
test_aws_spf_coldstart()
