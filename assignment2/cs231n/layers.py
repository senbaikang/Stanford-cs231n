from builtins import range
import numpy as np
import math


def affine_forward(x, w, b):
    """
    Computes the forward pass for an affine (fully-connected) layer.

    The input x has shape (N, d_1, ..., d_k) and contains a minibatch of N
    examples, where each example x[i] has shape (d_1, ..., d_k). We will
    reshape each input into a vector of dimension D = d_1 * ... * d_k, and
    then transform it to an output vector of dimension M.

    Inputs:
    - x: A numpy array containing input data, of shape (N, d_1, ..., d_k)
    - w: A numpy array of weights, of shape (D, M)
    - b: A numpy array of biases, of shape (M,)

    Returns a tuple of:
    - out: output, of shape (N, M)
    - cache: (x, w, b)
    """
    out = None
    ###########################################################################
    # TODO: Implement the affine forward pass. Store the result in out. You   #
    # will need to reshape the input into rows.                               #
    ###########################################################################
    out = np.dot(x.reshape(x.shape[0], -1), w) + b
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x, w, b)
    return out, cache


def affine_backward(dout, cache):
    """
    Computes the backward pass for an affine layer.

    Inputs:
    - dout: Upstream derivative, of shape (N, M)
    - cache: Tuple of:
      - x: Input data, of shape (N, d_1, ... d_k)
      - w: Weights, of shape (D, M)
      - b: Biases, of shape (M,)

    Returns a tuple of:
    - dx: Gradient with respect to x, of shape (N, d1, ..., d_k)
    - dw: Gradient with respect to w, of shape (D, M)
    - db: Gradient with respect to b, of shape (M,)
    """
    x, w, b = cache
    dx, dw, db = None, None, None
    ###########################################################################
    # TODO: Implement the affine backward pass.                               #
    ###########################################################################
    x_shape = x.shape
    dx = np.dot(dout, w.T).reshape(x_shape)
    dw = np.dot(x.reshape(x_shape[0], -1).T, dout)
    db = np.sum(dout, axis=0)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dw, db


def relu_forward(x):
    """
    Computes the forward pass for a layer of rectified linear units (ReLUs).

    Input:
    - x: Inputs, of any shape

    Returns a tuple of:
    - out: Output, of the same shape as x
    - cache: x
    """
    out = None
    ###########################################################################
    # TODO: Implement the ReLU forward pass.                                  #
    ###########################################################################
    out = np.maximum(0, x)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = x
    return out, cache


def relu_backward(dout, cache):
    """
    Computes the backward pass for a layer of rectified linear units (ReLUs).

    Input:
    - dout: Upstream derivatives, of any shape
    - cache: Input x, of same shape as dout

    Returns:
    - dx: Gradient with respect to x
    """
    dx, x = None, cache
    ###########################################################################
    # TODO: Implement the ReLU backward pass.                                 #
    ###########################################################################
    dx = dout * (x > 0)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx


