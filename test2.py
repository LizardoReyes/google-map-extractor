import time
import requests
from datetime import datetime, timezone
import uuid
import random

def truquito():
    url = "https://mobile-api.datacamp.com/graphql"

    # Principal
    bearer_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJneUZvOVJGU21lTUIzcGZRNk1oMkhFa182dksySDYxR05tbF9aSENZZzdnIn0.eyJleHAiOjE3NTg1ODAxODcsImlhdCI6MTc1MDgwNDE4NywiYXV0aF90aW1lIjoxNzUwODA0MTg3LCJqdGkiOiJkMTYyZGNiNS02MjFjLTRiNTctOGQ4Ny03Yjk4MjEyMDYyOTIiLCJpc3MiOiJodHRwczovL2F1dGguZGF0YWNhbXAuY29tL3JlYWxtcy9kYXRhY2FtcC11c2VycyIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiJhNDE0NDEwYS01YzEzLTQ4MDMtOTVhNi1hOTY1NmY5ZmExMGIiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJEQjJEMkI1Ri1ERUM4LTQyMjUtQkNBQS0xRDM0NTA0RDg2OTYiLCJzaWQiOiJhYmMzMDUyMC1mZTNmLTRmOGYtYWE3YS0wMThmYTk1ZTlmN2YiLCJhY3IiOiIxIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLWRhdGFjYW1wLXVzZXJzIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgZW1haWwgZGMtdXNlci1pZCBwcm9maWxlIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInVzZXJfaWQiOjE3NjIwNjAwLCJuYW1lIjoiTGl6YXJkbyBSZXllcyIsInByZWZlcnJlZF91c2VybmFtZSI6ImNpYmVydXRpbGlkYWRlc0BnbWFpbC5jb20iLCJpZGVudGl0eV9wcm92aWRlcl9hbGlhcyI6Imdvb2dsZSIsImdpdmVuX25hbWUiOiJMaXphcmRvIiwiZmFtaWx5X25hbWUiOiJSZXllcyIsImVtYWlsIjoiY2liZXJ1dGlsaWRhZGVzQGdtYWlsLmNvbSJ9.iqhxmXMr30Zy08cFdEbLCw5oWGXZET5wmJP4eSn1iqV-uuBa4LF__f-lG2wJRsK_RgWsoG7cAFHOrDM6PjKvZZ-fl-NkOJ70NAZyw8Q3DhrtuDhIsEeFCW21SuqbEPA8hzCi7ZCSBwpi1lPei7nHbz2T5Ll4dBGXlF8HSZDBdIroH5vU6ZnuJLDJADn8SUrpS-Gsbx64JssYj61HuxmAs0LrHD03NP_5EHCtG1iisrYmc1Znrq3W9s5XbnVwZagU9VN834FBAoqBdjpsjuyDv8mRYdAkeKJqpt4uZrbM9nhyJ0FP6lLaS1Ibq_OCa0geCPp8Gw0Ni1VO77zXATQGRQ"
    # Secundaria
    #bearer_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJneUZvOVJGU21lTUIzcGZRNk1oMkhFa182dksySDYxR05tbF9aSENZZzdnIn0.eyJleHAiOjE3NjE0Mjk3NTQsImlhdCI6MTc1MzY1Mzc1NSwiYXV0aF90aW1lIjoxNzUzNjUzNzU0LCJqdGkiOiIxMTE1MDMwYy05OTE2LTRhNDctYWRmMy0wZWY3MzM4ZjkyY2UiLCJpc3MiOiJodHRwczovL2F1dGguZGF0YWNhbXAuY29tL3JlYWxtcy9kYXRhY2FtcC11c2VycyIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiI2OWQ4OWE3MS00ZTdlLTQ1NDgtYWQzNy00MzhmNWQwMmY5NzEiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJEQjJEMkI1Ri1ERUM4LTQyMjUtQkNBQS0xRDM0NTA0RDg2OTYiLCJzaWQiOiJmYTA5YWFjZi0wNmJhLTQ1MDktOTE1YS0wY2FlOTJhYjBlNDQiLCJhY3IiOiIxIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLWRhdGFjYW1wLXVzZXJzIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgZW1haWwgZGMtdXNlci1pZCBwcm9maWxlIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInVzZXJfaWQiOjE4MjY0Mzg0LCJuYW1lIjoiTGl6YXJkbyBSZXllcyBKYXJhIiwicHJlZmVycmVkX3VzZXJuYW1lIjoibGl6YXJkby5yZXllc0B1bm1zbS5lZHUucGUiLCJpZGVudGl0eV9wcm92aWRlcl9hbGlhcyI6Imdvb2dsZSIsImdpdmVuX25hbWUiOiJMaXphcmRvIiwiZmFtaWx5X25hbWUiOiJSZXllcyBKYXJhIiwiZW1haWwiOiJsaXphcmRvLnJleWVzQHVubXNtLmVkdS5wZSJ9.d91Z5-_J6b1nuh1IEJhuEQgFeH4HVQMSpDAcPoAzUxmC9AbJRsniPy2vlnBcWxX6IYOSiVllGIhPRL0ilftyEeolCg6XbGu2PUh58OWJm28jA6C15Cl8MBxc1NN8g9TkVAzktadasF8TpeEGjRPASjmch3jCTZKOahewX4rVOTeUgIg5Ygmc6gtoKJbup7i5yETxg3Om7JDpZK8CScNE0E-xLXp-smxGzKUDQRiM6mKSukqnydQat-XfoDC1-2dU3mm1iga9HFNpBDHIvvv-DqyhvotYtyBcQRD4vX9LD46xPZBCbiU8t-aOcuYVe0C2H74BDr3brhcz9eo-N9fzBQ"

    # Cookies
    cookies = {
    }

    # Headers personalizados
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
        "Origin": "https://practice.datacamp.com",
        "Priority": "u=1, i",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "Referer": "https://practice.datacamp.com/p/588/chapter/97077?completionRedirect=https%3A%2F%2Fcampus.datacamp.com%2Fcourses%2Fintermediate-sql%2Faggregate-functions-3%3Fex%3D1",
        "Accept-Language": "es-419,es;q=0.9,fi;q=0.8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "x-app-version": "0.0.0",
        "x-dc-lang": "es-ES",
        "x-graphql-operation-name": "syncSessions",
    }

    fecha1 = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    fecha2 = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    fecha3 = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    fecha4 = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    fecha5 = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    fecha6 = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    fecha7 = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    fecha8 = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')

    payload = {
        "operationName": "syncSessions",
        "variables": {
            "sessions": [
                {
                    "startedAt": fecha3,
                    "endedAt": fecha8,
                    "cancelled": False,
                    "workouts": [
                        {
                            "poolId": 588,
                            "version": "192bd61b9416c9003cbd48053fd5f726e4208902:669526",
                            "startedAt": fecha3,
                            "endedAt": fecha7,
                            "cancelled": False,
                            "exercises": [
                                {
                                    "viewId": 1753379,
                                    "version": "192bd61b9416c9003cbd48053fd5f726e4208902:669526",
                                    "correct": True,
                                    "answer": {
                                        "type": "SELECT_ANSWER",
                                        "options": [
                                            {
                                                "block": {
                                                    "type": "BlockPlain",
                                                    "content": "To select missing values."
                                                }
                                            },
                                            {
                                                "block": {
                                                    "type": "BlockPlain",
                                                    "content": "To exclude missing values."
                                                }
                                            },
                                            {
                                                "block": {
                                                    "type": "BlockPlain",
                                                    "content": "All options are correct."
                                                }
                                            },
                                            {
                                                "block": {
                                                    "type": "BlockPlain",
                                                    "content": "To identify missing values."
                                                }
                                            }
                                        ],
                                        "selectedOptions": [
                                            "All options are correct."
                                        ]
                                    },
                                    "startedAt": fecha3,
                                    "endedAt": fecha4,
                                    "cancelled": False,
                                    "multiplexerCodeExecutions": []
                                },
                                {
                                    "viewId": 1571968,
                                    "version": "5a8b06d392f37b52663947ba768818d7f719862a",
                                    "correct": True,
                                    "answer": {
                                        "type": "SELECT_ANSWER",
                                        "options": [
                                            {
                                                "block": {
                                                    "type": "BlockCode",
                                                    "content": "SELECT name, founding_year\nFROM companies\nWHERE founding_year <= 2013\nLIMIT 5;\n"
                                                }
                                            },
                                            {
                                                "block": {
                                                    "type": "BlockCode",
                                                    "content": "SELECT name, founding_year\nFROM companies\nWHERE founding_year > 2012\nLIMIT 5;\n"
                                                }
                                            },
                                            {
                                                "block": {
                                                    "type": "BlockCode",
                                                    "content": "SELECT name, founding_year\nFROM companies\nWHERE founding_year >= 2012\nLIMIT 5;\n"
                                                }
                                            }
                                        ],
                                        "selectedOptions": [
                                            "SELECT name, founding_year\nFROM companies\nWHERE founding_year > 2012\nLIMIT 5;\n"
                                        ]
                                    },
                                    "startedAt": fecha1,
                                    "endedAt": fecha5,
                                    "cancelled": False,
                                    "multiplexerCodeExecutions": []
                                },
                                {
                                    "viewId": 1572804,
                                    "version": "1606e405fcb358b9387b4882d9f4b4487812da58",
                                    "correct": True,
                                    "answer": {
                                        "type": "SELECT_ANSWER",
                                        "options": [
                                            {
                                                "block": {
                                                    "type": "BlockPlain",
                                                    "content": "After `FROM` and before `SELECT`."
                                                }
                                            },
                                            {
                                                "block": {
                                                    "type": "BlockPlain",
                                                    "content": "Before `FROM` and after `SELECT`."
                                                }
                                            },
                                            {
                                                "block": {
                                                    "type": "BlockPlain",
                                                    "content": "After `SELECT` and after `FROM`."
                                                }
                                            }
                                        ],
                                        "selectedOptions": [
                                            "After `FROM` and before `SELECT`."
                                        ]
                                    },
                                    "startedAt": fecha2,
                                    "endedAt": fecha6,
                                    "cancelled": False,
                                    "multiplexerCodeExecutions": []
                                }
                            ],
                            "uuid": str(uuid.uuid4()),
                            "isDailyPractice": False,
                            "chapterMainId": 97077
                        }
                    ],
                    "uuid": str(uuid.uuid4()),
                    "status": "IN_PROGRESS"
                }
            ],
            "platform": "WEB",
            "application": "PRACTICE_WEB"
        },
        "query": "mutation syncSessions($sessions: [SyncSessionInput!]!, $platform: Platform, $application: ApplicationName) {\n  syncSessions(\n    sessions: $sessions\n    platform: $platform\n    application: $application\n  ) {\n    shouldRetry\n    __typename\n  }\n}\n"
    }

    response = requests.post(url, json=payload, headers=headers, cookies=cookies)

    # Leer respuesta
    if response.ok:
        print("✅ Éxito:", response.json())
    else:
        print(f"❌ Error {response.status_code}: {response.text}")


def main():
    while True:
        try:
            truquito()
            print("✅ Truquito ejecutado correctamente.")
        except Exception as e:
            print(f"❌ Ocurrió un error: {e}")
        tiempo_espera = random.uniform(3, 5)
        print(f"Esperando {tiempo_espera:.2f} segundos...")
        time.sleep(tiempo_espera)

if __name__ == "__main__":
    main()