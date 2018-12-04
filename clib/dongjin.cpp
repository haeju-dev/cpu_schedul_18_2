#include "myheader.h"
#define MAX 100
void open_f(struct Process p[]);
void CPU(struct Process p[]);
//void sort_rr(struct Process *RR[]);
//void sort_sjf(struct Process *SJF[]);
void enqueue(struct Process p[]);
void dequeue(struct Process p[]);
void node_pr(struct Process *p);
void visual(struct Process p[]);

struct Process RR[100] = {};
struct Process SJF[100] = {};
struct Process FCFS[100] = {};

int total_burst = 0;
int time = 1;
int i = 0;
int j = 0;
int c = 0;
int front_rr = 0;
int rear_rr = 0;

int front_sjf = 0;
int rear_sjf = 0;

int front_fcfs = 0;
int rear_fcfs = 0;

int clock = 0;
int temp = 0;
int main(void) {

    /*struct Process ready;*/
    struct Process p[10];
    memset(&p, 0, sizeof(struct Process));
    memset(&RR, 0, sizeof(struct Process));
    memset(&SJF, 0, sizeof(struct Process));
    memset(&FCFS, 0, sizeof(struct Process));

    open_f(p);

#pragma region Total burst
    for (int count = 0; count < i; count++) {
        total_burst += p[count].burst;
    }
#pragma endregion
    printf("total burst : %d\n", total_burst);
    CPU(p);


    return 0;
}

void open_f(struct Process p[]) {
    FILE *fp;
    fp = fopen("C:\\Users\\김동진\\Desktop\\process1.txt", "r");

    while (!feof(fp)) {
        char buffer[100] = {};
        fscanf(fp, "%[^\n]\n", buffer);
        int tmp[4];
        sscanf(buffer, "%d %d %d %d", tmp, tmp + 1, tmp + 2, tmp + 3);
        p[i].number = *tmp;
        p[i].priority = *(tmp + 1);
        p[i].arr = *(tmp + 2);
        p[i].burst = *(tmp + 3);
        p[i].rest = *(tmp + 3);
        i++;
        //node_pr(p);
    }
    printf(" i = %d\n", i);
    fclose(fp);
}

void node_pr(struct Process *p) {
    printf("%d %d %d %d\n", p->number, p->priority, p->arr, p->burst);
}

void CPU(struct Process p[]) {

    while (true)
    {


        if (clock == total_burst) { //total burst와 같으면 종료
            break;
        }

        switch (p[j].priority)
        {
            case 1: {
                if (p[j].rest > 0) {
                    enqueue(p);
                    dequeue(p);
                }
                else {
                    printf("Process [%d] Wating time : %d\n", j, clock - p[j].arr - p[j].burst);
                    j = 2;

                }
                break;
            }
            case 2: {
                if ((rear_sjf) == (front_sjf)) {
                    if (p[j].rest > 0) {
                        enqueue(p);
                        dequeue(p);
                    }
                    else {
                        printf("Process [%d] Wating time : %d\n", j, clock - p[j].arr - p[j].burst);
                        j = 3;

                    }
                }
                break;
            }
            case 3: {
                if ((rear_rr == front_rr) && (rear_sjf == front_sjf)) {
                    if (p[j].rest > 0) {
                        enqueue(p);
                        dequeue(p);
                    }
                    else {

                        printf("Process [%d] Wating time : %d\n", j, clock - p[j].arr - p[j].burst);
                    }
                    break;
                }
            }
            default:
                break;
        }
        //도착시간 비교
        for (int count = 0; count < i; count++) {
            if ((p[count].arr) == time) {
                j = count;
                break;
            }
        }
        clock++;
        time++;
        if (j == i) {
            j = 0;
        }
    }
}
void sort_rr(struct Process *RR[]) {
    for (int count = 0; count < front_rr; count++) {
        for (int count_2 = 0; count_2 < front_rr; count_2++) {
            if (RR[count]->arr < RR[count_2]->arr)
            {
                temp = RR[count]->arr;
                RR[count]->arr = RR[count_2]->arr;
                RR[count_2]->arr = temp;
            }
        }
    }
}
void sort_sjf(struct Process *SJF[]) {
    for (int count = 0; count < i - 1; count++) {
        for (int count_2 = 0; count_2 < i - 1; count_2++) {
            if (SJF[count_2]->burst < SJF[count_2 + 1]->burst)
            {
                temp = SJF[count_2]->arr;
                SJF[count_2]->arr = SJF[count_2 + 1]->arr;
                SJF[count_2 + 1]->arr = temp;
            }
        }
    }
}

void visual(struct Process p[]) {
    printf("-----------------------------------------\n");
    printf("p[%d] rest%d\n", p[j].number, p[j].rest);
    printf("-----------------------------------------\n");
}

void enqueue(struct Process p[]) {
    switch (p[j].priority)
    {
        case 1: {
            p[j].rest = p[j].rest - 1;
            RR[rear_rr] = p[j];
            visual(p);
            rear_rr = (rear_rr + 1) % MAX;
            break;
        }
        case 2: {
            if (rear_sjf == front_sjf) {
                p[j].rest = p[j].rest - 1;
                SJF[rear_sjf] = p[j];
                visual(p);
                rear_sjf = (rear_sjf + 1) % MAX;
                break;
            }
        }
        case 3: {
            if (rear_rr == front_rr && rear_sjf == front_sjf) {
                p[j].rest = p[j].rest - 1;
                FCFS[rear_fcfs] = p[j];
                visual(p);
                rear_fcfs = (rear_fcfs + 1) % MAX;
                break;
            }
        }
        default:
            break;
    }

}
void dequeue(struct Process p[]) {
    switch (p[j].priority)
    {
        case 1: {
            front_rr = (front_rr + 1) % MAX;
            break;
        }
        case 2: {
            front_sjf = (front_sjf + 1) % MAX;
            break;
        }
        case 3: {
            front_fcfs = (front_fcfs + 1) % MAX;
            break;
        }
        default:
            break;
    }

}

