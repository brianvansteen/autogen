import autogen

config_list = autogen.config_list_from_json(
        env_or_file="OAI_CONFIG_LIST.json" # added to .gitignore
)

llm_config = {
    "cache_seed": 41,  # change the cache_seed for different trials; 41 is default, or NONE
    "temperature": 0, # creativity
    "config_list": config_list,
    "timeout": 120,  # in seconds
}

user_proxy = autogen.UserProxyAgent(
    name="User",
    system_message="Executor. Execute the code written by the coder from the code directory and suggest updates if there are errors.",
    #system_message="Executor. Execute the code written by the Coder, and suggest changes if there are errors.",
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "code",
        "use_docker": False
    },
    human_input_mode="NEVER",
)

coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config,
    # system_message="""
    # Save the code in a file before executing it, put # filename: <filename> inside the code block as the first line.
    # You are a Coder, and your job is to install required libraries and write complete Python code.
    # You primarily are a Python game programmer.
    # Make sure to save the code to disk.
    # """,
    system_message="""
    If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line.
    Coder. Your job is to write complete code. You primarily are a game programmer.  Make sure to save the code to disk.
    """,
)

product_manager = autogen.AssistantAgent(
    name="Product_manager",
    # system_message="""
    # You own the product, you help plan how to create games, and you validate game playing capabilities.
    # """,
    system_message="Help plan out to create games.",
    llm_config=llm_config,
)

group_chat = autogen.GroupChat( # array of agent in group chat
    agents=[user_proxy, coder, product_manager], messages=[], max_round=20
)
manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=llm_config) # group chat manager

user_proxy.initiate_chat(
    manager, # with the manager
    message=
    """
    Make sure to save the file to disk.
    I would like to create a snake game in Python!  Make sure the game ends when the player hits the side of the screen.
    """,
    # message="""
    # I want to create a snake game in Python. The player must move the snake around the playing area, without colliding with objects and itself.
    # The snake can eat pellets that causes the snake to get longer.
    # """,
)





