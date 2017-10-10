#pragma once

#ifdef __cplusplus
#include <cstddef>
extern "C" {
#endif


void lstm_forward(float * input, float * weight, float * output);



#ifdef __cplusplus
}
#endif
