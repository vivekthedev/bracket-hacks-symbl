import symbl
import json

app_id = "62673662517a687a44615133724f3663596150466343696a47696d6753394750"
app_secret = "316b776f7259714e6f695763795a47525569315a593576435147525370665f6c585f3147534c50357743424439594d624a5a7433647678787861774d4151586e"

credentials = {"app_id": app_id, "app_secret": app_secret}


def get_transcription(file_path):
    conversation_object = symbl.Video.process_file(file_path, credentials=credentials)
    messages = conversation_object.get_messages()
    messages_parsed = messages.to_dict()
    messages_ls = []
    for message in messages_parsed["messages"]:
        start_timestamp = str(
            message["start_time"] - messages_parsed["messages"][0]["start_time"]
        )
        end_timestamp = str(
            message["end_time"] - messages_parsed["messages"][0]["start_time"]
        )
        text = message["text"]
        message_dict = {
            "start_timestamp": start_timestamp,
            "end_timestamp": end_timestamp,
            "text": text,
        }
        messages_ls.append(message_dict)
    return messages_ls
