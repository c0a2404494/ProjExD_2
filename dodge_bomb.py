import os
import math
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {  # 移動量辞書
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：横方向，縦方向の画面内外判定結果
    画面内ならTrue，画面外ならFalse
    """
    yoko, tate = True, True  # 初期値：画面内
    if rct.left < 0 or WIDTH < rct.right:  # 横方向の画面外判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: # 縦方向の画面外判定
        tate = False
    return yoko, tate  # 横方向，縦方向の画面内判定結果を返す


def gameover(screen: pg.Surface) -> None:
    """
    1. 画面をブラックアウトし，
    2. 泣いているこうかとん画像と
    3. 「Game Over」の文字列を
    4. 5秒間表示させ，
    5. display.update()する
    """
    blackout = pg.Surface((WIDTH, HEIGHT))
    blackout.set_alpha(200)
    pg.draw.rect(blackout, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    screen.blit(blackout, (0, 0))

    sad_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    sad_rct_left = sad_img.get_rect(center=(WIDTH // 2 - 250, HEIGHT // 2))
    sad_rct_right = sad_img.get_rect(center=(WIDTH // 2 + 250, HEIGHT // 2))
    screen.blit(sad_img, sad_rct_left)
    screen.blit(sad_img, sad_rct_right)

    font = pg.font.SysFont(None, 100)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rct = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rct)

    pg.display.update()

    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    無限に拡大，加速するのはおかしいので，10段階程度の大きさ，
    加速度を準備する
    """
    bb_accs = [a for a in range(1,11)]
    bb_imgs = []
    for i in range(1, 11):
        bb_img = pg.Surface((20*i, 20*i))
        bb_img.set_colorkey((0, 0, 0))
        pg.draw.circle(bb_img, (255, 0, 0), (10*i, 10*i), 10*i)
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs




def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    sum_mv = (0, 0)
    kk_rct.center = 300, 200
 
    bb_img = pg.Surface((20, 20))  # 空のSurfaceを作る（爆弾用）
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤い円を描く
    bb_img.set_colorkey((0, 0, 0))  # 黒を透明色に設定
    bb_rct = bb_img.get_rect()  # 爆弾Rectを取得
    bb_rct.centerx = random.randint(0, WIDTH)  # 横座標用の乱数
    bb_rct.centery = random.randint(0, HEIGHT)  # 縦座標用の乱数
    bb_imgs, bb_accs = init_bb_imgs()
    vx, vy = +5, +5  # 爆弾の移動速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return
        
        bb_imgs, bb_accs = init_bb_imgs()
        avx = vx*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]

        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
       
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 移動をなかったことにする
        screen.blit(kk_img, kk_rct)
        idx = min(tmr // 500, 9)
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]
        bb_img = bb_imgs[idx]
        bb_rct = bb_img.get_rect(center=bb_rct.center)
        bb_rct.move_ip(avx, avy)  # 爆弾の移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *= -1
        if not tate:  # 縦方向にはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)  # 爆弾の描画
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()