import pygame

pygame.init()  # Pygameの初期化
screen = pygame.display.set_mode((400, 500))  # 画面サイズの設定
pygame.display.set_caption("Pygameで描画してみる")  # ウィンドウのタイトルを設定

running = True  # ゲームループの開始
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # 画面を白で塗りつぶす
    pygame.display.flip()  # 画面の更新

pygame.quit()  # Pygameの終了処理
