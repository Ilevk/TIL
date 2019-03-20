#include <stdio.h>

#define SIZE 10000

int main() {
    int N;
    double max=0;
    double multi;
    int arr[10000] = {0,};

    scanf("%d", &N);

    for(int i=0; i<N; i++){
        scanf("%f", &arr[i]);
    }

    for(int i=0;i<N;i++){
        multi=1.0;
        for(int j=0;j<N-i;j++){
            multi *= arr[i+j];
            if(multi > max)
                max = multi;
        }
    }
    printf("%.3lf", max);
}