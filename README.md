# TNB Pygame Tutorials(日本語版)

このリポジトリはPythonのゲーム開発用ライブラリであるPygameのチュートリアルをまとめたものです。  
ゲーム内で使っている画像などは @kt2763 (たなべ)の作ったものですが、著作権は主張していません。ご自由に改変等してご利用ください。  
※その際、特にこちらに伝達する必要はありません。

## 公開ステータス

| 英名 | 日本語名 | ステータス | README |
|------|---------|----------|--------|
| Tetris | テトリス | 開発済み | [tetris/README.md](tetris/README.md) |
| Pong | ポン | 開発済み | [pong/README.md](pong/README.md) |
| Tic-Tac-Toe | 三目並べ（3×3） | 開発済み | [tic-tac-toe/README.md](tic-tac-toe/README.md) |
| Snake | スネーク | 開発予定 |
| Breakout/Arkanoid | ブレイクアウト/アルカノイド | 開発予定 |
| Space Invaders | スペースインベーダー | 開発予定 |
| Flappy Bird Clone | Flappy Bird クローン | 開発予定 |
| Match-3 | マッチ3（Bejeweled 型） | 開発予定 |
| Pac-Man Lite | パックマン ライト | 開発予定 |
| Asteroids | アステロイド | 開発予定 |
| 2D Platformer | 2D プラットフォーマー（1 ステージ） | 開発予定 |
| Simple Roguelike | シンプル・ローグライク | 開発予定 |
| Frogger | フロッガー | 開発予定 |
| Bomberman Lite | ボンバーマン ライト | 開発予定 |
| Angry Birds Style Slingshot | Angry Birds風スリングショット | 開発予定 |
| Pinball Mini | ピンボール ミニ | 開発予定 |
| Minesweeper | マインスイーパー | 開発予定 |
| 2048 | 2048 | 開発予定 |
| Endless Runner | エンドレスランナー | 開発予定 |
| Top-Down Shooter | トップダウンシューター | 開発予定 |
| Minimal Tower Defense | ミニマルタワーディフェンス | 開発予定 |
| Multiplayer Pong | マルチプレイ ポン | 開発予定 |

## 日本語フォントの設定

Pygameでデフォルトのフォントがたいてい日本語対応していないので、日本語を表示したい場合は別途指定する必要があります。

各ゲームでは、以下のようにプラットフォームに応じて適切な日本語フォントを自動選択するように設定されています：

```python
# フォントの設定
FONT_PATH = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
if sys.platform == "win32":
    FONT_PATH = "C:/Windows/Fonts/meiryo.ttc"
else:
    FONT_PATH = "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc"
```

### Ubuntuの場合

```shell
sudo apt -y install fontconfig
```
