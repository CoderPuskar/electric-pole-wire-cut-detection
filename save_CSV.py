import serial
import csv
import time

# === Configure your COM port ===
COM_PORT = "COM8"   # Change to your actual port (e.g., COM4, COM5…)
BAUD_RATE = 115200  # Must match Serial.begin() in Arduino code

FILENAME = "wire_data_uncut.csv"

# Open CSV file for writing
with open(FILENAME, mode="a", newline="") as file:
    writer = csv.writer(file)

    # Write header if file is empty
    if file.tell() == 0:
        writer.writerow(["esp_id", "vibration", "x", "y", "z", "label"])

    # Open serial connection
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # wait for Arduino/ESP to reset

    print("Collecting UNCUT (not cut) wire data... Press Ctrl+C to stop.")

    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode("utf-8", errors="ignore").strip()
                if line:
                    # Example Arduino format:
                    # esp1,Vibration:0,X:1.23,Y:-0.54,Z:9.81
                    # esp2,Vibration:1,X:2.34,Y:0.76,Z:8.91

                    parts = line.split(",")
                    if len(parts) >= 5:
                        esp_id = parts[0]
                        vib = parts[1].split(":")[1].strip()
                        x = parts[2].split(":")[1].strip()
                        y = parts[3].split(":")[1].strip()
                        z = parts[4].split(":")[1].strip()

                        # Label = 0 (uncut wire)
                        writer.writerow([esp_id, vib, x, y, z, 0])
                        print(f"{esp_id} => V:{vib}, X:{x}, Y:{y}, Z:{z}, Label:0")

    except KeyboardInterrupt:
        print("\nStopped data collection.")
        ser.close()
