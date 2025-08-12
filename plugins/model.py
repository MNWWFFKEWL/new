import os


def connect(api_key: str | None = None) -> str:
    """Return an API key for connecting to OpenAI.

    The function first checks the ``api_key`` parameter. If it is ``None``,
    ``OPENAI_API_KEY`` in the environment is used when available. The
    parameter also supports ``env:VAR`` indirection, in which case the value of
    the environment variable ``VAR`` is looked up.

    Parameters
    ----------
    api_key:
        Direct API key value or ``env:VAR`` indirection. If omitted, the
        ``OPENAI_API_KEY`` environment variable is consulted.

    Returns
    -------
    str
        The API key that should be used when talking to OpenAI.
    """

    # If no API key was passed, fall back to the environment variable.
    if api_key is None:
        env_key = os.environ.get("OPENAI_API_KEY")
        if env_key:
            return env_key
        raise ValueError("No OpenAI API key provided and OPENAI_API_KEY is not set")

    # Support ``env:VAR`` indirection for explicit configuration.
    if api_key.startswith("env:"):
        env_name = api_key.split(":", 1)[1]
        env_key = os.environ.get(env_name)
        if env_key:
            return env_key
        raise ValueError(f"Environment variable '{env_name}' is not set")

    return api_key
