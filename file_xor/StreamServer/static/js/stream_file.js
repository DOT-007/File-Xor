document.addEventListener('DOMContentLoaded', function () {
  // mediaLink is provided by the template via window.mediaLink
  var player = new Plyr('#stream-media', {
    controls: ['play-large', 'rewind', 'play', 'fast-forward', 'progress', 'current-time', 'mute', 'settings', 'pip', 'fullscreen'],
    settings: ['speed', 'loop'],
    speed: { selected: 1, options: [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2] },
    seek: 10,
    keyboard: { focused: true, global: true }
  });

  var mediaLink = window.mediaLink || '';

  if (mediaLink) {
    // Use Plyr's source API to reliably swap media and avoid reload/size issues
    try {
      player.source = {
        type: 'video',
        sources: [
          {
            src: mediaLink,
            type: 'video/mp4'
          }
        ]
      };
    } catch (e) {
      // Fallback: set <source> attributes and call load on the media element
      var sourceEl = document.querySelector('#stream-media source');
      if (sourceEl) {
        sourceEl.setAttribute('src', mediaLink);
        sourceEl.setAttribute('type', 'video/mp4');
        try { player.media.load(); } catch (err) { /* ignore */ }
      }
    }

    // Add small control buttons overlay (download & share)
    try {
      var wrapper = player && player.elements && player.elements.container && player.elements.container.querySelector('.plyr__video-wrapper');
      if (wrapper) {
        var downloadButton = document.createElement('div');
        downloadButton.className = 'plyr-download-button';
        downloadButton.setAttribute('role', 'button');
        downloadButton.addEventListener('click', function (ev) {
          ev.stopPropagation();
          var link = document.createElement('a');
          link.href = mediaLink;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        });
  wrapper.appendChild(downloadButton);

        var shareButton = document.createElement('div');
        shareButton.className = 'plyr-share-button';
        shareButton.setAttribute('role', 'button');
        shareButton.addEventListener('click', function (ev) {
          ev.stopPropagation();
          if (navigator.share) {
            navigator.share({ title: document.title || 'Play', url: mediaLink });
          }
        });
        wrapper.appendChild(shareButton);
      }
    } catch (e) {
      // non-fatal
      console.warn('Could not attach overlay buttons', e);
    }

    // Bottom action buttons
    var safeOpen = function (url) {
      // try custom protocol then fallback to opening the link
      window.location.href = url;
      setTimeout(function () { window.open(mediaLink, '_blank'); }, 500);
    };

    var downloadBtn = document.getElementById('download-btn');
    if (downloadBtn) downloadBtn.addEventListener('click', function (ev) {
      ev.stopPropagation();
      var a = document.createElement('a');
      a.href = mediaLink;
      a.download = '';
      document.body.appendChild(a);
      a.click();
      a.remove();
    });

    var copyBtn = document.getElementById('copy-link-btn');
    if (copyBtn) copyBtn.addEventListener('click', function (ev) {
      ev.stopPropagation();
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(mediaLink).then(function () { alert('Link copied to clipboard'); });
      } else {
        var tmp = document.createElement('textarea');
        tmp.value = mediaLink;
        document.body.appendChild(tmp);
        tmp.select();
        document.execCommand('copy');
        tmp.remove();
        alert('Link copied to clipboard');
      }
    });

    var vlcBtn = document.getElementById('vlc-btn');
    if (vlcBtn) vlcBtn.addEventListener('click', function (ev) {
      ev.stopPropagation();
      safeOpen('vlc://open?url=' + encodeURIComponent(mediaLink));
    });

    var mxBtn = document.getElementById('mx-btn');
    if (mxBtn) mxBtn.addEventListener('click', function (ev) {
      ev.stopPropagation();
      safeOpen('mxplayer://play?url=' + encodeURIComponent(mediaLink));
    });

    var nBtn = document.getElementById('nplayer-btn');
    if (nBtn) nBtn.addEventListener('click', function (ev) {
      ev.stopPropagation();
      safeOpen('nplayer-http://open?url=' + encodeURIComponent(mediaLink));
    });

  } else {
    var err = document.getElementById('error-message');
    if (err) err.textContent = 'Error: Media URL not provided';
  }

});
