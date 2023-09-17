# Code generator for FastStream

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

`faststream-gen` is a Python library that uses generative AI to
automatically generate [FastStream](https://faststream.airt.ai)
applications. Simply describe your application requirements, and
`faststream-gen` will generate a production-grade FastStream project
that is ready to deploy in no time.

![PyPI](https://img.shields.io/pypi/v/faststream-gen.png) ![PyPI -
Downloads](https://img.shields.io/pypi/dm/faststream-gen.png) ![PyPI -
Python
Version](https://img.shields.io/pypi/pyversions/faststream-gen.png)
![GitHub Workflow
Status](https://img.shields.io/github/actions/workflow/status/airtai/fastkafka-gen/test.yaml)
![GitHub](https://img.shields.io/github/license/airtai/fastkafka-gen.png)

------------------------------------------------------------------------

**Documentation**: https://faststream-gen.airt.ai

**Source Code**: https://github.com/airtai/faststream-gen

------------------------------------------------------------------------

## Getting Started

The code generator for [FastStream](https://faststream.airt.ai) is a
Python library that automates the process of creating FastStream
applications. It works by taking your application requirements and
swiftly turning them into a ready-to-deploy FastStream application.

The key features are:

- **Automatic FastStream project generation**: `faststream-gen` enables
  you to easily generate complete FastStream application with minimal
  effort. This library allows you to outline your application
  requirements, and it will quickly transform them into a fully-fledged
  FastStream project.
- **Tested code**: `faststream-gen` provides dependable code through
  rigorous testing, including pre-implemented integration tests,
  ensuring stability and functionality, saving development time, and
  preventing common bugs.
- **Deploy scripts**: Simplify the deployment of your FastStream
  application with built-in deploy scripts provided by `faststream-gen`.
  Whether you’re deploying to a local server, cloud infrastructure, or a
  custom environment, these scripts streamline the deployment process.
- **GitHub workflow files**: `faststream-gen` integrates seamlessly with
  your version control and continuous integration pipeline through its
  GitHub workflow files. These predefined configuration files are
  optimized for FastStream projects, enabling smooth integration with
  GitHub Actions. You can automate tasks such as code validation,
  testing, and deployment, ensuring that your FastStream application
  remains in top shape throughout its development lifecycle.

### Quick start

The following quick start guide will walk you through installing and
configuring the `faststream-gen` library, demonstrating the creation of
a new FastStream project in seconds.

#### Install

`faststream-gen` is published as a Python package and can be installed
with pip:

``` shell
pip install faststream-gen
```

If the installation was successful, you should now have the
**faststream-gen** installed on your system. Run the below command from
the terminal to see the full list of available commands:

``` shell
faststream_gen --help
```

                                                                                    
     Usage: faststream_gen [OPTIONS] [DESCRIPTION]                                  
                                                                                    
     Effortlessly create a new FastStream project based on the app description.     
                                                                                    
    ╭─ Arguments ──────────────────────────────────────────────────────────────────╮
    │   description      [DESCRIPTION]  Summarize your FastStream application in a │
    │                                   few sentences!                             │
    │                                                                              │
    │                                   Include details about messages, topics,    │
    │                                   servers, and a brief overview of the       │
    │                                   intended business logic.                   │
    │                                                                              │
    │                                   The simpler and more specific the app      │
    │                                   description is, the better the generated   │
    │                                   app will be. Please refer to the below     │
    │                                   example for inspiration:                   │
    │                                                                              │
    │                                   Create a FastStream application using      │
    │                                   localhost broker for testing and use the   │
    │                                   default port number.  It should consume    │
    │                                   messages from the "input_data" topic,      │
    │                                   where each message is a JSON encoded       │
    │                                   object containing a single attribute:      │
    │                                   'data'.  For each consumed message, create │
    │                                   a new message object and increment the     │
    │                                   value of the data attribute by 1. Finally, │
    │                                   send the modified message to the           │
    │                                   'output_data' topic.                       │
    │                                   [default: None]                            │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --input_file          -i      TEXT                   The path to the file    │
    │                                                      with the app            │
    │                                                      desription. This path   │
    │                                                      should be relative to   │
    │                                                      the current working     │
    │                                                      directory.              │
    │                                                      If the app description  │
    │                                                      is passed via both a    │
    │                                                      --input_file and a      │
    │                                                      command line argument,  │
    │                                                      the description from    │
    │                                                      the command line will   │
    │                                                      be used to create the   │
    │                                                      application.            │
    │                                                      [default: None]         │
    │ --output_path         -o      TEXT                   The path to the output  │
    │                                                      directory where the     │
    │                                                      generated project files │
    │                                                      will be saved. This     │
    │                                                      path should be relative │
    │                                                      to the current working  │
    │                                                      directory.              │
    │                                                      [default: .]            │
    │ --model               -m      [gpt-3.5-turbo-16k|gp  The OpenAI model that   │
    │                               t-4]                   will be used to create  │
    │                                                      the FastStream project. │
    │                                                      For better results, we  │
    │                                                      recommend using         │
    │                                                      'gpt-4'.                │
    │                                                      [default:               │
    │                                                      gpt-3.5-turbo-16k]      │
    │ --verbose             -v                             Enable verbose logging  │
    │                                                      by setting the logger   │
    │                                                      level to INFO.          │
    │ --dev                 -d                             Save the intermediate   │
    │                                                      faststream-gen files    │
    │                                                      within the output_path. │
    │ --install-completion                                 Install completion for  │
    │                                                      the current shell.      │
    │ --show-completion                                    Show completion for the │
    │                                                      current shell, to copy  │
    │                                                      it or customize the     │
    │                                                      installation.           │
    │ --help                                               Show this message and   │
    │                                                      exit.                   │
    ╰──────────────────────────────────────────────────────────────────────────────╯

#### Usage

The **faststream-gen** library uses OpenAI’s model to generate
FastStream projects. In order to use the library, you’ll need to
<a href="https://beta.openai.com/account/api-keys" target="_blank">create
an API key for OpenAI</a>.

Once you have your API key, store it in the **OPENAI_API_KEY**
environment variable. This is a necessary step for the library to work.

We’re now ready to create a new FastStream application with the
`faststream-gen` library.

Simply run the following command to create a new FastStream application
in the `my-awesome-project` directory:

``` shell
faststream_gen "Create a FastStream application using localhost broker for testing and use the default port number. It should consume messages from the 'input_data' topic, where each message is a JSON encoded object containing a single attribute: 'data'. For each consumed message, create a new message object and increment the value of the data attribute by 1. Finally, send the modified message to the 'output_data' topic." -o "./my-awesome-project"
```

    ✨  Generating a new FastStream application!
     ✔ Application description validated. 
     ✔ FastStream app skeleton code generated. akes around 15 to 30 seconds)...
     ✔ The app and the tests are generated.  around 30 to 40 seconds)...
     ✔ New FastStream project created. 
     ✔ Integration tests were successfully completed. 
     Tokens used: 10955
     Total Cost (USD): $0.03347
    ✨  All files were successfully generated!

Here’s a look at the directory hierarchy:

    my-awesome-project
    ├── .github
    │   └── workflows
    │       ├── deploy_docs.yml
    │       └── test.yml
    ├── .gitignore
    ├── LICENSE
    ├── README.md
    ├── app
    │   ├── __init__.py
    │   ├── __pycache__
    │   │   └── application.cpython-311.pyc
    │   └── application.py
    ├── dev_requirements.txt
    ├── requirements.txt
    ├── scripts
    │   ├── services.yml
    │   ├── start_kafka_broker_locally.sh
    │   ├── stop_kafka_broker_locally.sh
    │   └── subscribe_to_kafka_broker_locally.sh
    └── tests
        └── test_application.py

    6 directories, 15 files

Let’s take a quick look at the generated application and test code.

`application.py`:



    from pydantic import BaseModel, Field

    from faststream import FastStream, Logger
    from faststream.kafka import KafkaBroker


    class InputData(BaseModel):
        data: int = Field(
            ..., examples=[1], description="The data attribute in the input message"
        )


    class OutputData(BaseModel):
        data: int = Field(
            ..., examples=[2], description="The modified data attribute in the output message"
        )


    broker = KafkaBroker("localhost")
    app = FastStream(broker)


    to_output_data = broker.publisher("output_data")


    @broker.subscriber("input_data")
    async def on_input_data(msg: InputData, logger: Logger) -> None:
        logger.info(f"{msg=}")
        modified_msg = OutputData(data=msg.data + 1)
        await to_output_data.publish(modified_msg)

`test_application.py`:



    import pytest

    from faststream import Context
    from faststream.kafka import TestKafkaBroker

    from app.application import InputData, OutputData, broker, on_input_data


    @broker.subscriber("output_data")
    async def on_output_data(msg: OutputData):
        pass


    @pytest.mark.asyncio
    async def test_modify_data():
        async with TestKafkaBroker(broker):
            await broker.publish(InputData(data=1), "input_data")
            on_input_data.mock.assert_called_with(dict(InputData(data=1)))
            on_output_data.mock.assert_called_with(dict(OutputData(data=2)))

#### Start application

To start the application, navigate to the `my-awesome-project` directory
and run the following command:

``` shell
faststream run  my-awesome-project.app.application:app
```

You will see an output that is similar to this:

``` console
2023-09-15 13:41:21,948 INFO     - FastStream app starting...
2023-09-15 13:41:22,144 INFO     -      |            - Starting publishing:
2023-09-15 13:41:22,144 INFO     - FastStream app started successfully! To exit press CTRL+C
```

## Copyright

Copyright © 2023 onwards airt technologies ltd, Inc.

## License

This project is licensed under the terms of the
<a href="https://github.com/airtai/faststream-gen/blob/main/LICENSE" target="_blank">Apache
License 2.0</a>
