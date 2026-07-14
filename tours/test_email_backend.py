import json
from unittest.mock import Mock, patch

from django.core.mail import send_mail
from django.test import SimpleTestCase, override_settings

from shafnet_tours import email_backend


@override_settings(
    EMAIL_BACKEND="shafnet_tours.email_backend.BrevoAPIEmailBackend",
    BREVO_API_URL="https://api.brevo.com/v3/smtp/email",
    BREVO_TIMEOUT=15,
    DEFAULT_FROM_EMAIL="Shafnet Tours <verified@example.com>",
)
class BrevoEmailBackendTests(SimpleTestCase):
    @patch.dict("os.environ", {"BREVO_API_KEY": "test-api-key"})
    @patch.object(email_backend, "urlopen")
    def test_sends_django_email_through_brevo_api(self, urlopen):
        urlopen.return_value = Mock(status=201)

        result = send_mail(
            subject="Booking received",
            message="Your booking request was received.",
            from_email="Shafnet Tours <verified@example.com>",
            recipient_list=["traveller@example.com"],
        )

        self.assertEqual(result, 1)
        urlopen.assert_called_once()
        request = urlopen.call_args.args[0]
        payload = json.loads(request.data.decode("utf-8"))
        self.assertEqual(
            request.get_header("Api-key"),
            "test-api-key",
        )
        self.assertEqual(
            payload["to"],
            [{"email": "traveller@example.com"}],
        )
        self.assertEqual(
            payload["sender"],
            {"name": "Shafnet Tours", "email": "verified@example.com"},
        )
        self.assertEqual(urlopen.call_args.kwargs["timeout"], 15)
