from google_auth_oauthlib.flow import InstalledAppFlow

def get_refresh_token(client_credentials_path):

    # scope
    scopes = ['https://www.googleapis.com/auth/drive']

    # flow to start local server
    flow = InstalledAppFlow.from_client_secrets_file(client_credentials_path, scopes=scopes)
    credentials = flow.run_local_server(port=0)

    # get token
    refresh_token = credentials.refresh_token

    # write to file
    with open('refresh_token.txt', 'w') as f:
        f.write(refresh_token)

    # yield to also return token?

if __name__ == "__main__":
    client_credentials_path = 'credentials.json'
    get_refresh_token(client_credentials_path)
