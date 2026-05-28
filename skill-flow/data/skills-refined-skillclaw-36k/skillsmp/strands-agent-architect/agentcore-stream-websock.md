Implementing Real-Time Bidirectional Streaming with Amazon Bedrock AgentCore Runtime WebSockets

In the landscape of modern AI applications, the demand for real-time, interactive experiences has become a strategic imperative. For use cases such as conversational voice agents, financial data tickers, and collaborative tools, the ability to maintain persistent, low-latency communication between a client and an AI agent is paramount. Traditional request-response protocols like HTTP, while effective for many tasks, introduce inherent latency that can degrade the user experience in these dynamic scenarios. This document serves as a formal technical guide for architects and senior developers on implementing persistent WebSocket connections within the Amazon Bedrock AgentCore Runtime (hereafter referred to as 'AgentCore Runtime'). It provides an in-depth analysis of the architecture, authentication mechanisms, implementation patterns, and operational best practices required to build highly responsive and secure AI agents. The subsequent sections will deliver a comprehensive analysis of the WebSocket architecture and a practical guide to its implementation, enabling technical leaders to harness the full potential of real-time, bidirectional AI.

1.0 Foundational Concepts of the AgentCore WebSocket Architecture

Before beginning implementation, a strategic understanding of the underlying architecture is essential for building robust and scalable real-time agents. The AgentCore Runtime integrates WebSocket support to enable persistent, low-latency, and bidirectional streaming connections, moving beyond the limitations of traditional HTTP protocols for interactive use cases. This architectural choice is fundamental to developing sophisticated conversational applications that require immediate feedback and continuous context. This section dissects the core components, service contracts, and key benefits of this architecture, providing the foundational knowledge necessary for successful implementation.

1.1 Architectural Overview

The core function of AgentCore Runtime's WebSocket support is to enable persistent, bidirectional streaming connections between clients and agents, which is ideal for interactive applications requiring real-time data exchange. This capability extends the powerful features of the standard InvokeAgentRuntime API to a persistent connection model. Consequently, WebSocket-enabled agents inherit the key benefits of the AgentCore platform, including:

* Serverless Execution: Agents run in a secure, serverless environment, eliminating the need for infrastructure management. By maintaining a persistent WebSocket, the serverless environment efficiently manages the long-lived connection state, allowing architects to design real-time applications without provisioning for peak concurrent connections.
* Session Isolation: Each user session is executed in a dedicated microVM, providing complete separation of CPU, memory, and filesystem resources. This isolation is paramount for WebSocket streams, as the persistent connection is tied to a single microVM, guaranteeing that real-time conversational context and stateful data cannot leak between sessions.
* Integrated Identity Management: WebSocket connections leverage the same robust authentication and authorization mechanisms as other AgentCore services, ensuring secure access.
* Observability Features: Agent decision-making processes, including reasoning steps and tool invocations, are captured through built-in tracing. WebSocket streaming enhances observability by enabling the real-time push of trace data, providing immediate insight into an agent's reasoning process as it occurs, rather than only after the interaction is complete.

1.2 The AgentCore Runtime Service Contract for WebSockets

To ensure seamless integration with the managed hosting environment, AgentCore establishes a clear service contract that a containerized agent application must follow. This contract is not merely a set of arbitrary rules; it reflects established best practices for containerized applications operating behind a managed ingress or load balancer. By standardizing on port 8080 and a dedicated /ws path, AgentCore Runtime ensures predictable routing and health check integration, allowing any compliant container to function as a scalable WebSocket backend.

Requirement	Specification
Endpoint Path	/ws
Listening Port	8080
Alignment	Aligns with standard WebSocket server practices

By adhering to this simple but critical contract, any containerized agent can integrate with the AgentCore Runtime and leverage its WebSocket capabilities, regardless of the underlying programming language or framework.

1.3 Architectural Comparison: WebSocket vs. HTTP

Choosing the correct communication protocol is a critical architectural decision. AgentCore Runtime supports both WebSocket and HTTP protocols, each suited for different interaction patterns. The following guide outlines the recommended use cases for each.