def batchnorm_forward(x, gamma, beta, bn_param):
    """
    Forward pass for batch normalization.

    During training the sample mean and (uncorrected) sample variance are
    computed from minibatch statistics and used to normalize the incoming data.
    During training we also keep an exponentially decaying running mean of the
    mean and variance of each feature, and these averages are used to normalize
    data at test-time.

    At each timestep we update the running averages for mean and variance using
    an exponential decay based on the momentum parameter:

    running_mean = momentum * running_mean + (1 - momentum) * sample_mean
    running_var = momentum * running_var + (1 - momentum) * sample_var

    Note that the batch normalization paper suggests a different test-time
    behavior: they compute sample mean and variance for each feature using a
    large number of training images rather than using a running average. For
    this implementation we have chosen to use running averages instead since
    they do not require an additional estimation step; the torch7
    implementation of batch normalization also uses running averages.

    Input:
    - x: Data of shape (N, D)
    - gamma: Scale parameter of shape (D,)
    - beta: Shift paremeter of shape (D,)
    - bn_param: Dictionary with the following keys:
      - mode: 'train' or 'test'; required
      - eps: Constant for numeric stability
      - momentum: Constant for running mean / variance.
      - running_mean: Array of shape (D,) giving running mean of features
      - running_var Array of shape (D,) giving running variance of features

    Returns a tuple of:
    - out: of shape (N, D)
    - cache: A tuple of values needed in the backward pass
    """
    mode = bn_param['mode']
    eps = bn_param.get('eps', 1e-5)
    momentum = bn_param.get('momentum', 0.9)

    N, D = x.shape
    running_mean = bn_param.get('running_mean', np.zeros(D, dtype=x.dtype))
    running_var = bn_param.get('running_var', np.zeros(D, dtype=x.dtype))

    out, cache = None, None
    if mode == 'train':
        #######################################################################
        # TODO: Implement the training-time forward pass for batch norm.      #
        # Use minibatch statistics to compute the mean and variance, use      #
        # these statistics to normalize the incoming data, and scale and      #
        # shift the normalized data using gamma and beta.                     #
        #                                                                     #
        # You should store the output in the variable out. Any intermediates  #
        # that you need for the backward pass should be stored in the cache   #
        # variable.                                                           #
        #                                                                     #
        # You should also use your computed sample mean and variance together #
        # with the momentum variable to update the running mean and running   #
        # variance, storing your result in the running_mean and running_var   #
        # variables.                                                          #
        #                                                                     #
        # Note that though you should be keeping track of the running         #
        # variance, you should normalize the data based on the standard       #
        # deviation (square root of variance) instead!                        # 
        # Referencing the original paper (https://arxiv.org/abs/1502.03167)   #
        # might prove to be helpful.                                          #
        #######################################################################
        x_m = np.mean(x, axis=0)
        x_v = np.var(x, axis=0)
        x_i = (x - x_m) / np.sqrt(x_v + eps)
        out = gamma * x_i + beta

        running_mean = momentum * running_mean + (1 - momentum) * x_m
        running_var = momentum * running_var + (1 - momentum) * x_v

        cache = (x, x_m, x_v, x_i, eps, gamma)
        #######################################################################
        #                           END OF YOUR CODE                          #
        #######################################################################
    elif mode == 'test':
        #######################################################################
        # TODO: Implement the test-time forward pass for batch normalization. #
        # Use the running mean and variance to normalize the incoming data,   #
        # then scale and shift the normalized data using gamma and beta.      #
        # Store the result in the out variable.                               #
        #######################################################################
        x_i = (x - running_mean) / np.sqrt(running_var + eps)
        out = gamma * x_i + beta
        #######################################################################
        #                          END OF YOUR CODE                           #
        #######################################################################
    else:
        raise ValueError('Invalid forward batchnorm mode "%s"' % mode)

    # Store the updated running means back into bn_param
    bn_param['running_mean'] = running_mean
    bn_param['running_var'] = running_var

    return out, cache


def batchnorm_backward(dout, cache):
    """
    Backward pass for batch normalization.

    For this implementation, you should write out a computation graph for
    batch normalization on paper and propagate gradients backward through
    intermediate nodes.

    Inputs:
    - dout: Upstream derivatives, of shape (N, D)
    - cache: Variable of intermediates from batchnorm_forward.

    Returns a tuple of:
    - dx: Gradient with respect to inputs x, of shape (N, D)
    - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
    - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
    """
    dx, dgamma, dbeta = None, None, None
    ###########################################################################
    # TODO: Implement the backward pass for batch normalization. Store the    #
    # results in the dx, dgamma, and dbeta variables.                         #
    # Referencing the original paper (https://arxiv.org/abs/1502.03167)       #
    # might prove to be helpful.                                              #
    ###########################################################################
    x, x_m, x_v, x_i, eps, gamma = cache
    N, _ = dout.shape

    dgamma = np.sum(dout * x_i, axis=0)
    dbeta = np.sum(dout, axis=0)

    dx_i = dout * gamma
    dx_v = np.sum(dx_i * (x - x_m) * (-0.5) * (x_v + eps)**(-1.5), axis=0)
    dx_m = np.sum(dx_i * (-1 / np.sqrt(x_v + eps)), axis=0) + dx_v * np.mean(-2 * (x - x_m), axis=0)
    dx = dx_i / np.sqrt(x_v + eps) + dx_v * 2 * (x - x_m) / N + dx_m / N
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return dx, dgamma, dbeta


