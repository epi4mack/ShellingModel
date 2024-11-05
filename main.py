import numpy as np
import matplotlib.pyplot as plt
from random import choice
from matplotlib.colors import ListedColormap

from time import perf_counter

def create_initial_grid(n: int):
    total_cells = n * n
    blue_cells = int(total_cells * 0.45)
    red_cells = int(total_cells * 0.45)
    empty_cells = total_cells - blue_cells - red_cells

    cells = [1] * blue_cells + [2] * red_cells + [0] * empty_cells
    np.random.shuffle(cells)

    grid = np.array(cells).reshape(n, n)
    return grid


def is_empty(cell: tuple, grid) -> bool:
    x, y = cell
    return grid[x][y] == 0

def get_neighbors(cell: tuple, grid) -> list:
    x, y = cell
    n = len(grid)
    neighbors = []

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:

            if dx == 0 and dy == 0:
                continue

            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n:
                neighbors.append((nx, ny))

    return neighbors


def is_happy(cell: tuple, grid) -> bool:
    x, y = cell
    cell_color = grid[x][y]
    neighbors = get_neighbors(cell, grid)
    neighbor_colors = [grid[c[0]][c[1]] for c in neighbors]

    global happiness_threshold
    return neighbor_colors.count(cell_color) >= happiness_threshold


def swap_cells(grid, cell1: tuple, cell2: tuple) -> None:
    x1, y1 = cell1
    x2, y2 = cell2

    grid[x2][y2], grid[x1][y1] = grid[x1][y1], grid[x2][y2]


def get_unhappy_cells(grid) -> set:
    return {cell for cell in np.ndindex(grid.shape) if not is_empty(cell, grid) and not is_happy(cell, grid)}


def get_empty_cells(grid) -> set:
    return {cell for cell in np.ndindex(grid.shape) if is_empty(cell, grid)}


# Обновляет состояние счастья соседей клетки после перемещения клетки
def update_neighbors_happiness(cell: tuple, grid, unhappy_cells: set, empty_cells: set) -> None:
    neighbors = get_neighbors(cell, grid)

    for n in neighbors:
        if n not in empty_cells:
            if is_happy(n, grid):
                unhappy_cells.discard(n)
            else:
                unhappy_cells.add(n)


# Медленная функция
# def iterate(grid, k: int) -> None:
#
#     for i in range(k):
#         unhappy_cells = get_unhappy_cells(grid)
#
#         if not unhappy_cells:
#             global total
#             total = i
#             return
#
#         empty_cells = get_empty_cells(grid)
#
#         random_empty = choice(list(empty_cells))
#         random_unhappy = choice(list(unhappy_cells))
#
#         swap_cells(grid, random_unhappy, random_empty)

# Быстрая функция
def iterate(grid, k: int) -> None:
    unhappy_cells = get_unhappy_cells(grid)
    empty_cells = get_empty_cells(grid)

    for i in range(k):

        # Если несчастные клетки закончились - перестаём итерировать
        if not unhappy_cells:
            global total
            total = i
            return

        random_unhappy = choice(list(unhappy_cells))
        random_empty = choice(list(empty_cells))

        swap_cells(grid, random_unhappy, random_empty)  # Теперь на месте random_empty находится random_unhappy

        '''
        После замены клеток на месте random_unhappy лежит пустая клетка,
        а на месте random_empty - НЕ пустая, но мы не знаем, счастлива
        она теперь или нет.
        '''

        unhappy_cells.remove(random_unhappy)  # Теперь эта клетка пустая

        empty_cells.remove(random_empty)  # Теперь клетка на этих координатах точно НЕ пустая
        empty_cells.add(random_unhappy)  # Клетка на координатах random_unhappy теперь точно пустая

        if not is_happy(random_empty, grid):
            unhappy_cells.add(random_empty)

        # Обновляем состояние счастья соседей обеих клеток, которые поменяли местами
        update_neighbors_happiness(random_unhappy, grid, unhappy_cells, empty_cells)
        update_neighbors_happiness(random_empty, grid, unhappy_cells, empty_cells)

    total = k


def unhappy_percentage(grid) -> float:
    total_cells = grid.size
    unhappy_cells_count = len(get_unhappy_cells(grid))
    return round((unhappy_cells_count / total_cells) * 100, 2)

def empty_percentage(grid) -> float:
    total_cells = grid.size
    empty_cells_count = len(get_empty_cells(grid))
    return round((empty_cells_count / total_cells) * 100, 2)

if __name__ == '__main__':

    n = 100 # Размер матрицы
    happiness_threshold = 2 # Минимальное кол-во друзей для счастья
    k = 100_000_000 # Число итераций

    total = 0

    start = perf_counter()

    initial_grid = create_initial_grid(n)

    unhappy = unhappy_percentage(initial_grid)
    empty = empty_percentage(initial_grid)
    happy = 100 - (unhappy + empty)

    print(f'До итераций:\n   Несчастных: {unhappy}%\n   Счастливых: {happy}%\n   Пустых: {empty}%')

    final_grid = initial_grid.copy()

    iterate(final_grid, k)

    total_time = perf_counter() - start

    unhappy = unhappy_percentage(final_grid)
    empty = empty_percentage(final_grid)
    happy = 100 - (unhappy + empty)

    print(f'\nПосле итераций:\n   Несчастных: {unhappy}%\n   Счастливых: {happy}%\n   Пустых: {empty}%')
    print(f'\nЗаняло времени: {total_time:.2f} с.')

    colors = ['white', 'blue', 'red']
    cmap = ListedColormap(colors)

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    axes[0].imshow(initial_grid, cmap=cmap, vmin=0, vmax=2)
    axes[0].set_title('Начальная сетка')
    axes[0].axis('off')

    axes[1].imshow(final_grid, cmap=cmap, vmin=0, vmax=2)
    axes[1].set_title(f'Финальная сетка.\nЧисло шагов: {total:,}')
    axes[1].axis('off')

    unhappy_cells = get_unhappy_cells(final_grid)
    if unhappy_cells:
        print('Оставшиеся несчастные клетки:', *unhappy_cells)

    plt.tight_layout()
    plt.show()