Protocol Selection Guide

Use Case	Recommended Protocol
For real-time, interactive applications requiring persistent bidirectional communication.	WebSocket
For standard request-response patterns without the need for bidirectional streaming.	HTTP

While WebSockets provide superior performance for interactive applications, architects must consider the implications of managing stateful, long-lived connections. Unlike stateless HTTP requests that can be distributed across a fleet of compute resources, a WebSocket session is typically pinned to a single container instance for its lifetime. This necessitates robust session management and graceful error handling within the agent's logic to manage connection drops or container restarts, a consideration not as critical in traditional request-response architectures.

With a clear understanding of the architectural foundations, the next critical topic is securing these real-time connections through robust authentication.

2.0 Authentication and Authorization for WebSocket Connections

Securing persistent WebSocket connections is critical to protecting the integrity and confidentiality of real-time data streams. Because these connections can remain open for extended periods, they require robust authentication mechanisms to prevent unauthorized access. AgentCore Runtime provides multiple flexible and secure methods for authenticating clients, ensuring that only authorized users and applications can establish a connection with an agent. This section will evaluate the primary authentication patterns available for WebSocket streams.

2.1 Supported Authentication Mechanisms

AgentCore Runtime supports three primary methods for authenticating WebSocket connections, offering architects the flexibility to choose the pattern that best aligns with their application's security posture and existing identity infrastructure.

* AWS Signature Version 4 (SigV4): This is the standard AWS protocol for authenticating API requests. It uses AWS credentials (access key ID and secret access key) to create a cryptographic signature, which is then included in the connection request. This method is ideal for server-to-server communication or applications running within the AWS ecosystem.
* OAuth 2.0 Bearer Tokens: This pattern allows integration with external identity providers (IdPs) like Amazon Cognito, Okta, or Microsoft Entra ID. The client first authenticates with the IdP to obtain a JSON Web Token (JWT) and then presents this bearer token to AgentCore Runtime to establish the WebSocket connection. This is a common pattern for applications with an established user authentication system.
* SigV4 Pre-signed URLs: This method provides a secure way to grant temporary, time-limited access to the WebSocket endpoint. A trusted backend service generates a pre-signed URL using its AWS credentials, which includes an authentication signature and an expiration time. This URL can then be passed to a client application, allowing it to connect without needing direct access to long-term AWS credentials.

With these secure authentication methods in place, we can now proceed to the practical steps required to build and deploy a WebSocket-enabled agent.

3.0 Implementation Guide: Building a WebSocket-Enabled Agent

This section provides a practical, step-by-step guide to building, deploying, and invoking a bidirectional streaming agent. The process leverages the bedrock-agentcore Python SDK for client-side interactions and the Amazon Bedrock AgentCore starter toolkit for streamlined deployment. This approach provides developers with a concrete path from initial code to a fully deployed, real-time agent, demonstrating the simplicity and power of the AgentCore platform.

3.1 Prerequisites and Environment Setup

Before building the agent, ensure the following components are installed and configured in your development environment.

1. Frameworks: This guide utilizes the bedrock-agentcore Python SDK for programmatic client interaction and the Amazon Bedrock AgentCore starter toolkit for simplifying the agent deployment process.
2. Dependencies: The client application requires the websockets Python library to establish and manage the WebSocket connection. This can be installed using pip install websockets.

3.2 Agent Configuration and Deployment

The Amazon Bedrock AgentCore starter toolkit streamlines the deployment of a containerized agent into the serverless runtime environment. The process involves two simple commands executed from your project directory.

1. Configuration: The agent's deployment settings are configured using the following command, which interactively guides the user through the setup process based on the specified agent entrypoint file:
2. Deployment: Once configured, the agent is deployed to the AgentCore Runtime with a single command:
3. Output: A successful deployment will output the agent runtime's Amazon Resource Name (ARN). This ARN is a unique identifier for the deployed agent and is required for client invocation.

3.3 Client-Side Invocation

