from autogen_core import AgentId, SingleThreadedAgentRuntime

# Try to import using absolute imports first, then fall back to relative imports
try:
    from autogen.core.agents import Message, Modifier, Checker
except ImportError:
    # If running the file directly, use absolute import with the full path
    try:
        import sys
        import os
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
        from autogen.core.agents import Message, Modifier, Checker
    except ImportError:
        # Last resort: try a direct import if in the same directory
        from agents import Message, Modifier, Checker


async def main():
    # Create a local embedded runtime.
    runtime = SingleThreadedAgentRuntime()

    # Register the modifier and checker agents by providing
    # their agent types, the factory functions for creating instance and subscriptions.
    await Modifier.register(
        runtime,
        "modifier",
        # Modify the value by subtracting 1 
        lambda: Modifier(modify_val=lambda x: x - 1),
    )

    await Checker.register(
        runtime,
        "checker",
        # Run until the value is less than or equal to 1
        lambda: Checker(run_until=lambda x: x <= 1),
    )

    # Start the runtime and send a direct message to the checker.
    runtime.start()
    await runtime.send_message(Message(10), AgentId("checker", "default"))
    await runtime.stop_when_idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
