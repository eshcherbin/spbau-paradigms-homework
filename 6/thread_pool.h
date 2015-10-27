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

void lpush(struct TaskList**, struct Task*);
struct Task* lpop(struct TaskList**);

struct TaskQueue
{
    struct TaskList *front, *back;
};

void qinit(struct TaskQueue*);
void qpush(struct TaskQueue*, struct Task*);
struct Task* qpop(struct TaskQueue*);
int qempty(struct TaskQueue*);

void task_init(struct Task*, void (*f)(void*), void*);
void task_finit(struct Task*);

void *process_task(void*);

struct ThreadPool
{
    unsigned threads_nm;
    pthread_mutex_t mutex;
    pthread_cond_t cond;
    pthread_t *ths;
    struct TaskQueue queue;
    int end;
};

void thpool_init(struct ThreadPool*, unsigned);
void thpool_submit(struct ThreadPool*, struct Task*);
void thpool_wait(struct Task*);
void thpool_finit(struct ThreadPool*);

#endif
