from keras import layers
from pyradox.modules import *

class GeneralizedDenseNets(layers.Layer):
    """
    A generalization of Densely Connected Convolutional Networks (Dense Nets)
    Args:
        blocks          (list of int): numbers of layers for each dense block
        growth_rate:          (float): growth rate at convolution layers, default: 32
        reduction:            (float): compression rate at transition layers, default: 0.5
        epsilon:              (float): Small float added to variance to avoid dividing by zero in
                    batch normalisation, default: 1.001e-5
        activation (keras Activation): activation applied after batch normalization, default: relu
        use_bias               (bool): whether the convolution (block) layers use a bias vector, defalut: False

    """
    def __init__(self, blocks, growth_rate=32, reduction=0.5, epsilon=1.001e-5, activation='relu', use_bias=False):
        super().__init__()
        self.blocks = blocks
        self.growth_rate = growth_rate
        self.reduction = reduction
        self.epsilon = epsilon
        self.activation = activation
        self.use_bias = use_bias
        
    def __call__(self, inputs):
        x = inputs
        x = layers.ZeroPadding2D(padding=((3, 3), (3, 3)))(x)
        x = layers.Conv2D(64, 7, strides=2, use_bias=self.use_bias)(x)
        x = layers.BatchNormalization(epsilon=self.epsilon)(x)
        x = layers.Activation(self.activation)(x)
        x = layers.ZeroPadding2D(padding=((1, 1), (1, 1)))(x)
        x = layers.MaxPooling2D(3, strides=2)(x)
        
        for i in range(len(self.blocks)):
            for _ in range(self.blocks[i]):
                x = DenseNetConvolutionBlock(growth_rate=self.growth_rate)(x)
            x = DenseNetTransitionBlock(reduction=self.reduction)(x)
            
        x = layers.BatchNormalization(epsilon=self.epsilon)(x)
        x = layers.Activation(self.activation)(x)
        return x
        
class DenselyConnectedConvolutionalNetwork121(GeneralizedDenseNets):
    """
    A modified implementation of Densely Connected Convolutional Network 121
        growth_rate:          (float): growth rate at convolution layers, default: 32
        reduction:            (float): compression rate at transition layers, default: 0.5
        epsilon:              (float): Small float added to variance to avoid dividing by zero in
                    batch normalisation, default: 1.001e-5
        activation (keras Activation): activation applied after batch normalization, default: relu
        use_bias               (bool): whether the convolution (block) layers use a bias vector, defalut: False    
    """
    def __init__(self, growth_rate=32, reduction=0.5, epsilon=1.001e-5, activation='relu', use_bias=False):
        super().__init__([6, 12, 24, 16],growth_rate, reduction, epsilon, activation, use_bias)
        
class DenselyConnectedConvolutionalNetwork169(GeneralizedDenseNets):
    """
    A modified implementation of Densely Connected Convolutional Network 169
        growth_rate:          (float): growth rate at convolution layers, default: 32
        reduction:            (float): compression rate at transition layers, default: 0.5
        epsilon:              (float): Small float added to variance to avoid dividing by zero in
                    batch normalisation, default: 1.001e-5
        activation (keras Activation): activation applied after batch normalization, default: relu
        use_bias               (bool): whether the convolution (block) layers use a bias vector, defalut: False    
    """
    def __init__(self, growth_rate=32, reduction=0.5, epsilon=1.001e-5, activation='relu', use_bias=False):
        super().__init__([6, 12, 32, 32],growth_rate, reduction, epsilon, activation, use_bias)
class DenselyConnectedConvolutionalNetwork201(GeneralizedDenseNets):
    """
    A modified implementation of Densely Connected Convolutional Network 201
        growth_rate:          (float): growth rate at convolution layers, default: 32
        reduction:            (float): compression rate at transition layers, default: 0.5
        epsilon:              (float): Small float added to variance to avoid dividing by zero in
                    batch normalisation, default: 1.001e-5
        activation (keras Activation): activation applied after batch normalization, default: relu
        use_bias               (bool): whether the convolution (block) layers use a bias vector, defalut: False    
    """
    def __init__(self, growth_rate=32, reduction=0.5, epsilon=1.001e-5, activation='relu', use_bias=False):
        super().__init__([6, 12, 48, 32],growth_rate, reduction, epsilon, activation, use_bias)

