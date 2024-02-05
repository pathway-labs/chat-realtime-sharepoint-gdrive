import sys
import streamlit as st
import datetime

def get_inputs() -> list:
    last_indexed_files = []
    try:
        docs_list = st.session_state.vector_client.get_input_files()
        docs_list.sort(key=lambda x: (x["modified_at"], x.get("path", x.get("name"))), reverse=True)

        for added_file in docs_list:
            full_path = added_file.get("path", added_file.get("name"))
            if full_path is None:
                continue
            name = full_path.split("/")[-1]
            last_indexed_files.append(name)
    except Exception as e:
        print(f"Failed to get last indexed file: {e}", file=sys.stderr)
    return last_indexed_files


def get_last_change() -> str:
    try:
        dt = st.session_state.vector_client.get_vectorstore_statistics()[
            "last_modified"
        ]
    except Exception as e:
        print(f"Failed to get status string: {e}", file=sys.stderr)
        return ""
    
    # if time.time() - dt > 3600:
    #     return f"No documents have been added by users yet."
    
    formatted_time = datetime.datetime.fromtimestamp(dt)
    return (
        f"Last document change: {formatted_time} UTC."
    )

async def async_get_last_change():
    return get_last_change()

async def async_get_inputs():
    return get_inputs()

import asyncio

async def call_endpoints():  # reduce lag to endpoint by half
    tasks = [
        async_get_last_change(),
        async_get_inputs()
    ]

    results = await asyncio.gather(*tasks)
    return results