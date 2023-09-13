description = '''
**WebSockets description**

**Incoming events:**
1. **connect**
    - **Description:**
        The `connect` event is triggered when a client attempts to establish a WebSocket connection. The event verifies the client's authentication by inspecting the connection environment details. A successful verification allows the connection, whereas a failure sends an error to the client.
    - **Parameters:**
        - **sid**: A unique session identifier representing the connecting client.
        - **environ**: A dictionary containing the connection's environment details, which are used for verifying the client's authentication.
    - **Behavior:**
        1. Calls the `verify_socket_connection` function with the `environ` parameter to validate the client's credentials.
        2. If verification is successful, the connection is established.
        3. In case of verification failure, an error message (`{'detail': 'Invalid token'}`) is sent to the client and the connection attempt is denied.
    - **Usage:**
        - `await sio.connect(endpoint, {'Authorization': your_api_key})`

2. **chat**
    - **Description:**
        The `chat` event is designed for real-time message sending and handling via WebSocket. Upon receiving a message from a client, this event accepts the message data, converts it into the MessageBase model, and subsequently processes the message through the message-handling service.
    - **Parameters:**
        - **sid**: A unique session identifier for the client that has sent the message.
        - **data**: An object containing message details. The data is expected to match the `MessageBase` model.
    - **Behavior:**
        1. Receives data from the client.
        2. Converts the data into the MessageBase model using the `message_pydantic_to_sqlalchemy` function.
        3. Passes the converted message for processing through the `message_service`.
    - **`MessageBase` Model:**
        - **id**: A unique string identifier for the message.
        - **text**: The content of the message.
        - **user_id**: A string representing the user who sent the message.
        - **source**: A string indicating the origin or source of the message.
        - **related_message_id**: (Optional) A string identifier for a related message if any.
        - **created_at**: A timestamp indicating when the message was created.
        - **channel_id**: A string indicating the channel or room where the message was sent.
        
**Outgoing events:**

1. **new_token**
    - **Description:**
        The `new_token` event emits a portion of a GPT-generated answer, known as a token, to the client. It's useful for real-time incremental updates while generating an extensive GPT response.
    - **Data:**
        - **message_id**: The identifier of the temporary answer message.
        - **token**: A chunk or segment of the GPT-generated answer.
    - **Behavior:**
        Whenever a new token of a GPT answer is available, it is sent to the client using this event.

2. **message_end**
    - **Description:**
        The `message_end` event notifies the client when the token generation for a particular message has been completed.
    - **Data:**
        - **ended_message_id**: The identifier of the message for which token generation has been completed.
    - **Behavior:**
        When the GPT response is fully generated and all tokens have been sent, this event is triggered to indicate completion for a particular message.

3. **gpt_error**
    - **Description:**
        The `gpt_error` event is used to notify the client if there was an error during the OpenAI GPT request process.
    - **Data:**
        - **message_id**: The identifier of the temporary answer message.
        - **error**: A description of the encountered error.
    - **Behavior:**
        If there's any error while processing the GPT request, this event is triggered to notify the client about the error and provide a description.

4. **error**
    - **Description:**
        The `error` event is a general-purpose event to communicate any other kind of error encountered in the WebSocket communication process to the client.
    - **Data:**
        - **data**: A dictionary containing error details.
    - **Behavior:**
        This event is used to emit any error-related information, especially if it's not specific to GPT processing.


'''
