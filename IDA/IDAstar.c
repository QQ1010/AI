#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#define MAXSIZE 99            // 設定方塊最多為99個
#define MAXSTEP 100           // 設定iterative 步數，最多為100步

typedef struct item {         // 儲存方塊資訊
    int index;
    int position_x;
    int position_y;
    int width;
    int high;
}Item;

typedef struct node {          // 儲存移動方塊編號與方向
    int num;
    char direction;
}Node;

typedef struct table {         // 設定盤面資訊
    int table_high;
    int table_width;
    Item piece[MAXSIZE];                  // 存方塊的編號，位置，長，寬
    int ordering[MAXSIZE];                // 存當前盤面的順序
    int order_length;                     // 盤面的順序長度
    int number[MAXSIZE][MAXSIZE];         // 存目前的盤面
    int number_length;                    // 存盤面有多少方塊
    Node can_move_node[MAXSIZE];          // 存目前盤面可以移動的編號和方向
    int node_array_length;                // 存可以移動的數量
}Table;


void table_show(Table table) {                          // 顯示棋盤狀況
    printf("table:\n");
    for(int i = 0 ; i < table.table_high; i ++) {
        for(int j = 0 ; j < table.table_width; j ++) {
            printf("%d ",table.number[i][j]);
        }
        printf("\n");
    }
}

void node_show(Table table) {                          // 顯示可以移動的node有哪些和方向
    printf("node\n");
    for(int i = 0 ; i < table.node_array_length; i++) {
        printf("%d%c ",table.can_move_node[i].num,table.can_move_node[i].direction);
    }
    printf("\n");
}

void piece_show(Item piece[MAXSIZE]) {                // 顯示每個方塊的編號，位置，長，寬
    printf("piece:\n");
    int index = 1;
    while(piece[index].index != 0) {
        printf("index = %d,  (x,y) = (%d, %d),   high = %d, width = %d\n",piece[index].index,piece[index].position_x,piece[index].position_y,piece[index].high,piece[index].width);
        index ++;
    }
}

void show_order(Table table) {                      // 顯示目前盤面的順序
    printf("ordering:\n");
    for(int i = 0 ; i < table.order_length ; i++) {
        printf("%d ",table.ordering[i]);
    }
    printf("\n");
}


