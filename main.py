import cbpro


auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)
# Use the sandbox API (requires a different set of API access credentials)
auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase,
                                  api_url="https://api-public.sandbox.pro.coinbase.com")
