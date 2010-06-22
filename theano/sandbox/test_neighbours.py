from numpy import *
import theano
from theano import shared, function
import theano.tensor as T
from neighbours import images2neibs, neibs2images

mode = theano.config.mode
if mode=="FAST_COMPILE":
    mode='FAST_RUN'

def neibs_test():
    
    shape = (100,40,18,18)
    images = shared(arange(prod(shape), dtype='float32').reshape(shape))
    neib_shape = T.as_tensor_variable((2,2))#(array((2,2), dtype='float32'))

    f = function([], images2neibs(images, neib_shape), mode=mode)

    #print images.value
    neibs = f()
    #print neibs
    g = function([], neibs2images(neibs, neib_shape, images.shape), mode=mode)
    
    #print g()
    assert allclose(images.value,g())

neibs_test()