from dataclasses import dataclass, field
from urllib.parse import parse_qs, urljoin, urlparse

import requests

from lms_sfu import config

_BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) "
        "Gecko/20100101 Firefox/131.0"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
}


@dataclass
class MarkResult:
    ok: bool
    status_code: int
    body_preview: str
    final_url: str = ""
    redirects: list[str] = field(default_factory=list)
    error: str = ""


def parse_attendance_url(url: str) -> tuple[str, str]:
    """
    Достаёт qrpass и sessid из ссылки LMS attendance.

    Пример:
    https://lms.sfedu.ru/mod/attendance/attendance.php?qrpass=xxx&sessid=123
    """
    text = (url or "").strip().strip('"').strip("'")
    if not text:
        raise ValueError("Пустая ссылка")

    parsed = urlparse(text)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("Невалидная ссылка: нужен полный URL (http/https)")

    path = parsed.path.rstrip("/")
    if not path.endswith("/mod/attendance/attendance.php"):
        raise ValueError(
            "Невалидная ссылка: ожидается .../mod/attendance/attendance.php"
        )

    query = parse_qs(parsed.query)
    qrpass_values = query.get("qrpass") or []
    sessid_values = query.get("sessid") or []

    qrpass = (qrpass_values[0] if qrpass_values else "").strip()
    sessid = (sessid_values[0] if sessid_values else "").strip()

    if not qrpass:
        raise ValueError("В ссылке нет параметра qrpass")
    if not sessid:
        raise ValueError("В ссылке нет параметра sessid")
    if not sessid.isdigit():
        raise ValueError(f"Невалидный sessid: {sessid!r}")

    return qrpass, sessid


def _looks_like_login(url: str) -> bool:
    path = urlparse(url).path.lower()
    return "/login" in path


def mark_lesson(
    moodle_session: str,
    qrpass: str,
    sessid: str,
    base_url: str | None = None,
    max_redirects: int = 10,
) -> MarkResult:
    """Отмечает посещение по QR. Не падает на redirect loop — возвращает дебаг."""
    if not moodle_session or not moodle_session.strip():
        return MarkResult(
            ok=False,
            status_code=0,
            body_preview="",
            error="MOODLE_SESSION пустой",
        )

    base = (base_url or config.LMS_BASE_URL).rstrip("/")
    host = urlparse(base).hostname or "lms.sfedu.ru"
    start_url = f"{base}/mod/attendance/attendance.php"
    params = {"qrpass": qrpass, "sessid": sessid}

    http = requests.Session()
    http.headers.update(_BROWSER_HEADERS)
    http.cookies.set("MoodleSession", moodle_session.strip(), domain=host, path="/")

    redirects: list[str] = []
    url = start_url
    use_params = params

    try:
        for _ in range(max_redirects):
            response = http.get(url, params=use_params, allow_redirects=False, timeout=30)
            use_params = None

            if response.is_redirect or response.status_code in (301, 302, 303, 307, 308):
                location = response.headers.get("Location", "")
                if not location:
                    body = response.text or ""
                    return MarkResult(
                        ok=False,
                        status_code=response.status_code,
                        body_preview=body[:100],
                        final_url=response.url,
                        redirects=redirects,
                        error="Редирект без Location",
                    )

                next_url = urljoin(response.url, location)
                redirects.append(f"{response.status_code} -> {next_url}")

                if _looks_like_login(next_url):
                    return MarkResult(
                        ok=False,
                        status_code=response.status_code,
                        body_preview="",
                        final_url=next_url,
                        redirects=redirects,
                        error="Редирект на login — скорее всего протух MOODLE_SESSION",
                    )

                url = next_url
                continue

            body = response.text or ""
            login_hint = _looks_like_login(response.url)
            return MarkResult(
                ok=response.status_code == 200 and not login_hint,
                status_code=response.status_code,
                body_preview=body[:100],
                final_url=response.url,
                redirects=redirects,
                error="Похоже на страницу логина" if login_hint else "",
            )

        return MarkResult(
            ok=False,
            status_code=0,
            body_preview="",
            final_url=url,
            redirects=redirects,
            error=f"Слишком много редиректов (>{max_redirects})",
        )
    except requests.RequestException as exc:
        return MarkResult(
            ok=False,
            status_code=0,
            body_preview="",
            redirects=redirects,
            error=str(exc),
        )


def mark_lessons_for_users(
    users: dict[str, str],
    qrpass: str,
    sessid: str,
) -> dict[str, MarkResult]:
    """
    users: mapping имя_пользователя -> MoodleSession cookie.
    """
    return {
        user: mark_lesson(session, qrpass, sessid)
        for user, session in users.items()
    }
