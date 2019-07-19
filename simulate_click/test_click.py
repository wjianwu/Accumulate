import win32gui
import win32con
import win32api
import time


def get_position():
    print(win32api.GetCursorPos())


def move_position(p):
    win32api.SetCursorPos((p[0], p[1]))


def left_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def right_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)


get_position()
move_position([1535, 1067])
left_click()
time.sleep(1)
move_position([-1307, 525])
left_click()
