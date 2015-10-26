#include <stdio.h>
#include <stdlib.h>
#include "thread_pool.h"

void pqsort(void*);

int *a, rec_limit;

struct TaskArgs
{
    int l, r, depth;
    struct ThreadPool *pool;
};

void targs_set(struct TaskArgs *targs, int l, int r, int depth, struct ThreadPool *pool)
{
    targs->l = l;
    targs->r = r;
    targs->depth = depth;
    targs->pool = pool;
}

int cmp(const void *op1, const void *op2)
{
    int x, y;
    x = *((int*) op1);
    y = *((int*) op2);
    return (x < y ? -1 : (x == y ? 0 : 1));
}

void add_qsort_task(int l, int r, int depth, struct ThreadPool *pool)
{
    struct TaskArgs *new_targs;
    struct Task *new_task;
    new_targs = (struct TaskArgs*) malloc(sizeof(struct TaskArgs));
    targs_set(new_targs, l, r, depth, pool);
    new_task = (struct Task*) malloc(sizeof(struct Task));
    task_init(new_task, pqsort, (void*) new_targs);
    thpool_submit(pool, new_task);
}

void pqsort(void *args)
{
    struct TaskArgs *targs = args;
    int l, r, tmp;
    l = targs->l;
    r = targs->r;

    if (targs->depth > rec_limit)
        qsort(a + l, r - l, sizeof(int), cmp);
    else
    {
        int x, i, j;
        x = a[l + rand() % (r - l)];
        i = l;
        j = r;
        while (i < j)
        {
            for (; a[i] < x; i++);
            for (; a[j - 1] > x; j--);
            if (i < j)
            {
                tmp = a[i];
                a[i] = a[j - 1];
                a[j - 1] = tmp;
                i++;
                j--;
            }
        }
        for (; i < r && a[i] == x; i++);
        for (; j > l && a[j - 1] == x; j--);
        if (j > l)
            add_qsort_task(l, j, targs->depth + 1, targs->pool);
        if (i < r)
            add_qsort_task(i, r, targs->depth + 1, targs->pool);
    }
}

int main(int argc, char **argv)
{
    int i, n, sorted;
    unsigned threads_nm;
    struct ThreadPool pool;

    srand(42);

    if (argc != 4)
    {
        fprintf(stderr, "wrong number of arguments");
        exit(1);
    }
    threads_nm = atoi(argv[1]);
    n = atoi(argv[2]);
    rec_limit = atoi(argv[3]);

    a = (int*) malloc(n * sizeof(int));
    for (i = 0; i < n; i++)
        a[i] = rand();

    thpool_init(&pool, threads_nm);
    add_qsort_task(0, n, 0, &pool);

    pthread_mutex_lock(&pool.mutex);
    while (pool.total_tasks > pool.completed_tasks)
        pthread_cond_wait(&pool.cond_completed, &pool.mutex);
    pthread_mutex_unlock(&pool.mutex);
    
    thpool_finit(&pool);

    sorted = 1;
    for (i = 1; i < n; i++)
        sorted &= a[i - 1] <= a[i];

    printf("array is ");
    if (!sorted)
        printf("not ");
    printf("sorted\n");
 
    free(a);

    return 0;
}
