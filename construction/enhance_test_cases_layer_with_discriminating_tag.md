You are a QA developer expert in Python, using the pytest framework.

The architecture of the test cases is three layers:
1. Core client layer (folder=client) 
2. Test user session layer (folder=session)
3. Test Case layer (folder=test)

You have this test case layer base class:
```
{base_test}
```

```

You have these session layer classes:
```
{session_classes}
```

We have a User class that holds a username and password.
```
{user_class}
```
We have a core client set of classes:
```
{core_client_classes}
```

The issue at hand is, I want each core client class to enforce a tag on each prompt it creates or updates.
The tag is prefixed with pytest and the last part of the tag is the name of the TEST_USERNAME from the .env file.
The tag is used to delete all prompts created by the test user after each test case.

As such the tag needs to be available to the test case layer, and the core client layer needs to enforce it.
