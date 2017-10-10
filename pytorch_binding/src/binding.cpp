#include <iostream>
#include "rnn.h"

#include "TH.h"

extern "C"{


void pytorch_lstm_forward(THFloatTensor * input, THFloatTensor * weight, THFloatTensor * output){
  printf("C      pytorch_lstm_forward in binding.cpp \n");
  float * inPtr = input->storage->data + input->storageOffset;
  float * weightPtr = NULL;
  float * outPtr = NULL;
  lstm_forward(inPtr, weightPtr, outPtr);
  
}




}




