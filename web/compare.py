#!/usr/bin/env python
"""
@Time    :   2024/10/21 11:19:46
@Author  :   ChenHao
@Description  :   demo web for api compare
@Contact :   jerrychen1990@gmail.com
"""

import time

import streamlit as st
from liteai.api import chat
from loguru import logger

from web.config import AI_DEMO_COMPARE_CONFIG


def load_view():
    system_prompt = st.sidebar.text_area(
        "系统prompt", value=AI_DEMO_COMPARE_CONFIG["system_prompt"]
    )
    prompt = st.sidebar.text_area("请求prompt", value=AI_DEMO_COMPARE_CONFIG["prompt"])
    prompt_template = st.sidebar.text_area(
        "套在prompt上的模板,用{input}槽位表示",
        value=AI_DEMO_COMPARE_CONFIG["prompt_template"],
    )
    do_sample = st.sidebar.checkbox(label="是否采样", value=True)
    if do_sample:
        temperature = st.sidebar.slider(
            label="temperature", min_value=0.01, max_value=1.0, value=0.9, step=0.01
        )
        top_p = st.sidebar.slider(
            label="top_p", min_value=0.1, max_value=0.9, value=0.7, step=0.1
        )
    else:
        temperature = 0
        top_p = 0
    models = st.sidebar.multiselect(
        label="选择模型",
        options=AI_DEMO_COMPARE_CONFIG["models"],
        default=AI_DEMO_COMPARE_CONFIG["default_model"],
    )
    if do_sample:
        rounds = st.sidebar.number_input(
            label="生成多少个", min_value=1, max_value=10, value=1
        )
    else:
        rounds = 1
    submit = st.sidebar.button("生成")
    if submit:
        for round in range(rounds):
            cols = st.columns(len(models))
            for col, model in zip(cols, models):
                t = time.time()
                prompt_with_template = prompt_template.replace("{input}", prompt)
                resp = chat(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt_with_template},
                    ],
                    temperature=temperature,
                    top_p=top_p,
                )
                resp = resp.content
                logger.info(resp)
                cost = time.time() - t
                meta = f"{model} 第[{round+1}]轮，耗时:{cost:2.2f}s，{len(resp)}字"
                col.markdown(meta)
                col.markdown(resp)
                col.write("*" * 50)


load_view()
