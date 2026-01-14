#coding=utf-8

import os
import easygui
from openai import OpenAI
from Libs import DEL_PROXY_KEY_BUGS, APPEND_TO_DOCX
from random import choice

DEL_PROXY_KEY_BUGS()

def agent_talk(user_content, role_content):
    client = OpenAI(api_key=os.getenv("Ali_Qwen_API_KEY"), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
    response = client.chat.completions.create(
        model="qwen3-max-preview",
        extra_body={"enable_thinking": True},
        stream=True,
        messages=[
                {"role": "system", "content": role_content},
                {"role": "user", "content": user_content},
              ],
        stream_options={
            "include_usage": True
            },
    )
    
    reasoning_content = "" 
    answer_content = ""  
    is_answering = False
    
    print("\n" + "==" * 20 + "思考过程" + "==" * 20 ) 
    for chunk in response:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta
        if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
            if not is_answering:
                print(delta.reasoning_content, end="", flush=True)
            reasoning_content += delta.reasoning_content
    
        if hasattr(delta, "content") and delta.content:
            if not is_answering:
                is_answering = True
                print("\n"+"--" * 20 + "完整回复" + "--" * 20 )
            print(delta.content, end="", flush=True)
            answer_content += delta.content
    reasoning_text = reasoning_content
    answer_text = answer_content
    print("\n"+"=="*20 + "    "  + "==" * 20 + "\n\n")
    return answer_text, reasoning_text


content = "如何理解人工智能军事战略"

def get_role_content():
    think_manner = choice(["批判式", "开放式", "改革式", "思辨式", "补充式", "随从式", "递进式", "创新式", "辩驳式"])
    agent_role   = choice(["科学家", "军事家", "政治家", "哲学家", "数学家", "艺术家", "工程师", "理论家", "文学家"])
    role_content="思维模式为{}, 角色身份为{}。要求思维模式主要影响智能体的立场和推理方式，角色身份主要影响其知识背景和关注重点。用顺畅自然且客观的语言进行讨论，对输入内容进行展开讨论, 回答你对输入内容中问题的认识， 并提出新的问题，不要进行提纲式回答。".format(think_manner, agent_role)
    return role_content
    
for item in range(1000):
    content, thinking = agent_talk(content, get_role_content()) 
    APPEND_TO_DOCX("Agent {}:".format(item+1) +  content)