class GeneralizedVGG(layers.Layer):
    """
    A generalization of VGG networks

    Args:
        conv_config       (tuple of two int): number of convolution layers and number of filters for a VGG module
        dense_config      (list of int): the number of uniots in each dense layer
        conv_batch_norm   (bool): whether to use Batch Normalization in VGG modules, default: False
        conv_dropout      (float): the dropout rate in VGG modules, default: 0
        conv_activation   (keras Activation): activation function for convolution Layers, default: relu
        dense_batch_norm  (bool): whether to use Batch Normalization in dense layers, default: False
        dense_dropout     (float): the dropout rate in dense layers, default: 0
        dense_activation  (keras Activation): activation function for dense Layers, default: relu
        kwargs              (keyword arguments):  
    """
    
    def __init__(self, conv_config, dense_config, conv_batch_norm=False, conv_dropout=0, conv_activation='relu', dense_batch_norm=False, dense_dropout=0, dense_activation='relu', **kwargs):
        super().__init__()
        self.conv_config = conv_config
        self.dense_config = dense_config
        self.conv_batch_norm = conv_batch_norm
        self.conv_dropout = conv_dropout
        self.conv_activation = conv_activation
        self.dense_batch_norm = dense_batch_norm
        self.dense_dropout = dense_dropout
        self.dense_activation = dense_activation
        self.kwargs = kwargs
        
    def __call__(self, inputs):
        x = inputs
        for num_conv, num_filters in self.conv_config:
            x = VGGModule(num_conv=num_conv, num_filters=num_filters, batch_normalization=self.conv_batch_norm, dropout=self.conv_dropout, activation=self.conv_activation)(x)
        if len(self.dense_config) > 0:
            x = layers.Flatten()(x)
        for num_units in self.dense_config:
            x = DenselyConnected(units=num_units, batch_normalization=self.dense_batch_norm, dropout=self.dense_dropout, activation=self.dense_activation)(x)
        return x
    

class VGG16(GeneralizedVGG):
    """
    A modified implementation of VGG16 network

    Args:
        conv_batch_norm   (bool): whether to use Batch Normalization in VGG modules, default: False
        conv_dropout      (float): the dropout rate in VGG modules, default: 0
        conv_activation   (keras Activation): activation function for convolution Layers, default: relu
        use_dense         (bool): use the densely connected layers, default: True
        dense_batch_norm  (bool): whether to use Batch Normalization in dense layers (if use_dense = True), default: False
        dense_dropout     (float): the dropout rate in dense layers (if use_dense = True), default: 0
        dense_activation  (keras Activation): activation function for dense Layers (if use_dense = True), default: relu
        kwargs            (keyword arguments):  
    """
    
    def __init__(self, conv_batch_norm=False, conv_dropout=0, conv_activation='relu', use_dense=True, dense_batch_norm=False, dense_dropout=0, dense_activation='relu', **kwargs):
        conv_config = [
            (2, 64), 
            (2, 128),
            (3, 256), 
            (3, 512),
            (3, 512),
        ]
        dense_config = [4096, 4096] if use_dense else []
        super().__init__(conv_config, dense_config, conv_batch_norm, conv_dropout, conv_activation, dense_batch_norm, dense_dropout, dense_activation, **kwargs)
        

class VGG19(GeneralizedVGG):
    """
    A modified implementation of VGG19 network

    Args:
        conv_batch_norm   (bool): whether to use Batch Normalization in VGG modules, default: False
        conv_dropout      (float): the dropout rate in VGG modules, default: 0
        conv_activation   (keras Activation): activation function for convolution Layers, default: relu
        use_dense         (bool): use the densely connected layers, default: True
        dense_batch_norm  (bool): whether to use Batch Normalization in dense layers (if use_dense = True), default: False
        dense_dropout     (float): the dropout rate in dense layers (if use_dense = True), default: 0
        dense_activation  (keras Activation): activation function for dense Layers (if use_dense = True), default: relu
        kwargs            (keyword arguments):  
    """
    
    def __init__(self, conv_batch_norm=False, conv_dropout=0, conv_activation='relu', use_dense=True, dense_batch_norm=False, dense_dropout=0, dense_activation='relu', **kwargs):
        conv_config = [
            (2, 64), 
            (2, 128),
            (4, 256), 
            (4, 512),
            (4, 512),
        ]
        dense_config = [4096, 4096] if use_dense else []
        super().__init__(conv_config, dense_config, conv_batch_norm, conv_dropout, conv_activation, dense_batch_norm, dense_dropout, dense_activation, **kwargs)
        
                