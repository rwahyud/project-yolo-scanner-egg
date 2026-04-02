#!/usr/bin/env python3
"""
Egg Counting - Real-Time Static Mode
Hitung telur yang terlihat di frame
"""

import numpy as np
import cv2
import sys

print("\n" + "="*60)
print("  EGG COUNTING - REAL-TIME")
print("="*60 + "\n")

print("📹 Starting camera...")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Cannot open camera!")
    sys.exit(1)

print("✓ Camera ready")
print("📊 Tunjukkan telur ke kamera | Tekan Q untuk quit\n")

frame_count = 0

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        
        # Resize untuk processing lebih cepat
        frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_AREA)
        h, w = frame.shape[:2]
        display_frame = frame.copy()
        
        # Build color mask for egg-like tones (orange/brown) with wider tolerance.
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_hsv = np.array([5, 15, 60])
        upper_hsv = np.array([35, 220, 255])
        color_mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_OPEN, kernel)
        color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_CLOSE, kernel)

        # Circle detection is more stable for counting visible eggs in a static image.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (9, 9), 1.5)

        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=35,
            param1=120,
            param2=20,
            minRadius=18,
            maxRadius=95,
        )

        valid_circles = []

        if circles is not None:
            circles = np.round(circles[0, :]).astype(int)

            for cx, cy, radius in circles:
                if radius <= 0:
                    continue
                if cx < 0 or cy < 0 or cx >= w or cy >= h:
                    continue

                # Validate with color mask around center area.
                y0 = max(cy - radius // 3, 0)
                y1 = min(cy + radius // 3, h)
                x0 = max(cx - radius // 3, 0)
                x1 = min(cx + radius // 3, w)
                roi = color_mask[y0:y1, x0:x1]
                if roi.size == 0:
                    continue

                color_ratio = float(np.count_nonzero(roi)) / float(roi.size)
                if color_ratio < 0.12:
                    continue

                # Merge near-duplicate circles.
                duplicate = False
                for ex, ey, er in valid_circles:
                    dist = np.hypot(cx - ex, cy - ey)
                    if dist < min(radius, er) * 0.65:
                        duplicate = True
                        break

                if duplicate:
                    continue

                valid_circles.append((cx, cy, radius))

        egg_count = len(valid_circles)

        for cx, cy, radius in valid_circles:
            cv2.circle(display_frame, (cx, cy), radius, (0, 255, 0), 2)
            cv2.circle(display_frame, (cx, cy), 3, (255, 0, 0), -1)
        
        # Display counter - BIG and BOLD
        cv2.rectangle(display_frame, (10, 10), (w-10, 130), (0, 0, 0), -1)
        cv2.rectangle(display_frame, (10, 10), (w-10, 130), (0, 255, 0), 3)
        
        # Counter text - centered dan BESAR
        counter_text = str(egg_count)  # Just the number
        font = cv2.FONT_HERSHEY_DUPLEX
        font_scale = 4.0  # VERY LARGE
        thickness = 4
        text_size = cv2.getTextSize(counter_text, font, font_scale, thickness)[0]
        text_x = (w - text_size[0]) // 2
        text_y = 100
        
        cv2.putText(display_frame, counter_text, (text_x, text_y), font, 
                   font_scale, (0, 255, 0), thickness)
        
        # Info
        cv2.putText(display_frame, f"Frame: {frame_count}", (10, h-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(display_frame, "[Q=Quit]", (w-120, h-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # Show
        cv2.imshow("Egg Counting - Real-Time", display_frame)
        
        # Keyboard
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('Q'):
            print(f"\n✓ Exit")
            break

except KeyboardInterrupt:
    print("\n⚠ Interrupted")

finally:
    print("Closing...")
    cap.release()
    cv2.destroyAllWindows()
    print("✓ Done!")
