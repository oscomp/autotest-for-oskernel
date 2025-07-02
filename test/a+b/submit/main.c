#include <stdio.h>

int main(void) {
    int n;
    int a, b;
    while (~scanf("%d", &n)) {
        while (n--) {
            scanf("%d%d", &a, &b);
            printf("%d\n", a + b);
        }
    }
    return 0;
}