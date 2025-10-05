# put python doc here
"""
This script demonstrates how to perform a token exchange using the gpsoauth library.
It exchanges an OAuth token for a master token and then uses the master token to obtain
an authentication token for a specific Google service.
See https://github.com/simon-weber/gpsoauth?tab=readme-ov-file#alternative-flow

Pour récupérer l'AndroidID à partir d'un virtual device Android, vous pouvez utiliser les commandes suivantes avec adb (Android Debug Bridge) :
`adb shell settings get secure android_id`
`adb -s emulator-5554 shell settings get secure android_id`
"""

import gpsoauth

EMAIL = "contact@nicolasmura.fr"
ANDROID_ID = '56be6dfbf1d43206'
OAUTH_TOKEN = 'oauth2_4/0AVGzR1CyUaOF-liG_Bpvi9gybiKhFkD0ElF_WLheFwG3vutoWy1SEZliu0SRGKGcAgI20w'

master_response = gpsoauth.exchange_token(EMAIL, OAUTH_TOKEN, ANDROID_ID)
# if there's no token check the response for more details
master_token = master_response['Token']

auth_response = gpsoauth.perform_oauth(
    EMAIL, master_token, ANDROID_ID,
    service='sj', app='com.google.android.music',
    client_sig='...')
token = auth_response['Auth']
print("Master token:", master_token)
print("Service token:", token)
