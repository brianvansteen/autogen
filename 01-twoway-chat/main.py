import autogen

def main():
    config_list = autogen.config_list_from_json(
        env_or_file="OAI_CONFIG_LIST.json" # added to .gitignore
    )

    assistant = autogen.AssistantAgent(
        name="Assistant",
        llm_config={
            "config_list": config_list # get LLM and API key
        }
    )

    user_proxy = autogen.UserProxyAgent(
        name="user",
        human_input_mode="NEVER",
        code_execution_config={
            "work_dir": "coding", # to store any output code
            "use_docker": False
        }
    )

    user_proxy.initiate_chat(assistant, message="Plot a chart of META and TESLA stock price change.")

if __name__ == "__main__":
    main()
