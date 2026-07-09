from django.db import models


class Overlay(models.Model):
    """A message that floats above the video between `start` and `end` seconds.
    A row may also carry an MP3 that autoplays from `audio_start` seconds — so
    the same row can hold text, music, or both. Leave `message` blank for an
    audio-only row."""

    start = models.FloatField(
        default=0,
        help_text='Second of the video at which the text appears.',
    )
    end = models.FloatField(
        default=5,
        help_text='Second of the video at which the text disappears.',
    )
    message = models.CharField(
        max_length=120,
        blank=True,
        help_text='The main line shown in the cloud (leave blank for audio-only).',
    )
    submessage = models.CharField(
        max_length=160,
        blank=True,
        help_text='Optional smaller line beneath the main message.',
    )
    audio = models.FileField(
        upload_to='overlay_audio/',
        blank=True,
        help_text='Optional MP3 to autoplay during the video.',
    )
    audio_start = models.FloatField(
        default=0,
        help_text='Second of the video at which the music starts playing.',
    )
    audio_end = models.FloatField(
        null=True,
        blank=True,
        help_text='Optional second to stop the music. Leave blank to play until it ends.',
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Untick to hide this row without deleting it.',
    )

    class Meta:
        ordering = ['start']
        verbose_name = 'Text overlay'
        verbose_name_plural = 'Text overlays'

    def __str__(self):
        label = self.message[:40] or ('🎵 audio' if self.audio else 'overlay')
        return f'{self.start:g}–{self.end:g}s: {label}'


class Circle(models.Model):
    """A memory bubble shown at the end of the video. There are 12 positions;
    each can hold one object with an image and optional audio/video/message.
    Clicking the circle opens a full-screen popup with whatever media exists."""

    POSITION_CHOICES = [(i, f'Circle {i}') for i in range(1, 13)]

    position = models.PositiveSmallIntegerField(
        choices=POSITION_CHOICES,
        unique=True,
        help_text='Which of the 12 circles (1–12) this object fills.',
    )
    title = models.CharField(
        max_length=80,
        blank=True,
        help_text='Optional heading shown at the top of the popup.',
    )
    image = models.FileField(
        upload_to='circles/images/',
        help_text='Image shown as the circle itself (required).',
    )
    audio = models.FileField(
        upload_to='circles/audio/',
        blank=True,
        help_text='Optional audio to play in the popup.',
    )
    video = models.FileField(
        upload_to='circles/video/',
        blank=True,
        help_text='Optional video to play in the popup.',
    )
    message = models.TextField(
        blank=True,
        help_text='Optional written message to show in the popup.',
    )

    class Meta:
        ordering = ['position']
        verbose_name = 'Memory circle'
        verbose_name_plural = 'Memory circles'

    def __str__(self):
        return f'Circle {self.position}: {self.title or self.message[:30] or "memory"}'