Table build_puzzle(char *filename) {                          // 讀檔案並建立盤面並根據編號建立struct Item array
    FILE *file;
    Table table;
    int number = 0;
    file = fopen(filename,"r");
    if(file == NULL) {                                      // 檢查是否有這個檔案
        perror("Error opening file or no such file.");
    }
    for(int i = 0 ; i < MAXSIZE ; i++) {                     // 初始化盤面
        for(int j = 0 ; j < MAXSIZE ; j++) {
            table.number[i][j] = -1;
        }
    }

    fscanf(file,"%d",&table.table_high);                                // 讀盤面的長
    fscanf(file,"%d",&table.table_width);                               // 讀盤面的寬
    int index = 0;
    for(int i = 0 ; i < table.table_high; i++) {
        for(int j = 0 ; j < table.table_width ; j++) {
            fscanf(file,"%d",&table.number[i][j]);                 // 讀盤面，並存入table中
            if(number <= table.number[i][j]) {
                number = table.number[i][j];
            }
            if(table.piece[table.number[i][j]].index == 0) {             // 第一次讀到這個編號的方塊，將資料存入
                table.ordering[index] = table.number[i][j];
                table.piece[table.number[i][j]].index = table.number[i][j];
                table.piece[table.number[i][j]].position_x = i;
                table.piece[table.number[i][j]].position_y = j;
                table.piece[table.number[i][j]].high = 1;
                table.piece[table.number[i][j]].width = 1;
                index ++;
            }
            else if(table.piece[table.number[i][j]].index != 0) {
                table.piece[table.number[i][j]].high = i - table.piece[table.number[i][j]].position_x + 1;
                table.piece[table.number[i][j]].width = j - table.piece[table.number[i][j]].position_y + 1;
            }
        }
    }
    table.order_length = index;
    table.number_length = number;
    // 用close set判斷還有哪些可以走
    index = 0;
    for(int i = 1 ; i <= table.number_length ; i++) {
        bool up = true;
        bool down = true;
        bool right = true;
        bool left = true;
        // 檢查可不可以往上移
        for(int j = 0 ; j < table.piece[i].width ; j ++) {
            if(table.piece[i].position_x-1 < 0 || table.number[table.piece[i].position_x-1][table.piece[i].position_y+j] != 0) {
                up = false;
                break;
            }
        }
        if(up) {
            table.can_move_node[index].num = i;
            table.can_move_node[index].direction = 'U';
            index += 1;
        }
        // 檢查可不可以往下移
        for(int j = 0 ; j < table.piece[i].width ; j ++) {
            if(table.piece[i].position_x+table.piece[i].high >= table.table_high || table.number[table.piece[i].position_x+table.piece[i].high][table.piece[i].position_y+j] != 0) {
                down = false;
                break;
            }
        }
        if(down) {
            table.can_move_node[index].num = i;
            table.can_move_node[index].direction = 'D';
            index += 1;
        }
        // 檢查可不可以往右移
        for(int j = 0 ; j < table.piece[i].high ; j ++) {
            if(table.piece[i].position_y+table.piece[i].width >= table.table_width || table.number[table.piece[i].position_x+j][table.piece[i].position_y+table.piece[i].width] != 0) {
                right = false;
                break;
            }
        }
        if(right) {
            table.can_move_node[index].num = i;
            table.can_move_node[index].direction = 'R';
            index += 1;
        }
        // 檢查可不可以往左移
        for(int j = 0 ; j < table.piece[i].high ; j ++) {
            if(table.piece[i].position_y-1 < 0 || table.number[table.piece[i].position_x+j][table.piece[i].position_y-1] != 0) {
                left = false;
                break;
            }
        }
        if(left) {
            table.can_move_node[index].num = i;
            table.can_move_node[index].direction = 'L';
            index += 1;
        }
    }
    table.node_array_length = index;
    // printf("%d\n",table.node_array_length);
    // node_show(table);
    return table;
}



bool check_ordering(Table table) {                   // 檢查盤面目前的順序根據row major
    for(int i = 1; i <= table.number_length; i++) {
        if(table.ordering[i-1] != i) {
            return false;
        }
    }
    return true;
}

bool in_close_set(Table table,Item close_set[][50],int idx) {                 // 檢查現在這個盤面有沒有在close set，確認是否有走過這個盤面了
    int same[idx];
    memset(same,0,sizeof(same));
    for(int i = 0 ; i < idx ; i++) {
        for(int j = 0 ; j < table.number_length ; j++) {
            if(table.piece[j].position_x != close_set[i][j].position_x) {
                same[i] = 1;
            }
            if(table.piece[j].position_y != close_set[i][j].position_y) {
                same[i] = 1;
            }
        }
    }
    for(int i = 0 ; i < idx; i++) {
        if(same[i] == 0) {
            return true;
        }
    }
    return false;
}