def batchnorm_backward_alt(dout, cache):
    """
    Alternative backward pass for batch normalization.

    For this implementation you should work out the derivatives for the batch
    normalizaton backward pass on paper and simplify as much as possible. You
    should be able to derive a simple expression for the backward pass. 
    See the jupyter notebook for more hints.
     
    Note: This implementation should expect to receive the same cache variable
    as batchnorm_backward, but might not use all of the values in the cache.

    Inputs / outputs: Same as batchnorm_backward
    """
    dx, dgamma, dbeta = None, None, None
    ###########################################################################
    # TODO: Implement the backward pass for batch normalization. Store the    #
    # results in the dx, dgamma, and dbeta variables.                         #
    #                                                                         #
    # After computing the gradient with respect to the centered inputs, you   #
    # should be able to compute gradients with respect to the inputs in a     #
    # single statement; our implementation fits on a single 80-character line.#
    ###########################################################################
    x, x_m, x_v, x_i, eps, gamma = cache
    N, _ = dout.shape

    dgamma = np.sum(dout * x_i, axis=0)
    dbeta = np.sum(dout, axis=0)

    dx_i = dout * gamma
    dx_v = - np.sum(dx_i * (x - x_m) * (x_v + eps)**(-1.5), axis=0) / 2
    inter = dx_i / np.sqrt(x_v + eps)
    dx_m = np.sum(-inter, axis=0) + dx_v * -2 * np.mean(x - x_m, axis=0)
    dx = inter + (dx_v * 2 * (x - x_m) + dx_m) / N
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return dx, dgamma, dbeta


def layernorm_forward(x, gamma, beta, ln_param):
    """
    Forward pass for layer normalization.

    During both training and test-time, the incoming data is normalized per data-point,
    before being scaled by gamma and beta parameters identical to that of batch normalization.
    
    Note that in contrast to batch normalization, the behavior during train and test-time for
    layer normalization are identical, and we do not need to keep track of running averages
    of any sort.

    Input:
    - x: Data of shape (N, D)
    - gamma: Scale parameter of shape (D,)
    - beta: Shift paremeter of shape (D,)
    - ln_param: Dictionary with the following keys:
        - eps: Constant for numeric stability

    Returns a tuple of:
    - out: of shape (N, D)
    - cache: A tuple of values needed in the backward pass
    """
    out, cache = None, None
    eps = ln_param.get('eps', 1e-5)
    ###########################################################################
    # TODO: Implement the training-time forward pass for layer norm.          #
    # Normalize the incoming data, and scale and  shift the normalized data   #
    #  using gamma and beta.                                                  #
    # HINT: this can be done by slightly modifying your training-time         #
    # implementation of  batch normalization, and inserting a line or two of  #
    # well-placed code. In particular, can you think of any matrix            #
    # transformations you could perform, that would enable you to copy over   #
    # the batch norm code and leave it almost unchanged?                      #
    ###########################################################################
    x_m = np.mean(x, axis=1, keepdims=True)
    x_v = np.var(x, axis=1, keepdims=True)
    x_i = (x - x_m) / np.sqrt(x_v + eps)
    out = gamma * x_i + beta
    cache = (x, x_m, x_v, x_i, eps, gamma)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return out, cache


def layernorm_backward(dout, cache):
    """
    Backward pass for layer normalization.

    For this implementation, you can heavily rely on the work you've done already
    for batch normalization.

    Inputs:
    - dout: Upstream derivatives, of shape (N, D)
    - cache: Variable of intermediates from layernorm_forward.

    Returns a tuple of:
    - dx: Gradient with respect to inputs x, of shape (N, D)
    - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
    - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
    """
    dx, dgamma, dbeta = None, None, None
    ###########################################################################
    # TODO: Implement the backward pass for layer norm.                       #
    #                                                                         #
    # HINT: this can be done by slightly modifying your training-time         #
    # implementation of batch normalization. The hints to the forward pass    #
    # still apply!                                                            #
    ###########################################################################
    x, x_m, x_v, x_i, eps, gamma = cache
    _, D = dout.shape

    dgamma = np.sum(dout * x_i, axis=0)
    dbeta = np.sum(dout, axis=0)

    dx_i = dout * gamma
    dx_v = - np.sum(dx_i * (x - x_m) * (x_v + eps)**(-1.5), axis=1, keepdims=True) / 2
    inter = dx_i / np.sqrt(x_v + eps)
    dx_m = np.sum(-inter, axis=1, keepdims=True) + dx_v * -2 * np.mean(x - x_m, axis=1, keepdims=True)
    dx = inter + (dx_v * 2 * (x - x_m) + dx_m) / D
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dgamma, dbeta


