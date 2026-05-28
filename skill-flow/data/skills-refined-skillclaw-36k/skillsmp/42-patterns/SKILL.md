---
name: 42-patterns
description: Common patterns, structures, and best practices for 42 School projects. Use when starting projects, creating Makefiles, or structuring code.
---

# 42 Project Patterns

Standard patterns and structures for 42 School projects.

## Standard Project Structure

```
project_name/
├── Makefile                  # Build system
├── README.md                 # Documentation
├── include/
│   └── project_name.h        # Main header
├── src/
│   ├── main.c               # Entry point
│   ├── init.c               # Initialization
│   ├── utils.c              # Utility functions
│   └── cleanup.c            # Resource cleanup
└── obj/                     # Object files (gitignored)
```

## Standard Makefile Template

```makefile
NAME = program_name
CC = cc
CFLAGS = -Wall -Wextra -Werror
INCLUDES = -I include

SRC_DIR = src
OBJ_DIR = obj

SRC = main.c init.c utils.c cleanup.c
OBJS = $(addprefix $(OBJ_DIR)/, $(SRC:.c=.o))

all: $(NAME)

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(OBJ_DIR)
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

clean:
	rm -rf $(OBJ_DIR)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
```

## Header File Template

```c
/* ************************************************************************** */
/*                                                        :::      ::::::::   */
/*   project_name.h                                     :+:      :+:    :+:   */
/* ************************************************************************** */

#ifndef PROJECT_NAME_H
# define PROJECT_NAME_H

# include <stdlib.h>
# include <unistd.h>
# include <stdio.h>

/* Defines */
# define BUFFER_SIZE 1024
# define ERROR -1
# define SUCCESS 0

/* Structures */
typedef struct s_data
{
    int     value;
    char    *str;
}   t_data;

/* Function Prototypes */
// Initialization
int     init_data(t_data *data, int argc, char **argv);

// Utils
void    print_error(char *msg);
void    *ft_calloc(size_t count, size_t size);

// Cleanup
void    cleanup_data(t_data *data);

#endif
```

## Error Handling Pattern

```c
typedef enum e_error
{
    ERR_ARGS = 1,
    ERR_MALLOC,
    ERR_INVALID_INPUT,
    ERR_INIT
}   t_error;

int	handle_error(t_error error)
{
	static const char	*messages[] = {
		NULL,
		"Error\nInvalid number of arguments\n",
		"Error\nArgument must be numeric only\n",
		"Error\nArgument must be a positive integer\n",
		"Error\nValue exceeds maximum (2147483647)\n",
		"Error\nOne philosopher cannot eat (needs at least 2)\n",
		"Error\nFailed to initialize global mutex\n",
		"Error\nFailed to initialize fork mutex\n",
		"Error\nMemory allocation failed\n",
		"Error\nFailed to create philosopher thread\n",
		"Error\nFailed to create monitor thread\n"
	};

	if (error > 0 && error < (int)(sizeof(messages) / sizeof(messages[0])))
	{
		printf("%s", messages[error]);
	}
	return (1);
}
```

## Init-Process-Cleanup Pattern

```c
int main(int argc, char **argv)
{
    t_data  data;

    // 1. Validate input
    if (argc < 2)
        return (handle_error(ERR_ARGS));
    
    // 2. Initialize
    if (init_data(&data, argc, argv) != SUCCESS)
        return (handle_error(ERR_INIT));
    
    // 3. Process
    if (process_data(&data) != SUCCESS)
    {
        cleanup_data(&data);
        return (handle_error(ERR_PROCESS));
    }
    
    // 4. Cleanup
    cleanup_data(&data);
    return (SUCCESS);
}
```

## Memory Management Pattern

```c
// Always check malloc
void *safe_malloc(size_t size)
{
    void *ptr;

    ptr = malloc(size);
    if (!ptr)
    {
        write(2, "Error: malloc failed\n", 21);
        exit(1);
    }
    return (ptr);
}

// Free and NULL pattern
void safe_free(void **ptr)
{
    if (ptr && *ptr)
    {
        free(*ptr);
        *ptr = NULL;
    }
}
```

## .gitignore Template

```
# Executables
program_name
*.out
*.o
*.a

# Directories
obj/
.vscode/
.DS_Store

# Test files
test
a.out
```

## Common 42 Functions

### String Length
```c
size_t  ft_strlen(const char *s)
{
    size_t  i;

    i = 0;
    while (s[i])
        i++;
    return (i);
}
```

### String to Int
```c
int ft_atoi(const char *str)
{
    int result;
    int sign;

    result = 0;
    sign = 1;
    while (*str == ' ' || (*str >= 9 && *str <= 13))
        str++;
    if (*str == '-' || *str == '+')
    {
        if (*str == '-')
            sign = -1;
        str++;
    }
    while (*str >= '0' && *str <= '9')
    {
        result = result * 10 + (*str - '0');
        str++;
    }
    return (result * sign);
}
```

## Best Practices

1. **Always check return values**: malloc, open, pthread_create
2. **Initialize variables**: `int i = 0;` not `int i;`
3. **Use const for read-only params**: `const char *str`
4. **Protect against NULL**: Check pointers before dereferencing
5. **Clean resources**: Free all allocated memory, close all fds
6. **Split long functions**: Keep functions under 25 lines
7. **Use meaningful names**: `philosopher_count` not `pc`
8. **Comment complex logic**: Explain why, not what
9. **Test edge cases**: 0, 1, negative, very large numbers
10. **Run norminette regularly**: Before every commit
