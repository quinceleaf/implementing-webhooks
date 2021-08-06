# implementing-webhooks
Implementing webhook(s) in django
## Use Case

- External partner sends us messages via webhook
- Messages are delivered via POST requests with JSON payload to provided endpoint
- Partner includes identifying token to be used to authenticate requests


## Process

- Verify request
- Process payload as necessary
- Store incoming message for use in debugging & future auditing
- Cull out-of-date messages
- Reply with success response


## Structure

- Store JSON messages using `JSONField`
- Store time received, to permit ordering and culling of out-of-date messages


## Points of Note

- For webhook, request is verified with token, so can disable CSRF for POST request
- View receiving webhook is non-transactional, as there are (2) steps to process (receiving & processing), and best practice to keep the storage of message (for debugging) in separate transaction from business logic processing
- Store token in `.env` for security and load into `settings.WEBHOOK_TOKEN` at runtime
- Using `secrets.compare_digest()` to verify request token due to issues discussed in linked resources
- Messages are retained only for range of days specified in `settings.WEBHOOK_MESSAGE_RETENTION_TIME`
- URL path for webhook includes random string sequence, which helps guard against URL enumeration attacks from discovering endpoint


## Resources

- [Adam Johnson: How to Build a Webhook Receiver in Django](https://adamj.eu/tech/2021/05/09/how-to-build-a-webhook-receiver-in-django/)
- [Adam Johnson: Tweet thread](https://twitter.com/fapolloner/status/1391302758578458624)
- [Coda Hale: A Lesson In Timing Attacks (or, Don’t use MessageDigest.isEquals)](https://codahale.com/a-lesson-in-timing-attacks/)