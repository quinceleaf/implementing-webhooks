from django.conf import settings
from django.db.transaction import atomic, non_atomic_requests
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone


import datetime as dt
import json
from secrets import compare_digest


from apps.webhooks import models


@csrf_exempt
@require_POST
@non_atomic_requests
def receive_webhook(request):
    """Verify request, store message, process payload and cull out-of-date messages"""

    # Verify request
    given_token = request.headers.get("Webhook-Token", "")

    if not compare_digest(given_token, settings.WEBHOOK_TOKEN):
        return HttpResponseForbidden(
            "Incorrect token in Webhook-Token header",
            content_type="text/plain",
        )

    # Store incoming message for use in debugging & future auditing
    payload = json.loads(request.body)
    models.WebhookMessage.objects.create(
        received_at=timezone.now(),
        payload=payload,
    )

    # Process payload
    process_webhook_payload(payload)

    # Cull out-of-date messages
    models.WebhookMessage.objects.filter(
        received_at__lte=timezone.now()
        - dt.timedelta(days=settings.WEBHOOK_MESSAGE_RETENTION_TIME)
    ).delete()

    # Reply with success response
    return HttpResponse("Message received successfully", content_type="text/plain")


@atomic
def process_webhook_payload(payload):
    # TODO: Implement business logic, if any
    pass
