from django.contrib import admin

# admin 뒤에 / 붙여야 어드민 사이트 나옴
# Register your models here.
from .models import AudioFile


class AudioFileAdmin(admin.ModelAdmin):
    list_display = [ 'title', 'album','artist', 'genre', 'release','duration']  # 커스터마이징 코드
    list_filter = ('title','album',  'artist', 'genre', 'release','duration')
    search_fields = [ 'title','album', 'artist', 'genre', 'release','duration']


admin.site.register(AudioFile, AudioFileAdmin)
