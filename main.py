import numpy as np
from os import system
from random import randint

def get_random_cell(grid) -> tuple:
    n = len(grid)
    x, y = randint(0, n - 1), randint(0, n - 1)
    return x, y

def get_neighbors(cell: tuple, grid) -> list:
    x, y = cell
    n = len(grid)
    neighbors = []

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            # Пропускаем саму клетку
            if dx == 0 and dy == 0:
                continue
            # Новые координаты соседа
            nx, ny = x + dx, y + dy
            # Проверяем, что не вышли за границы сетки
            if 0 <= nx < n and 0 <= ny < n:
                neighbors.append((nx, ny))
                
    return neighbors


def is_happy(cell: tuple, grid) -> bool:
    x, y = cell
    cell_color = grid[x][y]

    neighbors = get_neighbors(cell, grid)
    neighbor_colors = [grid[c[0]][c[1]] for c in neighbors]

    return neighbor_colors.count(cell_color) > 1

def get_random_unhappy(grid) -> tuple:
    cell = get_random_cell(grid)

    while is_happy(cell, grid):
        cell = get_random_cell(grid)

    return cell

def get_random_void(grid) -> tuple:
    x, y = get_random_cell(grid)

    while grid[x][y] != 0:
        x, y = get_random_cell(grid)

    return x, y
     

def create_initial_grid(n: int):
    # Определим количество клеток для каждого типа
    total_cells = n * n
    blue_cells = int(total_cells * 0.45)
    red_cells = int(total_cells * 0.45)
    empty_cells = total_cells - blue_cells - red_cells
    
    # Создаем список с обозначениями для каждого типа клеток
    # 1 - синие клетки, 2 - красные клетки, 0 - пустые клетки
    cells = [1] * blue_cells + [2] * red_cells + [0] * empty_cells
    
    # Перемешиваем клетки случайным образом
    np.random.shuffle(cells)
    
    # Преобразуем в матрицу NxN
    grid = np.array(cells).reshape(n, n)
    
    return grid


if __name__ == '__main__':
    system('cls')
    n = 4 
    grid = create_initial_grid(n)
    
    x, y = get_random_cell(grid)
    cell_val = grid[x][y]

    print(is_happy((x,y), grid))

    print(grid)

    print(f'\nСоседи клетки {(x, y)} = {cell_val}: {get_neighbors((x, y), grid)}')
 