def dropout_forward(x, dropout_param):
    """
    Performs the forward pass for (inverted) dropout.

    Inputs:
    - x: Input data, of any shape
    - dropout_param: A dictionary with the following keys:
      - p: Dropout parameter. We keep each neuron output with probability p.
      - mode: 'test' or 'train'. If the mode is train, then perform dropout;
        if the mode is test, then just return the input.
      - seed: Seed for the random number generator. Passing seed makes this
        function deterministic, which is needed for gradient checking but not
        in real networks.

    Outputs:
    - out: Array of the same shape as x.
    - cache: tuple (dropout_param, mask). In training mode, mask is the dropout
      mask that was used to multiply the input; in test mode, mask is None.

    NOTE: Please implement **inverted** dropout, not the vanilla version of dropout.
    See http://cs231n.github.io/neural-networks-2/#reg for more details.

    NOTE 2: Keep in mind that p is the probability of **keep** a neuron
    output; this might be contrary to some sources, where it is referred to
    as the probability of dropping a neuron output.
    """
    p, mode = dropout_param['p'], dropout_param['mode']
    if 'seed' in dropout_param:
        np.random.seed(dropout_param['seed'])

    mask = None
    out = None

    if mode == 'train':
        #######################################################################
        # TODO: Implement training phase forward pass for inverted dropout.   #
        # Store the dropout mask in the mask variable.                        #
        #######################################################################
        mask = (np.random.rand(*x.shape) < p) / p
        out = x * mask
        #######################################################################
        #                           END OF YOUR CODE                          #
        #######################################################################
    elif mode == 'test':
        #######################################################################
        # TODO: Implement the test phase forward pass for inverted dropout.   #
        #######################################################################
        out = x
        #######################################################################
        #                            END OF YOUR CODE                         #
        #######################################################################

    cache = (dropout_param, mask)
    out = out.astype(x.dtype, copy=False)

    return out, cache


def dropout_backward(dout, cache):
    """
    Perform the backward pass for (inverted) dropout.

    Inputs:
    - dout: Upstream derivatives, of any shape
    - cache: (dropout_param, mask) from dropout_forward.
    """
    dropout_param, mask = cache
    mode = dropout_param['mode']

    dx = None
    if mode == 'train':
        #######################################################################
        # TODO: Implement training phase backward pass for inverted dropout   #
        #######################################################################
        dx = dout * mask
        #######################################################################
        #                          END OF YOUR CODE                           #
        #######################################################################
    elif mode == 'test':
        dx = dout
    return dx


def conv_forward_naive(x, w, b, conv_param):
    """
    A naive implementation of the forward pass for a convolutional layer.

    The input consists of N data points, each with C channels, height H and
    width W. We convolve each input with F different filters, where each filter
    spans all C channels and has height HH and width WW.

    Input:
    - x: Input data of shape (N, C, H, W)
    - w: Filter weights of shape (F, C, HH, WW)
    - b: Biases, of shape (F,)
    - conv_param: A dictionary with the following keys:
      - 'stride': The number of pixels between adjacent receptive fields in the
        horizontal and vertical directions.
      - 'pad': The number of pixels that will be used to zero-pad the input. 
        

    During padding, 'pad' zeros should be placed symmetrically (i.e equally on both sides)
    along the height and width axes of the input. Be careful not to modfiy the original
    input x directly.

    Returns a tuple of:
    - out: Output data, of shape (N, F, H', W') where H' and W' are given by
      H' = 1 + (H + 2 * pad - HH) / stride
      W' = 1 + (W + 2 * pad - WW) / stride
    - cache: (x, w, b, conv_param)
    """
    out = None
    ###########################################################################
    # TODO: Implement the convolutional forward pass.                         #
    # Hint: you can use the function np.pad for padding.                      #
    ###########################################################################
    s = conv_param['stride']
    zp = conv_param['pad']
    num_train, num_channel, num_height, num_width = x.shape
    num_filter, _, num_height_f, num_width_f = w.shape
    h_p = 1 + (num_height + 2 * zp - num_height_f) / s
    w_p = 1 + (num_width + 2 * zp - num_width_f) / s

    if ((h_p - math.floor(h_p)) > 0.0) | ((w_p - math.floor(w_p)) > 0.0):
      raise ValueError('Output dimension is not of integer!')
    else:
      h_p = int(h_p)
      w_p = int(w_p)
    
    x_p = np.pad(x, ((0, 0), (0, 0), (zp, zp), (zp, zp)), 'constant')
    w_i = w.reshape(num_filter, -1)
    out = np.zeros((1, num_filter, h_p, w_p))

    for i in range(num_train):
      x_i = np.zeros((num_channel * num_height_f * num_width_f, 1))
      for j in range(h_p):
        for k in range(w_p):
          temp = x_p[i, :, j * s:j * s + num_height_f, k * s:k * s + num_width_f].reshape(-1, 1)
          x_i = np.concatenate((x_i, temp), axis=-1)
      
      x_i = x_i[:, 1:]
      out = np.concatenate((out, (np.dot(w_i, x_i) + b.reshape(-1, 1)).reshape(1, num_filter, h_p, w_p)), axis=0)
    
    out = out[1:, :, :, :]
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x, w, b, conv_param)
    return out, cache


