#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#define WIDTH 10
#define HEIGHT 10
#define CHECK_W 23
#define CHECK_S 19
#define CHECK_A 1
#define CHECK_D 4
#define FOOD_COUNT 2

struct SnakeHead
{
    int x;
    int y;
    int snakeSize;
};

void clear(void);
void initialize_grid(int grid[], struct SnakeHead *head);
int check_move(char nextMove, char lastMove);
int update_grid(int grid[], struct SnakeHead *head, int nextMove);
void print_grid(int grid[], struct SnakeHead *head);
void create_food(int grid[]);

int main(void)
{
    char lastMove = 'd', nextMove;
    int check = 0;

    struct SnakeHead head;
    head.snakeSize = 2; // Don't set higher than WIDTH.
    head.x = head.snakeSize - 1;
    head.y = HEIGHT / 2;

    int grid[WIDTH * HEIGHT];
    initialize_grid(grid, &head);

    while (1)
    {
        clear();
        print_grid(grid, &head);
        while (1)
        {
            printf("Next move: ");
            fflush(stdin);
            scanf("%c%*c", &nextMove);
            check = check_move(nextMove, lastMove);
            if (check == 1)
            {
                printf("Invalid move\n");
                continue;
            }
            else if (check == 2)
            {
                printf("You can only input W/A/S/D\n");
                continue;
            }
            else if (check == 3)
            {
                printf("You Can't go backwards\n");
                continue;
            }
            check = update_grid(grid, &head, (nextMove & 31));
            if (check == 0)
            {
                break;
            }
            else if (check == 1)
            {
                printf("Internal Error");
                continue;
            }
            else if (check == 2)
            {
                printf("Collided with the wall");
                return check;
            }
            else if (check == 3)
            {
                printf("Ate yourself");
                return check;
            }
        }
        lastMove = nextMove;
    }

    return 0;
}

void clear(void)
{
#if defined(_WIN32) || defined(_WIN64) || defined(WINDOWS)
    system("cls");
#else
    system("clear");
#endif
}

void initialize_grid(int grid[], struct SnakeHead *head)
{
    for (int i = 0; i < WIDTH * HEIGHT; i++)
    {
        grid[i] = 0;
    }
    for (int i = 0; i < head->snakeSize; i++)
    {
        grid[HEIGHT * head->y + head->x - i] = head->snakeSize - i;
    }
    for (int i = 0; i < FOOD_COUNT; i++)
    {
        create_food(grid);
    }
}
int check_move(char nextMove, char lastMove)
{
    if (!isalpha(nextMove))
    {
        return 1;
    }
    int nMove = nextMove & 31, lMove = lastMove & 31;
    if (nMove != CHECK_W && nMove != CHECK_A && nMove != CHECK_S && nMove != CHECK_D)
    {
        return 2;
    }
    if ((nMove == CHECK_W && lMove == CHECK_S) ||
        (nMove == CHECK_S && lMove == CHECK_W) ||
        (nMove == CHECK_A && lMove == CHECK_D) ||
        (nMove == CHECK_D && lMove == CHECK_A))
    {
        return 3;
    }
    return 0;
}

int update_grid(int grid[], struct SnakeHead *head, int nextMove)
{
    switch (nextMove)
    {
    case CHECK_W:
        head->y -= 1;
        break;
    case CHECK_S:
        head->y += 1;
        break;
    case CHECK_A:
        head->x -= 1;
        break;
    case CHECK_D:
        head->x += 1;
        break;
    default:
        return 1;
    }
    if (head->x < 0 || head->x >= WIDTH || head->y < 0 || head->y >= HEIGHT)
    {
        return 2;
    }

    if (grid[HEIGHT * head->y + head->x] == -1)
    {
        head->snakeSize++;
        create_food(grid);
    }
    else
    {
        for (int i = 0; i < WIDTH * HEIGHT; i++)
        {
            grid[i] = (grid[i] > 0) ? grid[i] - 1 : grid[i];
        }
    }

    if (grid[HEIGHT * head->y + head->x] > 0)
    {
        return 3;
    }

    grid[HEIGHT * head->y + head->x] = head->snakeSize;

    return 0;
}

void print_grid(int grid[], struct SnakeHead *head)
{
    for (int i = 0; i < HEIGHT; i++)
    {
        for (int j = 0; j < WIDTH; j++)
        {
            int current_cell = grid[WIDTH * i + j];
            if (grid[WIDTH * i + j] > 0)
            {
                printf("%s", (current_cell == head->snakeSize) ? "()" : "[]");
            }
            else if (current_cell == -1)
            {
                printf("<>");
            }
            else
            {
                printf("##");
            }
        }
        printf("\n");
    }
}

void create_food(int grid[])
{
    int pos;
    do
    {
        pos = rand() % (HEIGHT * WIDTH);
    } while (grid[pos] > 0);
    grid[pos] = -1;
}