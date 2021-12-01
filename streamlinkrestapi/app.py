import sys
import logging
from streamlink import (
    Streamlink
)
from flask import (
    Flask,
    current_app,
    redirect,
    stream_with_context
)
from webargs import (
    fields,
    flaskparser
)

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

app = Flask(__name__)

def session() -> Streamlink:
    session = Streamlink()
    session.set_plugin_option('twitch', 'disable-ads', True)
    session.set_plugin_option('twitch', 'disable-hosting', True)
    session.set_plugin_option('twitch', 'disable-reruns', True)
    return session

def stream(url: str, quality: str = 'best', proxy: bool = True, playlist: bool = False, streamlink_session: Streamlink = session()):
    streams = streamlink_session.streams(url)
    stream = streams.get(quality)
    if proxy:
        def _stream():
            stream_fd = stream.open()
            while True:
                yield stream_fd.read(-1)
        return current_app.response_class(stream_with_context(_stream()))
    else:
        if playlist:
            return redirect(stream.url_master)
        else:
            return redirect(stream.url)

@app.route('/')
def index():
    return ''

@app.route('/twitch/<string:twitch_id>', methods=['GET'])
@flaskparser.use_args(
    argmap=dict(
        quality=fields.Str(default='best',
                           missing='best'),
        proxy=fields.Boolean(default=True,
                             missing=True),
        playlist=fields.Boolean(default=False,
                                missing=False)
    ),
    location='query',
    as_kwargs=True)
def twitch(twitch_id: str,
           quality: str,
           proxy: bool = True,
           playlist: bool = False,
           *args,
           **kwargs):
    return stream(url=f'twitch.tv/{twitch_id}',
                  quality=quality,
                  proxy=proxy,
                  playlist=playlist)
