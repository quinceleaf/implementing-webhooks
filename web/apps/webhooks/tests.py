from django.conf import settings
from django.test import Client, override_settings, TestCase
from django.urls import reverse
from django.utils import timezone


import datetime as dt
from http import HTTPStatus
import random


from apps.webhooks import models


TOKEN_FOR_TESTS = "Gym0nlxpjcjyjwd9es1htjzyrga-l7y90yobkhj866oyfq6ftbnfnt0d-dqzm&ri309c97g2ao91fxgcnz352m6jqqt5mukhx7yvu-smb58xakhcdrli7"


@override_settings(WEBHOOK_TOKEN=TOKEN_FOR_TESTS)
class WebhookTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.endpoint = reverse("apps.webhooks:webhook-partners")

    def test_bad_method(self):
        response = self.client.get(self.endpoint)

        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_missing_token(self):
        response = self.client.post(
            self.endpoint,
        )

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.content.decode() == "Incorrect token in Webhook-Token header"

    def test_bad_token(self):
        false_token = "8bp3sh88d7bm6b9oamkjpt19ci9pgsx7gidj"
        response = self.client.post(
            self.endpoint,
            HTTP_WEBHOOK_TOKEN=false_token,
        )

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.content.decode() == "Incorrect token in Webhook-Token header"

    def test_success(self):
        start = timezone.now()
        outdated_message = models.WebhookMessage.objects.create(
            received_at=start
            - dt.timedelta(
                days=settings.WEBHOOK_MESSAGE_RETENTION_TIME + random.randint(3, 5)
            ),
        )

        true_token = settings.WEBHOOK_TOKEN
        response = self.client.post(
            self.endpoint,
            HTTP_WEBHOOK_TOKEN=true_token,
            content_type="application/json",
            data={"content": "This is a random, sample message"},
        )

        assert response.status_code == HTTPStatus.OK
        assert response.content.decode() == "Message received successfully"
        assert not WebhookMessage.objects.filter(id=outdated_message.id).exists()

        webhook_message = WebhookMessage.objects.get()
        assert webhook_message.received_at >= start
        assert webhook_message.payload == {
            "content": "This is a random, sample message"
        }
