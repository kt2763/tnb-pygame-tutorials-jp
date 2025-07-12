# Pygameライブラリとその他の必要なモジュールをインポート
import pygame  # ゲーム開発用のライブラリ
import random  # ランダムな数値を生成するため
import math    # 数学的な計算（角度計算など）のため
import sys     # システム情報（OS判定など）のため

# ゲームウィンドウの設定
WINDOW_WIDTH = 800   # ウィンドウの横幅（ピクセル）
WINDOW_HEIGHT = 600  # ウィンドウの縦幅（ピクセル）
FPS = 60            # 1秒間に画面を更新する回数（フレームレート）

# 色の定義（RGB形式：赤、緑、青の値を0〜255で指定）
BLACK = (0, 0, 0)        # 黒色
WHITE = (255, 255, 255)  # 白色

# パドル（ラケット）の設定
PADDLE_WIDTH = 15    # パドルの幅
PADDLE_HEIGHT = 100  # パドルの高さ
PADDLE_SPEED = 5     # パドルの移動速度

# ボールの設定
BALL_SIZE = 15   # ボールのサイズ（正方形の一辺）
BALL_SPEED = 7   # ボールの初期速度

# スコアとゲーム設定
SCORE_FONT_SIZE = 50  # スコア表示のフォントサイズ
WIN_SCORE = 5         # 勝利に必要な得点

# フォントの設定
FONT_PATH = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
if sys.platform == "win32":
    FONT_PATH = "C:/Windows/Fonts/meiryo.ttc"
else:
    FONT_PATH = "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"


# パドル（プレイヤーが操作するラケット）のクラス
class Paddle:
    # パドルを作成する初期化メソッド
    def __init__(self, x, y):
        # pygame.Rectで四角形を作成（x座標, y座標, 幅, 高さ）
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED  # パドルの移動速度
        self.score = 0             # プレイヤーのスコア

    # パドルを上に移動するメソッド
    def move_up(self):
        # パドルの上端が画面の上端（0）より下にある場合のみ移動
        if self.rect.top > 0:
            self.rect.y -= self.speed  # y座標を減らす（上に移動）

    # パドルを下に移動するメソッド
    def move_down(self):
        # パドルの下端が画面の下端より上にある場合のみ移動
        if self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.speed  # y座標を増やす（下に移動）

    # パドルを画面に描画するメソッド
    def draw(self, screen):
        # 白い四角形として描画（画面, 色, 四角形）
        pygame.draw.rect(screen, WHITE, self.rect)


