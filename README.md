# 📧 CYE Backend Challenge - Email Server

In this task, you will use Python, [FastAPI], and [SQLite3] to create an email
microservice. Your API present a JSON interface to let us create, read,
update, and destroy email objects in a local database.

<!-- MarkdownTOC autolink="true" style="ordered" -->

1. [Email Schema](#email-schema)
1. [API Specification](#api-specification)
    1. [GET `/emails`](#get-emails)
    1. [POST `/emails`](#post-emails)
    1. [GET `/emails/{id:int}`](#get-emailsidint)
    1. [PATCH `/emails/{id:int}`](#patch-emailsidint)
    1. [DELETE `/emails/{id:int}`](#delete-emailsidint)
1. [Environment Setup](#environment-setup)
1. [Testing](#testing)
1. [Helpful Literature](#helpful-literature)
1. [Optional: Bonus Tasks](#optional-bonus-tasks)

<!-- /MarkdownTOC -->

## Email Schema

Emails are represented with the following properties:

- `id` (integer, read-only)
    - Automatically-selected unique identifier for the email.
- `body` (string)
    - Email message.
- `subject` (string, max 50 chars)
    - Email subject consisting of up to 50 characters.
- `sender` (string)
    - Sender's email address.
- `recipient` (string)
    - Recipient's email address.
- `has_attachments` (bool)
    - Whether this email has attachments.
- `created` (datetime, read-only)
    - Automatically-set time at which this email was created. When
      representing as JSON, use any well-known string format (the output of
      `str`, illustrated below, is fine).

Here is an example as JSON.

```json
{
    "id": 1,
    "body": "Good luck!",
    "subject": "CYE Interview Challenge",
    "sender": "johndoe@umass.edu",
    "recipient": "you@umass.edu",
    "has_attachments": true,
    "created": "2021-03-15 14:31:32.733388"
}
```

See the [starter code](./main.py) for an example as a Python `dict`.

## API Specification

You will need to implement the following endpoints in your API. Implementation
details are mostly up to you, but make sure to consider [status codes] for
both success and error cases. Make sure you document your choices!

Your API should use a local SQLite database called `email.db`. We
recommend using the [Python `sqlite3` module][sqlite3]. It handles the
connection and lets you write queries without external dependencies. The
documentation shows you everything you need to know.

##### GET `/emails`

Get an array of all emails in the database.

##### POST `/emails`

Create one new email with given info, auto-assign it an ID, and save it to the
database. Remember to set the `created` time.

##### GET `/emails/{id:int}`

Get the email from the database with primary key `id`. Note that `{id:int}` is
a placeholder for an integer value. GET `/email/1` would try to get the email
with ID 1.

##### PATCH `/emails/{id:int}`

Update writable fields on the email with the given ID. A request to this
endpoint might look like this. The endpoint would update the fields specified
in the body.

```json
{
    "sender": "janedoe@umass.edu",
    "has_attachments": false
}
```

##### DELETE `/emails/{id:int}`

Delete the email with the given ID.

## Environment Setup

You will need a recent (3.7+) version of Python for this challenge. The
starter code uses [Pipenv] for dependency and script management. The following
should be enough to set up and enter a development environment:

```sh
$ pip install pipenv
$ pipenv install --dev
$ pipenv shell
```

When it comes time to start the server, use the following command:

```sh
$ pipenv run start
```

## Testing

The `tests/` directory contains a sample [PyTest] test. You are free and
encouraged to add more tests.

Run the tests using:

```sh
$ pipenv run test
```

## Helpful Literature

- [FastAPI basics](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [FastAPI request body tutorial](https://fastapi.tiangolo.com/tutorial/body/)
- [Pydantic (FastAPI validation library) docs][pydantic]
- [`sqlite3` module][sqlite3]
- [`async`/`await` in Python][async]
- [HTTP statuses][status codes]

## Optional: Bonus Tasks

If you are interested in our tech stack, feel free to explore any of the
following tasks. Not doing these tasks will not have any adverse effects on
your submission. The tasks are listed roughly in order of difficulty.

- Disallow newline (`\n`) characters in the `subject` field.
- Add email format validation for the `sender` and `recipient` fields.
- Use SQLAlchemy instead of directly using the SQLite3 module.
- Sort the result of GET `/emails` by created date (newest first).
- Add the following query parameters to GET `/emails`:
    - `/emails?sender=X`: Emails sent by `X`.
    - `/emails?recipient=X`: Emails received by `X`.
    - `/emails?before=X`: Emails created before date `X`.

[async]: https://fastapi.tiangolo.com/async/#in-a-hurry
[fastapi]: https://pypi.org/project/fastapi/
[pydantic]: https://pydantic-docs.helpmanual.io/
[status codes]: https://httpstatuses.com/
[pipenv]: https://pipenv.pypa.io/en/latest/
[pytest]: https://docs.pytest.org/en/stable/
[sqlite3]: https://docs.python.org/3/library/sqlite3.html