After the agent is successfully deployed, a client application can establish a persistent WebSocket connection. The following Python script demonstrates how to invoke the agent using SigV4 authentication.

SigV4 Client Example

import asyncio
import json
import websockets
from bedrock_agentcore.runtime import AgentCoreRuntimeClient

# The ARN of the deployed agent
runtime_arn = "arn:aws:bedrock-agentcore:us-west-2:<ACCOUNT_ID>:runtime/websocket_echo_agent-xyz123"

async def main():
    # Initialize the AgentCore Runtime client
    client = AgentCoreRuntimeClient(region="us-west-2")

    # Generate the authenticated WebSocket URL and headers using SigV4
    ws_url, headers = client.generate_ws_connection(
        runtime_arn=runtime_arn
    )

    try:
        # Establish the WebSocket connection
        async with websockets.connect(ws_url, additional_headers=headers) as ws:
            # Send a JSON-formatted message to the agent
            await ws.send(json.dumps({"inputText": "Hello!"}))

            # Receive the response from the agent
            response = await ws.recv()
            print(f"Received: {response}")

    except websockets.exceptions.InvalidStatus as e:
        print(f"WebSocket handshake failed with status code: {e.response.status_code}")
        print(f"Response headers: {e.response.headers}")
        print(f"Response body: {e.response.body.decode()}")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())


This script performs several key operations to establish and manage the real-time connection:

* client.generate_ws_connection(): This method abstracts the complexity of the AWS Signature Version 4 signing process. It takes the agent's runtime ARN and generates a fully authenticated WebSocket URL and the necessary HTTP headers required for the connection handshake.
* websockets.connect(): Using the URL and headers generated by the previous step, this function from the websockets library establishes the persistent connection with the AgentCore Runtime endpoint.
* ws.send() and ws.recv(): These asynchronous methods are used for bidirectional communication over the established connection. The client sends a JSON-formatted message with ws.send() and waits to receive a response from the agent with ws.recv(), enabling a real-time conversational flow.

Having covered the standard SigV4 implementation, the following section will examine different authentication patterns for client invocation.

4.0 Advanced Invocation Patterns

The choice of authentication pattern is a critical architectural decision. Embedding static SigV4 credentials directly in a client-side web or mobile application is a severe security anti-pattern. Instead, such applications must use temporary credentials, which can be securely vended via pre-signed URLs or brokered through an OAuth 2.0 flow from a trusted backend. This section provides detailed code examples and analysis for the primary methods of establishing an authenticated WebSocket connection with AgentCore Runtime.

4.1 Connection via SigV4 Pre-signed URL

A pre-signed URL is a secure and effective method for granting temporary access to a WebSocket endpoint without exposing long-term credentials to the client application. A trusted backend service generates the URL, which includes a SigV4 signature and an expiration time.

Pre-signed URL Client Example

from bedrock_agentcore.runtime import AgentCoreRuntimeClient
import websockets
import asyncio
import json
import os

async def websocket_with_session():
    client = AgentCoreRuntimeClient(region="us-west-2")
    session_id = "user-123-conversation-456"
    runtime_arn = os.getenv('AGENT_ARN')

    # Generate a pre-signed URL valid for 300 seconds (5 minutes)
    presigned_url = client.generate_presigned_url(
        runtime_arn=runtime_arn,
        session_id=session_id,
        expires=300
    )

    try:
        async with websockets.connect(presigned_url) as ws:
            await ws.send(json.dumps({"inputText": "Hello!"}))
            response = await ws.recv()
            print(f"Received: {response}")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(websocket_with_session())


* Function: The client.generate_presigned_url() method is used to create the temporary, authenticated URL.
* Parameters: It requires the runtime_arn of the agent, a unique session_id to maintain conversation context, and an expires parameter that defines the URL's validity period in seconds.
* Use Case: This pattern is highly recommended for client-side applications (e.g., web or mobile) where embedding static credentials would be a significant security risk. It delegates the responsibility of authentication to a secure backend, providing short-term, scoped access directly to the client.

