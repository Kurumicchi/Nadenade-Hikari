import cv2
import numpy as np
import json


def calibrate_hsv(sample):
    mean = np.mean(sample, axis=(0, 1))
    std = np.std(sample, axis=(0, 1))

    lower_hsv = np.array([
        max(0, mean[0] - 2 * std[0]),
        max(0, mean[1] - 2 * std[1]),
        max(0, mean[2] - 2 * std[2])
    ], dtype=np.uint8)

    upper_hsv = np.array([
        min(179, mean[0] + 2 * std[0]),
        min(255, mean[1] + 2 * std[1]),
        min(255, mean[2] + 2 * std[2])
    ], dtype=np.uint8)

    return lower_hsv, upper_hsv

def save_calibration(lower_hsv, upper_hsv):
    data = {
        "lower_hsv": lower_hsv.tolist(),
        "upper_hsv": upper_hsv.tolist()
    }

    with open("calibration.json", "w") as file:
        json.dump(data, file, indent=4)

def main():
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Could not open camera.")
        return

    calibrated = False
    lower_hsv = None
    upper_hsv = None

    while True:
        success, frame = camera.read()

        if not success:
            print("Could not read camera frame.")
            break

        frame = cv2.flip(frame, 1)

        height, width = frame.shape[:2]

        box_size = 100
        x1 = (width - box_size) // 2
        y1 = (height - box_size) // 2
        x2 = x1 + box_size
        y2 = y1 + box_size

    # Draw calibration box
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "Place your hand inside the box",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        if not calibrated:
            cv2.putText(
                frame,
                "SPACE = Calibrate",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )
        else:
            cv2.putText(
                frame,
                "R = Recalibrate    Q = Quit",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )

        cv2.imshow("Nadenade Hikari - Calibration", frame)

        # Create mask after calibration
        if calibrated:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            mask = cv2.inRange(
                hsv,
                lower_hsv,
                upper_hsv
            )

            cv2.imshow("Calibrated Result", mask)

        key = cv2.waitKey(1) & 0xFF

        # SPACE = calibrate
        if key == ord(" "):
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            sample = hsv[y1:y2, x1:x2]

            lower_hsv, upper_hsv = calibrate_hsv(sample)

            save_calibration(lower_hsv, upper_hsv)
            
            calibrated = True

            print("\nCalibration complete!")
            print(f"Lower HSV: {lower_hsv}")
            print(f"Upper HSV: {upper_hsv}")

        # R = recalibrate
        elif key == ord("r"):
            calibrated = False
            lower_hsv = None
            upper_hsv = None

            cv2.destroyWindow("Calibrated Result")

            print("\nCalibration reset.")

        # Q = quit
        elif key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()