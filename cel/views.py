import os

from django.conf import settings
from django.shortcuts import render

from .models import Circle, Overlay

# Must match the fps used when the frames were extracted from the video.
FPS = 12
CIRCLE_COUNT = 12


def home(request):
    frames_dir = os.path.join(settings.BASE_DIR, 'static', 'frames')
    try:
        frame_count = len([
            name for name in os.listdir(frames_dir)
            if name.lower().endswith('.jpg')
        ])
    except FileNotFoundError:
        frame_count = 0

    duration = frame_count / FPS if FPS else 0

    overlays = [
        {
            'start': overlay.start,
            'end': overlay.end,
            'message': overlay.message,
            'submessage': overlay.submessage,
            'audio': overlay.audio.url if overlay.audio else '',
            'audio_start': overlay.audio_start,
            'audio_end': overlay.audio_end,
        }
        for overlay in Overlay.objects.filter(is_active=True)
    ]

    by_position = {c.position: c for c in Circle.objects.all()}
    circles = []
    for pos in range(1, CIRCLE_COUNT + 1):
        c = by_position.get(pos)
        circles.append({
            'position': pos,
            'title': c.title if c else '',
            'image': c.image.url if (c and c.image) else '',
            'audio': c.audio.url if (c and c.audio) else '',
            'video': c.video.url if (c and c.video) else '',
            'message': c.message if c else '',
            'filled': bool(c),
        })

    context = {
        'frame_count': frame_count,
        'fps': FPS,
        'duration': duration,
        'overlays': overlays,
        'circles': circles,
    }
    return render(request, 'cel/index.html', context)