# ボールのクラス
class Ball:
    # ボールを作成する初期化メソッド
    def __init__(self):
        # ボールを画面中央に配置
        # // は整数除算（小数点以下を切り捨て）
        self.rect = pygame.Rect(
            WINDOW_WIDTH // 2 - BALL_SIZE // 2,   # x座標（画面中央）
            WINDOW_HEIGHT // 2 - BALL_SIZE // 2,  # y座標（画面中央）
            BALL_SIZE,    # 幅
            BALL_SIZE     # 高さ
        )
        self.reset()  # ボールの初期設定を行う

    # ボールを初期位置に戻し、新しい方向に発射するメソッド
    def reset(self):
        # ボールを画面中央に配置
        self.rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        
        # ランダムな角度を生成（-45度から45度の間）
        # math.piは円周率（π）、pi/4は45度をラジアンで表現
        angle = random.uniform(-math.pi/4, math.pi/4)
        
        # 左右どちらかの方向をランダムに選択（-1:左、1:右）
        direction = random.choice([-1, 1])
        
        # 速度を計算（三角関数を使って角度から速度成分を計算）
        self.velocity_x = direction * BALL_SPEED * math.cos(angle)  # x方向の速度
        self.velocity_y = BALL_SPEED * math.sin(angle)              # y方向の速度

    # ボールを移動させるメソッド
    def move(self):
        # 現在の位置に速度を加えて移動
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # 上下の壁に当たったら跳ね返る
        if self.rect.top <= 0 or self.rect.bottom >= WINDOW_HEIGHT:
            self.velocity_y = -self.velocity_y  # y方向の速度を反転

    # パドルを画面に描画するメソッド
    def draw(self, screen):
        # 白い四角形として描画（画面, 色, 四角形）
        pygame.draw.rect(screen, WHITE, self.rect)

    # パドルとの衝突をチェックするメソッド
    def check_paddle_collision(self, paddle):
        # ボールとパドルが重なっているかチェック
        if self.rect.colliderect(paddle.rect):
            # x方向の速度を反転（跳ね返る）
            self.velocity_x = -self.velocity_x
            
            # パドルのどこに当たったかを計算（-1から1の範囲）
            # 中心より上なら負の値、下なら正の値
            relative_intersect_y = (paddle.rect.centery - self.rect.centery) / (PADDLE_HEIGHT / 2)
            # 跳ね返る角度を計算（最大45度）
            bounce_angle = relative_intersect_y * math.pi/4
            
            # 現在の速さを計算（ピタゴラスの定理）
            speed = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
            # ボールが左側か右側かで方向を決定
            direction = 1 if self.rect.centerx < WINDOW_WIDTH // 2 else -1
            # 新しい速度を計算
            self.velocity_x = direction * speed * math.cos(bounce_angle)
            self.velocity_y = speed * -math.sin(bounce_angle)
            
            # ボールがパドルにめり込まないように位置を調整
            if self.rect.centerx < WINDOW_WIDTH // 2:
                self.rect.left = paddle.rect.right  # 左パドルの場合
            else:
                self.rect.right = paddle.rect.left  # 右パドルの場合


