import autogen

def main():
    config_list = autogen.config_list_from_json(
        env_or_file="OAI_CONFIG_LIST.json" # added to .gitignore
    )

    # Start logging
    logging_session_id = autogen.runtime_logging.start(config={"dbname": "logs.db"})
    print("Logging session ID: " + str(logging_session_id))

    assistant = autogen.AssistantAgent(
        name="Assistant",
        llm_config={
            "config_list": config_list # get LLM and API key
        }
    )

    user_proxy = autogen.UserProxyAgent(
        name="user",
        human_input_mode="TERMINATE",
        # human_input_mode="NEVER", # be a part of the chat with the agent or not; or ALWAYS or TERMINATE
        code_execution_config={
            "work_dir": "coding", # to store any output code
            "use_docker": False
        }
    )

    # initiate chat using assistant
    user_proxy.initiate_chat(assistant, message="Plot a chart of META and TESLA stock price change.")

    autogen.runtime_logging.stop()

if __name__ == "__main__":
    main()