Table move(Table table,int num,char direct,Item close_set[][50],int idx) {                // 處理移動
    Table next;
    next = table;
    if(direct == 'U') {
        // 移動table中的number array
        next.piece[num].position_x -= 1;
        for(int i = 0 ; i < next.piece[num].width; i++) {
            for(int j = 0 ; j < next.piece[num].high ; j++) {
                next.number[next.piece[num].position_x+j][next.piece[num].position_y+i] = num;
            }
            next.number[next.piece[num].position_x+next.piece[num].high][next.piece[num].position_y+i] = 0;
        }
        // 重新排列order array
        int visited[MAXSIZE] = {0};
        int index = 0;
        for(int i = 0 ; i < next.table_high; i++) {
            for(int j = 0 ; j < next.table_width; j++) {
                if(visited[next.number[i][j]] != 1) {
                    next.ordering[index] = next.number[i][j];
                    visited[next.number[i][j]] = 1;
                    index ++;
                }
                else if(next.number[i][j] == 0) {
                    next.ordering[index] = 0;
                    index ++;
                }
            }
        }
        index = 0;
        // 重新安排table的can_move_node array
        for(int i = 1 ; i <= next.number_length ; i++) {
            bool up = true;
            bool down = true;
            bool right = true;
            bool left = true;
            // 檢查可不可以往上移
            for(int j = 0 ; j < next.piece[i].width ; j ++) {
                if(next.piece[i].position_x-1 < 0 || next.number[next.piece[i].position_x-1][next.piece[i].position_y+j] != 0) {
                    up = false;
                    break;
                }
            }
            if(up) {
                next.piece[i].position_x -= 1;
                if(in_close_set(next,close_set,idx) == false) {
                    next.can_move_node[index].num = i;
                    next.can_move_node[index].direction = 'U';
                    index += 1;
                }
                next.piece[i].position_x += 1;
            }
            // 檢查可不可以往下移
            for(int j = 0 ; j < next.piece[i].width ; j ++) {
                if(i == num) {
                    down = false;
                    break;
                }
                else if(next.piece[i].position_x+next.piece[i].high >= next.table_high || next.number[next.piece[i].position_x+next.piece[i].high][next.piece[i].position_y+j] != 0) {
                    down = false;
                    break;
                }
            }
            if(down) {
                next.piece[i].position_x += 1;
                if(in_close_set(next,close_set,idx) == false) {
                    next.can_move_node[index].num = i;
                    next.can_move_node[index].direction = 'D';
                    index += 1;
                }
                next.piece[i].position_x -= 1;
            }
            // 檢查可不可以往右移
            for(int j = 0 ; j < next.piece[i].high ; j ++) {
                if(next.piece[i].position_y+next.piece[i].width >= next.table_width || next.number[next.piece[i].position_x+j][next.piece[i].position_y+next.piece[i].width] != 0) {
                    right = false;
                    break;
                }
            }
            if(right) {
                next.piece[i].position_y += 1;
                if(in_close_set(next,close_set,idx) == false) {
                    next.can_move_node[index].num = i;
                    next.can_move_node[index].direction = 'R';
                    index += 1;
                }
                next.piece[i].position_y -= 1;
            }
            // 檢查可不可以往左移
            for(int j = 0 ; j < next.piece[i].high ; j ++) {
                if(next.piece[i].position_y-1 < 0 || next.number[next.piece[i].position_x+j][next.piece[i].position_y-1] != 0) {
                    left = false;
                    break;
                }
            }
            if(left) {
                next.piece[i].position_y -= 1;
                if(in_close_set(next,close_set,idx) == false) {
                    next.can_move_node[index].num = i;
                    next.can_move_node[index].direction = 'L';
                    index += 1;
                }
                next.piece[i].position_y += 1;
            }
        }
        next.node_array_length = index;
    }
    else if(direct == 'D') {
        // 移動table中的number array
        next.piece[num].position_x += 1;
        for(int i = 0 ; i < next.piece[num].width; i++) {
            for(int j = 0 ; j < next.piece[num].high ; j++) {
                next.number[next.piece[num].position_x+j][next.piece[num].position_y+i] = num;
            }
            next.number[next.piece[num].position_x-1][next.piece[num].position_y+i] = 0;
        }
        // 重新排列order array
        int visited[MAXSIZE] = {0};
        int index = 0;
        for(int i = 0 ; i < next.table_high; i++) {
            for(int j = 0 ; j < next.table_width; j++) {
                if(visited[next.number[i][j]] != 1) {
                    next.ordering[index] = next.number[i][j];
                    visited[next.number[i][j]] = 1;
                    index ++;
                }
                else if(next.number[i][j] == 0) {
                    next.ordering[index] = 0;
                    index ++;
                }
            }
        }
        index = 0;
        // 重新安排table的can_move_node array
        for(int i = 1 ; i <= next.number_length ; i++) {
            bool up = true;
            bool down = true;
            bool right = true;
            bool left = true;
            // 檢查可不可以往上移
            for(int j = 0 ; j < next.piece[i].width ; j ++) {
                if(i == num) {
                    up = false;
                    break;
                }
                if(next.piece[i].position_x-1 < 0 || next.number[next.piece[i].position_x-1][next.piece[i].position_y+j] != 0) {
                    up = false;
                    break;
                }
            }
            if(up) {
                next.piece[i].position_x -= 1;
                if(in_close_set(next,close_set,idx) == false) {
                    next.can_move_node[index].num = i;
                    next.can_move_node[index].direction = 'U';
                    index += 1;
                }
                next.piece[i].position_x += 1;
            }
            // 檢查可不可以往下移
            for(int j = 0 ; j < next.piece[i].width ; j ++) {
                if(next.piece[i].position_x+next.piece[i].high >= next.table_high || next.number[next.piece[i].position_x+next.piece[i].high][next.piece[i].position_y+j] != 0) {
                    down = false;
                    break;
                }
            }
            if(down) {
                next.piece[i].position_x += 1;
                if(in_close_set(next,close_set,idx) == false) {
                    next.can_move_node[index].num = i;
                    next.can_move_node[index].direction = 'D';
                    index += 1;
                }
                next.piece[i].position_x -= 1;
            }
            // 檢查可不可以往右移
            for(int j = 0 ; j < next.piece[i].high ; j ++) {
                if(next.piece[i].position_y+next.piece[i].width >= next.table_width || next.number[next.piece[i].position_x+j][next.piece[i].position_y+next.piece[i].width] != 0) {
                    right = false;
                    break;
                }
            }
            if(right) {
                next.piece[i].position_y += 1;
                if(in_close_set(next,close_set,idx) == false) {
                    next.can_move_node[index].num = i;
                    next.can_move_node[index].direction = 'R';
                    index += 1;
                }
                next.piece[i].position_y -= 1;
            }
            // 檢查可不可以往左移
            for(int j = 0 ; j < next.piece[i].high ; j ++) {
                if(next.piece[i].position_y-1 < 0 || next.number[next.piece[i].position_x+j][next.piece[i].position_y-1] != 0) {
                    left = false;
                    break;
                }
            }
            if(left) {
                next.piece[i].position_y -= 1;
                if(in_close_set(next,close_set,idx) == false) {
                    next.can_move_node[index].num = i;
                    next.can_move_node[index].direction = 'L';
                    index += 1;
                }
                next.piece[i].position_y += 1;
            }
        }
        next.node_array_length = index;
    }
    else if(direct == 'L') {
        // 移動table中的number array
        next.piece[num].position_y -= 1;
        for(int i = 0 ; i < next.piece[num].high; i++) {
            for(int j = 0 ; j < next.piece[num].width; j++) {
                next.number[next.piece[num].position_x+i][next.piece[num].position_y+j] = num;
            }
            next.number[next.piece[num].position_x+i][next.piece[num].position_y+next.piece[num].width] = 0;
        }
        // 重新排列order array
        int visited[MAXSIZE] = {0};
        int index = 0;
        for(int i = 0 ; i < next.table_high; i++) {
            for(int j = 0 ; j < next.table_width; j++) {
                if(visited[next.number[i][j]] != 1) {
                    next.ordering[index] = next.number[i][j];
                    visited[next.number[i][j]] = 1;
                    index ++;
                }
                else if(next.number[i][j] == 0) {
                    next.ordering[index] = 0;
                    index ++;
                }
            }
        }
        index = 0;
        // 重新安排table的can_move_node array
        for(int i = 1 ; i <= next.number_length ; i++) {
            bool up = true;
            bool down = true;
            bool right = true;
            bool left = true;
            // 檢查可不可以往上移
            for(int j = 0 ; j < next.piece[i].width ; j ++) {
                if(next.piece[i].position_x-1 < 0 || next.number[next.piece[i].position_x-1][next.piece[i].position_y+j] != 0) {
                    up = false;
                    break;
                }
            }
            if(up) {
                next.piece[i].position_x -= 1;
                if(in_close_set(next,close_set,idx) == false) {
                    next.can_move_node[index].num = i;
                    next.can_move_node[index].direction = 'U';
                    index += 1;
                }
                next.piece[i].position_x += 1;
            }
            // 檢查可不可以往下移
            for(int j = 0 ; j < next.piece[i].width ; j ++) {
                if(next.piece[i].position_x+next.piece[i].high >= next.table_high || next.number[next.piece[i].position_x+next.piece[i].high][next.piece[i].position_y+j] != 0) {
                    down = false;
                    break;
                }
            }
            if(down) {
                next.piece[i].position_x += 1;
                if(in_close_set(next,close_set,idx) == false) {
                    next.can_move_node[index].num = i;
                    next.can_move_node[index].direction = 'D';
                    index += 1;
                }
                next.piece[i].position_x -= 1;
            }
            // 檢查可不可以往右移
            for(int j = 0 ; j < next.piece[i].high ; j ++) {
                if(i == num) {
                    right = false;
                    break;
                }
                else if(next.piece[i].position_y+next.piece[i].width >= next.table_width || next.number[next.piece[i].position_x+j][next.piece[i].position_y+next.piece[i].width] != 0) {
                    right = false;
                    break;
                }
            }
            if(right) {
                next.piece[i].position_y += 1;
                if(in_close_set(next,close_set,idx) == false) {
                    next.can_move_node[index].num = i;
                    next.can_move_node[index].direction = 'R';
                    index += 1;
                }
                next.piece[i].position_y -= 1;
            }
            // 檢查可不可以往左移
            for(int j = 0 ; j < next.piece[i].high ; j ++) {
                if(next.piece[i].position_y-1 < 0 || next.number[next.piece[i].position_x+j][next.piece[i].position_y-1] != 0) {
                    left = false;
                    break;
                }
            }
            if(left) {
                next.piece[i].position_y -= 1;
                if(in_close_set(next,close_set,idx) == false) {
                    next.can_move_node[index].num = i;
                    next.can_move_node[index].direction = 'L';
                    index += 1;
                }
                next.piece[i].position_y += 1;
            }
        }
        next.node_array_length = index;
    }
    else if(direct == 'R') {
        // 移動table中的number array
        next.piece[num].position_y += 1;
        for(int i = 0 ; i < next.piece[num].high; i++) {
            for(int j = 0 ; j < next.piece[num].width; j++) {
                next.number[next.piece[num].position_x+i][next.piece[num].position_y+j] = num;
            }
            next.number[next.piece[num].position_x+i][next.piece[num].position_y-1] = 0;
        }
        // 重新排列order array
        int visited[MAXSIZE] = {0};
        int index = 0;
        for(int i = 0 ; i < next.table_high; i++) {
            for(int j = 0 ; j < next.table_width; j++) {
                if(visited[next.number[i][j]] != 1) {
                    next.ordering[index] = next.number[i][j];
                    visited[next.number[i][j]] = 1;
                    index ++;
                }
                else if(next.number[i][j] == 0) {
                    next.ordering[index] = 0;
                    index ++;
                }
            }
        }
        index = 0;
        // 重新安排table的can_move_node array
        for(int i = 1 ; i <= next.number_length ; i++) {
            bool up = true;
            bool down = true;
            bool right = true;
            bool left = true;
            // 檢查可不可以往上移
            for(int j = 0 ; j < next.piece[i].width ; j ++) {
                if(next.piece[i].position_x-1 < 0 || next.number[next.piece[i].position_x-1][next.piece[i].position_y+j] != 0) {
                    up = false;
                    break;
                }
            }
            if(up) {
                next.piece[i].position_x -= 1;
                if(in_close_set(next,close_set,idx) == false) {
                    next.can_move_node[index].num = i;
                    next.can_move_node[index].direction = 'U';
                    index += 1;
                }
                next.piece[i].position_x += 1;
            }
            // 檢查可不可以往下移
            for(int j = 0 ; j < next.piece[i].width ; j ++) {
                if(next.piece[i].position_x+next.piece[i].high >= next.table_high || next.number[next.piece[i].position_x+next.piece[i].high][next.piece[i].position_y+j] != 0) {
                    down = false;
                    break;
                }
            }
            if(down) {
                next.piece[i].position_x += 1;
                if(in_close_set(next,close_set,idx) == false) {
                    next.can_move_node[index].num = i;
                    next.can_move_node[index].direction = 'D';
                    index += 1;
                }
                next.piece[i].position_x -= 1;
            }
            // 檢查可不可以往右移
            for(int j = 0 ; j < next.piece[i].high ; j ++) {
                if(next.piece[i].position_y+next.piece[i].width >= next.table_width || next.number[next.piece[i].position_x+j][next.piece[i].position_y+next.piece[i].width] != 0) {
                    right = false;
                    break;
                }
            }
            if(right) {
                next.piece[i].position_y += 1;
                if(in_close_set(next,close_set,idx) == false) {
                    next.can_move_node[index].num = i;
                    next.can_move_node[index].direction = 'R';
                    index += 1;
                }
                next.piece[i].position_y -= 1;
            }
            // 檢查可不可以往左移
            for(int j = 0 ; j < next.piece[i].high ; j ++) {
                if(i == num) {
                    left = false;
                    break;
                }
                else if(next.piece[i].position_y-1 < 0 || next.number[next.piece[i].position_x+j][next.piece[i].position_y-1] != 0) {
                    left = false;
                    break;
                }
            }
            if(left) {
                next.piece[i].position_y -= 1;
                if(in_close_set(next,close_set,idx) == false) {
                    next.can_move_node[index].num = i;
                    next.can_move_node[index].direction = 'L';
                    index += 1;
                }
                next.piece[i].position_y += 1;
            }
        }
        next.node_array_length = index;
    }
    return next;
}


