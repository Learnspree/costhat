from costhat import *

def truncate(f):
    return float('%.3f'%(f))

def test_aws_spf_coldstart():

    test-netcore = LambdaEndpoint('test-netcore')
    test-netcore-service = LambdaService('test-netcore-service', [test-netcore])
    test-netcore-costs = {'capi' : 0, 'cio' : 0, 'ccmp' : 5.62, "coth" : 0}
    test-netcore.configure_endpoint(test-netcore-costs)

    aws-logger = LambdaEndpoint('aws-logger')
    aws-logger-service = LambdaService('aws-logger-service', [aws-logger])
    aws-logger-costs = {'capi' : 0, 'cio' : 0, 'ccmp' : 22.7, "coth" : 0}
    aws-logger.configure_endpoint(aws-logger-costs)

    common-metrics = LambdaEndpoint('common-metrics')
    common-metrics-service = LambdaService('common-metrics-service', [common-metrics])
    common-metrics-costs = {'capi' : XXX, 'cio' : XXX, 'ccmp' : 20.83, "coth" : 0}
    common-metrics.configure_endpoint(common-metrics-costs)
    
    common-cost-metrics = LambdaEndpoint('common-cost-metrics')
    common-cost-metrics-service = LambdaService('common-cost-metrics-service', [common-cost-metrics])
    common-cost-metrics-costs = {'capi' : 0, 'cio' : XXX, 'ccmp' : 2.49, "coth" : 0}
    common-cost-metrics.configure_endpoint(common-cost-metrics-costs)

    test-netcore_cg = [(aws-logger-service, aws-logger, 1)]
    test-netcore.set_callgraph(test-netcore_cg)

    aws-logger_cg = [(common-metrics-service, common-metrics, 1)]
    aws-logger.set_callgraph(aws-logger_cg)

    common-metrics_cg = [(common-cost-metrics-service, common-cost-metrics, 1)]
    common-metrics.set_callgraph(common-metrics_cg)

    model = CosthatModel([test-netcore-service, aws-logger-service, common-metrics-service, common-cost-metrics-service])

    # test cold start 100 calls
    coldstart100 = {test-netcore : { test-netcore-service : 100 }}
    costs = truncate(model.calculate_costs(coldstart100))
    expected = XXX
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
