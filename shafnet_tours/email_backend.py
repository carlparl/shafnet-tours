import os
import json
from email.utils import parseaddr
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend


class BrevoAPIError(Exception):
    """Raised when Brevo rejects a transactional email request."""


def _address(value):
    name, email = parseaddr(value or "")
    if not email:
        return None

    result = {"email": email}
    if name:
        result["name"] = name
    return result


def _address_list(values):
    return [item for value in values or [] if (item := _address(value))]


class BrevoAPIEmailBackend(BaseEmailBackend):
    """Send Django email messages through Brevo's HTTPS API."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_key = os.getenv("BREVO_API_KEY", "").strip()
        self.api_url = getattr(
            settings,
            "BREVO_API_URL",
            "https://api.brevo.com/v3/smtp/email",
        )
        self.timeout = getattr(settings, "BREVO_TIMEOUT", 15)

    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        if not self.api_key:
            if self.fail_silently:
                return 0
            raise BrevoAPIError("BREVO_API_KEY is not configured.")

        sent = 0
        for message in email_messages:
            try:
                if self._send_message(message):
                    sent += 1
            except Exception:
                if not self.fail_silently:
                    raise
        return sent

    def _send_message(self, message):
        recipients = _address_list(message.to)
        if not recipients:
            return False

        sender = _address(message.from_email or settings.DEFAULT_FROM_EMAIL)
        if not sender:
            raise BrevoAPIError("DEFAULT_FROM_EMAIL is not a valid email address.")

        payload = {
            "sender": sender,
            "to": recipients,
            "subject": message.subject,
            "textContent": message.body or "",
            "tags": ["shafnet-transactional"],
        }

        cc = _address_list(message.cc)
        bcc = _address_list(message.bcc)
        reply_to = _address_list(message.reply_to)
        if cc:
            payload["cc"] = cc
        if bcc:
            payload["bcc"] = bcc
        if reply_to:
            payload["replyTo"] = reply_to[0]

        for alternative in getattr(message, "alternatives", ()):
            if hasattr(alternative, "content"):
                content = alternative.content
                mimetype = alternative.mimetype
            else:
                content, mimetype = alternative
            if mimetype == "text/html":
                payload["htmlContent"] = content
                break

        request = Request(
            self.api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "accept": "application/json",
                "api-key": self.api_key,
                "content-type": "application/json",
            },
            method="POST",
        )

        try:
            response = urlopen(request, timeout=self.timeout)
            status_code = getattr(response, "status", None)
            if status_code is None:
                status_code = response.getcode()
            response.close()
        except HTTPError as error:
            status_code = error.code
        except URLError as error:
            raise BrevoAPIError("Could not connect to the Brevo API.") from error

        if status_code != 201:
            raise BrevoAPIError(
                "Brevo rejected the email request "
                f"with HTTP status {status_code}."
            )
        return True