Table final_state(Table table) {       // 計算最後的目標盤面
    Table final_state = table;
    int tmp_high = 0;
    int tmp_width = 0;
    for(int i = 0 ; i < table.table_high ; i++) {
        for(int j = 0 ; j < table.table_width ; j++) {
            final_state.number[i][j] = 0;
        }
    }
    int index = 1;
    for(int i = 0 ; i < table.table_high ; i++) {
        for(int j = 0 ; j < table.table_width ; j++) {
            if(final_state.number[i][j] == 0) {
                final_state.piece[index].position_x = i;
                final_state.piece[index].position_y = j;
                for(int k = 0 ; k < final_state.piece[index].high ; k++) {
                    for(int l = 0 ; l < final_state.piece[index].width ; l++) {
                        final_state.number[i + k][j + l] = index;
                    }
                }
                index += 1;
            }
        }
    }
    // 重新排列order array
        int visited[MAXSIZE] = {0};
        index = 0;
        for(int i = 0 ; i < final_state.table_high; i++) {
            for(int j = 0 ; j < final_state.table_width; j++) {
                if(visited[final_state.number[i][j]] != 1) {
                    final_state.ordering[index] = final_state.number[i][j];
                    visited[final_state.number[i][j]] = 1;
                    index ++;
                }
                else if(final_state.number[i][j] == 0) {
                    final_state.ordering[index] = 0;
                    index ++;
                }
            }
        }
        // table_show(final_state);
    return final_state;
}

