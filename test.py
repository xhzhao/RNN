import torch
from torch.autograd import Variable
import intelrnn_pytorch as irnn

N = 15
T = 64
D = 500
H = 500


input = Variable(torch.randn(N, T, D))
h0 = Variable(torch.randn(1, T, H))
c0 = Variable(torch.randn(1, T, H))

rnn = irnn.LSTM(T, D, H, 1)
rnn(input, h0)
#irnn.intel_lstm_forward(input, weight, output)
