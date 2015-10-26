#ifndef __THREAD_POOL_H__
#define __THREAD_POOL_H__

#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

struct Task
{
    void (*f)(void*);
    void *arg;
    pthread_cond_t cond;
    int completed;
    pthread_mutex_t mutex;
};

struct TaskList
{
    struct Task *task;
    struct TaskList *next;
};

void push(struct TaskList**, struct Task*);
struct Task* pop(struct TaskList**);

void task_init(struct Task*, void (*f)(void*), void*);
void task_finit(struct Task*);

void *process_task(void*);

struct ThreadPool
{
    unsigned threads_nm;
    pthread_mutex_t mutex;
    pthread_cond_t cond, cond_completed;
    pthread_t *ths;
    struct TaskList *lst, *completed_lst;
    int end, total_tasks, completed_tasks;
};

void thpool_init(struct ThreadPool*, unsigned);
void thpool_submit(struct ThreadPool*, struct Task*);
void thpool_wait(struct Task*);
void thpool_finit(struct ThreadPool*);

#endif
