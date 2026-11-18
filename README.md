# AI Water Management

Detects water leaks from flow data and controls a tank pump safely.

> **Status:** concept prototype. It runs on simulated data and has not been deployed or tested with real hardware or real-world data.

## What it is
A Python tool with two parts: a leak detector that studies night-time water flow, and a tank controller that switches a pump on at a low level and off when the tank is full. It builds on my Automatic Motor Cutoff System.

## Why I made it
Hidden leaks waste a lot of water, and pumps that run on after a tank is full waste water and electricity.

## Who it is for
Households, apartment buildings, and small utilities, and students learning anomaly detection on sensor data.

## How it was made
1. Flow is simulated hourly with a daily usage pattern and noise. From day 6 a constant 40 L/h leak is added.
2. At 2-4 am usage is near zero, so the lowest flow of that window is the leak signal.
3. The first four days set a baseline (mean and standard deviation). A day is flagged when its night minimum has a z-score above 3.
4. `TankController` uses hysteresis: pump on at 20% or below, off at 95% or above, so it does not switch rapidly.

## Languages and tools
Python 3 (standard library only). Tests with pytest.

## Run it
```bash
python water_monitor.py
```

Example output:
```text
Night minimum flow (L/h) per day: [0.7, 1.1, 1.0, 1.6, 1.0, 41.1, 40.2, 40.0]
LEAK ALERT day 6: night flow 41.1 L/h (z-score 79.9)
```

Run the tests with `pip install pytest` and then `pytest`.

## Limitations
Simulated data only. The detector finds steady leaks, not small ones or bursts, and the water level and flow sensors are not connected.

## Future work
Add real flow and level sensors (ESP32 or Arduino), per-appliance usage learning, SMS or app alerts, and a time-series model.

## Author
Sakthivel. Computer Science and Engineering, Lovely Professional University.

## License
MIT. See [LICENSE](LICENSE).
