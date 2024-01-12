import pygame
from random import randint

# Инициализация PyGame
pygame.init()

# Константы для размеров
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
INITIAL_POSITION_X = SCREEN_WIDTH // 2
INITIAL_POSITION_Y = SCREEN_HEIGHT // 2

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)

# Скорость движения змейки
SPEED = 7

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля
pygame.display.set_caption("Змейка")

# Настройка времени
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=(INITIAL_POSITION_X, INITIAL_POSITION_Y),
                 body_color=COLOR_WHITE):
        """Инициализирует объект с заданной позицией."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Отрисовывает объект на поверхности."""
        pass


class Apple(GameObject):
    """Класс яблока в игре."""

    def __init__(self):
        """Инициализирует яблоко и размещает его в случайной позиции."""
        super().__init__(body_color=COLOR_RED)
        self.randomize_position()

    def randomize_position(self):
        """Размещает яблоко в случайной позиции на игровом поле."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (93, 216, 228), rect, 1)


class Snake(GameObject):
    """Класс змейки в игре."""

    def __init__(self):
        """Инициализирует змейку с начальными параметрами."""
        super().__init__(position=(INITIAL_POSITION_X, INITIAL_POSITION_Y),
                         body_color=COLOR_GREEN)
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.positions = [self.position]

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self, surface):
        """Отрисовывает змейку на игровом поле."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (93, 216, 228), rect, 1)

        # Отрисовка головы змейки
        head = self.positions[0]
        head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, (93, 216, 228), head_rect, 1)

    def move(self):
        """Перемещает змейку и удаляет последний элемент, если необходимо."""
        x, y = self.positions[0]
        new_x = (x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_y = (y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        self.positions.insert(0, (new_x, new_y))
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку к начальному состоянию."""
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [self.position]


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш игрока для управления игровым объектом."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры, где происходит инициализация"""
    """и управление игровым процессом."""
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        elif snake.last:
            last_rect = pygame.Rect((snake.last[0], snake.last[1]),
                                    (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        # Проверка столкновения с собой
        for segment in snake.positions[1:]:
            if snake.get_head_position() == segment:
                snake.reset()
                screen.fill(BOARD_BACKGROUND_COLOR)
                break

        # Отрисовка головы змейки и яблока
        snake.draw(screen)
        apple.draw(screen)

        # Обновление экрана
        pygame.display.update()


if __name__ == "__main__":
    main()
