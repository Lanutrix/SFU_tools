import requests

from lms_sfu import config


def mark_lesson(
    moodle_session: str,
    qrpass: str,
    sessid: str,
    base_url: str | None = None,
) -> bool:
    """Отмечает посещение по QR. Возвращает True при HTTP 200."""
    url = f"{(base_url or config.LMS_BASE_URL).rstrip('/')}/mod/attendance/attendance.php"
    response = requests.get(
        url,
        params={"qrpass": qrpass, "sessid": sessid},
        cookies={"MoodleSession": moodle_session},
    )
    return response.status_code == 200


def mark_lessons_for_users(
    users: dict[str, str],
    qrpass: str,
    sessid: str,
) -> dict[str, bool]:
    """
    users: mapping имя_пользователя -> MoodleSession cookie.
    """
    results: dict[str, bool] = {}
    for user, session in users.items():
        results[user] = mark_lesson(session, qrpass, sessid)
    return results