def conv_backward_naive(dout, cache):
    """
    A naive implementation of the backward pass for a convolutional layer.

    Inputs:
    - dout: Upstream derivatives.
    - cache: A tuple of (x, w, b, conv_param) as in conv_forward_naive

    Returns a tuple of:
    - dx: Gradient with respect to x
    - dw: Gradient with respect to w
    - db: Gradient with respect to b
    """
    dx, dw, db = None, None, None
    ###########################################################################
    # TODO: Implement the convolutional backward pass.                        #
    ###########################################################################
    x, w, _, conv_param = cache
    s = conv_param['stride']
    zp = conv_param['pad']
    num_train, num_channel, num_height, num_width = x.shape
    num_filter, _, num_height_f, num_width_f = w.shape
    h_p = int(1 + (num_height + 2 * zp - num_height_f) / s)
    w_p = int(1 + (num_width + 2 * zp - num_width_f) / s)

    x_p = np.pad(x, ((0, 0), (0, 0), (zp, zp), (zp, zp)), 'constant')
    w_i = w.reshape(num_filter, -1)

    db = np.sum(np.sum(np.sum(dout, axis=-1), axis=-1), axis=0)

    dx = np.zeros((1, num_channel, num_height, num_width))
    dw = np.zeros((num_filter, num_channel * num_height_f * num_width_f))

    for i in range(num_train):
      x_i = np.zeros((num_channel * num_height_f * num_width_f, 1))
      for j in range(h_p):
        for k in range(w_p):
          temp = x_p[i, :, j * s:j * s + num_height_f, k * s:k * s + num_width_f].reshape(-1, 1)
          x_i = np.concatenate((x_i, temp), axis=-1)
      
      x_i = x_i[:, 1:]
      dout_i = dout[i, :, :, :].reshape(-1, h_p * w_p)

      dx_i = np.dot(w_i.T, dout_i)
      dw_i = np.dot(dout_i, x_i.T)

      dw += dw_i

      dx_temp = np.zeros((num_channel, num_height + 2 * zp, num_width + 2 * zp))
      _, num_local_matrix = dx_i.shape

      for ii in range(num_local_matrix):
        dx_i_temp = dx_i[:, ii].reshape(-1, num_height_f, num_width_f)
        col_idx = ii // h_p
        row_idx = ii % w_p
        dx_i_temp = np.pad(dx_i_temp, ((0, 0), (col_idx * s, num_height + 2 * zp - num_height_f - col_idx * s), (row_idx * s, num_width + 2 * zp - num_width_f - row_idx * s)), 'constant')
        dx_temp += dx_i_temp
      
      if zp == 0:
        dx = np.concatenate((dx, dx_temp.reshape(1, num_channel, num_height, num_width)), axis=0)
      else:
        dx = np.concatenate((dx, dx_temp[:, zp:-zp, zp:-zp].reshape(1, num_channel, num_height, num_width)), axis=0)

    dx = dx[1:, :, :, :]
    dw = dw.reshape(num_filter, -1, num_height_f, num_width_f)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dw, db


