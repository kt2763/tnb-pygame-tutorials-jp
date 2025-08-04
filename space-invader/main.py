import sys

import pygame

# Pygameの初期化
pygame.init()

# 画面サイズの設定
SCREEN_WIDTH = 800  # 画面の幅
SCREEN_HEIGHT = 600  # 画面の高さ

# 色の定義（RGB値）
BLACK = (0, 0, 0)  # 黒色
WHITE = (255, 255, 255)  # 白色
GREEN = (0, 255, 0)  # 緑色
RED = (255, 0, 0)  # 赤色

# プレイヤー（自機）の設定
PLAYER_WIDTH = 50  # プレイヤーの幅
PLAYER_HEIGHT = 30  # プレイヤーの高さ
PLAYER_SPEED = 5  # プレイヤーの移動速度

# 弾の設定
BULLET_WIDTH = 5  # 弾の幅
BULLET_HEIGHT = 10  # 弾の高さ
BULLET_SPEED = 7  # 弾の速度

# 敵（インベーダー）の設定
ENEMY_WIDTH = 40  # 敵の幅
ENEMY_HEIGHT = 30  # 敵の高さ
ENEMY_SPEED = 1  # 敵の移動速度
ENEMY_ROWS = 5  # 敵の行数
ENEMY_COLS = 10  # 敵の列数


class Player:
    """プレイヤー（自機）のクラス"""

    def __init__(self):
        self.x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2  # 画面中央に配置
        self.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10  # 画面下部に配置
        self.bullets = []  # 弾のリスト

    def move_left(self):
        """左に移動"""
        if self.x > 0:
            self.x -= PLAYER_SPEED

    def move_right(self):
        """右に移動"""
        if self.x < SCREEN_WIDTH - PLAYER_WIDTH:
            self.x += PLAYER_SPEED

    def shoot(self):
        """弾を発射"""
        bullet_x = self.x + PLAYER_WIDTH // 2 - BULLET_WIDTH // 2
        bullet_y = self.y
        self.bullets.append([bullet_x, bullet_y])

    def update_bullets(self):
        """弾の位置を更新"""
        for bullet in self.bullets[:]:  # コピーを作って安全に削除
            bullet[1] -= BULLET_SPEED  # 弾を上に移動
            if bullet[1] < 0:  # 画面外に出たら削除
                self.bullets.remove(bullet)

    def draw(self, screen):
        """プレイヤーと弾を描画"""
        # プレイヤーを緑色の四角形で描画
        pygame.draw.rect(screen, GREEN, (self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT))

        # 弾を白色の四角形で描画
        for bullet in self.bullets:
            pygame.draw.rect(
                screen, WHITE, (bullet[0], bullet[1], BULLET_WIDTH, BULLET_HEIGHT)
            )


class Enemy:
    """敵（インベーダー）のクラス"""

    def __init__(self):
        self.enemies = []  # 敵のリスト
        self.direction = 1  # 移動方向（1: 右, -1: 左）

        # 敵を格子状に配置
        for row in range(ENEMY_ROWS):
            for col in range(ENEMY_COLS):
                x = col * (ENEMY_WIDTH + 10) + 50  # 敵のx座標
                y = row * (ENEMY_HEIGHT + 10) + 50  # 敵のy座標
                self.enemies.append([x, y])

    def update(self):
        """敵の位置を更新"""
        # 端に到達したかチェック
        move_down = False
        for enemy in self.enemies:
            if enemy[0] <= 0 or enemy[0] >= SCREEN_WIDTH - ENEMY_WIDTH:
                move_down = True
                break

        # 端に到達した場合は下に移動して方向転換
        if move_down:
            self.direction *= -1
            for enemy in self.enemies:
                enemy[1] += 20  # 下に移動

        # 左右に移動
        for enemy in self.enemies:
            enemy[0] += self.direction * ENEMY_SPEED

    def draw(self, screen):
        """敵を描画"""
        for enemy in self.enemies:
            pygame.draw.rect(
                screen, RED, (enemy[0], enemy[1], ENEMY_WIDTH, ENEMY_HEIGHT)
            )


def check_collisions(player, enemies):
    """弾と敵の衝突判定"""
    for bullet in player.bullets[:]:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], BULLET_WIDTH, BULLET_HEIGHT)

        for enemy in enemies.enemies[:]:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], ENEMY_WIDTH, ENEMY_HEIGHT)

            # 弾と敵が衝突した場合
            if bullet_rect.colliderect(enemy_rect):
                player.bullets.remove(bullet)  # 弾を削除
                enemies.enemies.remove(enemy)  # 敵を削除
                break


def main():
    """メイン関数"""
    # 画面を作成
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("スペースインベーダー")

    # 時計オブジェクト（FPS制御用）
    clock = pygame.time.Clock()

    # ゲームオブジェクトを作成
    player = Player()  # プレイヤーを作成
    enemies = Enemy()  # 敵を作成

    # ゲームループ
    running = True
    while running:
        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # ウィンドウを閉じる
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # スペースキーで弾を発射
                    player.shoot()

        # キーボード入力の処理
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  # 左矢印キーで左に移動
            player.move_left()
        if keys[pygame.K_RIGHT]:  # 右矢印キーで右に移動
            player.move_right()

        # ゲームオブジェクトの更新
        player.update_bullets()  # 弾の位置を更新
        enemies.update()  # 敵の位置を更新
        check_collisions(player, enemies)  # 衝突判定

        # 画面を黒色でクリア
        screen.fill(BLACK)

        # ゲームオブジェクトを描画
        player.draw(screen)  # プレイヤーを描画
        enemies.draw(screen)  # 敵を描画

        # 画面を更新
        pygame.display.flip()

        # FPSを60に制限
        clock.tick(60)

        # 全ての敵を倒した場合
        if not enemies.enemies:
            print("おめでとう！全ての敵を倒しました！")
            running = False

    # Pygameを終了
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
