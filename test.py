import json
from SecretsManager import create_token_from_code, create_secret, refresh_channel_secret

if __name__ == "__main__":
    response = create_token_from_code('tv67nk96eh7qwdqk6mekexrb4bc4h6')
    response = create_secret('shepbot/wv_shep', json.dumps(response), 'Access token for wv_shep')
    print(response)