def max_pool_forward_naive(x, pool_param):
    """
    A naive implementation of the forward pass for a max-pooling layer.

    Inputs:
    - x: Input data, of shape (N, C, H, W)
    - pool_param: dictionary with the following keys:
      - 'pool_height': The height of each pooling region
      - 'pool_width': The width of each pooling region
      - 'stride': The distance between adjacent pooling regions

    No padding is necessary here. Output size is given by 

    Returns a tuple of:
    - out: Output data, of shape (N, C, H', W') where H' and W' are given by
      H' = 1 + (H - pool_height) / stride
      W' = 1 + (W - pool_width) / stride
    - cache: (x, pool_param)
    """
    out = None
    ###########################################################################
    # TODO: Implement the max-pooling forward pass                            #
    ###########################################################################
    num_height_f = pool_param['pool_height']
    num_width_f = pool_param['pool_width']
    s = pool_param['stride']
    num_train, num_channel, num_height, num_width = x.shape
    h_p = 1 + (num_height - num_height_f) / s
    w_p = 1 + (num_width - num_width_f) / s

    if ((h_p - math.floor(h_p)) > 0.0) | ((w_p - math.floor(w_p)) > 0.0):
      raise ValueError('Output dimension is not of integer!')
    else:
      h_p = int(h_p)
      w_p = int(w_p)

    out = np.zeros((1, num_channel, h_p, w_p))

    for i in range(num_train):
      out_temp = np.zeros((1, h_p, w_p))
      for j in range(num_channel):
        x_ij = np.zeros((num_height_f * num_width_f, 1))
        for k in range(h_p):
          for ii in range(w_p):
            temp = x[i, j, k * s:k * s + num_height_f, ii * s:ii * s + num_width_f].reshape(-1, 1)
            x_ij = np.concatenate((x_ij, temp), axis=-1)

        x_ij = x_ij[:, 1:]
        out_temp = np.concatenate((out_temp, np.amax(x_ij, axis=0).reshape(1, h_p, w_p)), axis=0)
      
      out_temp = out_temp[1:, :, :]

      out = np.concatenate((out, out_temp.reshape(1, num_channel, h_p, w_p)), axis=0)
    
    out = out[1:, :, :, :]
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    cache = (x, pool_param)
    return out, cache


def max_pool_backward_naive(dout, cache):
    """
    A naive implementation of the backward pass for a max-pooling layer.

    Inputs:
    - dout: Upstream derivatives
    - cache: A tuple of (x, pool_param) as in the forward pass.

    Returns:
    - dx: Gradient with respect to x
    """
    dx = None
    ###########################################################################
    # TODO: Implement the max-pooling backward pass                           #
    ###########################################################################
    x, pool_param = cache
    num_height_f = pool_param['pool_height']
    num_width_f = pool_param['pool_width']
    s = pool_param['stride']
    num_train, num_channel, num_height, num_width = x.shape
    h_p = int(1 + (num_height - num_height_f) / s)
    w_p = int(1 + (num_width - num_width_f) / s)

    dx = np.zeros((1, num_channel, num_height, num_width))

    for i in range(num_train):
      dx_temp = np.zeros((1, num_height, num_width))
      for j in range(num_channel):
        x_ij = np.zeros((num_height_f * num_width_f, 1))
        for k in range(h_p):
          for ii in range(w_p):
            temp = x[i, j, k * s:k * s + num_height_f, ii * s:ii * s + num_width_f].reshape(-1, 1)
            x_ij = np.concatenate((x_ij, temp), axis=-1)

        x_ij = x_ij[:, 1:]
        dout_ij_temp = dout[i, j, :, :].reshape(-1, h_p * w_p) * (x_ij == np.amax(x_ij, axis=0))

        dx_ij = np.zeros((num_height, num_width))
        _, num_local_matrix = dout_ij_temp.shape

        for jj in range(num_local_matrix):
          col_idx = jj // h_p
          row_idx = jj % w_p
          dx_ij += np.pad(dout_ij_temp[:, jj].reshape(num_height_f, num_width_f), ((col_idx * s, num_height - num_height_f - col_idx * s), (row_idx * s, num_width - num_width_f - row_idx * s)), 'constant')
        
        dx_temp = np.concatenate((dx_temp, dx_ij.reshape(1, num_height, num_width)), axis=0)
      
      dx_temp = dx_temp[1:, :, :]

      dx = np.concatenate((dx, dx_temp.reshape(1, num_channel, num_height, num_width)), axis=0)

    dx = dx[1:, :, :, :]
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx


