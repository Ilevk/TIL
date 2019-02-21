#include <stdio.h>

#define SIZE 15

int matrix[SIZE][SIZE];

int solve(int y, int x){
    if( y==1 || x==1 ) matrix[y][x] = 1;

}


int main() {
    int row, column, k;
    scanf("%d %d %d", &row, &column, &k);
//    int krow = (k/column)+1;
//    int kcolumn = k%(column+1)+1;
//    int result = (factorial(krow+kcolumn-2)/(factorial(krow-1) * factorial(kcolumn-1)))*(factorial(row+column-krow-kcolumn)/(factorial(row-krow) * factorial(column-kcolumn)));
    printf("%d", result);
}