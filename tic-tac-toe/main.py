# Pygameライブラリとその他の必要なモジュールをインポート
import pygame
import sys

# Pygameの初期化
pygame.init()

# ゲームウィンドウの設定
WINDOW_SIZE = 600  # ウィンドウのサイズ（正方形）
CELL_SIZE = WINDOW_SIZE // 3  # 各セルのサイズ（3x3グリッド）
LINE_WIDTH = 10  # グリッド線の太さ
MARK_SIZE = 80  # XとOマークのサイズ
MARK_WIDTH = 15  # XとOマークの線の太さ

# 色の定義（RGB形式）
BACKGROUND_COLOR = (240, 240, 240)  # 背景色（薄いグレー）
LINE_COLOR = (0, 0, 0)  # グリッド線の色（黒）
X_COLOR = (66, 130, 246)  # Xマークの色（青）
O_COLOR = (242, 85, 96)  # Oマークの色（赤）
TEXT_COLOR = (0, 0, 0)  # テキストの色（黒）

# ゲームウィンドウの作成
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("○×ゲーム (Tic-Tac-Toe)")

# フォントの設定
font_path = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
if sys.platform == "win32":
    font_path = "C:/Windows/Fonts/meiryo.ttc"
else:
    font_path = "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"

font = pygame.font.Font(font_path, 60)
small_font = pygame.font.Font(font_path, 30)


class TicTacToe:
    """○×ゲームのメインクラス"""

    def __init__(self):
        """ゲームの初期化"""
        # 3x3のゲームボード（0: 空、1: X、2: O）
        self.board = [[0 for _ in range(3)] for _ in range(3)]
        # 現在のプレイヤー（1: X、2: O）
        self.current_player = 1
        # ゲーム終了フラグ
        self.game_over = False
        # 勝者（0: なし、1: X、2: O、3: ドロー）
        self.winner = 0

    def draw_grid(self):
        """グリッド線を描画"""
        # 垂直線を2本描画
        for i in range(1, 3):
            pygame.draw.line(
                screen,
                LINE_COLOR,
                (i * CELL_SIZE, 0),
                (i * CELL_SIZE, WINDOW_SIZE),
                LINE_WIDTH
            )

        # 水平線を2本描画
        for i in range(1, 3):
            pygame.draw.line(
                screen,
                LINE_COLOR,
                (0, i * CELL_SIZE),
                (WINDOW_SIZE, i * CELL_SIZE),
                LINE_WIDTH
            )

    def draw_marks(self):
        """XとOのマークを描画"""
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 1:  # Xマーク
                    self.draw_x(row, col)
                elif self.board[row][col] == 2:  # Oマーク
                    self.draw_o(row, col)

    def draw_x(self, row, col):
        """Xマークを描画"""
        # セルの中心座標を計算
        center_x = col * CELL_SIZE + CELL_SIZE // 2
        center_y = row * CELL_SIZE + CELL_SIZE // 2

        # Xの左上から右下への線
        start_pos1 = (center_x - MARK_SIZE // 2, center_y - MARK_SIZE // 2)
        end_pos1 = (center_x + MARK_SIZE // 2, center_y + MARK_SIZE // 2)
        pygame.draw.line(screen, X_COLOR, start_pos1, end_pos1, MARK_WIDTH)

        # Xの右上から左下への線
        start_pos2 = (center_x + MARK_SIZE // 2, center_y - MARK_SIZE // 2)
        end_pos2 = (center_x - MARK_SIZE // 2, center_y + MARK_SIZE // 2)
        pygame.draw.line(screen, X_COLOR, start_pos2, end_pos2, MARK_WIDTH)

    def draw_o(self, row, col):
        """Oマークを描画"""
        # セルの中心座標を計算
        center_x = col * CELL_SIZE + CELL_SIZE // 2
        center_y = row * CELL_SIZE + CELL_SIZE // 2

        # 円を描画
        pygame.draw.circle(
            screen,
            O_COLOR,
            (center_x, center_y),
            MARK_SIZE // 2,
            MARK_WIDTH
        )

    def handle_click(self, pos):
        """マウスクリックを処理"""
        if self.game_over:
            return

        # クリック位置からセルの行と列を計算
        col = pos[0] // CELL_SIZE
        row = pos[1] // CELL_SIZE

        # セルが空の場合のみマークを配置
        if self.board[row][col] == 0:
            self.board[row][col] = self.current_player

            # 勝者をチェック
            if self.check_winner():
                self.game_over = True
                self.winner = self.current_player
            elif self.check_draw():
                self.game_over = True
                self.winner = 3  # ドロー
            else:
                # プレイヤーを交代
                self.current_player = 2 if self.current_player == 1 else 1

    def check_winner(self):
        """勝者をチェック"""
        # 横のラインをチェック
        for row in range(3):
            if (self.board[row][0] == self.board[row][1] == self.board[row][2] != 0):
                return True

        # 縦のラインをチェック
        for col in range(3):
            if (self.board[0][col] == self.board[1][col] == self.board[2][col] != 0):
                return True

        # 斜めのラインをチェック（左上から右下）
        if (self.board[0][0] == self.board[1][1] == self.board[2][2] != 0):
            return True

        # 斜めのラインをチェック（右上から左下）
        if (self.board[0][2] == self.board[1][1] == self.board[2][0] != 0):
            return True

        return False

    def check_draw(self):
        """ドロー（引き分け）をチェック"""
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 0:
                    return False
        return True

    def draw_game_over_message(self):
        """ゲーム終了時のメッセージを表示"""
        if self.winner == 1:
            message = "X の勝ち！"
        elif self.winner == 2:
            message = "O の勝ち！"
        else:
            message = "引き分け！"

        # メッセージの背景を描画
        text_surface = font.render(message, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))

        # 背景の矩形を描画（半透明）
        bg_rect = text_rect.inflate(40, 20)
        pygame.draw.rect(screen, (255, 255, 255), bg_rect)
        pygame.draw.rect(screen, LINE_COLOR, bg_rect, 3)

        # メッセージを描画
        screen.blit(text_surface, text_rect)

        # リスタートの案内を表示
        restart_text = small_font.render("スペースキーでもう一度", True, TEXT_COLOR)
        restart_rect = restart_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + 60))
        screen.blit(restart_text, restart_rect)

    def reset_game(self):
        """ゲームをリセット"""
        self.board = [[0 for _ in range(3)] for _ in range(3)]
        self.current_player = 1
        self.game_over = False
        self.winner = 0

    def run(self):
        """ゲームのメインループ"""
        clock = pygame.time.Clock()
        running = True

        while running:
            # イベント処理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左クリック
                        self.handle_click(pygame.mouse.get_pos())
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.game_over:
                        self.reset_game()

            # 画面をクリア
            screen.fill(BACKGROUND_COLOR)

            # ゲーム要素を描画
            self.draw_grid()
            self.draw_marks()

            # ゲーム終了時のメッセージを表示
            if self.game_over:
                self.draw_game_over_message()

            # 画面を更新
            pygame.display.flip()
            clock.tick(60)  # 60 FPS

        # Pygameを終了
        pygame.quit()
        sys.exit()


def main():
    """メイン関数"""
    game = TicTacToe()
    game.run()


if __name__ == "__main__":
    main()
