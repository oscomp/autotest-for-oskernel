#include <bsp.h>
#include "test.h"
size_t brk(size_t pos);


int booted = 0;
extern char *_heap_cur;
extern char *_heap_line;
extern char *_ioheap_line;

// test brk
void test3(){
    printf("=============test3===============\n");
    booted = 1;
    size_t free_heap_size = get_free_heap_size();
    printf("[test3]Before alloc,free heap size is %ld\n", free_heap_size);
    size_t cur_pos = brk(0);
    printf("[test3]Before alloc,heap  pos: %ld\n", cur_pos);
    // printf("brk::  heap_line %ld, ioheap_line %ld, heap_cur %ld\n",
    //              (size_t)_heap_line, (size_t)_ioheap_line, (size_t)_heap_cur);

    size_t alloc_pos = brk(cur_pos + 64);
    alloc_pos = brk(0);
    printf("[test3]After alloc,heap pos: %ld\n",alloc_pos);

    size_t alloc_pos_1 = brk(alloc_pos + 64);
    alloc_pos_1 = brk(0);
    printf("[test3]Alloc again,heap pos: %ld\n",alloc_pos_1);


    size_t free_heap_size_1 = get_free_heap_size();
    printf("[test3]After alloc,free heap size is %ld\n", free_heap_size_1);

    printf("=============end test3===========\n");
}
