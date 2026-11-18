"""Water monitoring: night-flow leak detection and a tank pump controller.

Leak idea: at 2-4 am almost nobody uses water, so the lowest flow of the night
should be near zero. A rise in that minimum over several days suggests a leak.
"""
import random
import statistics


def simulate_flow(days=8, leak_from_day=5, leak_lph=40, seed=11):
    """Hourly flow in litres/hour for each day (list of 24 values)."""
    rng = random.Random(seed)
    usage = [2, 1, 1, 1, 3, 20, 60, 80, 50, 30, 25, 30, 45, 30, 20, 20, 30, 50, 70, 60, 40, 25, 10, 4]
    out = []
    for d in range(days):
        day = [max(0.0, u + rng.gauss(0, u * 0.1 + 0.5)) for u in usage]
        if d >= leak_from_day:
            day = [v + leak_lph for v in day]   # constant leak adds to every hour
        out.append(day)
    return out


def night_minimum(day):
    return min(day[2:5])   # hours 02:00-04:59


def detect_leak(days, baseline_days=4, z_limit=3.0):
    base = [night_minimum(d) for d in days[:baseline_days]]
    mean, std = statistics.mean(base), max(statistics.pstdev(base), 0.5)
    alerts = []
    for i, d in enumerate(days[baseline_days:], start=baseline_days):
        z = (night_minimum(d) - mean) / std
        if z > z_limit:
            alerts.append((i + 1, round(night_minimum(d), 1), round(z, 1)))
    return alerts


class TankController:
    """Pump on below `low` %, off above `high` % (hysteresis avoids rapid cycling)."""

    def __init__(self, low=20, high=95):
        self.low, self.high, self.pump_on = low, high, False

    def update(self, level_percent):
        if level_percent >= self.high:
            self.pump_on = False
        elif level_percent <= self.low:
            self.pump_on = True
        return self.pump_on


if __name__ == "__main__":
    days = simulate_flow()
    print("Night minimum flow (L/h) per day:", [round(night_minimum(d), 1) for d in days])
    for day, flow, z in detect_leak(days):
        print(f"LEAK ALERT day {day}: night flow {flow} L/h (z-score {z})")
    tank, level = TankController(), 50.0
    for step in range(30):
        level += 4 if tank.pump_on else -3
        tank.update(level)
    print(f"Tank after 30 steps: {level:.0f}%, pump {'on' if tank.pump_on else 'off'}")
