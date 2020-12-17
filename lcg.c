#include <stdio.h>
#include <stdint.h>

static uint32_t state = 1;

void srand(uint32_t s0) {
  state = s0;
}

uint32_t rand() {
  state = (state*1103515245+12345) % 2147483648;
  return state;
}

int main() {
  srand(123);
  for(size_t i = 0; i < 100; ++i) {
    printf("%u\n", rand());
  }
  return 0;
}
