from costhat import *

def truncate(f):
    return float('%.3f'%(f))

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

test_basic_lambda_service()
