import anthropic
import dotenv
import argparse
import os


def construct_apikey():
    """construct .env file for loading api_key and base_url

    Returns:
        bool: whether .env file has been successfully created
    """
    file_path = ".env"
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            pass
        return construct_apikey()
    else:
        print(f".env file has been created in {os.path.abspath(file_path)}")
        return True


def load_apikey():
    """load anthropic api_key and base_url

    Raises:
        ValueError: invalid anthropic api_key settings

    Returns:
        str, str: api_key and base_url
    """
    dotenv.load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    base_url = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")

    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")
    return api_key, base_url


def test_apikey():
    """test whether the api_key is valid during a small query

    Returns:
        bool: whether the test pass or fail
    """
    try:
        api_key, base_url = load_apikey()
    except ValueError as e:
        print(f"Error loading API key: {e}")
        return False

    client = anthropic.Anthropic(base_url=base_url, api_key=api_key)
    try:
        # a test message
        message = client.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, Claude",
                }
            ],
            model="claude-3-opus-20240229",
        )
        print("API call successful!")
        print(f"Claude's response: {message.content}")
        return True

    except anthropic.APIError as e:
        print(f"Anthropic API Error: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add arguments for constructing files")
    parser.add_argument(
        "--mode", type=str, default="default", help="load api-key and base-url"
    )

    args = parser.parse_args()

    if args.mode == "construct":
        construct_apikey()

    elif args.mode == "debug":
        test_apikey()

    elif args.mode == "default":
        print("No mode selected, testing...")
        try:
            assert construct_apikey() is True
            assert test_apikey() is True
            print("All tests passed!😊, enjoy your MCP world!")
        except Exception as e:
            print(f"Test failed, {e}")

    else:
        print("Some error occured, invalid mode selected")
