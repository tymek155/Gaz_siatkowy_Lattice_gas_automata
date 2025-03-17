Go to [English version](#english-version)
# Ogólne informacje i wykorzystanie
## Projekt realizuje implementację symulacji gazu siatkowego - Lattice gas automata. Kod był uruchamiany i napisany w środowisku PyCharm.  

Głównym elementem reprezentującym cząstki gazu w moim programie jest klasa `Czastka`. W jej polach dla każdej z cząstek określane są ich położenie oraz wartość prędkości na danej 
osi (X lub Y, nigdy na obu). Wartości te inicjowane są w konstruktorze. Dodatkowo w klasie znajduje się 
funkcja `move`, przyjmuje ona jako argument siatkę `gird`. Funkcja `move` odpowiada za ruch cząsteczek na całej planszy i ich interakcję z barierami (bariery w wizualizacji są koloru białego). Funkcja sprawdza, która 
prędkość dla danej cząstki jest niezerowa (jedna musi być zerowa), następnie oblicza w jakim miejscu 
zgodnie z prędkością powinna znaleźć się cząstka. Jeżeli byłaby to bariera (czyli wartość `grid`, siatki 
całej planszy, w tamtym miejscu wynosi 0) ruch nie jest wykonywany, a jedynie zmieniana jest wartość 
prędkości cząsteczki na przeciwną. W części `else` dzieje się to samo, tylko w przypadku ruchu względem osi X. 
Dodatkowo w obu przypadkach, poprzednie miejsce, w którym znajdowała się cząsteczka jest zamieniane na wartość 1 
(wolne od cząsteczek, możliwe do poruszania się), a nowe miejsce zajmowane przez cząsteczkę na wartość 2 (w wizualizacji kolor pomarańczowy, w tym miejscu znajduje się cząsteczka).  

```python
class Czastka: 
    def __init__(self, x, y, dx, dy): 
        self.x = x 
        self.y = y 
        self.dx = dx 
        self.dy = dy 
 
    def move(self, grid): 
        if self.dy != 0: 
            next_y = self.y + self.dy 
            if grid[next_y][self.x] == 0: 
                self.dy = -self.dy 
            else: 
                grid[self.y][self.x] = 1 
                self.y = next_y 
                grid[self.y][self.x] = 2 
        else: 
            next_x = self.x +self.dx 
            if grid[self.y][next_x] == 0: 
                self.dx = -self.dx 
            else: 
                grid[self.y][self.x] = 1 
                self.x = next_x 
                grid[self.y][self.x] = 2
```

Następna funkcja `collision` odpowiada 
za kolizje między cząsteczkami. Zgodnie z instrukcją uwzględniłem tylko kolizję, w przypadku której tylko dwie 
cząsteczki znajdują się w jednym polu. Funkcja rozpoczyna się od stworzenia słownika, w którym zliczam występowanie 
współrzędnych każdej z cząstek. Następnie na bazie słownika tworzę listę krotek współrzędnych, które występują 
więcej niż 1 raz. Dla każdej współrzędnej z listy uruchamiana jest funkcja `solve_collision`. Funkcja ta z kolei 
wyszukuje cząstki dla których występuje kolizja dla danej współrzędnej do listy. Jeżeli długość listy (czyli 
ilość cząstek) to 2, wtedy stosuję zgodnie z instrukcją rozwiązywanie kolizji (tylko wtedy, jeżeli w polu znajdują 
się tylko 2 cząstki). Sprawdzam za pomocą `if`, czy cząstki poruszają się po tej samej osi, jeżeli tak jest to w 
zależności od osi przekazuję prędkości na oś X lub oś Y.  

```python
def solve_collision(coord, czastk_list): 
    collisions = [] 
    for czastka in czastk_list: 
        if czastka.x == coord[0] and czastka.y == coord[1]: 
            collisions.append(czastka) 
 
    if len(collisions) == 2: 
        if collisions[0].dx != 0 and collisions[0].dx == -collisions[1].dx: 
            collisions[0].dy = collisions[0].dx 
            collisions[0].dx = 0 
 
            collisions[1].dy = collisions[1].dx 
            collisions[1].dx = 0 
 
        elif collisions[0].dy != 0 and collisions[0].dy == -collisions[1].dy: 
            collisions[0].dx = collisions[0].dy 
            collisions[0].dy = 0 
 
            collisions[1].dx = collisions[1].dy 
            collisions[1].dy = 0 
 
 
def collision(czastk_list): 
    coord_count = {} 
 
    for czastka in czastk_list: 
        coord = (czastka.x, czastka.y) 
        if coord in coord_count: 
            coord_count[coord] += 1 
        else: 
            coord_count[coord] = 1 
 
    collision_coords = [coord for coord, count in coord_count.items() if count > 1] 
 
    for coord in collision_coords: 
        solve_collision(coord, czastk_list) 
```
W pliku `main.py` importowane są wymagane do działania programu 
biblioteki oraz funkcje i klasy. Globalnie inicjalizuję zmienne określające wielkość pola, szerokość oraz 
wysokość okna (a także proporcjonalne przeliczenie na piksele). Inicjowana jest także siatka będąca bazą do wizualizacji. 
W funkcji `init_grid` macierz grid jest zerowana na jej krawędziach, wyrysowywana jest także zgodnie z instrukcją przegroda 
z lewej strony. Funkcja `draw_board` służy do wizualizowania działania programu, rysowane są białe i pomarańczowe kwadraty, w zależności czy mamy do czynienia z barierą czy cząstką. Funkcja `generate_particles_left` generuje w lewej części planszy 
listę cząsteczek gazu o losowym położeniu i wektorach prędkości dla podanej w argumencie ilości. W głównej funkcji `main` 
inicjowane jest działanie `pygame`, dodany jest element `clock` pozwalający na kontrolę prędkości animacji, inicjowana jest 
macierz grid oraz generowane są cząsteczki w lewej części planszy (ja wygenerowałem 1000 cząsteczek). W pętli głównej kontrolowane 
jest działanie programu, stale inicjowana jest macierz `grid`, w pętli `for` wykonywany jest ruch dla każdej z cząstek z listy, wyrysowywana 
jest wizualizacja, na końcu kontrolowane są kolizje. W `clock.tick()` możliwe jest ustawienie generowanej liczby klatek na sekundę.

```python
import pygame 
import random 
from czastka import Czastka, collision 
 
CELL_SIZE = 4 
GRID_WIDTH = 200 
GRID_HEIGHT = 190 
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE 
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE 
 
grid = [[1 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)] 
 
def init_grid(): 
    for x in range(GRID_WIDTH): 
        grid[0][x] = 0 
        grid[GRID_HEIGHT - 1][x] = 0 
    for y in range (GRID_HEIGHT): 
        grid[y][0] = 0 
        grid[y][GRID_WIDTH - 1] = 0 
 
    barrier_x = GRID_WIDTH // 4 
    for y in range(GRID_HEIGHT): 
        if GRID_HEIGHT // 2 -10 <= y<= GRID_HEIGHT//2+10: 
            continue 
        grid[y][barrier_x]= 0 
 
def draw_board(screen): 
    for y in range(GRID_HEIGHT): 
        for x in range(GRID_WIDTH): 
            if grid[y][x] == 0: 
                color = (255,255,255) 
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)) 
            elif grid[y][x] == 2: 
                color = (255,165,0) 
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)) 
 
def generate_particles_left(num_particles): 
    particles = [] 
    for _ in range(num_particles): 
        x = random.randint(1, GRID_WIDTH // 4 - 2) 
        y = random.randint(1, GRID_HEIGHT - 2) 
        dx, dy = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])  
        particle = Czastka(x, y, dx, dy) 
        particles.append(particle) 
    return particles 
 
def main(): 
    pygame.init() 
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) 
    clock = pygame.time.Clock() 
    running = True 
    init_grid() 
 
    #czastka1 = Czastka(GRID_WIDTH - 2, GRID_HEIGHT - 100, -1, 0)  # Cząstka leci w lewo (w osi X) 
    #czastka2 = Czastka(2, GRID_HEIGHT - 100, 1, 0)  # Cząstka leci w prawo (w osi X) 
 
    czastki = generate_particles_left(1000) 
 
    while running: 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False 
        init_grid() 
        #colision_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)] 
 
        for czastka in czastki: 
            czastka.move(grid) 
 
        #draw_grid(screen) 
        screen.fill((0,0,0)) 
        draw_board(screen) 
        collision(czastki) 
 
        pygame.display.flip() 
        clock.tick(10) 
 
    pygame.quit() 
 
main()
```

# Technologie
W kodzie użyto:
* Python 3.12
* NumPy 2.2.2
* moduł `random`

# Przykładowe wizualizacje
![image](https://github.com/user-attachments/assets/6c4e9363-b73f-4b2e-a343-13dbdd7ac64d)

![image](https://github.com/user-attachments/assets/26dfc115-de8a-49a6-9bf0-3d64abb7dc12)

![image](https://github.com/user-attachments/assets/e0a7b122-c072-423d-9462-3d14ae150a33)

# English version

# General Information and usage 
## The project implements a lattice gas simulation - Lattice gas automata. The code was run and written in the PyCharm environment.

The main element representing gas particles in my program is the `Czastka` class. In its fields, the position and velocity value on 
a given axis (X or Y, never both) are defined for each particle. These values are initialized in the constructor. Additionally, the 
class includes the `move` function, which takes a `gird` grid as an argument. The `move` function is responsible for the movement of 
particles across the board and their interaction with barriers (barriers in the visualization are white). The function checks which 
velocity for a given particle is non-zero (one must be zero), then calculates where the particle should be located according to the 
velocity. If it would be a barrier (i.e., the `grid` value at that location is 0), the movement is not performed, and only the particle’s 
velocity is changed to the opposite value. In the `else` part, the same happens, but for movement relative to the X axis. Additionally, 
in both cases, the previous location where the particle was situated is changed to the value 1 (free from particles, available for movement), 
and the new location occupied by the particle is set to the value 2 (orange in visualization, indicating the particle’s presence).  

```python
class Czastka: 
    def __init__(self, x, y, dx, dy): 
        self.x = x 
        self.y = y 
        self.dx = dx 
        self.dy = dy 
 
    def move(self, grid): 
        if self.dy != 0: 
            next_y = self.y + self.dy 
            if grid[next_y][self.x] == 0: 
                self.dy = -self.dy 
            else: 
                grid[self.y][self.x] = 1 
                self.y = next_y 
                grid[self.y][self.x] = 2 
        else: 
            next_x = self.x +self.dx 
            if grid[self.y][next_x] == 0: 
                self.dx = -self.dx 
            else: 
                grid[self.y][self.x] = 1 
                self.x = next_x 
                grid[self.y][self.x] = 2
```

The next function `collision` is responsible for collisions between particles. According to the instructions, 
I included only collisions where **exactly two particles** are in the same cell. The function starts by creating a 
dictionary to count the occurrences of each particle's coordinates. Based on this dictionary, a list of coordinate tuples that 
appear more than once is generated. For each coordinate in this list, the `solve_collision` function is triggered.  The `solve_collision` 
function searches for particles involved in a collision at the given coordinate and adds them to a list. If the list length (i.e., 
the number of particles) is **exactly 2**, collision resolution is applied (only if there are exactly two particles in the cell). 
Using an `if` statement, it checks whether the particles move along the **same axis** (X or Y). If true, the velocities are adjusted 
based on the axis (X or Y velocities are swapped).  

```python
def solve_collision(coord, czastk_list): 
    collisions = [] 
    for czastka in czastk_list: 
        if czastka.x == coord[0] and czastka.y == coord[1]: 
            collisions.append(czastka) 
 
    if len(collisions) == 2: 
        if collisions[0].dx != 0 and collisions[0].dx == -collisions[1].dx: 
            collisions[0].dy = collisions[0].dx 
            collisions[0].dx = 0 
 
            collisions[1].dy = collisions[1].dx 
            collisions[1].dx = 0 
 
        elif collisions[0].dy != 0 and collisions[0].dy == -collisions[1].dy: 
            collisions[0].dx = collisions[0].dy 
            collisions[0].dy = 0 
 
            collisions[1].dx = collisions[1].dy 
            collisions[1].dy = 0 
 
 
def collision(czastk_list): 
    coord_count = {} 
 
    for czastka in czastk_list: 
        coord = (czastka.x, czastka.y) 
        if coord in coord_count: 
            coord_count[coord] += 1 
        else: 
            coord_count[coord] = 1 
 
    collision_coords = [coord for coord, count in coord_count.items() if count > 1] 
 
    for coord in collision_coords: 
        solve_collision(coord, czastk_list) 
```

The `main.py` file imports the necessary libraries, functions, and classes required for the program to function. 
Global variables defining the field size, window width and height (including proportional pixel conversion) are initialized. 
A grid serving as the visualization base is also set up. In the `init_grid` function, the grid matrix is reset to zeros at its 
edges, and a barrier is drawn on the left side according to the instructions. The `draw_board` function visualizes the program’s 
operation by drawing white squares (for barriers) and orange squares (for particles) based on the grid’s values. The 
`generate_particles_left` function creates a list of gas particles in the left part of the board with random positions and velocity 
vectors for a specified quantity provided as an argument. In the main `main` function, Pygame is initialized, a `clock` element is added 
to control animation speed, the grid matrix is initialized, and particles are generated in the left section of the board (in this case, 
1,000 particles were generated). The main loop controls the program’s execution: the `grid` matrix is continuously reinitialized, a `for` 
loop iterates over each particle in the list to update their movements, the visualization is rendered, and collisions are checked at the end. 
The `clock.tick()` method allows setting the desired number of frames per second to control the animation speed.

```python
import pygame 
import random 
from czastka import Czastka, collision 
 
CELL_SIZE = 4 
GRID_WIDTH = 200 
GRID_HEIGHT = 190 
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE 
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE 
 
grid = [[1 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)] 
 
def init_grid(): 
    for x in range(GRID_WIDTH): 
        grid[0][x] = 0 
        grid[GRID_HEIGHT - 1][x] = 0 
    for y in range (GRID_HEIGHT): 
        grid[y][0] = 0 
        grid[y][GRID_WIDTH - 1] = 0 
 
    barrier_x = GRID_WIDTH // 4 
    for y in range(GRID_HEIGHT): 
        if GRID_HEIGHT // 2 -10 <= y<= GRID_HEIGHT//2+10: 
            continue 
        grid[y][barrier_x]= 0 
 
def draw_board(screen): 
    for y in range(GRID_HEIGHT): 
        for x in range(GRID_WIDTH): 
            if grid[y][x] == 0: 
                color = (255,255,255) 
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)) 
            elif grid[y][x] == 2: 
                color = (255,165,0) 
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)) 
 
def generate_particles_left(num_particles): 
    particles = [] 
    for _ in range(num_particles): 
        x = random.randint(1, GRID_WIDTH // 4 - 2) 
        y = random.randint(1, GRID_HEIGHT - 2) 
        dx, dy = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])  
        particle = Czastka(x, y, dx, dy) 
        particles.append(particle) 
    return particles 
 
def main(): 
    pygame.init() 
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) 
    clock = pygame.time.Clock() 
    running = True 
    init_grid() 
 
    #czastka1 = Czastka(GRID_WIDTH - 2, GRID_HEIGHT - 100, -1, 0)  # Cząstka leci w lewo (w osi X) 
    #czastka2 = Czastka(2, GRID_HEIGHT - 100, 1, 0)  # Cząstka leci w prawo (w osi X) 
 
    czastki = generate_particles_left(1000) 
 
    while running: 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False 
        init_grid() 
        #colision_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)] 
 
        for czastka in czastki: 
            czastka.move(grid) 
 
        #draw_grid(screen) 
        screen.fill((0,0,0)) 
        draw_board(screen) 
        collision(czastki) 
 
        pygame.display.flip() 
        clock.tick(10) 
 
    pygame.quit() 
 
main()
```

# Technologies  
The code uses:  
* Python 3.12
* NumPy 2.2.2
* `random` module

# Sample visualizations
![image](https://github.com/user-attachments/assets/6c4e9363-b73f-4b2e-a343-13dbdd7ac64d)

![image](https://github.com/user-attachments/assets/26dfc115-de8a-49a6-9bf0-3d64abb7dc12)

![image](https://github.com/user-attachments/assets/e0a7b122-c072-423d-9462-3d14ae150a33)



