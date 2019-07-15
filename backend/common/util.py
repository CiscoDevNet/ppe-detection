import os
import time


def ensure_dir(_dir):
    if not os.path.exists(_dir):
        os.mkdir(_dir)


def current_timestamp_ms():
    return int(time.time() * 1000)


def get_duration(start_at):
    return time.time() - start_at


def get_duration_us(start_at):
    return round(get_duration(start_at) * 1000000)
