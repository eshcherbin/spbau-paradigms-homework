CC ?= clang
CFLAGS ?= -O2 -Wall -Wextra -Wshadow -Werror -ansi -pedantic
LDFLAGS ?= -lpthread

all: pqsort.c thread_pool.c thread_pool.h
	$(CC) pqsort.c thread_pool.c $(LDFLAGS) -o pqsort

clean:
	rm pqsort -f

.PHONY: clean all
