from pyrogram.types import Message
from datetime import datetime
from mimetypes import guess_type
from file_xor import roxe
from config import TgConfig
from file_xor.StreamServer.WebErrorHandling import abort

async def get_message(message_id: int) -> Message | None:
    message = None
    
    try:
        message = await roxe.get_messages(TgConfig.FILEDB_CHANNEL, message_ids=message_id)
        if message.empty: message = None
    except Exception:
        pass

    return message

async def send_message(msg: Message, send_to: int = TgConfig.FILEDB_CHANNEL) -> Message:
    return await roxe.send_message(entity=send_to, message=msg)

def get_file_properties(msg: Message):
    attributes = (
        'document',
        'video',
        'audio',
        'voice',
        'photo',
        'video_note'
    )
    for attribute in attributes:
        media = getattr(msg, attribute, None)
        if media:
            file_type = attribute
            break

    if not media: abort(400, 'Unknown file type.')

    file_name = getattr(media, 'file_name', None)
    file_size = getattr(media, 'file_size', 0)

    if not file_name:
        file_format = {
            'video': 'mp4',
            'audio': 'mp3',
            'voice': 'ogg',
            'photo': 'jpg',
            'video_note': 'mp4'
        }.get(file_type)
        date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f'{file_type}-{date}.{file_format}'
    
    mime_type = guess_type(file_name)[0] or 'application/octet-stream'

    return file_name, file_size, mime_type