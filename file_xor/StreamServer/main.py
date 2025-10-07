from quart import Blueprint, Response, request, render_template, redirect , send_from_directory
from pathlib import Path
from math import ceil
from re import match as re_match, search as re_search
from .WebErrorHandling import abort
from file_xor import roxe
from config import TgConfig, ServerConfig
from file_xor.lib.runtime_utils import save_host_url
from file_xor.lib.url_utils import normalize_base_url
from file_xor.lib._StreamServer import get_message, get_file_properties

bp = Blueprint('main', __name__)


@bp.route("/")
async def index():
    # If no DOMAIN_URL is configured, persist current host URL for fallback
    if not ServerConfig.DOMAIN_URL:
        try:
            # request.host_url typically includes trailing slash and scheme
            save_host_url(request.host_url)
        except Exception:
            pass
    return await render_template('home_page.html')


@bp.route("/favicon.ico")
async def favicon():
    # Serve the favicon from this package's static/img folder using an
    # absolute path. Previously a relative path could resolve from the
    # application root and miss the file, causing 404s when the browser
    # requested /favicon.ico.
    pkg_static_img = Path(__file__).resolve().parent / 'static' / 'img'
    return await send_from_directory(str(pkg_static_img), "favicon.ico")

@bp.route('/alive')
async def ping():
    return 'Wrking gud'


@bp.route('/dl/<int:file_id>')
async def transmit_file(file_id):
    file = await get_message(file_id) or abort(404)
    code = request.args.get('code') or abort(401)
    range_header = request.headers.get('Range')

    # Extract secret_code from the stored message caption. The caption
    # is created in `getlink_files.py` as:
    #   ||sender_id={sender_id},\n secret_code={secret_code}||
    # Be robust to whitespace and optional quotes.
    caption = getattr(file, 'caption', '') or ''
    secret = None
    if caption:
        m = re_search(r'secret_code\s*=\s*([0-9a-fA-F]+)', caption)
        if m:
            secret = m.group(1)

    if not secret or code != secret:
        abort(403)

    file_name, file_size, mime_type = get_file_properties(file)

    start = 0
    end = file_size - 1
    chunk_size = ServerConfig.CHUNK_SIZE * 1024 * 1024  # 1 MB

    if range_header:
        range_match = re_match(r'bytes=(\d+)-(\d*)', range_header)
        if range_match:
            start = int(range_match.group(1))
            end = int(range_match.group(2)) if range_match.group(2) else file_size - 1
            if start > end or start >= file_size:
                abort(416, 'Requested range not satisfiable')
        else:
            abort(400, 'Invalid Range header')

    offset_chunks = start // chunk_size
    total_bytes_to_stream = end - start + 1
    chunks_to_stream = ceil(total_bytes_to_stream / chunk_size)

    content_length = total_bytes_to_stream
    headers = {
        'Content-Type': mime_type,
        'Content-Disposition': f'attachment; filename={file_name}',
        'Content-Range': f'bytes {start}-{end}/{file_size}',
        'Accept-Ranges': 'bytes',
        'Content-Length': str(content_length),
    }
    status_code = 206 if range_header else 200

    async def file_stream():
        bytes_streamed = 0
        chunk_index = 0
        async for chunk in roxe.stream_media(
            file,
            offset=offset_chunks,
            limit=chunks_to_stream,
        ):
            if chunk_index == 0: # Trim the first chunk if necessary
                trim_start = start % chunk_size
                if trim_start > 0:
                    chunk = chunk[trim_start:]

            remaining_bytes = content_length - bytes_streamed
            if remaining_bytes <= 0:
                break

            if len(chunk) > remaining_bytes: # Trim the last chunk if necessary
                chunk = chunk[:remaining_bytes]

            yield chunk
            bytes_streamed += len(chunk)
            chunk_index += 1

    return Response(file_stream(), headers=headers, status=status_code)

@bp.route('/stream/<int:file_id>')
async def stream_file(file_id):
    code = request.args.get('code') or abort(401)
    base = normalize_base_url(ServerConfig.get_domain_url())
    return await render_template('stream_file.html', mediaLink=f'{base}/dl/{file_id}?code={code}')