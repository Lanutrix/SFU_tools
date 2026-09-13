import requests
import config


USERS = {
    "user1": config.MOODLE_SESSION,
    "user2": config.MOODLE_SESSION,
}

def mark_lesson(users, qrpass, sessid):
    for user in users:
        cookies = {
            'MoodleSession': USERS[user],
        }

        params = {
            'qrpass': qrpass,
            'sessid': sessid,
        }

        response = requests.get('https://lms.sfedu.ru/mod/attendance/attendance.php', params=params, cookies=cookies)
        if response.status_code == 200:
            print(f"Lesson marked for {user}")
        else:
            print(f"Failed to mark lesson for {user}")

if __name__ == "__main__":
    mark_lesson(USERS, "fdsd1c", "39645")