# Local development

## Pre-commit prerequisite

We want to have standard formatting and not think about it at all. pre-commit hook allows you to code without thinking of code style

- Install `pre-commit` by running `pip install pre-commit`
- run `pre-commit install`

## Local environment

Locally we use Docker to easily get going.

Running `docker-compose up` will setup the following containers:
- `django-app` on port `8000`
- `nextjs-app` on port `3000`
- `postgres` on port `5432`
- `minio-s3` on port `9000/9001`
  - `minio` is used only in development to mimic the use of S3
  - production does **not** use `minio`


# Issues

We recommend creating an issue before a PR in the following cases
- bug spoted
- feedback
- feature request

It's easier to discuss, align on an approach and then implement the changes. Of course, we welcome PRs and the discussion can be had there if code can better further the discussion.