4.2 Connection via OAuth 2.0 Bearer Token

AgentCore Runtime also supports OAuth 2.0 bearer tokens for authenticating WebSocket connections. This pattern is ideal for applications that integrate with an external identity provider. To use this method, the agent runtime must first be configured with JWT authorization. The client application authenticates the user against the identity provider, receives a JWT bearer token, and includes this token in the Authorization header when establishing the WebSocket connection.

For detailed instructions on configuring the agent runtime for JWT inbound authorization, please refer to the "JWT inbound authorization and OAuth outbound access sample" section in the official documentation.

With a firm grasp of implementation and advanced authentication, the final step is to ensure that deployed applications are robust and reliable by adhering to best practices and having a clear troubleshooting strategy.

5.0 Best Practices and Troubleshooting

Architecting and maintaining robust, real-time AI agents requires adherence to established best practices and a clear strategy for troubleshooting common issues. Production-ready applications must be built on a foundation of reliability and security. This final section distills critical recommendations for endpoint configuration, testing, and authentication to help developers build dependable and secure WebSocket implementations in AgentCore Runtime.

5.1 Endpoint Configuration Best Practices

For an agent to integrate successfully with the AgentCore Runtime's WebSocket protocol, its containerized application must adhere to a specific service contract. Misconfiguration of these endpoints is a common source of deployment failures.

* Port: The agent's container must listen for incoming connections on port 8080.
* Path: The agent must serve WebSocket connections at the /ws path.

5.2 Recommended Testing Strategy

A systematic, incremental testing methodology is crucial for identifying issues early and ensuring reliability. Before deploying to the AgentCore Runtime, developers should validate their agent locally with increasing complexity.

1. Basic Local Connection: First, verify that the agent's container accepts WebSocket connections locally. Use a simple client to connect to ws://localhost:8080/ws and confirm that the handshake is successful.
2. Local Message Handling: Test the agent's core logic by sending simple text messages and confirming that it returns the expected responses. This validates the message parsing and business logic.
3. Local Session Management: Ensure that the agent can maintain context across multiple messages within a single conversation. Test multi-turn interactions to verify that session state is managed correctly on the local instance.
4. Local Error Handling: Validate that the agent can gracefully handle unexpected events, such as connection drops or malformed messages, without crashing.

5.3 Common Connection and Authentication Issues

Even with careful testing, issues can arise in a deployed environment. The following table summarizes common connection and authentication problems and their corresponding resolutions.

Troubleshooting Guide

Issue	Resolution
OAuth Connection Fails	Verify the bearer token is valid and has not expired. Check the token's claims (iss, aud, client_id) against the agent's authorizer configuration.
SigV4 Connection Fails	Ensure the input to the signing algorithm is correct. This commonly involves errors in constructing the canonical request, especially the WebSocket URL and headers. Verify that the HTTP request method is GET for the WebSocket upgrade request, as this is a frequent point of failure.
General Connection Failure	Confirm the agent correctly handles WebSocket upgrade requests and maintains the connection loop. Review container logs in Amazon CloudWatch for startup errors or runtime exceptions that may prevent the WebSocket server from initializing correctly. The log group path follows the pattern /aws/bedrock-agentcore/runtimes/<agent_id>-<endpoint_name>/runtime-logs.
Message Format Mismatch	Verify that the message format (e.g., JSON structure) being sent by the client is exactly what the agent expects, and vice versa.

6.0 Conclusion

The integration of WebSocket streaming into the AgentCore Runtime represents a significant advancement for the development of interactive AI applications. This technology enables persistent, low-latency, and bidirectional communication, providing the architectural foundation for building sophisticated conversational agents, real-time data processors, and collaborative tools. By leveraging the platform's serverless execution, session isolation, and integrated security, developers can create highly responsive and engaging user experiences without the burden of managing complex infrastructure. By following the architectural principles, implementation guides, and best practices detailed in this whitepaper, architects and developers are well-equipped to build the next generation of highly responsive and secure AI agents on AWS.