// 計算當前盤面heuristic function，回傳distance
int Manhattan_distance(Table table) {
    Table final = final_state(table);
    int dist = 0;
    for(int i = 1 ; i <= table.number_length ; i++) {
        dist += abs(final.piece[i].position_x - table.piece[i].position_x) + abs(final.piece[i].position_y - table.piece[i].position_y);
    }
    // printf("dist = %d\n",dist);
    return dist;
}

// IDA*的DFS
bool IDADFS(Table table, int gx, int flimit, int *next_flimit, Node moves[],int move_idx, Item close_set[][50],int close_idx,int *steps) {
    int hx = Manhattan_distance(table);
    if(hx + gx < *next_flimit && hx + gx != flimit) {
        *next_flimit = hx + gx;
    }
    if(hx == 0) {
        *steps = gx;
        return true;
    }
    if(hx + gx > flimit) {
        return false;
    }
    Table next_table = table;
    int num;
    char direct;
    for(int i = 0 ; i < table.node_array_length ; i++) {
        num = table.can_move_node[i].num;
        direct = table.can_move_node[i].direction;
        next_table = move(table,num,direct,close_set,close_idx);
        if(IDADFS(next_table,gx+1,flimit,next_flimit,moves,move_idx+1,close_set,close_idx,steps)) {
            moves[move_idx].num = num;
            moves[move_idx].direction = direct;
            return true;
        }
    }
    return false;
}

