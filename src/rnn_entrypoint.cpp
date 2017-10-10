#include <cstddef>
#include <iostream>
#include <rnn.h>


extern "C" {


void lstm_forward(float * input, float * weight, float * output)
  {
    printf("C      lstm_forward called \n");
  }


}
