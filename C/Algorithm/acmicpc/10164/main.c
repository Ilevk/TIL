#include <stdio.h>
#include <memory.h>

#define SIZE 16

int matrix[SIZE][SIZE];

int solve(int y, int x){
    if( y==1 || x==1 ) return matrix[x][y] = 1;
    if(matrix[x][y] != -1) return matrix[x][y];

    matrix[x][y] = solve(x-1,y) + solve(x, y-1);
    return matrix[x][y];
}

int result(int row, int column, int k){
    if(k==0){
        return solve(row,column);
    }  else {
//        int krow = (k / column) + 1;
//        int kcolumn = k % (column);
        int krow = (k + column - 1) / column;
        int kcolumn = (k % column);
        if (kcolumn == 0) kcolumn = column;
        return solve(krow, kcolumn) * solve(row - krow + 1, column - kcolumn + 1);
    }
}


int main() {
    int row, column, k;
    scanf("%d %d %d", &row, &column, &k);
    memset(matrix, -1, sizeof(matrix));
    int re = result(row, column, k);
    printf("%d\n", re);
}