def spatial_batchnorm_forward(x, gamma, beta, bn_param):
    """
    Computes the forward pass for spatial batch normalization.

    Inputs:
    - x: Input data of shape (N, C, H, W)
    - gamma: Scale parameter, of shape (C,)
    - beta: Shift parameter, of shape (C,)
    - bn_param: Dictionary with the following keys:
      - mode: 'train' or 'test'; required
      - eps: Constant for numeric stability
      - momentum: Constant for running mean / variance. momentum=0 means that
        old information is discarded completely at every time step, while
        momentum=1 means that new information is never incorporated. The
        default of momentum=0.9 should work well in most situations.
      - running_mean: Array of shape (D,) giving running mean of features
      - running_var Array of shape (D,) giving running variance of features

    Returns a tuple of:
    - out: Output data, of shape (N, C, H, W)
    - cache: Values needed for the backward pass
    """
    out, cache = None, None
    ###########################################################################
    # TODO: Implement the forward pass for spatial batch normalization.       #
    #                                                                         #
    # HINT: You can implement spatial batch normalization by calling the      #
    # vanilla version of batch normalization you implemented above.           #
    # Your implementation should be very short; ours is less than five lines. #
    ###########################################################################
    num_train, num_channel, num_height, num_width = x.shape
    out, cache = batchnorm_forward(np.transpose(x, (0, 2, 3, 1)).reshape(-1, num_channel), gamma, beta, bn_param)
    out = np.transpose(out.reshape(num_train, num_height, num_width, num_channel), (0, 3, 1, 2))
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return out, cache


def spatial_batchnorm_backward(dout, cache):
    """
    Computes the backward pass for spatial batch normalization.

    Inputs:
    - dout: Upstream derivatives, of shape (N, C, H, W)
    - cache: Values from the forward pass

    Returns a tuple of:
    - dx: Gradient with respect to inputs, of shape (N, C, H, W)
    - dgamma: Gradient with respect to scale parameter, of shape (C,)
    - dbeta: Gradient with respect to shift parameter, of shape (C,)
    """
    dx, dgamma, dbeta = None, None, None

    ###########################################################################
    # TODO: Implement the backward pass for spatial batch normalization.      #
    #                                                                         #
    # HINT: You can implement spatial batch normalization by calling the      #
    # vanilla version of batch normalization you implemented above.           #
    # Your implementation should be very short; ours is less than five lines. #
    ###########################################################################
    num_train, num_channel, num_height, num_width = dout.shape
    dx, dgamma, dbeta = batchnorm_backward_alt(np.transpose(dout, (0, 2, 3, 1)).reshape(-1, num_channel), cache)
    dx = np.transpose(dx.reshape(num_train, num_height, num_width, num_channel), (0, 3, 1, 2))
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################

    return dx, dgamma, dbeta


