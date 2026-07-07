import base64

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def get_gmail_service(credentials: Credentials):

    return build(
        "gmail",
        "v1",
        credentials=credentials,
        cache_discovery=False,
    )


def list_messages(
    credentials: Credentials,
    query: str | None = None,
    max_results: int = 10,
):

    service = get_gmail_service(credentials)

    request = (
        service.users()
        .messages()
        .list(
            userId="me",
            q=query,
            maxResults=max_results,
        )
    )

    response = request.execute()

    return response.get("messages", [])


def get_message(
    credentials: Credentials,
    message_id: str,
):

    service = get_gmail_service(credentials)

    message = (
        service.users()
        .messages()
        .get(
            userId="me",
            id=message_id,
            format="full",
        )
        .execute()
    )

    return parse_message(message)


def parse_message(message):

    payload = message.get("payload", {})

    headers = payload.get("headers", [])

    email = {
        "id": message.get("id"),
        "thread_id": message.get("threadId"),
        "labels": message.get("labelIds", []),
        "snippet": message.get("snippet"),
        "from": get_header(headers, "From"),
        "to": get_header(headers, "To"),
        "subject": get_header(headers, "Subject"),
        "date": get_header(headers, "Date"),
        "body": extract_body(payload),
    }

    return email


def get_header(headers, name):

    for header in headers:

        if header["name"].lower() == name.lower():
            return header["value"]

    return None


def extract_body(payload):

    #
    # Single-part email
    #
    if payload.get("body", {}).get("data"):
        return decode_base64(
            payload["body"]["data"]
        )

    #
    # Multipart email
    #
    if "parts" in payload:

        #
        # Prefer text/plain
        #
        for part in payload["parts"]:

            if part.get("mimeType") == "text/plain":

                data = (
                    part.get("body", {})
                    .get("data")
                )

                if data:
                    return decode_base64(data)

        #
        # Fallback to HTML
        #
        for part in payload["parts"]:

            if part.get("mimeType") == "text/html":

                data = (
                    part.get("body", {})
                    .get("data")
                )

                if data:
                    return decode_base64(data)

    return ""


def decode_base64(data: str):

    data += "=" * (-len(data) % 4)

    return (
        base64.urlsafe_b64decode(data)
        .decode(
            "utf-8",
            errors="ignore",
        )
    )