// IDA*
int IDAstar(Table table,FILE *output) {
    clock_t start,end;
    start = clock();
    int f_limit = 0;
    int next_flimit;
    int total_step;
    bool found = false;
    Node ans_move[MAXSIZE];
    f_limit = Manhattan_distance(table);
    for(int i = 0 ; i < MAXSTEP ; i++) {
        next_flimit = MAXSIZE;
        Item close_set[MAXSIZE][table.number_length];
        for(int j = 0 ; j < MAXSIZE ; j++) {
            close_set[j][0].index = -1;
        }
        Node IDA_move[i];
        printf("step = %d\n",i);
        if(IDADFS(table,0,f_limit,&next_flimit,IDA_move,0,close_set,0,&total_step)) {
            found = true;
            for(int j = 0 ; j < total_step ; j++) {
                ans_move[j].num = IDA_move[j].num;
                ans_move[j].direction = IDA_move[j].direction;
            }
            break;
        }
        // 檢查有沒有solution
        if(f_limit == next_flimit) {
            found = false;
            break;
        }
        else if(next_flimit == 99) {
            found = false;
            break;
        }
        // printf("f_limit = %d\n",f_limit);
        f_limit = next_flimit;
        // printf("next_flimit = %d\n",next_flimit);
    }
    end = clock();
    if(found) {
        double diff = end - start; // ms
        fprintf(output,"%s\n","By IDA*");
        fprintf(output,"%s %f %s\n","Total run time = ",diff/CLOCKS_PER_SEC," seconds");
        fprintf(output,"%s %d %s\n","An optimal solution has ",total_step," moves:");
        printf("By IDA*\n");
        printf("Total run time = %f seconds.\n", diff / CLOCKS_PER_SEC );
        printf("An optimal solution has %d moves:\n",total_step);
        for(int i = 0 ; i < total_step ; i++) {
            fprintf(output,"%d%c ",ans_move[i].num,ans_move[i].direction);
            printf("%d%c ",ans_move[i].num,ans_move[i].direction);
        }
        printf("\n");
        return total_step;
    }
    else {
        // printf("no solution\n");
        return 0;
    }
}

int main() {
    char filename[] = "input.txt";
    FILE *output;
    output = fopen("output.txt","w+");
    Table table;
    table = build_puzzle(filename);
    int IDA_step = 0;
    IDA_step = IDAstar(table,output);
    if(IDA_step == 0) {
        fprintf(output,"%s\n","By IDA*");
        fprintf(output,"%s\n","no solution");
        printf("By IDA*\n");
        printf("no solution\n");
    }
    fclose(output);
}