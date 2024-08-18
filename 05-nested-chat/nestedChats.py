import autogen

config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")
llm_config = {"config_list": config_list}

task = """Write a concise but engaging blogpost about Meta."""

writer = autogen.AssistantAgent(
    name="Writer",
    llm_config={"config_list": config_list},
    system_message="""
    You are a professional writer, known for your insightful and engaging articles.
    You transform complex concepts into compelling narratives.
    You should improve the quality of the content based on the feedback from the user.
    """,
)

user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "my_code",
        "use_docker": False,
    }
)

critic = autogen.AssistantAgent( # once writer responds, the critic is triggered
    name="Critic",
    llm_config={"config_list": config_list},
    system_message="""
    You are a critic, known for your thoroughness and commitment to standards.
    Your task is to scrutinize content for any harmful elements or regulatory violations, ensuring
    all materials align with required guidelines.
    For code
    """,
)


def reflection_message(recipient, messages, sender, config):
    print("Reflecting...") # when Critic is triggered
    return f"Reflect and provide critique on the following writing. \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}" # last message from sender


user_proxy.register_nested_chats(
    [
        {
            "recipient": critic,
            "message": reflection_message,
            "summary_method": "last_msg",
            "max_turns": 1
         }
    ],
    trigger=writer # when Critic is started, from writer response
)

user_proxy.initiate_chat(recipient=writer, message=task, max_turns=2, summary_method="last_msg") # max_turns to see user_proxy talk to writer and critic

"""
--------------------------------------------------------------------------------
Reflecting...

********************************************************************************
Starting a new chat....

********************************************************************************
User (to Critic):

Reflect and provide critique on the following writing.

---

Critic (to User):

The writing provided offers a compelling and enthusiastic overview of the concept of Meta and its potential impact on the digital landscape. However, to provide a balanced critique, here are some aspects that could be considered:

1. **Clarity and Specificity**: While the


---

Critic (to User):

The writing provided offers a compelling and enthusiastic overview of the concept of Meta and its potential impact on the digital landscape. However, to provide a balanced critique, here are some aspects that could be considered:

1. **Clarity and Specificity**: While the
"""