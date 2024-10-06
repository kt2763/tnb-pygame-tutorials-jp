import pygame
import sys
import random

pygame.init()  # Pygameの初期化

# 画面サイズの設定
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("テトリス風ゲーム")

# 色の定義
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

# グリッドの設定
CELL_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# テトリミノの形状定義（簡易版）
TETROMINOS = {
    "I": [(0, 1), (1, 1), (2, 1), (3, 1)],
    "O": [(1, 1), (2, 1), (1, 2), (2, 2)],
    "T": [(1, 0), (0, 1), (1, 1), (2, 1)],
    "S": [(1, 1), (2, 1), (0, 2), (1, 2)],
    "Z": [(0, 1), (1, 1), (1, 2), (2, 2)],
    "J": [(0, 1), (0, 2), (1, 2), (2, 2)],
    "L": [(2, 1), (0, 2), (1, 2), (2, 2)],
}


class Block:
    def __init__(self, shape):
        self.shape = TETROMINOS[shape]
        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )
        self.x = GRID_WIDTH // 2
        self.y = 0
        self.rotation = 0

    def rotate(self):
        # ブロックの形状を回転させる（90度回転）
        self.shape = [(-y, x) for x, y in self.shape]

    def draw(self, surface):
        for pos in self.shape:
            pygame.draw.rect(
                surface,
                self.color,
                (
                    (self.x + pos[0]) * CELL_SIZE,
                    (self.y + pos[1]) * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE,
                ),
            )


# ブロックの生成
def get_new_block():
    shape = random.choice(list(TETROMINOS.keys()))
    return Block(shape)


# 衝突判定の簡易実装
def check_collision(block, grid):
    for pos in block.shape:
        x = block.x + pos[0]
        y = block.y + pos[1]
        if y >= GRID_HEIGHT or x < 0 or x >= GRID_WIDTH:
            return True
        if grid[y][x]:
            return True
    return False


# ライン消去の実装
def clear_lines(grid):
    global score
    lines_cleared = 0
    for y in range(GRID_HEIGHT):
        if all(grid[y][x] for x in range(GRID_WIDTH)):
            lines_cleared += 1
            # 上の行を下に移動
            for move_y in range(y, 0, -1):
                grid[move_y] = grid[move_y - 1][:]
            grid[0] = [0 for _ in range(GRID_WIDTH)]
    if lines_cleared > 0:
        score += lines_cleared * 100


# グリッドの初期化
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# スコアの初期化
score = 0
font = pygame.font.SysFont("Arial", 24)

# タイマーイベントの設定
MOVE_DOWN = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_DOWN, 500)  # 500ミリ秒ごとにMOVE_DOWNイベントを発生

current_block = get_new_block()

running = True
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == MOVE_DOWN:
            current_block.y += 1
            if check_collision(current_block, grid):
                current_block.y -= 1
                # ブロックをグリッドに固定
                for pos in current_block.shape:
                    x = current_block.x + pos[0]
                    y = current_block.y + pos[1]
                    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                        grid[y][x] = current_block.color
                # ライン消去のチェック
                clear_lines(grid)
                # 新しいブロックを生成
                current_block = get_new_block()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_block.x -= 1
                if check_collision(current_block, grid):
                    current_block.x += 1
            elif event.key == pygame.K_RIGHT:
                current_block.x += 1
                if check_collision(current_block, grid):
                    current_block.x -= 1
            elif event.key == pygame.K_DOWN:
                current_block.y += 1
                if check_collision(current_block, grid):
                    current_block.y -= 1
            elif event.key == pygame.K_SPACE:
                current_block.rotate()
                if check_collision(current_block, grid):
                    # 回転後に衝突が発生した場合は元に戻す
                    for _ in range(3):
                        current_block.rotate()

    # 画面を白で塗りつぶす
    screen.fill(WHITE)

    # グリッド線を描画
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))

    # ゲーム画面の枠を描画
    pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 2)

    # グリッドに固定されたブロックを描画
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x]:
                pygame.draw.rect(
                    screen,
                    grid[y][x],
                    (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                )

    # 現在のブロックを描画
    current_block.draw(screen)

    # スコアの描画
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # 画面の更新
    pygame.display.update()

pygame.quit()
sys.exit()
