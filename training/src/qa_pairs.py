import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def clean_dataframe(df):
    df = df[['id', 'text', 'from', 'from_id', 'reply_to_message_id', 'forwarded_from']]
    df = df[df['text'].notna()]
    df = df[df['from_id'].notna()]
    df = df[df['forwarded_from'].isna()]
    df = df[~df['from'].str.contains('bot', na=False)]
    df = df.drop(columns=['forwarded_from', 'from'])
    df = df.sort_values('id')
    return df

def create_message_groups(df):
    df['group'] = (df['from_id'] != df['from_id'].shift()).cumsum()
    grouped_messages = df.groupby(['from_id', 'group'])['text'].agg('\n'.join).reset_index()
    message_map = df.set_index('id')['text'].to_dict()
    return grouped_messages, message_map

def extract_qa_pairs(df, grouped_messages, message_map):
    total = len(df)
    qa_pairs = pd.DataFrame(columns=['query', 'response'])
    for idx, row in df.iterrows():
        if not row['reply_to_message_id'] in message_map:
            continue
        query = message_map[row['reply_to_message_id']]
        response = grouped_messages[
            (grouped_messages['from_id'] == row['from_id']) & 
            (grouped_messages['group'] == (df['group'][idx]))
        ]['text'].iloc[0]
        qa_pairs = pd.concat([
            qa_pairs,
            pd.DataFrame({'query': [query], 'response': [response.capitalize()]})
        ], ignore_index=True)
        logging.info(f"{idx}/{total}")
    return qa_pairs

def save_qa_pairs(qa_pairs, output_path):
    qa_pairs.to_parquet(output_path, index=False)

def process_conversation_data(input_df, output_path):
    df = clean_dataframe(input_df)
    grouped_messages, message_map = create_message_groups(df)
    qa_pairs = extract_qa_pairs(df, grouped_messages, message_map)
    save_qa_pairs(qa_pairs, output_path)

def main(input_path, output_path):
    logging.info(f"Processing {input_path} to {output_path}")
    df = pd.read_parquet(input_path)
    process_conversation_data(df, output_path)

if __name__ == "__main__":
    main("data/SFW.parquet", "data/SFW_qa.parquet")
    main("data/NSFW.parquet", "data/NSFW_qa.parquet")