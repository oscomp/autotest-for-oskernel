#include <bsp.h>
#include "test.h"

// test free heap size
void test2(){
    printf("=============test2===============\n");
    size_t test = get_free_heap_size();
    printf("\n[test2]free heap size is %ld\n\n", test);
    printf("=============end test2===========\n");
}
