#include "thread_pool.h"

void lpush(struct TaskList **lst, struct Task *task)
{
    struct TaskList *new_node = malloc(sizeof(struct TaskList));
    new_node->task = task;
    new_node->next = *lst;
    *lst = new_node;
}

struct Task* lpop(struct TaskList **lst)
{
    struct Task *res;
    struct TaskList *old;
    if (!*lst)
        return NULL;
    res = (*lst)->task;
    old = *lst;
    *lst = (*lst)->next;
    free(old);

    return res;
}

void qinit(struct TaskQueue *queue)
{
    queue->front = queue->back = NULL;
}

void qpush(struct TaskQueue *queue, struct Task *task)
{
    lpush(&queue->back, task);
}

struct Task* qpop(struct TaskQueue *queue)
{
    struct Task *task;
    if (!queue->front)
    {
        task = lpop(&queue->back);
        while (task)
        {
            lpush(&queue->front, task);
            task = lpop(&queue->back);
        }
    }
    return lpop(&queue->front);
}

int qempty(struct TaskQueue *queue)
{
    return queue->front || queue->back;
}

struct Task* get_task(struct ThreadPool *pool)
{
    struct Task* res;
    pthread_mutex_lock(&pool->mutex);
    while (!qempty(&pool->queue) && !pool->end)
        pthread_cond_wait(&pool->cond, &pool->mutex);
    res = qpop(&pool->queue);
    pthread_mutex_unlock(&pool->mutex);
    return res;
}

void* process_task(void *arg)
{
    struct ThreadPool *pool;
    struct Task *task;
    pool = arg;
    task = get_task(pool);
    while (task)
    {
        pthread_mutex_lock(&task->mutex);
        assert(!task->completed);
        task->f(task->arg);
        task->completed = 1;
        pthread_cond_broadcast(&task->cond);
        pthread_mutex_unlock(&task->mutex);

        task = get_task(pool);
    }
    return NULL;
}

void thpool_init(struct ThreadPool *pool, unsigned threads_nm)
{
    int rc;
    unsigned i;
    pthread_mutex_init(&pool->mutex, NULL);
    pthread_cond_init(&pool->cond, NULL);
    qinit(&pool->queue);
    pool->end = 0;
    pool->threads_nm = threads_nm;
    
    pool->ths = malloc(threads_nm * sizeof(pthread_t));
    for (i = 0; i < threads_nm; i++)
    {
        rc = pthread_create(pool->ths + i, NULL, process_task, pool);
        if (rc)
        {
            perror("error");
            exit(1);
        }
    }
}

void thpool_submit(struct ThreadPool *pool, struct Task *task)
{
    pthread_mutex_lock(&pool->mutex);
    qpush(&pool->queue, task);
    pthread_cond_signal(&pool->cond);
    pthread_mutex_unlock(&pool->mutex);
}

void thpool_wait(struct Task *task)
{
    pthread_mutex_lock(&task->mutex);
    while (!task->completed)
        pthread_cond_wait(&task->cond, &task->mutex);
    pthread_mutex_unlock(&task->mutex);
}

void thpool_finit(struct ThreadPool *pool)
{
    unsigned i;

    pthread_mutex_lock(&pool->mutex);
    pool->end = 1;
    pthread_cond_broadcast(&pool->cond);
    pthread_mutex_unlock(&pool->mutex);

    for (i = 0; i < pool->threads_nm; i++)
        pthread_join(pool->ths[i], NULL);
    free(pool->ths);

    pthread_mutex_destroy(&pool->mutex);
    pthread_cond_destroy(&pool->cond);
}

void task_init(struct Task *task, void (*f)(void*), void *arg)
{
    task->f = f;
    task->arg = arg;
    task->completed = 0;
    pthread_mutex_init(&task->mutex, NULL);
    pthread_cond_init(&task->cond, NULL);
}

void task_finit(struct Task *task)
{
    free(task->arg);
    pthread_mutex_destroy(&task->mutex);
    pthread_cond_destroy(&task->cond);
}
