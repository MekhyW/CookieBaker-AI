import pandas as pd
import json
import os
import logging

logging.basicConfig(level=logging.INFO)

def concatenate_telegram_entities(entities):
    if isinstance(entities, str):
        return entities
    result = ""
    for entity in entities:
        if isinstance(entity, str):
            result += entity
        elif isinstance(entity, dict) and "text" in entity:
            result += entity["text"]
    return result

def json2df(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    relevant_data = data['messages']
    df = pd.DataFrame(relevant_data)
    df['text'] = df['text'].apply(concatenate_telegram_entities)
    df['chat_id'] = data['id']
    df = df.drop(columns=['text_entities'])
    return df

def join_df(df1, df2):
    df1 = df1.replace('', None)
    df2 = df2.replace('', None)
    for df in [df1, df2]:
        for col in df.columns:
            non_null_values = df[col].dropna()
            if len(non_null_values) > 0:
                numeric_values = pd.to_numeric(non_null_values, errors='coerce')
                if numeric_values.notna().sum() / len(non_null_values) > 0.5:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
    return pd.concat([df1, df2], ignore_index=True)

def save_df(df, file_path):
    df = df.replace('', None)
    for col in df.columns:
        non_null_values = df[col].dropna()
        if len(non_null_values) > 0:
            numeric_values = pd.to_numeric(non_null_values, errors='coerce')
            if numeric_values.notna().sum() / len(non_null_values) > 0.5:
                df[col] = pd.to_numeric(df[col], errors='coerce')
    df.to_parquet(file_path, index=False)

def main(folder_path, output_path):
    df_all = None
    for file in os.listdir(folder_path):
        if file.endswith(".json"):
            logging.info(f"Processing {file}")
            df = json2df(os.path.join(folder_path, file))
            df_all = df if df_all is None else join_df(df_all, df)
    logging.info(f"Saving dataframe to {output_path}")
    save_df(df_all, output_path)

if __name__ == "__main__":
    main("data/SFW", "data/SFW.parquet")
    main("data/NSFW", "data/NSFW.parquet")
