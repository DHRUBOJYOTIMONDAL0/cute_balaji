import os
import cv2
import numpy as np
import random
import math

script_dir = os.path.dirname(os.path.abspath(__file__))
INPUT_IMAGE = os.path.join(script_dir, 'balaji.png')

CANVAS_W, CANVAS_H = 1920, 1200  
FPS = 60
WINDOW_NAME = "Cute balaji Reveal"
FULLSCREEN = True

REVEAL_SECONDS = 8.0     
CROSSFADE_SECONDS = 4.0  
HOLD_SECONDS = 8.0       

SPARKLE_COUNT = 150 

def load_and_fit_with_blur(path, w, h):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {path}")

    ih, iw = img.shape[:2]
    
    scale_cover = max(w / iw, h / ih)
    cover_w, cover_h = int(iw * scale_cover), int(ih * scale_cover)
    cover_img = cv2.resize(img, (cover_w, cover_h), interpolation=cv2.INTER_LINEAR)
    
    cx_off = (cover_w - w) // 2
    cy_off = (cover_h - h) // 2
    bg = cover_img[cy_off:cy_off+h, cx_off:cx_off+w]
    
    bg = cv2.GaussianBlur(bg, (99, 99), 0)
    bg = cv2.convertScaleAbs(bg, alpha=0.35, beta=0) 
    
    scale_fit = min(w / iw, h / ih)
    new_w, new_h = int(iw * scale_fit), int(ih * scale_fit)
    resized_center = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    base_img = bg.copy()
    x_off = (w - new_w) // 2
    y_off = (h - new_h) // 2
    base_img[y_off:y_off + new_h, x_off:x_off + new_w] = resized_center
    
    return bg, base_img, resized_center, x_off, y_off, new_w

def get_skeleton_pixels(core_img, x_off, y_off):
    gray = cv2.cvtColor(core_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 5, 50, 50)
    edges = cv2.Canny(gray, 60, 140)
    
    edges[:, :2] = 0
    edges[:, -2:] = 0
    edges[:2, :] = 0
    edges[-2:, :] = 0
    
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=lambda c: cv2.arcLength(c, False), reverse=True)
    
    xs, ys = [], []
    for c in contours:
        for pt in c:
            xs.append(pt[0][0] + x_off)
            ys.append(pt[0][1] + y_off)
            
    return np.array(xs), np.array(ys)

def init_particles(count, h, left_bound, right_bound, max_w):
    particles = []
    for _ in range(count):
        if random.random() < 0.5 and left_bound > 0:
            x = random.randint(0, left_bound + 10)
        else:
            x = random.randint(right_bound - 10, max_w)
            
        particles.append({
            'x': x,
            'y': random.randint(0, h),
            'speed': random.uniform(1.0, 3.5),
            'size': random.randint(2, 4),
            'color': (random.randint(20, 60), random.randint(160, 210), 255)
        })
    return particles

def update_and_draw_particles(frame, particles, h, left_bound, right_bound, max_w):
    for p in particles:
        p['y'] += p['speed']
        
        if p['y'] - p['size'] > h:
            p['y'] = random.randint(-40, -10)
            if random.random() < 0.5 and left_bound > 0:
                p['x'] = random.randint(0, left_bound + 10)
            else:
                p['x'] = random.randint(right_bound - 10, max_w)
                
        cv2.circle(frame, (int(p['x']), int(p['y'])), p['size'] + 3, (p['color'][0]//4, p['color'][1]//4, p['color'][2]//4), -1, cv2.LINE_AA)
        cv2.circle(frame, (int(p['x']), int(p['y'])), p['size'], p['color'], -1, cv2.LINE_AA)

def show_frame(frame, delay_ms):
    cv2.imshow(WINDOW_NAME, frame)
    key = cv2.waitKey(delay_ms) & 0xFF
    return key != ord("q") and key != 27

def main():
    try:
        bg, base_img, core_img, x_off, y_off, center_w = load_and_fit_with_blur(INPUT_IMAGE, CANVAS_W, CANVAS_H)
    except FileNotFoundError as e:
        print(e)
        return

    delay_ms = max(1, int(1000 / FPS))

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    if FULLSCREEN:
        cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
    cv2.imshow(WINDOW_NAME, bg)
    cv2.waitKey(40)

    xs, ys = get_skeleton_pixels(core_img, x_off, y_off)
    total_pixels = len(xs)

    particles = init_particles(SPARKLE_COUNT, CANVAS_H, x_off, x_off + center_w, CANVAS_W)
    skeleton_layer = np.zeros_like(base_img)
    
    reveal_frames = max(1, int(REVEAL_SECONDS * FPS))
    idx = 0
    
    for i in range(reveal_frames):
        target = int((i + 1) * (total_pixels / reveal_frames))
        
        if target > idx:
            skeleton_layer[ys[idx:target], xs[idx:target]] = (150, 220, 255)
            idx = target
            
        glow = cv2.GaussianBlur(skeleton_layer, (3, 3), 0)
        glowing_skeleton = cv2.addWeighted(skeleton_layer, 0.8, glow, 1.0, 0)
        
        frame_composite = cv2.add(bg, glowing_skeleton)
        update_and_draw_particles(frame_composite, particles, CANVAS_H, x_off, x_off + center_w, CANVAS_W)
        
        if not show_frame(frame_composite, delay_ms): return

    crossfade_frames = max(1, int(CROSSFADE_SECONDS * FPS))
    for i in range(crossfade_frames):
        t = (i + 1) / crossfade_frames
        blended = cv2.addWeighted(frame_composite, 1 - t, base_img, t, 0)
        
        update_and_draw_particles(blended, particles, CANVAS_H, x_off, x_off + center_w, CANVAS_W)
        if not show_frame(blended, delay_ms): return

    hold_frames = max(1, int(HOLD_SECONDS * FPS))
    for _ in range(hold_frames):
        final_frame = base_img.copy()
        update_and_draw_particles(final_frame, particles, CANVAS_H, x_off, x_off + center_w, CANVAS_W)
        if not show_frame(final_frame, delay_ms): return

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()