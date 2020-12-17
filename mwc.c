#include <stdint.h>
#include <stdio.h>
#include <memory.h>
#include <limits.h>

typedef uint8_t state_t;
typedef uint16_t state2_t;

#define STATE_SIZE 4u
#define a ((state2_t)255u)

#define STATE_SIZE_BYTES STATE_SIZE*sizeof(state_t)

static state_t state[STATE_SIZE] = {1};

void srand(state_t s0[STATE_SIZE]) {
  memcpy(state, s0, STATE_SIZE_BYTES);
}

state_t rand() {
  state_t xleast = state[STATE_SIZE-1];
  memmove(state+1, state, STATE_SIZE_BYTES-sizeof(state_t));
  state2_t t = a*((state2_t)xleast) + ((state2_t)state[0]);
  state[1] = t;
  state[0] = t >> (CHAR_BIT*sizeof(state_t));
  return state[1];
}

int main() {
  for(size_t i = 0; i < 1000000; ++i) {
    rand();
  }
  uint64_t ctr = 0;
  state_t last[STATE_SIZE];
  memcpy(last, state, STATE_SIZE_BYTES);
  rand();
  ++ctr;
  while(memcmp(state, last, STATE_SIZE_BYTES) != 0) {
    rand();
    ++ctr;
  }
  printf("finished at %lu\n", ctr);
  return 0;
}