# ゲーム全体を管理するクラス
class Game:
    # ゲームの初期化
    def __init__(self):
        pygame.init()  # Pygameを初期化
        # ゲームウィンドウを作成
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pong")  # ウィンドウのタイトル設定
        self.clock = pygame.time.Clock()     # FPS制御用のクロック
        self.font = pygame.font.Font(FONT_PATH, SCORE_FONT_SIZE)  # スコア表示用フォント
        
        # パドルを作成（左側と右側）
        self.left_paddle = Paddle(50, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.right_paddle = Paddle(
            WINDOW_WIDTH - 50 - PADDLE_WIDTH,  # 右端から50ピクセル内側
            WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2  # 縦方向の中央
        )
        self.ball = Ball()  # ボールを作成
        
        # ゲーム状態の管理変数
        self.running = True      # ゲームが実行中かどうか
        self.game_over = False   # ゲームオーバーかどうか
        self.winner = None       # 勝者（なし/左プレイヤー/右プレイヤー）

    # イベント（キー入力など）を処理するメソッド
    def handle_events(self):
        # すべてのイベントを順番に処理
        for event in pygame.event.get():
            # ウィンドウの×ボタンが押された場合
            if event.type == pygame.QUIT:
                self.running = False
            # キーが押された場合
            elif event.type == pygame.KEYDOWN:
                # ESCキーで終了
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # スペースキーでゲームオーバー後に再スタート
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()

    # ゲームの状態を更新するメソッド（毎フレーム実行）
    def update(self):
        # ゲームオーバーの場合は何もしない
        if self.game_over:
            return

        # 現在押されているキーを取得
        keys = pygame.key.get_pressed()
        
        # 左パドルの操作（W:上、S:下）
        if keys[pygame.K_w]:
            self.left_paddle.move_up()
        if keys[pygame.K_s]:
            self.left_paddle.move_down()
        
        # 右パドルの操作（矢印キー上:上、矢印キー下:下）
        if keys[pygame.K_UP]:
            self.right_paddle.move_up()
        if keys[pygame.K_DOWN]:
            self.right_paddle.move_down()

        # ボールを移動
        self.ball.move()
        # パドルとの衝突をチェック
        self.ball.check_paddle_collision(self.left_paddle)
        self.ball.check_paddle_collision(self.right_paddle)

        # ボールが左側の壁を越えた場合（右プレイヤーの得点）
        if self.ball.rect.left <= 0:
            self.right_paddle.score += 1  # 右プレイヤーに1点追加
            self.check_win()              # 勝利条件をチェック
            if not self.game_over:
                self.ball.reset()         # ゲーム継続ならボールをリセット
        # ボールが右側の壁を越えた場合（左プレイヤーの得点）
        elif self.ball.rect.right >= WINDOW_WIDTH:
            self.left_paddle.score += 1   # 左プレイヤーに1点追加
            self.check_win()              # 勝利条件をチェック
            if not self.game_over:
                self.ball.reset()         # ゲーム継続ならボールをリセット

    # 勝利条件をチェックするメソッド
    def check_win(self):
        # 左プレイヤーが勝利スコアに達した場合
        if self.left_paddle.score >= WIN_SCORE:
            self.game_over = True
            self.winner = "左プレイヤー"
        # 右プレイヤーが勝利スコアに達した場合
        elif self.right_paddle.score >= WIN_SCORE:
            self.game_over = True
            self.winner = "右プレイヤー"

    # ゲームをリセットするメソッド
    def reset_game(self):
        self.left_paddle.score = 0   # 左プレイヤーのスコアを0に
        self.right_paddle.score = 0  # 右プレイヤーのスコアを0に
        self.ball.reset()            # ボールを初期位置に戻す
        self.game_over = False       # ゲームオーバー状態を解除
        self.winner = None           # 勝者をクリア

    # 画面を描画するメソッド
    def draw(self):
        # 画面を黒で塗りつぶす
        self.screen.fill(BLACK)
        
        # 中央の点線を描画
        for y in range(0, WINDOW_HEIGHT, 20):  # 20ピクセル間隔で繰り返し
            pygame.draw.rect(
                self.screen, WHITE,
                (WINDOW_WIDTH // 2 - 2, y, 4, 10)  # 中央に幅4、高さ10の四角形
            )
        
        # パドルとボールを描画
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        
        # スコアのテキストを作成
        left_score_text = self.font.render(
            str(self.left_paddle.score), True, WHITE  # 数値を文字列に変換
        )
        right_score_text = self.font.render(
            str(self.right_paddle.score), True, WHITE
        )
        
        # スコアを画面に表示（左側のスコア）
        self.screen.blit(
            left_score_text,
            (WINDOW_WIDTH // 4 - left_score_text.get_width() // 2, 50)
        )
        # スコアを画面に表示（右側のスコア）
        self.screen.blit(
            right_score_text,
            (3 * WINDOW_WIDTH // 4 - right_score_text.get_width() // 2, 50)
        )
        
        # ゲームオーバー時のメッセージ表示
        if self.game_over:
            # 勝利メッセージ
            win_text = self.font.render(f"{self.winner}の勝利！", True, WHITE)
            # 再スタートの案内
            restart_text = pygame.font.Font(FONT_PATH, 30).render(
                "スペースキーで再スタート", True, WHITE
            )
            
            # メッセージを画面中央に表示
            self.screen.blit(
                win_text,
                (WINDOW_WIDTH // 2 - win_text.get_width() // 2, WINDOW_HEIGHT // 2 - 50)
            )
            self.screen.blit(
                restart_text,
                (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT // 2 + 20)
            )
        
        # 画面を更新（描画した内容を実際に表示）
        pygame.display.flip()

    # ゲームのメインループ
    def run(self):
        # runningがTrueの間、ゲームを続ける
        while self.running:
            self.handle_events()  # イベント処理
            self.update()         # ゲーム状態の更新
            self.draw()           # 画面の描画
            self.clock.tick(FPS)  # FPSに合わせて処理速度を調整
        
        pygame.quit()  # ゲーム終了時にPygameを終了


# メイン関数（プログラムの開始点）
def main():
    game = Game()  # ゲームのインスタンスを作成
    game.run()     # ゲームを実行


# このファイルが直接実行された場合にmain関数を呼び出す
# （他のファイルからインポートされた場合は実行されない）
if __name__ == "__main__":
    main()