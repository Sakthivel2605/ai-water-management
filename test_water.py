import water_monitor as wm


def test_leak_is_detected_only_after_it_starts():
    alerts = wm.detect_leak(wm.simulate_flow(leak_from_day=5))
    assert alerts and min(a[0] for a in alerts) == 6   # day numbers start at 1


def test_no_alert_without_leak():
    assert wm.detect_leak(wm.simulate_flow(leak_from_day=99)) == []


def test_pump_hysteresis():
    t = wm.TankController(20, 95)
    assert t.update(15) is True and t.update(60) is True and t.update(96) is False
