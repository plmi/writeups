/*
  solution for https://crackmes.one/crackme/60d65d0833c5d410b8843014
  format: XXXX-XXXX-XXXX
  check one: characters 1-4 must be numeric
  check two: characters 6-9 must be 0
  check three: character 11 must be 'R'
*/

#include <stdio.h>
#include <time.h>
#include <stdlib.h>

#define KEY_LENGTH 15
#define RNG_MIN 1000
#define RNG_MAX 9999

int generateNumberInRange(int min, int max) {
  return rand() % (max + 1 - min) + min;
}

int main() {
  srand(time(0));
  char *serial = (char*)calloc(KEY_LENGTH, sizeof(char));
  for (int i = 0; i < KEY_LENGTH - 1; ++i) {
    if (i == 4 || i == 9) {
      serial[i] = '-';
    } else if (i == 10) {
      serial[i] = 'R';
    } else if (i >= 5 && i <= 9) {
      serial[i] = '0';
    } else {
      int number = generateNumberInRange(0, 9);
      serial[i] = number + '0';
    }
  }
  printf("serial: %s", serial);
  return 0;
}
