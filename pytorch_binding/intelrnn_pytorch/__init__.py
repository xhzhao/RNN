import torch
import intelrnn_pytorch as intel_rnn
from torch.autograd import Function
from torch.nn import Module
from torch.utils.ffi import _wrap_function
from ._intel_rnn import lib as _lib, ffi as _ffi

__all__ = []

def _import_symbols(locals):
    for symbol in dir(_lib):
        fn = getattr(_lib, symbol)
        locals[symbol] = _wrap_function(fn, _ffi)
        __all__.append(symbol)


_import_symbols(locals())

class func_LSTMCell(Function):
    def forward(self, input, hx):
        print("python func_LSTMCell forward")
        return input
 
    def backward(self, input):
        print("python func_LSTMCell backward")
        return input

class func_LSTM(Function):
    def forward(self, input, hx):
        print("python func_LSTM forward")
        lstm_forard = intel_rnn.pytorch_lstm_forward
        lstm_forard(input, input, input)
        return input

    def backward(self, input):
        print("python func_LSTM backward")
        return input


class LSTMCell(Module):
    def __init__(self, input_size, hidden_size, num_layers=1, bias=True, batch_first=False, dropout=0):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.bias = bias
        self.batch_first = batch_first
        self.dropout = dropout
        super(LSTMCell, self).__init__()

    def forward(self, input, hx):
        print("python LSTMCell forward")
        return input
 
    def backward(self, input):
        print("python LSTMCEll backward")

class LSTM(Module):
    def __init__(self, seq_length, input_size, hidden_size, num_layers=1, bias=True, batch_first=False, dropout=0):
        self.seq_length = seq_length
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.bias = bias
        self.batch_first = batch_first
        self.dropout = dropout
        super(LSTM, self).__init__()

    def forward(self, input, hx):
        print("python LSTM forward")
        return func_LSTM()(input, hx)

    def backward(self, input):
        print("python LSTM backward")
        return input

