# log-processor

## USAGE:
requires docker. `./run` to start the containerised application. 
Spin up a separate shell to talk to the api on `localhost:8000` using a REST client i.e. `curl`.

Endpoints:
- GET `/logs/$log_id` to get a json record of the log with the id `$log_id`
- POST `/logs` with a JSON body containing the log in order to insert logs

Use helper script `test_post` to test the endpoint once the container is up and running in the separate shell - it takes a single argument, the file containing the request body.

Example:

```
./run
[+] Building 1.0s (10/10) FINISHED                                                                                                                                                                              
 => [internal] load build definition from Dockerfile                                                                                                                                                       0.0s
 => => transferring dockerfile: 32B                                                                                                                                                                        0.0s
 => [internal] load .dockerignore                                                                                                                                                                          0.0s
 => => transferring context: 2B                                                                                                                                                                            0.0s
 => [internal] load metadata for docker.io/library/python:3.11.7                                                                                                                                           0.8s
 => [1/5] FROM docker.io/library/python:3.11.7@sha256:63bec515ae23ef6b4563d29e547e81c15d80bf41eff5969cb43d034d333b63b8                                                                                     0.0s
 => [internal] load build context                                                                                                                                                                          0.0s
 => => transferring context: 15.30kB                                                                                                                                                                       0.0s
 => CACHED [2/5] WORKDIR /log-processor/                                                                                                                                                                   0.0s
 => CACHED [3/5] COPY requirements.txt ./                                                                                                                                                                  0.0s
 => CACHED [4/5] RUN pip install --no-cache-dir -r requirements.txt                                                                                                                                        0.0s
 => [5/5] COPY . .                                                                                                                                                                                         0.0s
 => exporting to image                                                                                                                                                                                     0.0s
 => => exporting layers                                                                                                                                                                                    0.0s
 => => writing image sha256:41c36cf9c8acd967fd374ac1ab074f9adadf791e322c9c3a24fd063b8f1f775e                                                                                                               0.0s
 => => naming to docker.io/library/log-processor                                                                                                                                                           0.0s
 INFO:     Started server process [1]
 INFO:     Waiting for application startup.
 INFO:     Application startup complete.
 INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

 ```

 Then in a separate shell:

 ```
 ./test_post fixtures/all_valid_mixed.json 
 HTTP/1.1 200 OK
 date: Wed, 06 Mar 2024 17:50:17 GMT
 server: uvicorn
 content-length: 73
 content-type: application/json

 [{"event_id":"u_123","success":true},{"event_id":"s_123","success":true}]
 ```

 Then test GET to see the logs
 ```
 ❯ curl -D '/dev/fd/2' 'http://localhost:8000/logs/u_123'
 HTTP/1.1 200 OK
 date: Wed, 06 Mar 2024 17:51:11 GMT
 server: uvicorn
 content-length: 157
 content-type: application/json

{"type":"user","timestamp":"2024-03-01T13:45:00.000Z","event_id":"u_123","event":{"username":"my_user","email":"my_user@email.com","operation":"read/write"}}%  
```

jq is recommended (`brew install jq` if you have homebrew) to prettify JSON outputs:

```
❯ curl -D '/dev/fd/2' 'http://localhost:8000/logs/u_123' | jq
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
Dload  Upload   Total   Spent    Left  Speed
0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0HTTP/1.1 200 OK
date: Wed, 06 Mar 2024 17:52:29 GMT
server: uvicorn
content-length: 157
content-type: application/json

100   157  100   157    0     0   6115      0 --:--:-- --:--:-- --:--:--  6280
{
    "type": "user",
        "timestamp": "2024-03-01T13:45:00.000Z",
        "event_id": "u_123",
        "event": {
            "username": "my_user",
            "email": "my_user@email.com",
            "operation": "read/write"
        }
}
```
## TODO:
- `pydantic.dataclass` models to handle converting between log objects in app and json as well as log validations ala https://docs.pydantic.dev/latest/concepts/dataclasses/ and https://docs.pydantic.dev/latest/concepts/validators/.
- type hints missing.
- expand testing by adding negative cases, assert on exception messages when expecting an exception and use actual log objects.
- Include test runs before spinning up the api.
- svc.py:43-49 seem a bit rough - expecting a keyError exception as a guard to continue operation.
- is `dict.get("key")` quicker or cleaner than `dict["key"]`?
- better exception handling all around.
- upper and lower cases strings in validations.
- should the POST endpoint return 200 always as opposed to, say 201?
- don't just copy everything into the container, reduce the size and time to build.




