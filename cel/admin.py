from django.contrib import admin

from .models import Circle, Overlay


@admin.register(Overlay)
class OverlayAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'start', 'end', 'message', 'has_audio', 'is_active')
    list_editable = ('start', 'end', 'message', 'is_active')
    list_filter = ('is_active',)
    ordering = ('start',)
    fieldsets = (
        ('Text overlay', {
            'fields': ('start', 'end', 'message', 'submessage'),
            'description': 'The text floats above the frame between start and end (seconds).',
        }),
        ('Music (optional)', {
            'fields': ('audio', 'audio_start', 'audio_end'),
            'description': 'Upload an MP3 to autoplay from audio_start (seconds). '
                           'Leave audio_end blank to play until the track ends.',
        }),
        ('Visibility', {
            'fields': ('is_active',),
        }),
    )

    @admin.display(boolean=True, description='Audio')
    def has_audio(self, obj):
        return bool(obj.audio)


@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'has_image', 'has_audio', 'has_video', 'has_message')
    ordering = ('position',)
    fieldsets = (
        (None, {
            'fields': ('position', 'title', 'image'),
        }),
        ('Optional media (any combination)', {
            'fields': ('audio', 'video', 'message'),
        }),
    )

    @admin.display(boolean=True, description='Image')
    def has_image(self, obj):
        return bool(obj.image)

    @admin.display(boolean=True, description='Audio')
    def has_audio(self, obj):
        return bool(obj.audio)

    @admin.display(boolean=True, description='Video')
    def has_video(self, obj):
        return bool(obj.video)

    @admin.display(boolean=True, description='Message')
    def has_message(self, obj):
        return bool(obj.message)
