import pygame

pygame.init()  # Pygameの初期化
screen = pygame.display.set_mode((400, 500))  # 画面サイズの設定
pygame.display.set_caption("Pygameでイベント処理をしてみる")

x, y = 175, 225  # 四角形の位置
width, height = 50, 50  # 四角形の大きさ
velocity = 5  # 四角形の移動速度

running = True  # ゲームループ
while running:
    pygame.time.delay(50)  # ゲームのスピードを調整

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()  # キー入力の処理

    if keys[pygame.K_LEFT]:
        x -= velocity
    if keys[pygame.K_RIGHT]:
        x += velocity
    if keys[pygame.K_UP]:
        y -= velocity
    if keys[pygame.K_DOWN]:
        y += velocity

    screen.fill((255, 255, 255))  # 画面を白でクリア
    pygame.draw.rect(screen, (0, 0, 255), (x, y, width, height))  # 四角形を描画
    pygame.display.update()  # 描画内容を画面に反映

pygame.quit()