def spatial_groupnorm_forward(x, gamma, beta, G, gn_param):
    """
    Computes the forward pass for spatial group normalization.
    In contrast to layer normalization, group normalization splits each entry 
    in the data into G contiguous pieces, which it then normalizes independently.
    Per feature shifting and scaling are then applied to the data, in a manner identical to that of batch normalization and layer normalization.

    Inputs:
    - x: Input data of shape (N, C, H, W)
    - gamma: Scale parameter, of shape (C,)
    - beta: Shift parameter, of shape (C,)
    - G: Integer mumber of groups to split into, should be a divisor of C
    - gn_param: Dictionary with the following keys:
      - eps: Constant for numeric stability

    Returns a tuple of:
    - out: Output data, of shape (N, C, H, W)
    - cache: Values needed for the backward pass
    """
    out, cache = None, None
    eps = gn_param.get('eps',1e-5)
    ###########################################################################
    # TODO: Implement the forward pass for spatial group normalization.       #
    # This will be extremely similar to the layer norm implementation.        #
    # In particular, think about how you could transform the matrix so that   #
    # the bulk of the code is similar to both train-time batch normalization  #
    # and layer normalization!                                                # 
    ###########################################################################
    num_train, num_channel, num_height, num_width = x.shape

    # There is a conflict on the dimension of gamma and beta between the jupyter 
    # instruction and the above comment.
    gamma = gamma.reshape(1, -1, 1, 1)
    beta = beta.reshape(1, -1, 1, 1)

    if num_channel % G != 0:
      raise ValueError('Cannot evenly divide into groups!')
    
    x = x.reshape(num_train * G, num_channel // G * num_height * num_width)

    x_m = np.mean(x, axis=1, keepdims=True)
    x_v = np.var(x, axis=1, keepdims=True)
    x_i = (x - x_m) / np.sqrt(x_v + eps)
    x_temp = x_i.reshape(num_train, num_channel, num_height, num_width)
    out = gamma * x_temp + beta
    cache = (x, x_m, x_v, x_i, x_temp, eps, gamma, G)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return out, cache


def spatial_groupnorm_backward(dout, cache):
    """
    Computes the backward pass for spatial group normalization.

    Inputs:
    - dout: Upstream derivatives, of shape (N, C, H, W)
    - cache: Values from the forward pass

    Returns a tuple of:
    - dx: Gradient with respect to inputs, of shape (N, C, H, W)
    - dgamma: Gradient with respect to scale parameter, of shape (C,)
    - dbeta: Gradient with respect to shift parameter, of shape (C,)
    """
    dx, dgamma, dbeta = None, None, None

    ###########################################################################
    # TODO: Implement the backward pass for spatial group normalization.      #
    # This will be extremely similar to the layer norm implementation.        #
    ###########################################################################
    x, x_m, x_v, x_i, x_temp, eps, gamma, G = cache
    num_train, num_channel, num_height, num_width = dout.shape

    # Apparently, the dimension of dgamma and dbeta should be (1, C, 1, 1)
    dgamma = np.sum(dout * x_temp, axis=(0, 2, 3), keepdims=True)
    dbeta = np.sum(dout, axis=(0, 2, 3), keepdims=True)

    dx_temp = dout * gamma
    dx_i = dx_temp.reshape(num_train * G, num_channel // G * num_height * num_width)
    _, D = dx_i.shape

    dx_v = - np.sum(dx_i * (x - x_m) * (x_v + eps)**(-1.5), axis=1, keepdims=True) / 2
    inter = dx_i / np.sqrt(x_v + eps)
    dx_m = np.sum(-inter, axis=1, keepdims=True) + dx_v * -2 * np.mean(x - x_m, axis=1, keepdims=True)
    dx = inter + (dx_v * 2 * (x - x_m) + dx_m) / D
    dx = dx.reshape(num_train, num_channel, num_height, num_width)
    ###########################################################################
    #                             END OF YOUR CODE                            #
    ###########################################################################
    return dx, dgamma, dbeta


def svm_loss(x, y):
    """
    Computes the loss and gradient using for multiclass SVM classification.

    Inputs:
    - x: Input data, of shape (N, C) where x[i, j] is the score for the jth
      class for the ith input.
    - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
      0 <= y[i] < C

    Returns a tuple of:
    - loss: Scalar giving the loss
    - dx: Gradient of the loss with respect to x
    """
    N = x.shape[0]
    correct_class_scores = x[np.arange(N), y]
    margins = np.maximum(0, x - correct_class_scores[:, np.newaxis] + 1.0)
    margins[np.arange(N), y] = 0
    loss = np.sum(margins) / N
    num_pos = np.sum(margins > 0, axis=1)
    dx = np.zeros_like(x)
    dx[margins > 0] = 1
    dx[np.arange(N), y] -= num_pos
    dx /= N
    return loss, dx


def softmax_loss(x, y):
    """
    Computes the loss and gradient for softmax classification.

    Inputs:
    - x: Input data, of shape (N, C) where x[i, j] is the score for the jth
      class for the ith input.
    - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
      0 <= y[i] < C

    Returns a tuple of:
    - loss: Scalar giving the loss
    - dx: Gradient of the loss with respect to x
    """
    shifted_logits = x - np.max(x, axis=1, keepdims=True)
    Z = np.sum(np.exp(shifted_logits), axis=1, keepdims=True)
    log_probs = shifted_logits - np.log(Z)
    probs = np.exp(log_probs)
    N = x.shape[0]
    loss = -np.sum(log_probs[np.arange(N), y]) / N
    dx = probs.copy()
    dx[np.arange(N), y] -= 1
    dx /= N
    return loss, dx
