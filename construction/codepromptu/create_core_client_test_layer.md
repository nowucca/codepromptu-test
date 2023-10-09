You are a QA developer expert in Python, using the pytest framework.
You're writing tests for an API, described as:
```

### FastAPI (Version 0.1.0)

---

#### Public Endpoints:

1. **Add New Public Prompt**  
   - **Endpoint**: `POST /public/prompt/`
   - Requires admin user with basic authentication.
   - Accepts a new prompt in JSON format.
   - Responses: 201 (Successful), 422 (Validation Error).

2. **List All Public Prompts**  
   - **Endpoint**: `GET /public/prompt/`
   - Parameters: `skip` (defaults to 0), `limit` (defaults to 10).
   - Returns a list of prompts.
   - Responses: 200 (Successful), 422 (Validation Error).

3. **Delete a Public Prompt by GUID**  
   - **Endpoint**: `DELETE /public/prompt/{guid}`
   - Requires admin user with basic authentication.
   - Responses: 204 (Successful), 422 (Validation Error).

4. **Update a Public Prompt by GUID**  
   - **Endpoint**: `PUT /public/prompt/{guid}`
   - Requires admin user with basic authentication.
   - Accepts updated prompt data in JSON format.
   - Responses: 200 (Successful), 422 (Validation Error).

5. **Retrieve a Public Prompt by GUID**  
   - **Endpoint**: `GET /public/prompt/{guid}`
   - Returns specific prompt data.
   - Responses: 200 (Successful), 422 (Validation Error).

6. **Search Public Prompts**  
   - **Endpoint**: `GET /public/prompt/search/`
   - Parameters: `query` (required).
   - Returns a list of matching prompts.
   - Responses: 200 (Successful), 422 (Validation Error).

7. **List Public Prompts by Tag**  
   - **Endpoint**: `GET /public/prompt/tags/{tag}`
   - Returns prompts with a specific tag.
   - Responses: 200 (Successful), 422 (Validation Error).

8. **List Public Prompts by Classification**  
   - **Endpoint**: `GET /public/prompt/classification/{classification}`
   - Returns prompts of a specific classification.
   - Responses: 200 (Successful), 422 (Validation Error).

---

#### Private (Per-user) Endpoints:

1. **Test Login**  
   - **Endpoint**: `GET /private/login`
   - Tests login with basic authentication.
   - Response: 204 (Successful).

2. **Add New Private Prompt**  
   - **Endpoint**: `POST /private/prompt/`
   - Requires basic authentication.
   - Accepts a new prompt in JSON format.
   - Responses: 201 (Successful), 422 (Validation Error).

3. **List All Private Prompts**  
   - **Endpoint**: `GET /private/prompt/`
   - Parameters: `skip` (defaults to 0), `limit` (defaults to 10).
   - Requires basic authentication.
   - Returns a list of private prompts.
   - Responses: 200 (Successful), 422 (Validation Error).

4. **Delete a Private Prompt by GUID**  
   - **Endpoint**: `DELETE /private/prompt/{guid}`
   - Requires basic authentication.
   - Responses: 204 (Successful), 422 (Validation Error).

5. **Update a Private Prompt by GUID**  
   - **Endpoint**: `PUT /private/prompt/{guid}`
   - Requires basic authentication.
   - Accepts updated prompt data in JSON format.
   - Responses: 200 (Successful), 422 (Validation Error).

6. **Search Private Prompts**  
   - **Endpoint**: `GET /private/prompt/search`
   - Requires basic authentication.
   - Parameters: `query` (required).
   - Returns a list of matching private prompts.
   - Responses: 200 (Successful), 422 (Validation Error).

7. **List Private Prompts by Tag**  
   - **Endpoint**: `GET /private/prompt/tags?tags={tag1,tag2,...}`
   - Requires basic authentication.
   - Returns private prompts with a specific tag.
   - Responses: 200 (Successful), 422 (Validation Error).

8. **List Private Prompts by Classification**  
   - **Endpoint**: `GET /private/prompt/classification/{classification}/`
   - Requires basic authentication.
   - Returns private prompts of a specific classification.
   - Responses: 200 (Successful), 422 (Validation Error).

---


### Schemas:

---

#### 1. **Prompt**

- **Used In**: Request and response data for many endpoints related to prompts, both public and private.
  
- **Properties**:
  - `guid`: A unique identifier string for the prompt.
  - `internal_id`: An internal integer ID or null.
  - `content`: The content of the prompt as a string.
  - `input_variables`: An array of Variables (described below) for inputs.
  - `output_variables`: An array of Variables (described below) for outputs.
  - `tags`: An array of strings representing various tags associated with the prompt.
  - `classification`: A string that classifies the prompt.
  - `author`: An integer representing the author's ID.
  - `created_at`: A timestamp of when the prompt was created.
  - `updated_at`: A timestamp of the last update, or null if not updated.

#### 2. **HTTPValidationError**

- **Used In**: Error responses for validation issues (typically 422 responses).

- **Properties**:
  - `detail`: An array of ValidationError items which provide details about the validation error.
  
#### 3. **Variable**

- **Used In**: Within the `input_variables` and `output_variables` properties of the "Prompt" schema.

- **Properties**:
  - `name`: The name of the variable.
  - `description`: A description of the variable.
  - `type`: The type of the variable (e.g., string, integer).
  - `expected_format`: Expected format of the variable, defaults to "text/plain".

---

With these definitions in mind, it becomes clear that when interacting with prompt-related endpoints, the data exchanged (either sent or received) often adheres to the **Prompt** schema, which itself contains **Variable** items. On the other hand, if there are issues with the data validation (for example, missing required fields, incorrect data types), the response will likely adhere to the **HTTPValidationError** schema.

```

The architecture of the test cases is three layers:
1. Core client layer (folder=client) 
2. Test user session layer (folder=session)
3. Test Case layer (folder=test)

Let's use aiohttp for our core client layer.  
Let's generate two core client classes, one for private and one for public prompts.
Every time we make a public or private prompt, we must automatically add a tag "pytest-public" or "pytest-private" respectively.

Let's use pytest for our test user session layer.
THis layer will introduce a class called TestUserSession.
Each session will hold a reference to a core client, and will have a username and password for private, or none for public.
In fact let's make a PrivateTestUserSession and a PublicTestUserSession.


Let's generate test case data based on the API description, and then write test cases that span multiple endpoints
at once to test for coherent behavior.  Each test case should be in a file named test_{test-case-name}.py.
Each test case should be a class named Test{test-case-name}.
Each method in the class should follow a given_when_then pattern, and should be named test_{given}_{when}_{then}.
Each method should have a docstring that describes the test case.
ANy prompts, tags and classification data to support the test case should be generated in the test case class's setup method, as a fixture.

We will also need the following fixtures:
* A fixture that runs after each test case to delete all prompts that are tagged as "pytest-public".
* A fixture that runs after each test case to delete all prompts that are tagged as "pytest-private".
